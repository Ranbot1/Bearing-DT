#!/usr/bin/env python
"""Paper-oriented R1/R2 signal validation.

Primary evaluation mirrors the paper's Fig. 5 logic:
1) time-domain simulated vibration;
2) frequency-domain peak near the theoretical bearing fault frequency.

Envelope-spectrum analysis is included as a supplementary audit.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import hilbert, periodogram

from fmdtl.config import load_components
from fmdtl.sim import characteristic_frequencies, simulate_bearing


PAPER_6203_BPFI_HZ = 123.24


def parabolic_peak(freq: np.ndarray, power: np.ndarray, target: float, window_hz: float):
    mask = (freq >= target - window_hz) & (freq <= target + window_hz)
    idxs = np.where(mask)[0]
    if idxs.size == 0:
        raise ValueError("No frequency bins in requested search window")
    i = idxs[np.argmax(power[mask])]
    if i <= 0 or i >= len(power) - 1:
        return float(freq[i])

    y = np.log(power[i - 1 : i + 2] + 1e-300)
    denom = y[0] - 2.0 * y[1] + y[2]
    delta = 0.0 if denom == 0 else 0.5 * (y[0] - y[2]) / denom
    return float(freq[i] + delta * (freq[1] - freq[0]))


def spectrum_metrics(x: np.ndarray, fs: float, target_hz: float):
    x = x - np.mean(x)
    f_raw, p_raw = periodogram(x, fs=fs, window="hann", scaling="spectrum")

    envelope = np.abs(hilbert(x))
    f_env, p_env = periodogram(
        envelope - np.mean(envelope),
        fs=fs,
        window="hann",
        scaling="spectrum",
    )

    raw_peak = parabolic_peak(f_raw, p_raw, target_hz, 8.0)
    env_peak = parabolic_peak(f_env, p_env, target_hz, 8.0)

    return {
        "raw_peak_hz": raw_peak,
        "envelope_peak_hz": env_peak,
        "raw_error_vs_theory_pct": abs(raw_peak - target_hz) / target_hz * 100.0,
        "envelope_error_vs_theory_pct": abs(env_peak - target_hz) / target_hz * 100.0,
        "f_raw": f_raw,
        "p_raw": p_raw,
        "f_env": f_env,
        "p_env": p_env,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=Path("results/r1_r2_signal_validation"))
    args = parser.parse_args()

    _, geometry, dynamics, fault, simulation = load_components(args.config)
    result = simulate_bearing(geometry, dynamics, fault, simulation)

    x = result["outer_y_acceleration_mps2"]
    t = result["time_s"]
    freqs = characteristic_frequencies(geometry)

    if fault.type == "inner":
        target = freqs["bpfi_hz"]
    elif fault.type == "outer":
        target = freqs["bpfo_hz"]
    else:
        raise ValueError("Paper signal evaluation expects inner or outer fault")

    metrics = spectrum_metrics(x, simulation.output_fs_hz, target)
    summary = {
        "fault_type": fault.type,
        "shaft_hz": freqs["shaft_hz"],
        "theoretical_target_hz": target,
        "raw_peak_hz": metrics["raw_peak_hz"],
        "raw_error_vs_theory_pct": metrics["raw_error_vs_theory_pct"],
        "envelope_peak_hz": metrics["envelope_peak_hz"],
        "envelope_error_vs_theory_pct": metrics["envelope_error_vs_theory_pct"],
    }

    if fault.type == "inner":
        summary["paper_fig5_reference_hz"] = PAPER_6203_BPFI_HZ
        summary["raw_error_vs_paper_pct"] = (
            abs(metrics["raw_peak_hz"] - PAPER_6203_BPFI_HZ)
            / PAPER_6203_BPFI_HZ
            * 100.0
        )
        summary["envelope_error_vs_paper_pct"] = (
            abs(metrics["envelope_peak_hz"] - PAPER_6203_BPFI_HZ)
            / PAPER_6203_BPFI_HZ
            * 100.0
        )

    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "metrics.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )

    fig = plt.figure(figsize=(10, 4))
    plt.plot(t, x)
    plt.xlabel("Time [s]")
    plt.ylabel("Outer-y acceleration [m/s²]")
    plt.tight_layout()
    fig.savefig(args.out / "time_domain.png", dpi=180)
    plt.close(fig)

    fig = plt.figure(figsize=(10, 4))
    m = metrics["f_raw"] <= 500.0
    plt.semilogy(metrics["f_raw"][m], metrics["p_raw"][m] + 1e-30)
    plt.axvline(target, linestyle="--", label=f"Theory: {target:.3f} Hz")
    if fault.type == "inner":
        plt.axvline(
            PAPER_6203_BPFI_HZ,
            linestyle=":",
            label=f"Paper Fig.5: {PAPER_6203_BPFI_HZ:.2f} Hz",
        )
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Spectrum power")
    plt.legend()
    plt.tight_layout()
    fig.savefig(args.out / "frequency_domain.png", dpi=180)
    plt.close(fig)

    fig = plt.figure(figsize=(10, 4))
    m = metrics["f_env"] <= 500.0
    plt.semilogy(metrics["f_env"][m], metrics["p_env"][m] + 1e-30)
    plt.axvline(target, linestyle="--", label=f"Theory: {target:.3f} Hz")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Envelope-spectrum power")
    plt.legend()
    plt.tight_layout()
    fig.savefig(args.out / "envelope_audit.png", dpi=180)
    plt.close(fig)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
