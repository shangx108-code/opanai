# Baseline 002 Summary

Goal: test a first trainable surrogate that consumes the distorted image together with the reference observation, without relying on any external deep-learning framework.

## Scope

- Training split: 72 aberration cases x 6 objects = 432 samples
- Test split: 24 aberration cases x 6 objects = 144 samples
- Surrogate type: linear ridge regression on low-resolution image and reference features
- Input features: low-resolution distorted image plus low-resolution reference PSF
- Output target: low-resolution restored image

## Test results

- Mean fixed PSNR at native resolution: 24.284 dB
- Mean guided PSNR at native resolution: 27.391 dB
- Mean fixed PSNR at low resolution: 37.541 dB
- Mean guided PSNR at low resolution: 34.911 dB
- Mean surrogate PSNR at low resolution: 50.703 dB
- Mean surrogate gain over fixed at low resolution: 13.162 dB
- Mean gap from surrogate to guided at low resolution: -15.792 dB
- Surrogate better-than-fixed fraction: 0.972

## Interpretation boundary

This round tests learned calibration in the mildest possible form. The surrogate does beat the fixed baseline on held-out aberration cases, which supports the claim that reference information is learnable rather than only usable through explicit deconvolution. However, the training and test sets still share the same small object family and the surrogate is evaluated at low resolution, so this result should be treated as evidence for learnability, not yet as evidence for publishable optical generalization or the final passive diffractive implementation.

## Next executable step

Upgrade the surrogate from linear low-resolution regression to a differentiable optical-front-end approximation with stronger spatial capacity, while keeping the same train/test split and metrics ledger.
