#!/usr/bin/env python
"""Build a retained R1/R2 audit snapshot from the 4-DOF twin.

Outputs:
- full-resolution NPZ per class;
- compact Git-friendly CSV signal copies;
- raw/envelope spectra;
- numeric QA tables;
- PNG + SVG figures;
- config/runtime snapshots;
- SHA-256 manifest.

The committed audit snapshot may retain only the compact CSV/SVG subset,
while the script always generates the full binary artifacts locally.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import subprocess
from dataclasses import replace
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import yaml
from scipy.signal import hilbert, periodogram, resample_poly

from fmdtl.config import load_components
from fmdtl.sim import FaultParameters, characteristic_frequencies, simulate_bearing


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return "unknown"


def parabolic_peak(freq, power, target_hz, window_hz=8.0):
    mask = (freq >= target_hz - window_hz) & (freq <= target_hz + window_hz)
    idxs = np.where(mask)[0]
    i = idxs[np.argmax(power[mask])]
    if i <= 0 or i >= len(power) - 1:
        return float(freq[i])
    y = np.log(power[i - 1 : i + 2] + 1e-300)
    denom = y[0] - 2.0 * y[1] + y[2]
    delta = 0.0 if denom == 0 else 0.5 * (y[0] - y[2]) / denom
    return float(freq[i] + delta * (freq[1] - freq[0]))


def band_power(freq, power, target_hz, width_hz=2.0):
    mask = (freq >= target_hz - width_hz) & (freq <= target_hz + width_hz)
    return float(np.trapezoid(power[mask], freq[mask]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--duration-s", type=float, default=0.35)
    ap.add_argument("--discard-initial-s", type=float, default=0.05)
    ap.add_argument("--git-signal-fs-hz", type=int, default=4000)
    ap.add_argument("--full-res-excerpt-s", type=float, default=0.01)
    args = ap.parse_args()

    cfg, geometry, dynamics, base_fault, simulation = load_components(args.config)
    simulation = replace(
        simulation,
        duration_s=args.duration_s,
        discard_initial_s=args.discard_initial_s,
    )
    if int(simulation.output_fs_hz) % args.git_signal_fs_hz != 0:
        raise ValueError("output_fs_hz must be divisible by git_signal_fs_hz")

    out = args.out
    if out.exists():
        shutil.rmtree(out)
    data_dir, fig_dir, table_dir = out / "data", out / "figures", out / "tables"
    for d in (data_dir, fig_dir, table_dir):
        d.mkdir(parents=True, exist_ok=True)

    freqs = characteristic_frequencies(geometry)
    classes = ["normal", "inner", "outer"]
    signals = {}
    rows = []

    for class_name in classes:
        fault = (
            FaultParameters(type="normal")
            if class_name == "normal"
            else replace(base_fault, type=class_name)
        )
        result = simulate_bearing(geometry, dynamics, fault, simulation)
        t = result["time_s"]
        x = result["outer_y_acceleration_mps2"]
        np.savez_compressed(
            data_dir / f"{class_name}.npz",
            time_s=t,
            outer_y_acceleration_mps2=x,
            acceleration_mps2=result["acceleration_mps2"],
        )

        xc = x - np.mean(x)
        f_raw, p_raw = periodogram(
            xc, fs=simulation.output_fs_hz, window="hann", scaling="spectrum"
        )
        env = np.abs(hilbert(xc))
        f_env, p_env = periodogram(
            env - np.mean(env),
            fs=simulation.output_fs_hz,
            window="hann",
            scaling="spectrum",
        )
        target = (
            freqs["bpfi_hz"]
            if class_name == "inner"
            else freqs["bpfo_hz"]
            if class_name == "outer"
            else None
        )
        raw_peak = env_peak = raw_error = env_error = None
        if target is not None:
            raw_peak = parabolic_peak(f_raw, p_raw, target)
            env_peak = parabolic_peak(f_env, p_env, target)
            raw_error = abs(raw_peak - target) / target * 100.0
            env_error = abs(env_peak - target) / target * 100.0

        rows.append(
            {
                "class": class_name,
                "samples": len(x),
                "duration_retained_s": float(t[-1] - t[0]),
                "mean": float(np.mean(x)),
                "std": float(np.std(x)),
                "rms_ac": float(np.sqrt(np.mean(xc**2))),
                "peak_abs": float(np.max(np.abs(xc))),
                "target_hz": target,
                "raw_peak_hz": raw_peak,
                "raw_error_pct": raw_error,
                "envelope_peak_hz": env_peak,
                "envelope_error_pct": env_error,
            }
        )
        signals[class_name] = {
            "time": t,
            "x": x,
            "f_raw": f_raw,
            "p_raw": p_raw,
            "f_env": f_env,
            "p_env": p_env,
        }

    for label, target in (("bpfi", freqs["bpfi_hz"]), ("bpfo", freqs["bpfo_hz"])):
        for row in rows:
            s = signals[row["class"]]
            row[f"{label}_raw_band_power"] = band_power(
                s["f_raw"], s["p_raw"], target
            )
            row[f"{label}_env_band_power"] = band_power(
                s["f_env"], s["p_env"], target
            )

    # Exact tables used by the plots/claims.
    with (table_dir / "class_metrics.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    with (table_dir / "characteristic_frequencies.csv").open(
        "w", newline="", encoding="utf-8"
    ) as f:
        w = csv.writer(f)
        w.writerow(["name", "hz"])
        w.writerows(freqs.items())

    freq = signals["normal"]["f_raw"]
    mask = freq <= 500.0
    with (table_dir / "spectra_0_500hz.csv").open(
        "w", newline="", encoding="utf-8"
    ) as f:
        w = csv.writer(f)
        w.writerow(
            ["frequency_hz"]
            + [f"{c}_raw_power" for c in classes]
            + [f"{c}_envelope_power" for c in classes]
        )
        for i in np.where(mask)[0]:
            w.writerow(
                [freq[i]]
                + [signals[c]["p_raw"][i] for c in classes]
                + [signals[c]["p_env"][i] for c in classes]
            )

    # Git-friendly retained signal: complete stable segment, anti-aliased to 4 kHz.
    q = int(simulation.output_fs_hz) // args.git_signal_fs_hz
    compact = {}
    for c in classes:
        y = resample_poly(signals[c]["x"], 1, q)
        tt = signals[c]["time"][0] + np.arange(len(y)) / args.git_signal_fs_hz
        compact[c] = (tt, y)
    n = min(len(v[1]) for v in compact.values())
    compact_path = data_dir / f"signals_{args.git_signal_fs_hz}hz_full.csv"
    with compact_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["time_s"] + [f"{c}_mps2" for c in classes])
        for i in range(n):
            w.writerow([compact["normal"][0][i]] + [compact[c][1][i] for c in classes])

    # Full-resolution excerpt for direct audit of the original sampling grid.
    n_excerpt = int(round(args.full_res_excerpt_s * simulation.output_fs_hz)) + 1
    excerpt_path = data_dir / "signals_64khz_excerpt.csv"
    with excerpt_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["time_s"] + [f"{c}_mps2" for c in classes])
        for i in range(n_excerpt):
            w.writerow(
                [signals["normal"]["time"][i]]
                + [signals[c]["x"][i] for c in classes]
            )

    mpl.rcParams["svg.fonttype"] = "none"
    fig, axes = plt.subplots(3, 3, figsize=(12, 8))
    targets = {"normal": None, "inner": freqs["bpfi_hz"], "outer": freqs["bpfo_hz"]}
    for r, c in enumerate(classes):
        s = signals[c]
        idx = np.where(s["time"] < s["time"][0] + 0.08)[0]
        step = max(1, len(idx) // 800)
        idx = idx[::step]
        axes[r, 0].plot(s["time"][idx] - s["time"][0], s["x"][idx])
        axes[r, 0].set_ylabel(f"{c}\\naccel")
        axes[r, 0].set_xlabel("time [s]")

        m = s["f_raw"] <= 500.0
        axes[r, 1].semilogy(s["f_raw"][m], s["p_raw"][m] + 1e-30)
        axes[r, 2].semilogy(s["f_env"][m], s["p_env"][m] + 1e-30)
        axes[r, 1].set_xlabel("frequency [Hz]")
        axes[r, 2].set_xlabel("frequency [Hz]")
        if targets[c] is not None:
            axes[r, 1].axvline(targets[c], linestyle="--")
            axes[r, 2].axvline(targets[c], linestyle="--")

    for j, title in enumerate(("Time domain", "Raw spectrum", "Envelope spectrum")):
        axes[0, j].set_title(title)
    fig.suptitle("6203 twin audit: normal / inner / outer")
    fig.tight_layout()
    fig.savefig(fig_dir / "signal_audit_panel.svg")
    fig.savefig(fig_dir / "signal_audit_panel.png", dpi=180)
    plt.close(fig)

    fig = plt.figure(figsize=(10, 4))
    for c in classes:
        s = signals[c]
        m = s["f_env"] <= 300.0
        plt.semilogy(s["f_env"][m], s["p_env"][m] + 1e-30, label=c)
    plt.axvline(freqs["bpfi_hz"], linestyle="--", label=f"BPFI {freqs['bpfi_hz']:.2f} Hz")
    plt.axvline(freqs["bpfo_hz"], linestyle=":", label=f"BPFO {freqs['bpfo_hz']:.2f} Hz")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Envelope spectrum power")
    plt.legend()
    plt.tight_layout()
    fig.savefig(fig_dir / "class_envelope_comparison.svg")
    fig.savefig(fig_dir / "class_envelope_comparison.png", dpi=180)
    plt.close(fig)

    shutil.copy2(args.config, out / "config_snapshot.yaml")
    (out / "audit_runtime_overrides.json").write_text(
        json.dumps(
            {
                "simulation.duration_s": simulation.duration_s,
                "simulation.discard_initial_s": simulation.discard_initial_s,
                "git_signal_fs_hz": args.git_signal_fs_hz,
                "full_res_excerpt_s": args.full_res_excerpt_s,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    manifest = {
        "source_repo_commit": git_commit(),
        "base_config_sha256": sha256_file(args.config),
        "characteristic_frequencies_hz": freqs,
        "files": [],
    }
    for p in sorted(out.rglob("*")):
        if p.is_file() and p.name != "manifest.json":
            manifest["files"].append(
                {
                    "path": str(p.relative_to(out)),
                    "bytes": p.stat().st_size,
                    "sha256": sha256_file(p),
                }
            )
    (out / "manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )

    print(json.dumps({"out": str(out), "metrics": rows}, indent=2))


if __name__ == "__main__":
    main()
