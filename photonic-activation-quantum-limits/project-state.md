# Project State

- Project: Quantum limits of nonlinear activation in photonic neural networks
- Target journal: Nature Photonics
- Article type: Research Article
- Last updated: 2026-04-26 (later round)

## Research Goal

Establish a theory and design framework for the quantum resource limits of nonlinear activation in photonic neural networks, then support the framework with reproducible numerical evidence strong enough for journal review.

## Current Stage

Evidence-chain consolidation stage.

## Current Main Bottleneck

The paper now has multiple evidence layers, but still needs stronger cross-linking and a platform-facing interpretation so that the evidence reads as one coherent paper rather than several separate analyses.

## What Was Completed Across The Current Rounds

1. Read the user-provided project concept and fixed the current paper positioning around activation quantum cost rather than a generic classifier.
2. Verified current venue relevance and recent literature signals for Nature Photonics and closely related photonic-AI nonlinearity work.
3. Built a runnable minimal simulation scaffold in `/workspace/quantum_activation`.
4. Ran a first activation scan and saved the results to `/workspace/results/activation_cost_scan.csv`.
5. Extended the measurement-induced activation models to include detector efficiency, optical loss and dark count.
6. Generated device-aware activation-cost tables in `/workspace/results/device_activation_scan.csv`.
7. Generated a Monte Carlo two-moons benchmark in `/workspace/results/two_moons_benchmark.csv`.
8. Added an analytic Poisson discrimination lower bound and wrote the results to `/workspace/results/discrimination_bounds.csv`.
9. Generated a concept schematic for AQMA for later figure refinement.
10. Added a second benchmark, `/workspace/results/weak_signal_benchmark.csv`, for low-light weak-signal discrimination.
11. Generated real-data figure drafts in `/workspace/output` for energy-accuracy frontier, device budget heatmap and discrimination bound.

## Current Evidence Snapshot

- AQMA achieved the best proxy fit among measurement-induced models for sigmoid-like targets, with MSE 0.002363 at photon budget 1.0.
- Pure photon counting also fit sigmoid-like activation well, with MSE 0.002814 at photon budget 1.0.
- Binary activation remained expensive for measurement-induced models, with the best photon-counting proxy requiring budget 30.0 for MSE 0.005527.
- Kerr-like response best matched tanh-like targets in the current proxy scan, indicating the manuscript must distinguish function class rather than claim one mechanism dominates all targets.
- In the device-aware scan, sigmoid targets at max error 0.01 typically required 0.3-3 input photons for measurement-induced activations across the explored device settings.
- In the same scan, binary targets at max error 0.01 remained much more expensive, typically requiring 30-100 photons.
- In the Monte Carlo two-moons benchmark, measurement-induced models ranged from 66.8% to 98.1% accuracy depending on photon budget and device parameters, while the best AQMA result reached 97.9% and the best photon-counting result reached 98.1%.
- In the weak-signal benchmark, deterministic nonlinear baselines remain strongest in the current setup, with Kerr reaching 54.2% and the best AQMA reaching 53.8%, which is useful limiting evidence.
- Across photon budgets in the weak-signal benchmark, AQMA rises from about 51.3% at 0.3 photons to 53.8% at 10 photons, indicating only modest gains on this task class.
- The analytic discrimination lower bound predicts that at efficiency 0.9, loss 3 dB and dark count 0.01, at least 2.26, 8.91, 20.00 and 55.47 input photons are required to reach SNR targets 1, 2, 3 and 5, respectively.

## Current Acceptance Estimate

This is still below the stop condition for Nature Photonics, but the evidence is now much more complete and more trustworthy because it includes both positive and limiting cases. Current stage estimate: 42-52%.

## Next Highest-Priority Goal

Turn the current mixed evidence into a tighter paper-grade chain:

1. explain the benchmark split clearly: AQMA helps on some targets, but not all
2. connect the analytic floor to the benchmark behavior and device-scan regimes in manuscript-ready prose
3. tighten the paper's scope so the contribution is a framework with bounded claims, not an overgeneralized superiority claim

## Immediate Plan

1. Draft figure captions and Results text directly from the current real-data plots.
2. Add a platform-facing feasibility note linking explored efficiency-loss windows to plausible detector and PIC operating regimes.
3. Extend the theory note into a small Methods package with symbols, assumptions and claim boundaries.
4. Prepare the next review round using both favorable and limiting evidence, not only the best cases.
