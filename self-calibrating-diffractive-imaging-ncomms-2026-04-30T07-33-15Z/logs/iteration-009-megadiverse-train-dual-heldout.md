# Iteration 009 Megadiverse-Train Dual Heldout

- Timestamp: `2026-04-30T10:28:00Z`
- Action type: `training_family_diversity_crosses_zero`
- Stage: `active calculation/verification`
- Single bottleneck addressed: `new-family ledger was close to zero but still negative`

## Executed action

1. Added `scripts/run_baseline_phase_only_megadiverse_train_dual_heldout_multiseed.py`.
2. Kept the evaluation protocol frozen:
   - `same_family_heldout_aberration`
   - `new_family_heldout_object_family`
3. Kept model capacity frozen at:
   - `5 layers`
   - `10 phase basis functions`
   - `12x12 frontend`
4. Expanded the training object family from `36` to `50`.
5. Re-ran seeds `0, 1, 2`.

## Verified result

### New-family held-out object family

- Mean phase-only PSNR gain over fixed: `+0.431 dB`
- Previous value: `-0.899 dB`
- Better-than-fixed fraction: `0.5260`
- Mean phase-only SSIM gain over fixed: `+0.0132`

### Same-family held-out aberration

- Mean phase-only PSNR gain over fixed: `8.007 dB`
- Previous value: `9.147 dB`
- Better-than-fixed fraction: `1.0`

## Interpretation boundary

This is the first run in which the `new_family_heldout_object_family` ledger crosses from negative to positive average gain while the evaluation protocol remains unchanged. That means the most defensible current statement is:

- broader training-family diversity can recover positive average performance on genuinely new object families
- the model is no longer only strong on same-family held-out aberrations
- there remains a tradeoff: same-family peak performance softens somewhat as diversity increases

## Next shortest-path action

Do not change the ledgers. The next clean move is to stabilize this positive new-family margin by repeating with more seeds or slightly more held-out cases, so the reviewer-facing claim rests on a thicker statistics package rather than a single 3-seed crossing.
