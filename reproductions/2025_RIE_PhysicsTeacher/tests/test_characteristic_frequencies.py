from math import pi

from fmdtl.sim import BearingGeometry, characteristic_frequencies


def test_6203_characteristic_frequencies():
    geometry = BearingGeometry(
        ball_count=8,
        ball_diameter_m=0.00675,
        pitch_diameter_m=0.0285,
        contact_angle_rad=0.0,
        shaft_speed_rad_s=2 * pi * 25.0,
    )
    f = characteristic_frequencies(geometry)

    assert abs(f["shaft_hz"] - 25.0) < 1e-12
    assert abs(f["bpfi_hz"] - 123.6842105263158) < 1e-9
    assert abs(f["bpfo_hz"] - 76.31578947368422) < 1e-9
    assert abs(f["ftf_hz"] - 9.539473684210527) < 1e-9


def test_config_theory_is_consistent_with_paper_fig5_reference():
    """Paper gives 123.24 Hz; config geometry/speed gives 123.684 Hz.

    The small discrepancy is preserved rather than forcing the formula to
    reproduce the paper number exactly.
    """
    geometry = BearingGeometry(
        ball_count=8,
        ball_diameter_m=0.00675,
        pitch_diameter_m=0.0285,
        contact_angle_rad=0.0,
        shaft_speed_rad_s=2 * pi * 25.0,
    )
    bpfi = characteristic_frequencies(geometry)["bpfi_hz"]
    paper_reference = 123.24

    assert abs(bpfi - paper_reference) / paper_reference < 0.02
