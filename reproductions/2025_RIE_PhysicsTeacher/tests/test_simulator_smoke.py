from math import pi

import numpy as np

from fmdtl.sim import (
    BearingGeometry,
    DynamicParameters,
    FaultParameters,
    SimulationParameters,
    simulate_bearing,
)


def test_simulator_returns_finite_arrays():
    geometry = BearingGeometry(
        ball_count=8,
        ball_diameter_m=0.00675,
        pitch_diameter_m=0.0285,
        contact_angle_rad=0.0,
        shaft_speed_rad_s=2 * pi * 10.0,
    )
    dynamics = DynamicParameters(
        inner_mass_kg=1.0,
        outer_mass_kg=1.0,
        inner_stiffness_x_npm=1e6,
        inner_stiffness_y_npm=1e6,
        outer_stiffness_x_npm=1e6,
        outer_stiffness_y_npm=1e6,
        inner_damping_x_nspm=200.0,
        inner_damping_y_nspm=200.0,
        outer_damping_x_nspm=200.0,
        outer_damping_y_nspm=200.0,
        hertz_coefficient_npm32=1e8,
        radial_load_x_n=0.0,
        radial_load_y_n=100.0,
        clearance_m=1e-5,
        eccentricity_m=1e-6,
    )
    fault = FaultParameters(
        type="outer",
        depth_m=2e-5,
        angular_width_rad=np.deg2rad(8.0),
        outer_fault_angle_rad=np.deg2rad(270.0),
    )
    simulation = SimulationParameters(
        duration_s=0.01,
        output_fs_hz=2000.0,
        integration_max_step_s=1e-5,
        discard_initial_s=0.0,
    )

    result = simulate_bearing(geometry, dynamics, fault, simulation)

    assert result["time_s"].ndim == 1
    assert result["acceleration_mps2"].shape[1] == 4
    assert np.isfinite(result["acceleration_mps2"]).all()
