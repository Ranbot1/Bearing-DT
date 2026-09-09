#!/usr/bin/env python
"""Quantitative dual-impulse validation for the reconstructed spall model.

Acceptance logic is mechanism-based:
- kinematic entry/exit spacing (DITS);
- high-frequency exit impulse relative to entry;
- preservation of BPFI;
- negative-control ablation with trailing-edge impact disabled.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import replace
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import yaml
from scipy.signal import butter, hilbert, periodogram, sosfiltfilt

from fmdtl.config import load_components
from fmdtl.sim import (
    characteristic_frequencies,
    defect_passage_events,
    dual_impulse_spacing_s,
    simulate_bearing,
)


def _parabolic_peak(freq, power, target_hz, window_hz=8.0):
    mask = (freq >= target_hz - window_hz) & (freq <= target_hz + window_hz)
    idxs = np.where(mask)[0]
    if idxs.size == 0:
        raise ValueError("No bins in peak-search window")
    i = idxs[np.argmax(power[mask])]
    if i <= 0 or i >= len(power) - 1:
        return float(freq[i])
    y = np.log(power[i - 1 : i + 2] + 1e-300)
    denom = y[0] - 2.0 * y[1] + y[2]
    delta = 0.0 if denom == 0 else 0.5 * (y[0] - y[2]) / denom
    return float(freq[i] + delta * (freq[1] - freq[0]))


def _filtered_signals(x, fs_hz, split_hz=500.0):
    high = butter(4, split_hz, btype="highpass", fs=fs_hz, output="sos")
    low = butter(4, split_hz, btype="lowpass", fs=fs_hz, output="sos")
    return sosfiltfilt(high, x), sosfiltfilt(low, x)


def _local_peak(t, signal, center_s, half_window_s=2.5e-4):
    mask = (t >= center_s - half_window_s) & (t <= center_s + half_window_s)
    idxs = np.where(mask)[0]
    if idxs.size == 0:
        raise ValueError("Empty event window")
    i = idxs[np.argmax(np.abs(signal[mask]))]
    return {
        "time_s": float(t[i]),
        "peak_abs": float(abs(signal[i])),
        "rms": float(np.sqrt(np.mean(signal[mask] ** 2))),
    }


def analyze_run(geometry, dynamics, fault, simulation):
    result = simulate_bearing(geometry, dynamics, fault, simulation)
    t = result["time_s"]
    x = result["outer_y_acceleration_mps2"]
    fs = simulation.output_fs_hz

    high, low = _filtered_signals(x, fs)
    theory_spacing = dual_impulse_spacing_s(geometry, fault)
    margin = 3.0e-3
    events = defect_passage_events(
        geometry,
        fault,
        float(t[0] + margin),
        float(t[-1] - margin),
    )

    rows = []
    for event in events:
        entry = float(event["entry_s"])
        exit_ = float(event["exit_s"])
        pe = _local_peak(t, high, entry)
        px = _local_peak(t, high, exit_)

        pre = (t >= entry - 6.0e-4) & (t < entry - 1.5e-4)
        post = (t > entry + 1.5e-4) & (t <= entry + 6.0e-4)
        step = (
            float(abs(np.mean(low[post]) - np.mean(low[pre])))
            if np.any(pre) and np.any(post)
            else np.nan
        )
        rows.append(
            {
                "ball_index": int(event["ball_index"]),
                "entry_theory_s": entry,
                "exit_theory_s": exit_,
                "theory_spacing_s": theory_spacing,
                "entry_peak_s": pe["time_s"],
                "exit_peak_s": px["time_s"],
                "detected_spacing_s": px["time_s"] - pe["time_s"],
                "entry_hf_peak": pe["peak_abs"],
                "exit_hf_peak": px["peak_abs"],
                "exit_entry_peak_ratio": px["peak_abs"] / max(pe["peak_abs"], 1e-30),
                "entry_hf_rms": pe["rms"],
                "exit_hf_rms": px["rms"],
                "exit_entry_rms_ratio": px["rms"] / max(pe["rms"], 1e-30),
                "entry_lowpass_step": step,
            }
        )

    if not rows:
        raise RuntimeError("No complete defect passages in retained interval")

    detected = np.array([r["detected_spacing_s"] for r in rows])
    peak_ratios = np.array([r["exit_entry_peak_ratio"] for r in rows])
    rms_ratios = np.array([r["exit_entry_rms_ratio"] for r in rows])

    envelope = np.abs(hilbert(x - np.mean(x)))
    f_env, p_env = periodogram(
        envelope - np.mean(envelope),
        fs=fs,
        window="hann",
        scaling="spectrum",
    )
    target = characteristic_frequencies(geometry)["bpfi_hz"]
    bpfi_peak = _parabolic_peak(f_env, p_env, target)

    summary = {
        "n_passages": len(rows),
        "theoretical_dits_s": theory_spacing,
        "detected_dits_median_s": float(np.median(detected)),
        "dits_error_pct": float(
            abs(np.median(detected) - theory_spacing) / theory_spacing * 100.0
        ),
        "exit_entry_hf_peak_ratio_median": float(np.median(peak_ratios)),
        "exit_entry_hf_rms_ratio_median": float(np.median(rms_ratios)),
        "fraction_exit_peak_gt_entry": float(np.mean(peak_ratios > 1.0)),
        "entry_lowpass_step_median": float(
            np.nanmedian([r["entry_lowpass_step"] for r in rows])
        ),
        "theoretical_bpfi_hz": target,
        "envelope_bpfi_peak_hz": bpfi_peak,
        "envelope_bpfi_error_pct": float(abs(bpfi_peak - target) / target * 100.0),
    }
    return summary, rows, result, high, low


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--duration-s", type=float, default=0.105)
    ap.add_argument("--discard-initial-s", type=float, default=0.04)
    args = ap.parse_args()

    cfg, geometry, dynamics, fault, simulation = load_components(args.config)
    if fault.type != "inner":
        raise ValueError("R2 dual-impulse gate currently targets the paper's inner-race example")

    simulation = replace(
        simulation,
        duration_s=args.duration_s,
        discard_initial_s=args.discard_initial_s,
    )
    args.out.mkdir(parents=True, exist_ok=True)

    full, rows, result, high, low = analyze_run(
        geometry, dynamics, fault, simulation
    )
    ablated_fault = replace(fault, exit_impact_force_n=0.0)
    ablated, _, _, _, _ = analyze_run(
        geometry, dynamics, ablated_fault, simulation
    )

    criteria = {
        "dits_error_le_5pct": full["dits_error_pct"] <= 5.0,
        "exit_entry_peak_ratio_ge_1p2": full["exit_entry_hf_peak_ratio_median"] >= 1.2,
        "exit_entry_rms_ratio_ge_1p1": full["exit_entry_hf_rms_ratio_median"] >= 1.1,
        "bpfi_error_le_2pct": full["envelope_bpfi_error_pct"] <= 2.0,
        "impact_ablation_reduces_peak_ratio": (
            full["exit_entry_hf_peak_ratio_median"]
            > ablated["exit_entry_hf_peak_ratio_median"]
        ),
    }
    summary = {
        "model": full,
        "no_exit_impact_ablation": ablated,
        "criteria": criteria,
        "pass": bool(all(criteria.values())),
    }

    (args.out / "dual_impulse_metrics.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    with (args.out / "event_metrics.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    t = result["time_s"]
    x = result["outer_y_acceleration_mps2"]
    strongest = max(rows, key=lambda r: r["exit_hf_peak"])
    center0 = strongest["entry_theory_s"] - 8e-4
    center1 = strongest["exit_theory_s"] + 8e-4
    mask = (t >= center0) & (t <= center1)

    with (args.out / "strongest_passage.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["time_s", "raw_acceleration_mps2", "highpass_mps2", "lowpass_mps2"])
        for ti, xi, hi, li in zip(t[mask], x[mask], high[mask], low[mask]):
            writer.writerow([ti, xi, hi, li])

    fig = plt.figure(figsize=(10, 5))
    plt.plot((t[mask] - strongest["entry_theory_s"]) * 1e3, x[mask], label="raw")
    plt.axvline(0.0, linestyle="--", label="entry")
    plt.axvline(
        (strongest["exit_theory_s"] - strongest["entry_theory_s"]) * 1e3,
        linestyle=":",
        label="exit",
    )
    plt.xlabel("Time relative to entry [ms]")
    plt.ylabel("Outer-y acceleration [m/s²]")
    plt.legend()
    plt.tight_layout()
    fig.savefig(args.out / "dual_impulse_time.svg")
    fig.savefig(args.out / "dual_impulse_time.png", dpi=180)
    plt.close(fig)

    fig = plt.figure(figsize=(10, 5))
    plt.plot((t[mask] - strongest["entry_theory_s"]) * 1e3, high[mask])
    plt.axvline(0.0, linestyle="--", label="entry")
    plt.axvline(
        (strongest["exit_theory_s"] - strongest["entry_theory_s"]) * 1e3,
        linestyle=":",
        label="exit",
    )
    plt.xlabel("Time relative to entry [ms]")
    plt.ylabel("High-pass acceleration [m/s²]")
    plt.legend()
    plt.tight_layout()
    fig.savefig(args.out / "dual_impulse_highpass.svg")
    fig.savefig(args.out / "dual_impulse_highpass.png", dpi=180)
    plt.close(fig)

    (args.out / "config_snapshot.yaml").write_text(
        yaml.safe_dump(cfg, sort_keys=False), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))
    if not summary["pass"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
