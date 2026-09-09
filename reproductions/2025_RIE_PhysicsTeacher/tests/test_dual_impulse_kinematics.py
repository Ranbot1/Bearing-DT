from math import pi

import numpy as np

from fmdtl.sim import (
    BearingGeometry,
    FaultParameters,
    defect_passage_events,
    dual_impulse_spacing_s,
)


def _geometry():
    return BearingGeometry(
        ball_count=8,
        ball_diameter_m=0.00675,
        pitch_diameter_m=0.0285,
        contact_angle_rad=0.0,
        shaft_speed_rad_s=2 * pi * 25.0,
    )


def test_inner_dual_impulse_spacing_matches_kinematics():
    fault = FaultParameters(
        type="inner",
        depth_m=5e-5,
        angular_width_rad=np.deg2rad(6.0),
    )
    spacing = dual_impulse_spacing_s(_geometry(), fault)
    assert abs(spacing - 0.001078014184397163) < 1e-12


def test_passage_event_spacing_is_exact_by_geometry():
    fault = FaultParameters(
        type="inner",
        depth_m=5e-5,
        angular_width_rad=np.deg2rad(6.0),
    )
    events = defect_passage_events(_geometry(), fault, 0.05, 0.10)
    assert events
    expected = dual_impulse_spacing_s(_geometry(), fault)
    for event in events:
        assert abs((event["exit_s"] - event["entry_s"]) - expected) < 1e-12


def test_initial_ball_angle_shifts_events_without_changing_spacing():
    fault = FaultParameters(
        type="inner",
        depth_m=5e-5,
        angular_width_rad=np.deg2rad(6.0),
    )
    g0 = _geometry()
    g1 = BearingGeometry(
        ball_count=g0.ball_count,
        ball_diameter_m=g0.ball_diameter_m,
        pitch_diameter_m=g0.pitch_diameter_m,
        contact_angle_rad=g0.contact_angle_rad,
        shaft_speed_rad_s=g0.shaft_speed_rad_s,
        initial_ball_angle_rad=0.37,
    )
    e0 = defect_passage_events(g0, fault, 0.05, 0.10)
    e1 = defect_passage_events(g1, fault, 0.05, 0.10)
    assert e0 and e1
    assert e0[0]["entry_s"] != e1[0]["entry_s"]
    assert abs(e0[0]["spacing_s"] - e1[0]["spacing_s"]) < 1e-12
