# Project State

- Project ID: `self-calibrating-diffractive-imaging-ncomms-2026-04-30T07-33-15Z`
- Locked title: `Self-calibrating diffractive optical neural operators for imaging through dynamic aberrations`
- Target journal: `Nature Communications`
- Stage: `active calculation/verification`
- First formal execution time: `2026-04-30T07-33-15Z`
- Authoritative concept source: `/workspace/user_files/01-1-.txt`

## Current single bottleneck

The project now has an explicit angular-spectrum propagation kernel and a minimum multi-seed robustness package, but the evidence chain still lacks a harder held-out object-family generalization test and a more optical-faithful differentiable frontend.

## Confirmed core story

A fixed passive diffractive optical processor co-propagates an object wave and a known reference wave, uses coherent interference to encode the instantaneous distortion state, and aims to restore images under dynamic aberrations without iterative adaptive optics or heavy electronic post-processing.

## Working manuscript spine

1. Problem: dynamic aberrations and weak scattering limit fast optical imaging.
2. Gap: most diffractive optical neural networks assume static or distribution-averaged degradation and lack true self-calibration.
3. Claim: a passive reference-assisted diffractive operator can perform distribution-level self-calibrated image restoration within a bounded family of dynamic optical distortions.
4. Required evidence: quantitative comparison against conventional D2NN, classical restoration, and digital neural reconstruction under Zernike, Kolmogorov, and thin phase-screen perturbations.

## Immediate next action

Freeze the new physical baseline as the reference ledger, then harden the learned-calibration result with held-out object families and replace the linear low-resolution surrogate with a more optical-faithful differentiable frontend baseline.

## Verified progress

- `baseline-001-reference-psf` has been promoted from an early scaffold to the current physical reference baseline.
- The current physical baseline now uses an explicit angular-spectrum propagation kernel with declared `Δx`, `λ`, `z`, and frequency-coordinate ranges.
- `baseline-001-reference-psf-multiseed` completed across 5 seeds and produced `multiseed_summary.csv`, per-seed sample metrics, seed logs, and a SHA-256 manifest.
- Across 5 seeds, the physical baseline achieved mean PSNR gain `1.661 ± 0.122` dB (95% CI half-width) and mean SSIM gain `0.1133 ± 0.0075`, with guided improvement fraction `1.0` for both PSNR and SSIM.
- `baseline-002-trainable-surrogate` completed as the first learned-calibration package.
- On held-out aberration cases, the trainable surrogate achieved mean low-resolution PSNR `50.703 dB` versus `37.541 dB` for the fixed low-resolution baseline, but this comparison still shares the same small object family between train and test and is therefore not yet strong enough for manuscript evidence.
- The current result supports the narrower calibration premise and the learnability premise, but does not yet validate the full passive diffractive neural-operator claim.

## Automation

- Hourly iteration schedule: enabled
- Schedule timezone: `Asia/Shanghai`
- Stop condition: all 5 reviewer-style acceptance estimates exceed 0.80 and the evidence chain is complete
