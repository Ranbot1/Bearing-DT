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
