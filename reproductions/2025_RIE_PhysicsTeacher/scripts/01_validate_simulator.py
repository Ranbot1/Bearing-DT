#!/usr/bin/env python
from __future__ import annotations

import argparse
from math import pi
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import yaml
from scipy.signal import hilbert, periodogram

from fmdtl.sim import (
    BearingGeometry,
    DynamicParameters,
    FaultParameters,
    SimulationParameters,
    characteristic_frequencies,
    simulate_bearing,
)


def load_config(path: Path):
    cfg = yaml.safe_load(path.read_text(encoding="utf-8"))
    b = cfg["bearing"]
    d = cfg["dynamics"]
    f = cfg["fault"]
    s = cfg["simulation"]

    geometry = BearingGeometry(
        ball_count=int(b["ball_count"]),
        ball_diameter_m=float(b["ball_diameter_m"]),
        pitch_diameter_m=float(b["pitch_diameter_m"]),
        contact_angle_rad=np.deg2rad(float(b["contact_angle_deg"])),
        shaft_speed_rad_s=2 * pi * float(b["shaft_speed_rpm"]) / 60.0,
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
    return cfg, geometry, dynamics, fault, simulation


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=Path("results/simulator_validation"))
    args = parser.parse_args()

    _, geometry, dynamics, fault, simulation = load_config(args.config)
    result = simulate_bearing(geometry, dynamics, fault, simulation)
    x = result["outer_y_acceleration_mps2"]
    t = result["time_s"]
    fs = simulation.output_fs_hz

    freqs = characteristic_frequencies(geometry)
    envelope = np.abs(hilbert(x - np.mean(x)))
    f_env, p_env = periodogram(envelope - np.mean(envelope), fs=fs)

    args.out.mkdir(parents=True, exist_ok=True)

    (args.out / "characteristic_frequencies.yaml").write_text(
        yaml.safe_dump(freqs, sort_keys=False), encoding="utf-8"
    )

    fig = plt.figure(figsize=(10, 4))
    plt.plot(t, x)
    plt.xlabel("Time [s]")
    plt.ylabel("Outer-y acceleration [m/s²]")
    plt.tight_layout()
    fig.savefig(args.out / "waveform.png", dpi=180)
    plt.close(fig)

    fig = plt.figure(figsize=(10, 4))
    mask = f_env <= 500.0
    plt.semilogy(f_env[mask], p_env[mask] + 1e-30)
    for key in ("bpfi_hz", "bpfo_hz", "bsf_hz"):
        plt.axvline(freqs[key], linestyle="--", label=f"{key}: {freqs[key]:.2f} Hz")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Envelope PSD")
    plt.legend()
    plt.tight_layout()
    fig.savefig(args.out / "envelope_spectrum.png", dpi=180)
    plt.close(fig)

    print("Characteristic frequencies:")
    for key, value in freqs.items():
        print(f"  {key}: {value:.6f}")
    print(f"Saved validation artifacts to {args.out}")


if __name__ == "__main__":
    main()
