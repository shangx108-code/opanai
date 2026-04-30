# Iteration 002 Trainable Surrogate

- Timestamp: `2026-04-30T08:05:00Z`
- Action type: `trainable_surrogate_baseline`
- Stage: `active calculation/verification`
- Single bottleneck addressed: `missing first trainable surrogate baseline`

## Executed action

Implemented and ran `scripts/run_baseline_trainable_surrogate.py`, a minimal ridge-regression surrogate that:

1. reuses the same dynamic-aberration generator from baseline 001,
2. consumes low-resolution distorted images together with low-resolution reference PSFs,
3. learns a direct restoration map on the training split,
4. evaluates on held-out aberration cases and writes metrics, summary tables, and a montage.

## Verified result

- Training samples: `432`
- Test samples: `144`
- Mean fixed PSNR at native resolution: `24.284 dB`
- Mean guided PSNR at native resolution: `27.391 dB`
- Mean fixed PSNR at low resolution: `37.541 dB`
- Mean guided PSNR at low resolution: `34.911 dB`
- Mean surrogate PSNR at low resolution: `50.703 dB`
- Mean surrogate gain over fixed at low resolution: `13.162 dB`
- Surrogate better-than-fixed fraction: `0.972`

## Interpretation boundary

This round establishes that reference information is learnable in a simple trainable surrogate, not only exploitable through explicit deconvolution. But the result is still bounded by two strong simplifications: the model operates at low resolution and the train/test splits share the same small synthetic object family. Therefore it is not yet manuscript-grade evidence for distribution-level optical generalization.

## Output package

- `results/baselines/baseline-002-trainable-surrogate/test_metrics.csv`
- `results/baselines/baseline-002-trainable-surrogate/summary_table.csv`
- `results/baselines/baseline-002-trainable-surrogate/summary.json`
- `results/baselines/baseline-002-trainable-surrogate/summary.md`
- `results/baselines/baseline-002-trainable-surrogate/example_montage.png`

## Next shortest-path action

Harden the split by introducing held-out object families and then replace the linear surrogate with a differentiable optical-front-end approximation that keeps the same evaluation ledger.
