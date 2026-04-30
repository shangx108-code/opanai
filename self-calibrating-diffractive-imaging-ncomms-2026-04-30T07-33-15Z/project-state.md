# Project State

- Project ID: `self-calibrating-diffractive-imaging-ncomms-2026-04-30T07-33-15Z`
- Locked title: `Self-calibrating diffractive optical neural operators for imaging through dynamic aberrations`
- Target journal: `Nature Communications`
- Stage: `early framing`
- First formal execution time: `2026-04-30T07-33-15Z`
- Authoritative concept source: `/workspace/user_files/01-1-.txt`

## Current single bottleneck

No canonical GitHub long-term space and no minimal executable environment had been established, so the project could not yet enter reproducible quantitative iteration.

## Confirmed core story

A fixed passive diffractive optical processor co-propagates an object wave and a known reference wave, uses coherent interference to encode the instantaneous distortion state, and aims to restore images under dynamic aberrations without iterative adaptive optics or heavy electronic post-processing.

## Working manuscript spine

1. Problem: dynamic aberrations and weak scattering limit fast optical imaging.
2. Gap: most diffractive optical neural networks assume static or distribution-averaged degradation and lack true self-calibration.
3. Claim: a passive reference-assisted diffractive operator can perform distribution-level self-calibrated image restoration within a bounded family of dynamic optical distortions.
4. Required evidence: quantitative comparison against conventional D2NN, classical restoration, and digital neural reconstruction under Zernike, Kolmogorov, and thin phase-screen perturbations.

## Immediate next action

Build and verify the minimal simulation environment, then start the first quantitative package around propagation, perturbation generation, and baseline comparison.
