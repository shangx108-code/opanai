# Baseline 001 Summary

Goal: test whether a co-propagating reference PSF can improve restoration under dynamic aberrations before any diffractive-network training.

## Scope

- Dynamic perturbation family: low-order Zernike-like defocus, astigmatism, and coma
- Propagation model: angular spectrum
- Sample spacing Δx: 8.000e-06 m
- Wavelength λ: 5.320e-07 m
- Propagation distance z: 1.200e-02 m
- Frequency coordinates fx range: -6.250e+04 to 6.152e+04 1/m
- Frequency coordinates fy range: -6.250e+04 to 6.152e+04 1/m
- Restoration comparison:
  - fixed reference-free Wiener deconvolution using a nominal PSF
  - reference-guided Wiener deconvolution using the instantaneous PSF from the co-propagating reference
- Objects: 6 synthetic binary patterns
- Aberration cases: 8
- Total evaluated samples: 48

## Aggregate results

- Mean fixed PSNR: 12.946 dB
- Mean guided PSNR: 14.440 dB
- Mean PSNR gain: 1.493 dB
- Mean fixed SSIM: 0.6753
- Mean guided SSIM: 0.7775
- Mean SSIM gain: 0.1022
- Guided better fraction by PSNR: 1.000
- Guided better fraction by SSIM: 1.000

## Interpretation boundary

This is a pre-network baseline scaffold, not yet evidence for the full passive diffractive neural-operator claim. What it does establish is a first executable reference point: when the instantaneous distortion kernel is available through a co-path reference, adaptive restoration outperforms a fixed non-adaptive baseline under the same dynamic aberration family.

## Next executable step

Replace the pure post-detection adaptive deconvolution with a trainable optical-frontend surrogate or differentiable diffractive layer stack, while keeping the same perturbation generator and metrics ledger.
