#!/usr/bin/env python
"""Generate normal/inner/outer virtual bearing signals from the 4-DOF simulator."""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import replace
from pathlib import Path

import numpy as np
import yaml

from fmdtl.config import load_components
from fmdtl.sim import FaultParameters, simulate_bearing


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=Path("data/generated/pu_6203"))
    parser.add_argument("--classes", nargs="+", default=["normal", "inner", "outer"])
    args = parser.parse_args()

    cfg, geometry, dynamics, base_fault, simulation = load_components(args.config)
    args.out.mkdir(parents=True, exist_ok=True)

    manifest = {
        "config": str(args.config),
        "config_sha256": sha256_file(args.config),
        "classes": [],
        "sampling_hz": simulation.output_fs_hz,
        "duration_s": simulation.duration_s,
        "discard_initial_s": simulation.discard_initial_s,
    }

    for class_name in args.classes:
        if class_name == "normal":
            fault = FaultParameters(type="normal")
        elif class_name in {"inner", "outer"}:
            fault = replace(base_fault, type=class_name)
        else:
            raise ValueError(f"Unsupported class: {class_name}")

        result = simulate_bearing(geometry, dynamics, fault, simulation)
        out_file = args.out / f"{class_name}.npz"
        np.savez_compressed(
            out_file,
            time_s=result["time_s"],
            outer_y_acceleration_mps2=result["outer_y_acceleration_mps2"],
            acceleration_mps2=result["acceleration_mps2"],
        )

        x = result["outer_y_acceleration_mps2"]
        manifest["classes"].append(
            {
                "class": class_name,
                "file": out_file.name,
                "n_samples": int(x.size),
                "rms": float(np.sqrt(np.mean((x - np.mean(x)) ** 2))),
                "std": float(np.std(x)),
            }
        )

    (args.out / "manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    (args.out / "config_snapshot.yaml").write_text(
        yaml.safe_dump(cfg, sort_keys=False), encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
