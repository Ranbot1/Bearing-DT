# Reproduction Status

Status: **PHYSICS_REPRODUCED — R1 passed; R2 mechanism gates passed; Teacher dataset pilot passed**

Last update: 2026-09-09

## Completed

- repository contract / constraints
- staged acceptance criteria
- evidence ledger
- 6203 geometry config
- PU operating-condition config
- paper training hyperparameters
- 4-DOF second-order ODE implementation
- Hertz nonlinear contact
- localized inner/outer defect hook
- characteristic-frequency functions
- simulator validation plotting script
- confirmed network macro-architecture encoded:
  - 4 Conv
  - BN
  - CBAM
  - 128-d feature
  - 128→64→1 discriminator
- MK-MMD loss primitive
- smoke/unit test sources

## Not yet accepted

- exact paper numerical parameters for the trailing-edge collision term
- high-fidelity amplitude/resonance calibration to the physical rig
- exact Fig. 7/9 conv channels/kernels
- exact preprocessing/input representation
- Paderborn data loader + manifest
- Teacher training
- full MADA/global+subdomain training loop
- HUST ball-fault simulator
- paper-level accuracy reproduction

## Current gate

R1 mechanism sanity is now accepted for:
- inner BPFI;
- speed scaling;
- outer BPFO after correcting the load-zone angle.

R2 mechanism-level validation is now accepted:
- Fig.5 BPFI frequency evidence: PASS;
- dual-impulse DITS: PASS;
- exit > entry high-frequency impulse: PASS;
- no-exit-impact negative control: PASS.

This remains a mechanism-level reconstruction, not a calibrated high-fidelity physical-rig twin.

A fixed audit snapshot is now retained under `artifacts/audit_snapshots/20260909_6203_r1r2/`, including generated twin data, fault-band spectra, metrics and code-generated SVG figures.

The generated evidence used for this gate is now retained in:
`artifacts/audit_snapshots/20260909_6203_r1r2/`
so the signal values, spectra, figure, config, and hashes can be inspected independently.

Teacher dataset construction pilot is now accepted:
- 18 raw windows, shape 18×2048;
- normal / inner / outer balanced;
- train / val / test balanced;
- simulation-run-isolated splits;
- train / val / test raw-value audit CSVs retained;
- NPZ SHA-256 retained;
- code-generated Teacher-window SVG retained.

**R3 Teacher pretraining remains BLOCKED only on the paper-faithful input/preprocessing ambiguity.**

See [PREPROCESSING_AUDIT.md](PREPROCESSING_AUDIT.md).

## Next coding milestone

1. recover Fig.7/Fig.9 input tensor and Conv details from stronger evidence if possible;
2. if unavailable, create an explicitly named fallback track (not paper-confirmed);
3. only then run Teacher pretraining and report 3-seed held-out simulated-domain performance.
