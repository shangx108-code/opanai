# Iteration 021 Robust-Mask Mitigation

- Timestamp: `2026-05-01T00:00:00Z`
- Action type: `robust_mask_mitigation_training`
- Stage: `active calculation/verification`
- Single bottleneck addressed: `phase-mask quantization and lateral-shift sensitivity remained the dominant tolerance failure`

## Executed action

1. Added `scripts/run_robust_mask_tolerance_compare.py`.
2. Injected mask perturbation into phase-only training through a robust training variant set:
   - unperturbed mask
   - `4`-bit quantized mask
   - `3`-bit quantized mask
   - `1`-pixel shifted mask
3. Re-trained the phase-only stack under the mixed-train regime with these perturbations in-loop.
4. Compared the resulting robust phase-only model against the current tolerance baseline.

## Verification result

- Environment check passed in the long-term project space.
- Comparison outputs:
  - `results/tolerance/robust_mask_tolerance_metrics.csv`
  - `results/tolerance/robust_mask_tolerance_compare.csv`
  - `results/tolerance/robust_mask_tolerance_compare.json`
- Clean reference performance improved versus the tolerance baseline:
  - COCO: `+2.1783 dB` vs baseline `+1.4540 dB`
  - ImageNet: `+2.8116 dB` vs baseline `+1.0733 dB`
- Robust-mask mitigation strongly repairs the previously catastrophic `1 px` shift and `3/4 bit` quantization cases:
  - `1 px` shift, COCO: `+2.0569 dB` vs baseline `-13.7673 dB`
  - `1 px` shift, ImageNet: `+2.3911 dB` vs baseline `-10.8126 dB`
  - `3`-bit quantization, COCO: `+2.0673 dB` vs baseline `-13.0224 dB`
  - `3`-bit quantization, ImageNet: `+2.3374 dB` vs baseline `-10.5161 dB`
  - `4`-bit quantization, COCO: `+2.1784 dB` vs baseline `-11.0465 dB`
  - `4`-bit quantization, ImageNet: `+2.5652 dB` vs baseline `-8.4410 dB`
- Remaining failure:
  - `2 px` lateral shift remains strongly negative and is not fixed by the current robust-mask training.
