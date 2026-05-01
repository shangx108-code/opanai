# Iteration 006 Expanded-Train Dual Heldout

- Timestamp: `2026-04-30T09:32:00Z`
- Action type: `expanded_training_family_retest`
- Stage: `active calculation/verification`
- Single bottleneck addressed: `reviewer concern that the phase-only model may just memorize a small object family`

## Executed action

1. Added `scripts/run_baseline_phase_only_dual_heldout_expanded_train_multiseed.py`.
2. Expanded the training object family from `6` to `14` objects.
3. Kept both evaluation ledgers unchanged:
   - `same_family_heldout_aberration`
   - `new_family_heldout_object_family`
4. Re-ran the `3-layer phase-only` pipeline for seeds `0, 1, 2`.

## Verified result

### Same-family held-out aberration

- Mean phase-only PSNR gain over fixed: `8.770 dB`
- Better-than-fixed fraction: `0.9896`

### New-family held-out object family

- Mean phase-only PSNR gain over fixed: `-4.323 dB`
- Previous value before training-family expansion: `-5.343 dB`
- Better-than-fixed fraction: `0.0052`

## Interpretation boundary

Expanding the training object family helps the new-family ledger, but only partially. The result improves from strongly negative to less negative, which means the previous failure was not only pure memorization of a tiny training set. However, the current model still does not achieve non-negative gain on genuinely new object families, so the reviewer concern is reduced but not closed.

## Next shortest-path action

The next credible move is no longer wording. It is to increase model capacity or training diversity while preserving the same two ledgers:

- either increase phase-only capacity beyond the current basis-limited `3-layer` setup
- or broaden training families further and re-run the exact same dual-ledger protocol
