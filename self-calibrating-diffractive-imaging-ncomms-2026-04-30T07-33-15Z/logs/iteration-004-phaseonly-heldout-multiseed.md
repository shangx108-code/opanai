# Iteration 004 Phase-Only Heldout Multiseed

- Timestamp: `2026-04-30T09:05:00Z`
- Action type: `phaseonly_frontend_multiseed_execution`
- Stage: `active calculation/verification`
- Single bottleneck addressed: `missing phase-only multilayer held-out execution package`

## Executed action

1. Added `scripts/run_baseline_phase_only_heldout_multiseed.py`.
2. Implemented a real `3-layer` phase-only Fresnel frontend with explicit `lambda`, `dx`, `z`, and FFT `fx/fy` ranges in the seed logs.
3. Used held-out aberration cases with the same object family to avoid over-claiming object-family generalization.
4. Ran the baseline for seeds `0, 1, 2`.
5. Generated:
   - `heldout_metrics_seed0.csv`
   - `heldout_metrics_seed1.csv`
   - `heldout_metrics_seed2.csv`
   - `run_log_seed_0.txt`
   - `run_log_seed_1.txt`
   - `run_log_seed_2.txt`
   - `multiseed_summary.csv`
   - `sha256_manifest.txt`

## Verified result

- Phase-only layer count: `3`
- Seed count: `3`
- Multi-seed mean phase-only PSNR: `37.186 dB`
- Multi-seed mean phase-only PSNR gain over fixed: `14.959 dB`
- Multi-seed phase-only PSNR std: `0.851 dB`
- Multi-seed phase-only PSNR 95% CI half-width: `0.963 dB`
- Multi-seed mean phase-only SSIM: `0.99645`
- Multi-seed phase-only better-than-fixed fraction: `1.0`

## Interpretation boundary

This closes the immediate reviewer-facing requirement that the script no longer look like a weak single-layer or single-seed toy. The current evidence is for held-out aberration cases within the same object family. It should not yet be described as object-family generalization.

## Next shortest-path action

Keep the same phase-only multi-layer stack, but add a second evaluation ledger that separates:

- held-out aberration cases on the same object family
- held-out object-family cases under the same training protocol

This will prevent the current strong same-family result from being mistaken for broader structural generalization.
