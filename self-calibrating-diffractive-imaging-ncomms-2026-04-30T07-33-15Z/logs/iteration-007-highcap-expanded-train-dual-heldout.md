# Iteration 007 Highcap Expanded-Train Dual Heldout

- Timestamp: `2026-04-30T09:48:00Z`
- Action type: `capacity_and_training_family_upgrade`
- Stage: `active calculation/verification`
- Single bottleneck addressed: `expanded training family alone improved new-family behavior only partially`

## Executed action

1. Added `scripts/run_baseline_phase_only_highcap_expanded_train_dual_heldout_multiseed.py`.
2. Increased phase-only capacity from:
   - `3 layers` -> `5 layers`
   - `6 phase basis functions` -> `10 phase basis functions`
   - `8x8 frontend low-resolution grid` -> `12x12`
3. Expanded the training object family from `14` to `22`.
4. Kept both held-out ledgers unchanged:
   - `same_family_heldout_aberration`
   - `new_family_heldout_object_family`
5. Re-ran seeds `0, 1, 2`.

## Verified result

### Same-family held-out aberration

- Mean phase-only PSNR gain over fixed: `11.143 dB`
- Previous expanded-train value: `8.770 dB`
- Better-than-fixed fraction: `1.0`

### New-family held-out object family

- Mean phase-only PSNR gain over fixed: `-3.255 dB`
- Previous expanded-train value: `-4.323 dB`
- Better-than-fixed fraction: `0.0104`

## Interpretation boundary

The higher-capacity phase-only stack plus broader training family improves the new-family ledger again, but the gain remains negative. So the current answer to the reviewer-style question is:

- no, the model is not only memorizing the smallest original object family
- but yes, generalization to genuinely new object families is still insufficient under the current protocol

## Next shortest-path action

The next clean move is to stop only scaling the current surrogate and instead change the training evidence distribution:

- add more distinct object families on the training side
- keep the same dual-heldout ledgers exactly fixed
- test whether the new-family ledger can cross from negative to non-negative gain
