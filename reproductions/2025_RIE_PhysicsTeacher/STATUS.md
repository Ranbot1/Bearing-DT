# Reproduction Status

Status: **PHYSICS_REPRODUCED_PARTIAL — R1 passed; R2 Fig.5 frequency evidence passed**

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

- exact dual-impulse localized-spall function
- paper-level Fig. 5 simulation reproduction
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

R2 is only a **partial pass**: the Fig.5 frequency-domain mechanism evidence is reproduced, but dual-impulse time morphology / amplitude / resonance fidelity are not yet accepted.

**Do not enable R3 Teacher pretraining until the three-class virtual dataset generator and per-class QA are completed.**

## Next coding milestone

1. reproduce Fig. 5 inner-race simulation around 123.24 Hz;
2. add normal / inner / outer virtual-dataset generator for PU;
3. lock the exact network input/preprocessing from the paper;
4. enable Teacher pretraining only after steps 1–3 pass.
