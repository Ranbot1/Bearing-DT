# 6203 Twin Signal Audit Snapshot — 2026-09-09

This directory retains **code-generated** artifacts so the R1/R2 mechanism claims can be checked directly from repository files.

## Generated twin data retained in Git

- `data/signals_checkpoints.csv`  
  Normal / inner / outer signal checkpoints obtained from the generated 64 kHz twin signals after anti-aliased reduction to 1 kHz. The retained 0.10 s interval still contains BPFI/BPFO-scale dynamics and is small enough for direct Git inspection.
- `tables/spectra_0_500hz.csv`  
  Raw-spectrum and envelope-spectrum powers computed from the **full-resolution 0.30 s, 64 kHz generated signals**.
- `tables/class_metrics.csv`  
  Per-class statistics plus BPFI/BPFO peak locations and errors.
- `tables/characteristic_frequencies.csv`  
  Theoretical shaft, BPFI, BPFO, BSF and FTF frequencies.

## Code-generated figure retained in Git

- `figures/fault_frequency_audit.svg`  
  Inner/outer envelope-spectrum audit with the theoretical BPFI/BPFO locations marked.

## Provenance

- `config_snapshot.yaml`: base simulator configuration.
- `audit_runtime_overrides.json`: short fixed audit-run settings.
- `manifest.json`: generation-side SHA-256 provenance, including the full-resolution NPZ files generated in the same run. Text-file line-ending normalization by Git may change the byte-level hash after commit.

The same run generated full-resolution `normal.npz`, `inner.npz`, and `outer.npz`. Their SHA-256 values are preserved in `manifest.json`. They are reproducible with:

```bash
python scripts/06_build_audit_snapshot.py \
  --config configs/paper_6203.yaml \
  --out artifacts/local_full_snapshot \
  --duration-s 0.35 \
  --discard-initial-s 0.05
```

The local full snapshot also contains PNG/SVG figures and full-resolution binary arrays.

## Important limitation

Several dynamics and defect parameters remain `INFERRED`. These files verify the **mechanism-level reproduction pipeline**, not high-fidelity waveform matching to the physical Paderborn rig.
