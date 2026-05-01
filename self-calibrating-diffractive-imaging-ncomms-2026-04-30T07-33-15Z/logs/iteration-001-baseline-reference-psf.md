# Iteration 001 Baseline Reference PSF

- Timestamp: `2026-04-30T07:55:00Z`
- Action type: `first_quantitative_baseline`
- Stage: `active calculation/verification`
- Single bottleneck addressed: `missing first executable dynamic-aberration baseline`

## Executed action

Implemented and ran `scripts/run_baseline_reference_psf.py`, a minimal Fourier-optics scaffold that:

1. generates low-order dynamic aberrations using defocus, astigmatism, and coma,
2. blurs synthetic objects with the corresponding PSF,
3. compares a fixed reference-free Wiener baseline against a reference-guided baseline using the instantaneous PSF,
4. writes metrics tables, JSON summary, markdown summary, and a visual montage.

## Verified result

- Samples evaluated: `48`
- Mean fixed PSNR: `27.019 dB`
- Mean guided PSNR: `31.289 dB`
- Mean PSNR gain: `4.270 dB`
- Mean fixed SSIM: `0.9818`
- Mean guided SSIM: `0.9907`
- Mean SSIM gain: `0.0088`
- Guided better fraction by PSNR: `0.896`
- Guided better fraction by SSIM: `0.771`

## Interpretation boundary

This result supports the narrow claim that same-path reference information can improve adaptive restoration under dynamic aberrations. It does not yet establish that a passive diffractive neural operator can internalize this gain without explicit post-detection deconvolution.

## Output package

- `results/baselines/baseline-001-reference-psf/baseline_metrics.csv`
- `results/baselines/baseline-001-reference-psf/baseline_summary.csv`
- `results/baselines/baseline-001-reference-psf/baseline_summary.json`
- `results/baselines/baseline-001-reference-psf/baseline_summary.md`
- `results/baselines/baseline-001-reference-psf/example_montage.png`

## Next shortest-path action

Implement a trainable surrogate that consumes the distorted image together with the reference observation, so the next comparison tests learned calibration rather than explicit adaptive deconvolution.
