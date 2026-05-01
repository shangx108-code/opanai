# Iteration 008 Ultradiverse-Train Dual Heldout

- Timestamp: `2026-04-30T10:06:00Z`
- Action type: `training_family_diversity_push`
- Stage: `active calculation/verification`
- Single bottleneck addressed: `new-family ledger was still negative after capacity and moderate training-family expansion`

## Executed action

1. Added `scripts/run_baseline_phase_only_ultradiverse_train_dual_heldout_multiseed.py`.
2. Kept the evaluation protocol fixed:
   - `same_family_heldout_aberration`
   - `new_family_heldout_object_family`
3. Kept phase-only capacity fixed at the previous higher-capacity setting:
   - `5 layers`
   - `10 phase basis functions`
   - `12x12 frontend`
4. Expanded the training object family further from `22` to `36`.
5. Re-ran seeds `0, 1, 2`.

## Verified result

### Same-family held-out aberration

- Mean phase-only PSNR gain over fixed: `9.147 dB`
- Previous value: `11.143 dB`
- Better-than-fixed fraction: `1.0`

### New-family held-out object family

- Mean phase-only PSNR gain over fixed: `-0.899 dB`
- Previous value: `-3.255 dB`
- Better-than-fixed fraction: `0.3177`
- Mean phase-only SSIM: `0.8219`

## Interpretation boundary

This is the strongest evidence so far that training-family diversity is the right direction. The new-family ledger improves substantially and approaches the non-negative threshold, but it is still slightly negative on average. So the current statement is:

- the model is clearly not only memorizing a tiny training family
- object-family generalization is now much closer to acceptable
- but the evidence still stops just short of claiming positive average gain on new families

## Next shortest-path action

Keep the same dual-ledger evaluation frozen and make one more training-family expansion pass before changing any other part of the method. The current trend suggests that another diversity push has a real chance of crossing the non-negative line.
