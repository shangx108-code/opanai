# Project State

- Project: Quantum limits of nonlinear activation in photonic neural networks
- Target journal: Nature Photonics
- Article type: Research Article
- Last updated: 2026-04-26

## Research Goal

Establish a theory and design framework for the quantum resource limits of nonlinear activation in photonic neural networks, then support the framework with reproducible numerical evidence strong enough for journal review.

## Current Stage

Device-aware evidence build-up stage.

## Current Main Bottleneck

The paper still lacks a sufficiently strong multi-layer evidence chain that links analytic bounds, function-level scans, benchmark accuracy and device-feasibility conclusions without overclaiming.

## What Was Completed Across The First Two Rounds

1. Read the user-provided project concept and fixed the current paper positioning around activation quantum cost rather than a generic classifier.
2. Verified current venue relevance and recent literature signals for Nature Photonics and closely related photonic-AI nonlinearity work.
3. Built a runnable minimal simulation scaffold in `/workspace/quantum_activation`.
4. Ran a first activation scan and saved the results to `/workspace/results/activation_cost_scan.csv`.
5. Extended the measurement-induced activation models to include detector efficiency, optical loss and dark count.
6. Generated device-aware activation-cost tables in `/workspace/results/device_activation_scan.csv`.
7. Generated a Monte Carlo two-moons benchmark in `/workspace/results/two_moons_benchmark.csv`.
8. Added an analytic Poisson discrimination lower bound and wrote the results to `/workspace/results/discrimination_bounds.csv`.
9. Generated a concept schematic for AQMA for later figure refinement.

## Current Evidence Snapshot

- AQMA achieved the best proxy fit among measurement-induced models for sigmoid-like targets, with MSE 0.002363 at photon budget 1.0.
- Pure photon counting also fit sigmoid-like activation well, with MSE 0.002814 at photon budget 1.0.
- Binary activation remained expensive for measurement-induced models, with the best photon-counting proxy requiring budget 30.0 for MSE 0.005527.
- Kerr-like response best matched tanh-like targets in the current proxy scan, indicating the manuscript must distinguish function class rather than claim one mechanism dominates all targets.
- In the device-aware scan, sigmoid targets at max error 0.01 typically required 0.3-3 input photons for measurement-induced activations across the explored device settings.
- In the same scan, binary targets at max error 0.01 remained much more expensive, typically requiring 30-100 photons.
- In the Monte Carlo two-moons benchmark, measurement-induced models ranged from 66.8% to 98.1% accuracy depending on photon budget and device parameters, while the best AQMA result reached 97.9% and the best photon-counting result reached 98.1%.
- The analytic discrimination lower bound predicts that at efficiency 0.9, loss 3 dB and dark count 0.01, at least 2.26, 8.91, 20.00 and 55.47 input photons are required to reach SNR targets 1, 2, 3 and 5, respectively.

## Current Acceptance Estimate

This is still below the stop condition for Nature Photonics, but the project is no longer at pure-concept stage. Current stage estimate: 35-45%.

## Next Highest-Priority Goal

Turn the current mixed evidence into a tighter paper-grade chain:

1. refine the benchmark suite so the task-level evidence is broader than one toy dataset
2. tighten the theory section so "quantum limit" rests on explicit lower-bound statements and clearly labeled scope
3. convert the current tables into publication-grade real-data figures with captions anchored to true simulation outputs

## Immediate Plan

1. Add a second benchmark and generate energy-accuracy frontiers rather than isolated best accuracies.
2. Expand the lower-bound note into a Methods-ready derivation section with assumptions and limitations.
3. Replace single-point narrative claims with parameter-window statements grounded in the new tables.
4. Draft figure captions and Results text that are careful about what is shown versus what remains conjectural.
