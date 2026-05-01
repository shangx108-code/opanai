# Iteration 010 Thickstats Validation

- Timestamp: `2026-04-30T10:52:00Z`
- Action type: `statistical_thickening_after_zero_crossing`
- Stage: `active calculation/verification`
- Single bottleneck addressed: `positive new-family gain existed, but statistics were still thin`

## Executed action

1. Added `scripts/run_baseline_phase_only_megadiverse_train_dual_heldout_thickstats.py`.
2. Kept the method and dual-ledger protocol frozen:
   - training object family count: `50`
   - phase-only capacity: `5 layers`, `10 phase basis functions`, `12x12 frontend`
   - ledgers:
     - `same_family_heldout_aberration`
     - `new_family_heldout_object_family`
3. Increased statistics thickness from:
   - `3 seeds` -> `5 seeds`
   - `16 held-out cases` -> `24 held-out cases`
4. Re-ran the full package.

## Verified result

### New-family held-out object family

- Mean phase-only PSNR gain over fixed: `+0.484 dB`
- Standard deviation across seeds: `0.264 dB`
- 95% CI half-width: `0.231 dB`
- Better-than-fixed fraction: `0.5438`
- Mean phase-only SSIM gain over fixed: `+0.0146`

### Same-family held-out aberration

- Mean phase-only PSNR gain over fixed: `7.748 dB`
- Standard deviation across seeds: `0.393 dB`
- 95% CI half-width: `0.344 dB`
- Better-than-fixed fraction: `1.0`

## Interpretation boundary

The positive new-family result survives thicker statistics. This is stronger than the earlier 3-seed crossing because both the seed count and held-out case count were increased while the protocol stayed fixed. The most defensible current statement is now:

- positive average gain on new object families is reproducible under a thicker statistics package
- the positive margin is still modest, so it should be described as a narrow but real crossover rather than a large-margin win
- same-family performance remains much stronger than new-family performance

## Next shortest-path action

The next clean move is no longer to prove sign stability. It is to improve the size of the positive margin on the new-family ledger without changing the ledger itself.
