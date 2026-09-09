"""Configuration helpers for the 2025 physics-teacher reproduction."""

from __future__ import annotations

from math import pi
from pathlib import Path

import numpy as np
import yaml

from .sim import (
    BearingGeometry,
    DynamicParameters,
    FaultParameters,
    SimulationParameters,
)


def load_yaml(path: str | Path) -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def build_from_config(cfg: dict):
    b = cfg["bearing"]
    d = cfg["dynamics"]
    f = cfg["fault"]
    s = cfg["simulation"]

    geometry = BearingGeometry(
        ball_count=int(b["ball_count"]),
        ball_diameter_m=float(b["ball_diameter_m"]),
        pitch_diameter_m=float(b["pitch_diameter_m"]),
        contact_angle_rad=np.deg2rad(float(b["contact_angle_deg"])),
        shaft_speed_rad_s=2.0 * pi * float(b["shaft_speed_rpm"]) / 60.0,
    )
    dynamics = DynamicParameters(**{k: float(v) for k, v in d.items()})
    fault = FaultParameters(
        type=f["type"],
        depth_m=float(f["depth_m"]),
        angular_width_rad=np.deg2rad(float(f["angular_width_deg"])),
        outer_fault_angle_rad=np.deg2rad(float(f["outer_fault_angle_deg"])),
        initial_inner_fault_angle_rad=np.deg2rad(
            float(f["initial_inner_fault_angle_deg"])
        ),
    )
    simulation = SimulationParameters(
        duration_s=float(s["duration_s"]),
        output_fs_hz=float(s["output_fs_hz"]),
        integration_max_step_s=float(s["integration_max_step_s"]),
        rtol=float(s["rtol"]),
        atol=float(s["atol"]),
        discard_initial_s=float(s["discard_initial_s"]),
    )
    return geometry, dynamics, fault, simulation


def load_components(path: str | Path):
    cfg = load_yaml(path)
    return cfg, *build_from_config(cfg)
