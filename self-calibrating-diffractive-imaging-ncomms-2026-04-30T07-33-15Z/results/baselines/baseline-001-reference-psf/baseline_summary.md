# Baseline 001 Summary

Goal: test whether a co-propagating reference PSF can improve restoration under dynamic aberrations before any diffractive-network training.

## Scope

- Dynamic perturbation family: low-order Zernike-like defocus, astigmatism, and coma
- Restoration comparison:
  - fixed reference-free Wiener deconvolution using a nominal PSF
  - reference-guided Wiener deconvolution using the instantaneous PSF from the co-propagating reference
- Objects: 6 synthetic binary patterns
- Aberration cases: 8
- Total evaluated samples: 48

## Aggregate results

- Mean fixed PSNR: 27.019 dB
- Mean guided PSNR: 31.289 dB
- Mean PSNR gain: 4.270 dB
- Mean fixed SSIM: 0.9818
- Mean guided SSIM: 0.9907
- Mean SSIM gain: 0.0088
- Guided better fraction by PSNR: 0.896
- Guided better fraction by SSIM: 0.771

## Interpretation boundary

This is a pre-network baseline scaffold, not yet evidence for the full passive diffractive neural-operator claim. What it does establish is a first executable reference point: when the instantaneous distortion kernel is available through a co-path reference, adaptive restoration outperforms a fixed non-adaptive baseline under the same dynamic aberration family.

## Next executable step

Replace the pure post-detection adaptive deconvolution with a trainable optical-frontend surrogate or differentiable diffractive layer stack, while keeping the same perturbation generator and metrics ledger.
