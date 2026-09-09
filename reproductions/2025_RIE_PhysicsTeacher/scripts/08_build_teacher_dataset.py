#!/usr/bin/env python
"""Construct a run-isolated PU-6203 simulated Teacher dataset.

This script stores raw simulated vibration windows. It deliberately does NOT
apply an unconfirmed time-frequency/2D transform; that transformation remains
a later gate until the paper's exact preprocessing is recovered.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from dataclasses import replace
from math import pi
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import yaml

from fmdtl.config import load_components
from fmdtl.sim import FaultParameters, simulate_bearing


CLASSES = ("normal", "inner", "outer")
LABELS = {name: i for i, name in enumerate(CLASSES)}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-config", type=Path, required=True)
    ap.add_argument("--dataset-config", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    base_cfg, geometry0, dynamics, fault0, simulation0 = load_components(args.base_config)
    dcfg = yaml.safe_load(args.dataset_config.read_text(encoding="utf-8"))
    construction = dcfg["construction"]
    rng = np.random.default_rng(int(dcfg["dataset"]["seed"]))

    window = int(construction["window_samples"])
    stride = int(construction["stride_samples"])
    duration = float(construction["simulation_duration_s"])
    discard = float(construction["discard_initial_s"])

    args.out.mkdir(parents=True, exist_ok=True)
    windows = []
    labels = []
    splits = []
    run_ids = []
    rows = []
    run_rows = []

    for class_name in CLASSES:
        for split in ("train", "val", "test"):
            n_runs = int(construction["runs"][split])
            for run_index in range(n_runs):
                phase = (
                    float(rng.uniform(0.0, 2.0 * pi))
                    if construction["randomize_initial_ball_phase"]
                    else geometry0.initial_ball_angle_rad
                )
                geometry = replace(geometry0, initial_ball_angle_rad=phase)
                if class_name == "normal":
                    fault = FaultParameters(type="normal")
                else:
                    fault = replace(fault0, type=class_name)
                simulation = replace(
                    simulation0,
                    duration_s=duration,
                    discard_initial_s=discard,
                )

                run_id = f"{class_name}_{split}_r{run_index:02d}"
                result = simulate_bearing(geometry, dynamics, fault, simulation)
                x = result["outer_y_acceleration_mps2"].astype(np.float32)

                if not np.isfinite(x).all():
                    raise RuntimeError(f"Non-finite values in {run_id}")

                starts = list(range(0, len(x) - window + 1, stride))
                if not starts:
                    raise RuntimeError(
                        f"{run_id} is too short for window={window}; retained={len(x)}"
                    )

                run_rows.append(
                    {
                        "run_id": run_id,
                        "class": class_name,
                        "split": split,
                        "initial_ball_angle_rad": phase,
                        "n_signal_samples": int(len(x)),
                        "n_windows": len(starts),
                        "signal_rms": float(np.sqrt(np.mean((x - np.mean(x)) ** 2))),
                    }
                )

                for local_index, start in enumerate(starts):
                    sample = x[start : start + window]
                    sample_id = len(windows)
                    windows.append(sample)
                    labels.append(LABELS[class_name])
                    splits.append(split)
                    run_ids.append(run_id)
                    rows.append(
                        {
                            "sample_id": sample_id,
                            "class": class_name,
                            "label": LABELS[class_name],
                            "split": split,
                            "run_id": run_id,
                            "window_index_in_run": local_index,
                            "start_sample": start,
                            "window_samples": window,
                            "stride_samples": stride,
                            "initial_ball_angle_rad": phase,
                            "mean": float(np.mean(sample)),
                            "std": float(np.std(sample)),
                            "rms_ac": float(
                                np.sqrt(np.mean((sample - np.mean(sample)) ** 2))
                            ),
                        }
                    )

    x_all = np.stack(windows).astype(np.float32)
    y_all = np.asarray(labels, dtype=np.int64)
    split_all = np.asarray(splits)
    run_all = np.asarray(run_ids)

    np.savez_compressed(
        args.out / "teacher_windows_raw.npz",
        x=x_all,
        y=y_all,
        split=split_all,
        run_id=run_all,
    )

    with (args.out / "sample_manifest.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    with (args.out / "run_manifest.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(run_rows[0].keys()))
        writer.writeheader()
        writer.writerows(run_rows)

    summary = {
        "dataset_id": dcfg["dataset"]["id"],
        "shape": list(x_all.shape),
        "sampling_hz": int(dcfg["paper_confirmed"]["sampling_hz"]),
        "window_samples": window,
        "stride_samples": stride,
        "class_counts": {
            c: int(sum(row["class"] == c for row in rows)) for c in CLASSES
        },
        "split_counts": {
            s: int(sum(row["split"] == s for row in rows))
            for s in ("train", "val", "test")
        },
        "run_counts": {
            s: int(sum(row["split"] == s for row in run_rows))
            for s in ("train", "val", "test")
        },
        "base_config_sha256": sha256_file(args.base_config),
        "dataset_config_sha256": sha256_file(args.dataset_config),
        "input_transform_status": construction["input_transform"],
        "run_isolated_split": True,
    }
    (args.out / "summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )

    # Retained visual QA: first raw window from each class in the train split.
    fig = plt.figure(figsize=(10, 6))
    for class_name in CLASSES:
        idx = next(
            i
            for i, row in enumerate(rows)
            if row["class"] == class_name and row["split"] == "train"
        )
        t = np.arange(window) / float(dcfg["paper_confirmed"]["sampling_hz"])
        plt.plot(t * 1e3, x_all[idx], label=class_name, alpha=0.8)
    plt.xlabel("Time [ms]")
    plt.ylabel("Outer-y acceleration [m/s²]")
    plt.legend()
    plt.tight_layout()
    fig.savefig(args.out / "teacher_window_examples.svg")
    fig.savefig(args.out / "teacher_window_examples.png", dpi=180)
    plt.close(fig)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
