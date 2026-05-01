# Iteration 005 Dual Heldout Ledgers

- Timestamp: `2026-04-30T09:18:00Z`
- Action type: `dual_ledger_phaseonly_generalization_split`
- Stage: `active calculation/verification`
- Single bottleneck addressed: `same-family gain was strong but object-family generalization boundary was missing`

## Executed action

1. Added `scripts/run_baseline_phase_only_dual_heldout_multiseed.py`.
2. Reused the same trained `3-layer phase-only` Fresnel frontend for two separate evaluation ledgers:
   - `same_family_heldout_aberration`
   - `new_family_heldout_object_family`
3. Ran both ledgers for seeds `0, 1, 2`.
4. Generated separate per-seed metrics, run logs, `multiseed_summary.csv`, and `sha256_manifest.txt` inside each ledger directory.

## Verified result

### Same-family held-out aberration

- Multi-seed mean phase-only PSNR: `37.186 dB`
- Multi-seed mean phase-only PSNR gain over fixed: `14.959 dB`
- Multi-seed phase-only SSIM: `0.99645`
- Better-than-fixed fraction: `1.0`

### New-family held-out object family

- Multi-seed mean phase-only PSNR: `14.933 dB`
- Multi-seed mean phase-only PSNR gain over fixed: `-5.343 dB`
- Multi-seed phase-only SSIM: `0.66568`
- Better-than-fixed fraction: `0.0104`

## Interpretation boundary

The current `3-layer phase-only` system generalizes well to unseen aberration realizations within the same object family, but it does not generalize to a new object family under the current training protocol. This means the present result supports aberration-side robustness, not broader structural object-family generalization.

## Next shortest-path action

Keep the same dual-ledger bookkeeping, but improve the training protocol rather than the wording:

- enlarge the training object family
- keep the same held-out object-family ledger
- retest whether the new-family ledger can at least recover non-negative gain over fixed
