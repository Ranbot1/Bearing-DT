# 6203 Twin Signal Audit Snapshot — 2026-09-09

This directory contains **code-generated and retained** audit artifacts for the R1/R2 physics validation.

## What is actually retained in Git

### Generated twin data

- `data/signals_1khz/part_01.csv ... part_07.csv`
  - complete retained stable interval from 0.05 s to 0.35 s;
  - normal / inner / outer signals;
  - anti-aliased downsampling from the original 64 kHz simulation to 1 kHz;
  - sufficient to independently inspect BPFO/BPFI-scale periodic evidence.
- `data/signals_64khz_excerpt_1ms.csv`
  - 1 ms excerpt at the original **64 kHz** sampling grid;
  - retained so the repository also contains un-downsampled waveform values.

### Signal-processing data

- `tables/characteristic_frequencies.csv`
  - theoretical shaft / BPFI / BPFO / BSF / FTF frequencies.
- `tables/class_metrics.csv`
  - waveform statistics, raw-spectrum target peaks, envelope-spectrum target peaks and fault-band energies.
- `tables/spectra_fault_band_60_140hz.csv`
  - exact raw/envelope spectrum values covering both BPFO and BPFI neighborhoods.

### Code-generated figures

- `figures/inner_time_domain.svg`
- `figures/inner_raw_spectrum.svg`
- `figures/inner_envelope_spectrum.svg`
- `figures/class_envelope_comparison.svg`

These SVGs are generated from the same retained simulation run; they are not externally generated images.

## Key audit numbers from this fixed snapshot

| Item | Value |
|---|---:|
| theoretical BPFI | 123.6842 Hz |
| inner raw-spectrum local peak | 125.4680 Hz |
| inner raw error | 1.442% |
| inner envelope peak | 123.7564 Hz |
| inner envelope error | **0.058%** |
| theoretical BPFO | 76.3158 Hz |
| outer raw-spectrum local peak | 76.6760 Hz |
| outer raw error | 0.472% |
| outer envelope peak | 76.2874 Hz |
| outer envelope error | **0.037%** |

The shorter fixed snapshot has coarser frequency resolution than the longer R1/R2 run, so the raw-spectrum inner peak error is larger; the envelope-spectrum mechanism check remains close to theory.

## Provenance

- `config_snapshot.yaml`: simulator configuration copied into the snapshot.
- `audit_runtime_overrides.json`: short-run overrides.
- `manifest.json`: retained-file SHA-256 values plus hashes for the full-resolution NPZ files produced by the same run.

The complete 64 kHz NPZ arrays are generated locally by `scripts/06_build_audit_snapshot.py`. Git retains the complete 0.30 s mechanism-band signal at 1 kHz plus a raw 64 kHz excerpt so that the repository remains inspectable without turning Git history into a bulk binary store.

## Limitation

Effective mass, stiffness, damping, Hertz coefficient, clearance and defect dimensions remain `INFERRED`. This snapshot validates **mechanism-level signal behavior**, not high-fidelity physical-rig waveform matching.
