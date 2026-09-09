"""Four-DOF ball-bearing dynamics for the 2025 physics-teacher reproduction.

Evidence levels
---------------
CONFIRMED from Zhang et al. (2025):
- 4-DOF inner/outer ring x-y model;
- Hertzian nonlinear contact;
- localized faults;
- simulated signals are expected to retain the dual-impulse mechanism.

REFERENCED reconstruction:
- smooth half-cosine spall displacement profile follows the time-varying
  displacement modeling family used by Luo/Guo and cited by Zhang et al.;
- a transient trailing-edge collision term is included because Luo et al.
  explicitly identify it as necessary for the high-frequency exit impulse.

INFERRED:
- numerical impact-force amplitude and duration remain configuration
  parameters until the exact paper values/equations can be recovered.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, pi, sin
from typing import Literal

import numpy as np
from scipy.integrate import solve_ivp


FaultType = Literal["normal", "inner", "outer"]
DefectProfile = Literal["rectangular", "half_cosine"]


@dataclass(frozen=True)
class BearingGeometry:
    ball_count: int
    ball_diameter_m: float
    pitch_diameter_m: float
    contact_angle_rad: float
    shaft_speed_rad_s: float
    initial_ball_angle_rad: float = 0.0


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
    profile: DefectProfile = "half_cosine"
    exit_impact_force_n: float = 0.0
    exit_impact_duration_s: float = 8.0e-5


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


def fault_relative_speed_rad_s(
    geometry: BearingGeometry, fault: FaultParameters
) -> float:
    """Angular speed of a ball relative to the defective race."""
    omega_c = cage_speed_rad_s(geometry)
    if fault.type == "outer":
        return omega_c
    if fault.type == "inner":
        return omega_c - geometry.shaft_speed_rad_s
    return 0.0


def dual_impulse_spacing_s(
    geometry: BearingGeometry, fault: FaultParameters
) -> float:
    """Kinematic entry-to-exit time for the configured angular defect width."""
    omega_rel = abs(fault_relative_speed_rad_s(geometry, fault))
    if omega_rel <= 0.0:
        raise ValueError("Fault must be inner or outer with nonzero relative speed")
    if fault.angular_width_rad <= 0.0:
        raise ValueError("angular_width_rad must be positive")
    return fault.angular_width_rad / omega_rel


def _wrap_angle(angle: float) -> float:
    return (angle + pi) % (2.0 * pi) - pi


def _fault_relative_angle(
    *,
    ball_angle: float,
    time_s: float,
    geometry: BearingGeometry,
    fault: FaultParameters,
) -> float:
    if fault.type == "outer":
        center = fault.outer_fault_angle_rad
    elif fault.type == "inner":
        center = (
            fault.initial_inner_fault_angle_rad
            + geometry.shaft_speed_rad_s * time_s
        )
    else:
        return 0.0
    return _wrap_angle(ball_angle - center)


def defect_passage_events(
    geometry: BearingGeometry,
    fault: FaultParameters,
    start_s: float,
    end_s: float,
) -> list[dict[str, float | int]]:
    """Return kinematic entry/exit events for all rolling elements.

    For an inner-race defect the ball-defect relative angle decreases, so the
    +width/2 edge is entry and -width/2 is exit. For an outer-race defect the
    order is reversed.
    """
    if fault.type == "normal":
        return []
    omega_rel = fault_relative_speed_rad_s(geometry, fault)
    if omega_rel == 0.0 or fault.angular_width_rad <= 0.0:
        return []

    half = 0.5 * fault.angular_width_rad
    entry_edge = half if omega_rel < 0.0 else -half
    spacing = fault.angular_width_rad / abs(omega_rel)

    events: list[dict[str, float | int]] = []
    # Wide k range is harmless and keeps the helper independent of run length.
    for ball_index in range(geometry.ball_count):
        theta0 = (
            geometry.initial_ball_angle_rad
            + 2.0 * pi * ball_index / geometry.ball_count
        )
        if fault.type == "inner":
            theta0 -= fault.initial_inner_fault_angle_rad
        else:
            theta0 -= fault.outer_fault_angle_rad

        for k in range(-256, 257):
            entry_s = (entry_edge + 2.0 * pi * k - theta0) / omega_rel
            exit_s = entry_s + spacing
            if entry_s >= start_s and exit_s <= end_s:
                events.append(
                    {
                        "ball_index": ball_index,
                        "entry_s": float(entry_s),
                        "exit_s": float(exit_s),
                        "spacing_s": float(spacing),
                    }
                )
    return sorted(events, key=lambda item: item["entry_s"])


def _defect_clearance_increment(
    *,
    ball_angle: float,
    time_s: float,
    geometry: BearingGeometry,
    fault: FaultParameters,
) -> float:
    """Additional contact displacement caused by the local spall."""
    if fault.type == "normal" or fault.depth_m <= 0.0:
        return 0.0

    relative = _fault_relative_angle(
        ball_angle=ball_angle,
        time_s=time_s,
        geometry=geometry,
        fault=fault,
    )
    half = 0.5 * fault.angular_width_rad
    if abs(relative) > half:
        return 0.0

    if fault.profile == "rectangular":
        return fault.depth_m
    if fault.profile == "half_cosine":
        # Zero at both spall edges; maximum additional displacement at center.
        return fault.depth_m * cos(pi * relative / fault.angular_width_rad)
    raise ValueError(f"Unsupported defect profile: {fault.profile}")


def _trailing_edge_impact_force(
    *,
    ball_angle: float,
    time_s: float,
    geometry: BearingGeometry,
    fault: FaultParameters,
) -> float:
    """Approximate transient force at the spall trailing edge.

    Luo et al. identify the trailing-edge collision as the origin of the
    higher-frequency second impulse. The exact collision-force constants used
    in Zhang et al. are not reported in the accessible text, so amplitude and
    duration are explicit INFERRED configuration parameters.
    """
    if (
        fault.type == "normal"
        or fault.exit_impact_force_n <= 0.0
        or fault.exit_impact_duration_s <= 0.0
        or fault.angular_width_rad <= 0.0
    ):
        return 0.0

    relative = _fault_relative_angle(
        ball_angle=ball_angle,
        time_s=time_s,
        geometry=geometry,
        fault=fault,
    )
    omega_rel = fault_relative_speed_rad_s(geometry, fault)
    exit_edge = -0.5 * fault.angular_width_rad if omega_rel < 0.0 else 0.5 * fault.angular_width_rad

    # Convert the requested temporal FWHM to an angular Gaussian sigma.
    sigma_angle = max(
        abs(omega_rel) * fault.exit_impact_duration_s / 2.355,
        1.0e-12,
    )
    distance = _wrap_angle(relative - exit_edge)
    if abs(distance) > 4.0 * sigma_angle:
        return 0.0
    return fault.exit_impact_force_n * np.exp(
        -0.5 * (distance / sigma_angle) ** 2
    )


def _contact_forces(
    time_s: float,
    q: np.ndarray,
    geometry: BearingGeometry,
    dynamics: DynamicParameters,
    fault: FaultParameters,
) -> tuple[float, float]:
    """Sum nonlinear Hertz and trailing-edge impact forces."""
    xi, yi, xo, yo = q
    omega_c = cage_speed_rad_s(geometry)

    fx = 0.0
    fy = 0.0
    for j in range(geometry.ball_count):
        theta = (
            geometry.initial_ball_angle_rad
            + 2.0 * pi * j / geometry.ball_count
            + omega_c * time_s
        )
        local_defect = _defect_clearance_increment(
            ball_angle=theta,
            time_s=time_s,
            geometry=geometry,
            fault=fault,
        )

        relative = (xi - xo) * cos(theta) + (yi - yo) * sin(theta)
        delta = relative - 0.5 * dynamics.clearance_m - local_defect

        normal_force = (
            dynamics.hertz_coefficient_npm32 * delta**1.5
            if delta > 0.0
            else 0.0
        )
        normal_force += _trailing_edge_impact_force(
            ball_angle=theta,
            time_s=time_s,
            geometry=geometry,
            fault=fault,
        )
        if normal_force <= 0.0:
            continue

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
