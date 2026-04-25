# Project State

## Project
- Working title: Quantum limits of nonlinear activation in photonic neural networks
- Target journal: Nature Photonics
- Source note: initialized from `/workspace/user_files/01-1-.txt` on 2026-04-25

## Research goal
Build a publishable theory-and-simulation paper that turns the vague claim "photonic neural networks need nonlinearity" into a journal-grade result: a quantitative resource framework for nonlinear activation under quantum noise, finite shots, detector inefficiency and loss, together with a near-limit measurement-induced activation architecture and a device-level design map.

## Current stage
Results-generation and manuscript-assembly stage. The project now has a citation-checked novelty package, a Figure-3-grade single-neuron frontier result, a first real task-level benchmark, and one tighter trainable-network benchmark under the same photon-budget accounting.

## Current main bottleneck
The main bottleneck is now the absence of a full integrated manuscript draft that incorporates the stronger trainable Figure-4 evidence into submission-grade Introduction, Results, Discussion, and supplementary logic. The key evidentiary objection to the old random-feature surrogate has now been materially reduced, so the limiting risk has shifted from "missing stronger task benchmark" to "evidence exists but is not yet assembled into a reviewer-proof paper."

## Highest-priority objective for the current round
Generate and validate the smallest stronger trainable-network benchmark that tests whether the Figure-3 activation-resource physics still changes system-level design once the hidden layer is trained under the same total photon-budget accounting.

## Proposed central claim
The real scalability bottleneck of photonic neural networks is not linear optics but the physical cost of nonlinear activation; this cost can be cast as a quantum resource problem, and measurement-induced adaptive activation can approach the low-energy Pareto frontier only inside explicitly quantified detector-, loss-, and sampling-limited regimes.

## Mandatory evidence package
- Formal definition of activation quantum cost, discrimination cost, and task-level energy-accuracy cost
- Unified activation model covering electronic, Kerr-like, saturable, photon-counting, homodyne, and AQMA-style measurement-feedback activation
- Single-neuron approximation benchmark for at least five target activation families
- Small-network task benchmark showing when measurement-induced nonlinearity is useful and when it is not
- Robustness scans over detector efficiency, dark count, optical loss, and finite-shot sampling
- Clear separation from closely related literature in Nature Photonics, Nature Communications, and adjacent photonic-AI work

## What is already strong
- The question is pitched at a field level rather than as one more classifier demo
- The project has one explicit lower bound for boundary discrimination cost
- The project has two concrete same-axis implementable baselines beside that bound
- The project has a Figure-3 submission package with panel structure, regime annotations, caption logic, claim boundaries, and Results-ready prose
- The project now has both a random-feature task benchmark and a stronger trainable-network task benchmark under the same budget accounting
- The target venue is scope-compatible with nonlinear optics, quantum optics, optoelectronic components, and photonic AI
- The paper can be framed as design rules plus limits, which fits a theory-heavy route better than a hardware-claim route
- The novelty case is now citation-checked against the strongest 2024-2025 comparator papers

## This run's concrete result
### Goal
- Remove the strongest remaining reviewer objection to Figure 4 by replacing the stylized random-feature-only surrogate with the smallest real trainable-network benchmark that preserves the same photonic activation accounting.

### Real outputs completed in this run
- Added a reproducible trainable benchmark script in `trainable_task_benchmark.py`.
- Saved real outputs in `trainable_task_benchmark/`.
- Added a claim-boundary note in `trainable_task_benchmark_assumptions.md`.
- Added a manuscript-facing interpretation package in `figure4_trainable_benchmark_package.md`.

### Trainable-benchmark conclusions now locked
- The Figure-3 route physics survives hidden-layer training rather than washing out once the representation is allowed to adapt.
- Physical activation beats the trainable linear no-activation baseline in `22/30` scanned `(task, eta, budget)` conditions.
- Activation is still not justified in `8/30` scanned conditions, all on `two_moons` at low or intermediate budgets, so the manuscript still has genuine negative regions.
- Route preference remains non-universal: on-off beats homodyne in `14/30` matched comparisons, so the best implementable route still depends on task and budget.

## What is still missing
- A full integrated manuscript draft that replaces the old Figure-4 placeholder logic with the stronger trainable benchmark narrative
- A final cleaned reference ledger covering all non-core citations, not only the key comparator set
- A clean supplementary package aligned to the upgraded Figure-4 evidence
- A final archive-ready manuscript package with main text, supplementary text, figure callouts, and submission-facing provenance

## Acceptance probability (stage estimate)
- Nature Photonics: 58-66% after adding the stronger trainable Figure-4 benchmark
- Reason: the project has now closed the most obvious reviewer attack on system-level evidence by showing that the route- and budget-dependent design law survives hidden-layer training. The ceiling remains limited by incomplete manuscript assembly, incomplete bibliography cleanup, and the absence of a final submission-grade Figure-4/main-text integration.

## Last update
2026-04-25: replaced the strongest remaining Figure-4 evidence gap by writing and running `trainable_task_benchmark.py`, saving outputs in `trainable_task_benchmark/`, and packaging the manuscript-safe conclusions in `trainable_task_benchmark_assumptions.md` and `figure4_trainable_benchmark_package.md`. This shifts the next bottleneck from "missing stronger task benchmark" to "missing full integrated manuscript draft with upgraded Figure-4 evidence."
