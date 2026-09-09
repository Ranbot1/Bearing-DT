# Snapshot-specific interpretation

This fixed Git snapshot is intentionally shorter than the longer R1/R2 run described in the main validation report.

## Snapshot window

- simulation duration: 0.35 s
- discarded transient: 0.05 s
- retained full-resolution analysis interval: 0.30 s
- sampling rate used for spectral analysis: 64 kHz
- periodogram bin spacing: approximately 3.33 Hz

Because the retained interval is short, the raw spectrum has coarser frequency resolution than the longer validation run.

## Snapshot metrics

From `tables/class_metrics.csv`:

| Class | Theory | Raw peak | Raw error | Envelope peak | Envelope error |
|---|---:|---:|---:|---:|---:|
| Inner | BPFI 123.684 Hz | 125.468 Hz | 1.442% | 123.756 Hz | 0.058% |
| Outer | BPFO 76.316 Hz | 76.676 Hz | 0.472% | 76.287 Hz | 0.037% |

Both remain within the R1 mechanism-level ±2% acceptance band.

The longer R1/R2 validation report uses a longer stable signal and therefore obtains a more precise interpolated raw-spectrum estimate. The fixed Git snapshot exists for **artifact auditability**, not to replace the longer-run metrics.
