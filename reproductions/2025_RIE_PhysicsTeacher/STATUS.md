# Reproduction Status

Status: **PARTIAL — R0 scaffold + R1 physics implementation started**

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

**Do not proceed to claim R3 Teacher reproduction until R1/R2 simulator evidence is saved and reviewed.**

## Next coding milestone

1. reproduce Fig. 5 inner-race simulation around 123.24 Hz;
2. add normal / inner / outer virtual-dataset generator for PU;
3. lock the exact network input/preprocessing from the paper;
4. enable Teacher pretraining only after steps 1–3 pass.
