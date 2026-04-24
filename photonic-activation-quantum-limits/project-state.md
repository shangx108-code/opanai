# Project State

- Project: Quantum limits of nonlinear activation in photonic neural networks
- Target journal: Nature Photonics
- Article type: Research Article
- Last updated: 2026-04-25

## Research Goal

Establish a theory and design framework for the quantum resource limits of nonlinear activation in photonic neural networks, then support the framework with reproducible numerical evidence strong enough for journal review.

## Current Stage

Concept consolidation and v0 single-neuron simulation stage.

## Current Main Bottleneck

The paper has a strong framing but still lacks the task-level and device-constrained evidence that selective reviewers will require beyond a concept article.

## What Was Completed In This Round

1. Read the user-provided project concept and fixed the current paper positioning around activation quantum cost rather than a generic classifier.
2. Verified current venue relevance and recent literature signals for Nature Photonics and closely related photonic-AI nonlinearity work.
3. Built a runnable minimal simulation scaffold in `/workspace/quantum_activation`.
4. Ran a first activation scan and saved the results to `/workspace/results/activation_cost_scan.csv`.

## Preliminary Results From The First Scan

- AQMA achieved the best proxy fit among measurement-induced models for sigmoid-like targets, with MSE 0.002363 at photon budget 1.0.
- Pure photon counting also fit sigmoid-like activation well, with MSE 0.002814 at photon budget 1.0.
- Binary activation remained expensive for measurement-induced models, with the best photon-counting proxy requiring budget 30.0 for MSE 0.005527.
- Kerr-like response best matched tanh-like targets in the current proxy scan, indicating the manuscript must distinguish function class rather than claim one mechanism dominates all targets.

## Current Acceptance Estimate

This is still far below the stop condition for Nature Photonics. Current stage estimate: 20-30%.

## Next Highest-Priority Goal

Turn the v0 single-neuron evidence into two publishability-critical modules:

1. task-level energy-accuracy results on at least one low-light classification benchmark
2. detector-efficiency and loss-constrained feasibility maps tied to real device ranges

## Immediate Plan

1. Expand the activation scan into epsilon-to-photon-budget curves instead of one best-point table.
2. Add detector efficiency, dark count, and loss parameters into the measurement-induced models.
3. Build a small benchmark task that tests whether the activation-cost advantage survives in network inference.
4. Start a manuscript v0 that is explicit about what is already demonstrated and what is still only proposed.
