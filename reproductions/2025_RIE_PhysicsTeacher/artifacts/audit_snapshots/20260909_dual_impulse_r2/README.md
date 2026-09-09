# Dual-Impulse R2 Audit — 2026-09-09

This snapshot validates the localized-spall dual-impulse mechanism before Teacher dataset construction.

## Literature target

The 2025 reproduction paper explicitly adopts the Luo et al. localized-spall dynamics line and describes the dual-impulse behavior. The referenced mechanism distinguishes:

1. rolling element entering the spall → lower-frequency step response;
2. rolling element striking the trailing edge on exit → higher-frequency transient impulse.

The accessible literature supports a smooth spall-displacement profile and an explicit trailing-edge collision term. The exact collision-force constants used by the 2025 paper are not available in the accessible text.

Therefore:

- half_cosine spall profile is REFERENCED reconstruction;
- exit_impact_force_n=500 N and exit_impact_duration_s=80 us are INFERRED;
- no claim is made that those two numerical values are the authors' original values.

## Quantitative gate

| Metric | Reconstructed model | No-exit-impact negative control |
|---|---:|---:|
| theoretical DITS | 1.078014 ms | 1.078014 ms |
| detected DITS median | 1.093750 ms | 1.046875 ms |
| DITS error | **1.460%** | 2.889% |
| median exit/entry HF peak ratio | **1.785** | 0.870 |
| median exit/entry HF RMS ratio | **1.310** | 0.876 |
| fraction exit peak > entry | 0.571 | 0.286 |
| theoretical BPFI | 123.6842 Hz | 123.6842 Hz |
| envelope BPFI peak | **123.3852 Hz** | 116.3070 Hz |
| BPFI error | **0.242%** | 5.965% |

Acceptance criteria:

- DITS error <= 5%;
- median exit/entry HF peak >= 1.2;
- median exit/entry HF RMS >= 1.1;
- BPFI error <= 2%;
- disabling the trailing-edge impact must reduce the exit/entry HF ratio.

**Result: PASS (mechanism-level R2 dual-impulse gate).**

## Retained evidence

- dual_impulse_metrics.json — aggregate metrics and negative-control results.
- event_metrics.csv — all seven complete defect passages used by the gate.
- strongest_passage.csv — raw / high-pass / low-pass values around the strongest passage.
- dual_impulse_compact.svg — code-generated visualization of the retained passage.

## Interpretation

The previous rectangular-clearance model reproduced the entry/exit timing but failed the dual-impulse morphology: the exit HF impulse was not stronger than the entry event. The reconstructed model fixes this by separating the smooth spall displacement from a transient trailing-edge collision term.

This is a mechanism reconstruction, not a completed high-fidelity calibration of the physical Paderborn rig.
