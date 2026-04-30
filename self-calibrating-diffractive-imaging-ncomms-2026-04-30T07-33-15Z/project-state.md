# Project State

- Project ID: `self-calibrating-diffractive-imaging-ncomms-2026-04-30T07-33-15Z`
- Locked title: `Self-calibrating diffractive optical neural operators for imaging through dynamic aberrations`
- Target journal: `Nature Communications`
- Stage: `active calculation/verification`
- First formal execution time: `2026-04-30T07-33-15Z`
- Authoritative concept source: `/workspace/user_files/01-1-.txt`

## Current single bottleneck

The project now has a runnable physical baseline, but it still lacks the first trainable optical-frontend surrogate or differentiable diffractive baseline needed to test whether the reference advantage survives beyond post-detection adaptive deconvolution.

## Confirmed core story

A fixed passive diffractive optical processor co-propagates an object wave and a known reference wave, uses coherent interference to encode the instantaneous distortion state, and aims to restore images under dynamic aberrations without iterative adaptive optics or heavy electronic post-processing.

## Working manuscript spine

1. Problem: dynamic aberrations and weak scattering limit fast optical imaging.
2. Gap: most diffractive optical neural networks assume static or distribution-averaged degradation and lack true self-calibration.
3. Claim: a passive reference-assisted diffractive operator can perform distribution-level self-calibrated image restoration within a bounded family of dynamic optical distortions.
4. Required evidence: quantitative comparison against conventional D2NN, classical restoration, and digital neural reconstruction under Zernike, Kolmogorov, and thin phase-screen perturbations.

## Immediate next action

Implement the first trainable surrogate baseline on top of the same perturbation generator and metrics ledger, then compare it against the fixed and reference-guided restoration baselines already produced in `baseline-001-reference-psf`.

## Verified progress

- `baseline-001-reference-psf` completed as the first executable evidence package.
- Under 8 dynamic aberration cases and 6 synthetic objects, the reference-guided baseline outperformed the fixed baseline by mean PSNR gain `4.270 dB` and mean SSIM gain `0.0088`.
- The current result supports the narrower calibration premise but does not yet validate the full passive diffractive neural-operator claim.

## Automation

- Hourly iteration schedule: enabled
- Schedule timezone: `Asia/Shanghai`
- Stop condition: all 5 reviewer-style acceptance estimates exceed 0.80 and the evidence chain is complete
