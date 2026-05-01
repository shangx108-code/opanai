# Iteration 020 Mixed-Train Tolerance

- Timestamp: `2026-05-01T00:00:00Z`
- Action type: `mixed_train_tolerance_execution`
- Stage: `active calculation/verification`
- Single bottleneck addressed: `step 3 required real tolerance numbers instead of only a frozen fairness matrix`

## Executed action

1. Added `scripts/run_mixed_train_tolerance.py`.
2. Bound step 3 to the mixed-train natural-object regime.
3. Implemented first-pass tolerance execution for:
   - common perturbations across all four methods:
     - reference-channel misregistration
     - reference-channel intensity noise
   - phase-only engineering perturbations:
     - phase-mask quantization
     - phase-mask lateral shift

## Interpretation boundary

This is the first executable tolerance package. It covers the most important common perturbations plus phase-only engineering diagnostics, but it does not yet include the propagation-distance branch from the fairness matrix.

## Verification result

- Seeds: `3` (`0-2`)
- Training regime: `mixed synthetic + proxy natural`
- Common cross-method perturbations:
  - reference-channel intensity noise
  - reference-channel misregistration
  - propagation-distance error
- Phase-only engineering perturbations:
  - phase-mask quantization
  - phase-mask lateral shift
- Strongest stable pattern:
  - under common perturbations, `reference_psf_deconvolution` remains strongest
  - `phase_only_stack` remains positive on both datasets under reference noise:
    - COCO at noise `0.01`: `+1.3594 dB`
    - COCO at noise `0.02`: `+1.1405 dB`
    - ImageNet at noise `0.01`: `+1.0432 dB`
    - ImageNet at noise `0.02`: `+0.9048 dB`
- Phase-only engineering sensitivity is severe:
  - lateral shift `1 px` or `2 px` drives the phase-only stack strongly negative on both datasets
  - `3`-bit and `4`-bit phase quantization also drive the phase-only stack strongly negative
- Propagation-distance branch is now executed and shows comparatively mild sensitivity within `±5% z`:
  - `phase_only_stack` stays positive on both datasets across `-5%`, `0%`, and `+5%`
  - `reference_psf_deconvolution` remains strongest on this branch
  - `spectral_frontend` also remains positive on this branch
- The current first-pass misregistration implementation shows little change between `0 px` and `1 px`, so finer-grained subpixel stress is the more informative next tolerance refinement.
