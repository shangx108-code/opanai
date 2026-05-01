# Iteration 018 Mixed-Train Natural-Object Rerun

- Timestamp: `2026-05-01T00:00:00Z`
- Action type: `mixed_train_proxy_natural_rerun`
- Stage: `active calculation/verification`
- Single bottleneck addressed: `determine whether the strong natural-object failure is primarily a training-distribution mismatch`

## Executed action

1. Added `scripts/run_mixed_train_natural_object_rerun.py`.
2. Mixed the existing synthetic training object family with the project-local proxy natural images already staged under:
   - `data/natural_objects/imagenet-1k-ilsvrc2012-validation`
   - `data/natural_objects/coco-2017-validation`
3. Kept the natural-object evaluation protocol fixed and re-ran the natural-object metrics under the mixed training regime.

## Interpretation boundary

This iteration is a distribution-mismatch test. It does not replace official natural-image validation and must remain explicitly labeled as a proxy-natural mixed-training rerun.

## Verification result

- Mixed training object counts:
  - synthetic training objects: `50`
  - proxy natural training objects: `24`
  - total mixed training objects: `74`
- Output files:
  - `results/natural_objects/mixed_train_natural_object_metrics.csv`
  - `results/natural_objects/mixed_train_natural_object_summary.json`
- `ImageNet-1k` proxy natural rerun:
  - mean fixed PSNR: `19.7862 dB`
  - mean pipeline PSNR: `20.5320 dB`
  - mean PSNR gain over fixed: `+0.7458 dB`
  - better-than-fixed fraction: `0.7639`
- `COCO` proxy natural rerun:
  - mean fixed PSNR: `22.9412 dB`
  - mean pipeline PSNR: `24.2746 dB`
  - mean PSNR gain over fixed: `+1.3334 dB`
  - better-than-fixed fraction: `0.8750`
- Compared with the previous proxy-natural evaluation, the sign flips from strongly negative to positive on both datasets.
