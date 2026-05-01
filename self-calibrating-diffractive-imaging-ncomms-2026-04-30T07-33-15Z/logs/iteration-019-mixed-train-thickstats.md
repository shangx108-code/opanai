# Iteration 019 Mixed-Train Thickstats

- Timestamp: `2026-05-01T00:00:00Z`
- Action type: `mixed_train_proxy_natural_thickstats`
- Stage: `active calculation/verification`
- Single bottleneck addressed: `determine whether the positive mixed-train natural-object gain is statistically stable rather than a single-seed artifact`

## Executed action

1. Added `scripts/run_mixed_train_natural_object_thickstats.py`.
2. Increased the natural-object mixed-train validation thickness to:
   - seeds: `5` (`0-4`)
   - natural-object held-out cases per seed: `12`
3. Kept the mixed training regime fixed while re-running the proxy natural-object evaluation.

## Verification result

- Seeds: `5` (`0-4`)
- Natural-object held-out cases per seed: `12`
- `COCO` proxy natural thickstats:
  - mean PSNR gain over fixed: `+1.4520 dB`
  - 95% CI half-width: `0.1370 dB`
  - mean better-than-fixed fraction: `0.9111`
- `ImageNet-1k` proxy natural thickstats:
  - mean PSNR gain over fixed: `+0.9841 dB`
  - 95% CI half-width: `0.2501 dB`
  - mean better-than-fixed fraction: `0.7736`
- The positive mixed-train natural-object gain remains positive after thickening and does not collapse back toward the strongly negative baseline proxy-natural run.
