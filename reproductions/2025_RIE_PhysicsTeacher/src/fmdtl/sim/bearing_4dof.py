"""Four-DOF ball-bearing dynamics used as the paper-faithful physics baseline.

Important
---------
The paper confirms a 4-DOF Hertz-contact model with inner/outer ring x-y
motion. Several numerical parameters are not yet confirmed. The equations
below therefore reproduce the *model class* while keeping uncertain values
in configuration files and the evidence ledger.

State:
    q = [x_i, y_i, x_o, y_o]
    dq = [vx_i, vy_i, vx_o, vy_o]

The localized defect is represented as a temporary increase in local
clearance when a rolling element traverses a defect angular window.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, pi, sin
from typing import Literal

import numpy as np
from scipy.integrate import solve_ivp


FaultType = Literal["normal", "inner", "outer"]


@dataclass(frozen=True)
class BearingGeometry:
    ball_count: int
    ball_diameter_m: float
    pitch_diameter_m: float
    contact_angle_rad: float
    shaft_speed_rad_s: float


@dataclass(frozen=True)
class DynamicParameters:
    inner_mass_kg: float
    outer_mass_kg: float
    inner_stiffness_x_npm: float
    inner_stiffness_y_npm: float
    outer_stiffness_x_npm: float
    outer_stiffness_y_npm: float
    inner_damping_x_nspm: float
    inner_damping_y_nspm: float
    outer_damping_x_nspm: float
    outer_damping_y_nspm: float
    hertz_coefficient_npm32: float
    radial_load_x_n: float
    radial_load_y_n: float
    clearance_m: float
    eccentricity_m: float
    gravity_mps2: float = 9.80665


@dataclass(frozen=True)
class FaultParameters:
    type: FaultType = "normal"
    depth_m: float = 0.0
    angular_width_rad: float = 0.0
    outer_fault_angle_rad: float = 0.0
    initial_inner_fault_angle_rad: float = 0.0


@dataclass(frozen=True)
class SimulationParameters:
    duration_s: float
    output_fs_hz: float
    integration_max_step_s: float
    rtol: float = 1e-7
    atol: float = 1e-9
    discard_initial_s: float = 0.0


def characteristic_frequencies(geometry: BearingGeometry) -> dict[str, float]:
    """Return standard bearing characteristic frequencies in Hz."""
    fr = geometry.shaft_speed_rad_s / (2.0 * pi)
    ratio = (
        geometry.ball_diameter_m
        / geometry.pitch_diameter_m
        * cos(geometry.contact_angle_rad)
    )
    nb = geometry.ball_count

    return {
        "shaft_hz": fr,
        "bpfi_hz": 0.5 * nb * fr * (1.0 + ratio),
        "bpfo_hz": 0.5 * nb * fr * (1.0 - ratio),
        "bsf_hz": (
            geometry.pitch_diameter_m
            / (2.0 * geometry.ball_diameter_m)
            * fr
            * (1.0 - ratio**2)
        ),
        "ftf_hz": 0.5 * fr * (1.0 - ratio),
    }


def cage_speed_rad_s(geometry: BearingGeometry) -> float:
    """Classical cage angular speed for a stationary outer ring."""
    ratio = (
        geometry.ball_diameter_m
        / geometry.pitch_diameter_m
        * cos(geometry.contact_angle_rad)
    )
    return 0.5 * geometry.shaft_speed_rad_s * (1.0 - ratio)


def _wrap_angle(angle: float) -> float:
    return (angle + pi) % (2.0 * pi) - pi


def _inside_window(angle: float, center: float, width: float) -> bool:
    return abs(_wrap_angle(angle - center)) <= 0.5 * width


def _defect_clearance_increment(
    *,
    ball_angle: float,
    time_s: float,
    geometry: BearingGeometry,
    fault: FaultParameters,
) -> float:
    """Return the local clearance increment produced by a localized defect."""
    if fault.type == "normal" or fault.depth_m <= 0.0:
        return 0.0

    if fault.type == "outer":
        center = fault.outer_fault_angle_rad
        relative = ball_angle
    elif fault.type == "inner":
        center = (
            fault.initial_inner_fault_angle_rad
            + geometry.shaft_speed_rad_s * time_s
        )
        relative = ball_angle
    else:  # pragma: no cover - type guard
        raise ValueError(f"Unsupported fault type: {fault.type}")

    return (
        fault.depth_m
        if _inside_window(relative, center, fault.angular_width_rad)
        else 0.0
    )


def _contact_forces(
    time_s: float,
    q: np.ndarray,
    geometry: BearingGeometry,
    dynamics: DynamicParameters,
    fault: FaultParameters,
) -> tuple[float, float]:
    """Sum nonlinear Hertz contact forces acting on the inner ring."""
    xi, yi, xo, yo = q
    omega_c = cage_speed_rad_s(geometry)

    fx = 0.0
    fy = 0.0
    for j in range(geometry.ball_count):
        theta = 2.0 * pi * j / geometry.ball_count + omega_c * time_s
        local_defect = _defect_clearance_increment(
            ball_angle=theta,
            time_s=time_s,
            geometry=geometry,
            fault=fault,
        )

        relative = (xi - xo) * cos(theta) + (yi - yo) * sin(theta)
        delta = relative - 0.5 * dynamics.clearance_m - local_defect

        if delta <= 0.0:
            continue

        normal_force = dynamics.hertz_coefficient_npm32 * delta**1.5
        fx += normal_force * cos(theta)
        fy += normal_force * sin(theta)

    return fx, fy


def _rhs(
    time_s: float,
    state: np.ndarray,
    geometry: BearingGeometry,
    dynamics: DynamicParameters,
    fault: FaultParameters,
) -> np.ndarray:
    q = state[:4]
    dq = state[4:]
    xi, yi, xo, yo = q
    vxi, vyi, vxo, vyo = dq

    fix, fiy = _contact_forces(time_s, q, geometry, dynamics, fault)

    omega = geometry.shaft_speed_rad_s
    unbalance = dynamics.inner_mass_kg * dynamics.eccentricity_m * omega**2
    ux = unbalance * cos(omega * time_s)
    uy = unbalance * sin(omega * time_s)

    ax_i = (
        -dynamics.inner_damping_x_nspm * vxi
        - dynamics.inner_stiffness_x_npm * xi
        - fix
        + ux
        + dynamics.radial_load_x_n
    ) / dynamics.inner_mass_kg

    ay_i = (
        -dynamics.inner_damping_y_nspm * vyi
        - dynamics.inner_stiffness_y_npm * yi
        - fiy
        + uy
        + dynamics.radial_load_y_n
        - dynamics.inner_mass_kg * dynamics.gravity_mps2
    ) / dynamics.inner_mass_kg

    # Newton's third law: outer ring receives the opposite contact force.
    ax_o = (
        -dynamics.outer_damping_x_nspm * vxo
        - dynamics.outer_stiffness_x_npm * xo
        + fix
    ) / dynamics.outer_mass_kg

    ay_o = (
        -dynamics.outer_damping_y_nspm * vyo
        - dynamics.outer_stiffness_y_npm * yo
        + fiy
        - dynamics.outer_mass_kg * dynamics.gravity_mps2
    ) / dynamics.outer_mass_kg

    return np.array([vxi, vyi, vxo, vyo, ax_i, ay_i, ax_o, ay_o])


def simulate_bearing(
    geometry: BearingGeometry,
    dynamics: DynamicParameters,
    fault: FaultParameters,
    simulation: SimulationParameters,
) -> dict[str, np.ndarray]:
    """Integrate the 4-DOF system and return sampled displacement/acceleration."""
    if simulation.duration_s <= 0:
        raise ValueError("duration_s must be positive")
    if simulation.output_fs_hz <= 0:
        raise ValueError("output_fs_hz must be positive")

    n = int(round(simulation.duration_s * simulation.output_fs_hz)) + 1
    t_eval = np.linspace(0.0, simulation.duration_s, n)
    y0 = np.zeros(8, dtype=float)

    sol = solve_ivp(
        fun=lambda t, y: _rhs(t, y, geometry, dynamics, fault),
        t_span=(0.0, simulation.duration_s),
        y0=y0,
        method="DOP853",
        t_eval=t_eval,
        max_step=simulation.integration_max_step_s,
        rtol=simulation.rtol,
        atol=simulation.atol,
    )
    if not sol.success:
        raise RuntimeError(f"ODE solver failed: {sol.message}")

    states = sol.y.T
    accelerations = np.vstack(
        [_rhs(t, s, geometry, dynamics, fault)[4:] for t, s in zip(sol.t, states)]
    )

    keep = sol.t >= simulation.discard_initial_s
    return {
        "time_s": sol.t[keep],
        "displacement_m": states[keep, :4],
        "velocity_mps": states[keep, 4:],
        "acceleration_mps2": accelerations[keep],
        "outer_y_acceleration_mps2": accelerations[keep, 3],
    }
