# Project State

## Project
- Working title: Quantum limits of nonlinear activation in photonic neural networks
- Target journal: Nature Photonics
- Source note: initialized from `/workspace/user_files/01-1-.txt` on 2026-04-25

## Research goal
Build a publishable theory-and-simulation paper that turns the vague claim "photonic neural networks need nonlinearity" into a journal-grade result: a quantitative resource framework for nonlinear activation under quantum noise, finite shots, detector inefficiency and loss, together with a near-limit measurement-induced activation architecture and a device-level design map.

## Current stage
Task-level-consequence and manuscript-bridging stage. The project now has a first real Figure-4-style benchmark package that tests whether the Figure-3 activation frontier changes system-level design choices under a fixed activation photon budget.

## Current main bottleneck
The main bottleneck is now the lack of a manuscript-grade novelty-positioning section that explains why the new mixed positive-and-negative task-level result is distinct from recent 2024-2025 programmable and measurement-based photonic-nonlinearity papers. The project now has real task-level evidence, but without verified literature separation the novelty and significance case will remain capped.

## Highest-priority objective for the current round
Build the first minimal task-level benchmark that tests whether the Figure-3 frontier changes the preferred activation design once inference utility, detector efficiency and photon budget are all counted together.

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
- The project now has one explicit lower bound for boundary discrimination cost
- The project now also has one concrete same-axis comparison for a measurement-induced activation route
- The project now has a second concrete same-axis baseline using a displaced on-off counting route
- The project now has a Figure-3 submission package with panel structure, regime annotations, caption logic, claim boundaries, and Results-ready prose
- The target venue is scope-compatible with nonlinear optics, quantum optics, optoelectronic components, and photonic AI
- The paper can be framed as design rules plus limits, which fits a theory-heavy route better than a hardware-claim route
- The project now has one real task-level benchmark with both positive and negative regions rather than a purely aspirational Figure-4 placeholder

## This run's concrete result
### Goal
- Build the first real task-level benchmark that tests whether the single-neuron frontier changes the preferred implementable activation design under a fixed total activation budget.

### Real outputs completed in this run
- Added a reproducible benchmark script in `task_level_benchmark.py`.
- Added an assumptions ledger in `task_level_benchmark_assumptions.md` that states exactly what the task benchmark may and may not infer from Figure 3.
- Ran the benchmark and saved:
  - `task_level_benchmark/task_level_benchmark_results.csv`
  - `task_level_benchmark/task_level_benchmark_best_configs.csv`
  - `task_level_benchmark/task_level_benchmark_summary.md`
  - `task_level_benchmark/task_level_benchmark_summary.json`
- Added a manuscript-facing interpretation package in `figure4_minimal_benchmark_package.md`.

### Task-level numerical anchors now packaged for the manuscript
- Linear no-activation baseline:
  - `two_moons`: `0.882` test accuracy
  - `concentric_circles`: `0.484` test accuracy
- On `concentric_circles`, the best implementable activation beats the linear baseline in all `15/15` scanned `(eta, budget)` conditions.
- On `two_moons`, the best implementable activation does not beat the linear baseline in any scanned condition up to total activation budget `16`.
- Implementable route preference is not trivially inherited from Figure 3:
  - on-off beats homodyne in only `9/30` matched `(task, eta, budget)` comparisons.
  - homodyne is the best implementable route in most scanned `concentric_circles` settings.
  - on-off becomes preferred only in a smaller subset of higher-budget conditions.

### Design-relevant interpretation now locked
- The project now has a real task-level consequence: whether activation is worth paying for depends on task geometry, not only on the single-neuron frontier.
- The Figure-3 ranking between implementable routes does not transfer trivially to task-level preference once total activation budget is fixed.
- The strongest honest statement is now mixed rather than triumphalist:
  measurement-induced activation can be decisively worthwhile for nonlinear tasks with weak linear baselines, but it can remain unjustified for tasks that are already largely linearly separable in the scanned budget range.

## What is still missing
- A verified literature-positioning paragraph against 2024-2025 photonic nonlinearity papers that explains why the new task-level split is not redundant with recent photonic nonlinearity work
- A confirmed reference ledger separating verified citations from placeholders
- The first paper-integrated draft that places Figure 3 and the new minimal Figure-4 package into one continuous Results flow
- At least one tighter follow-up benchmark beyond the current random-feature surrogate if the manuscript is to push the task-level claim substantially harder

## Acceptance probability (stage estimate)
- Nature Photonics: 44-55% after adding the first real task-level benchmark package
- Reason: the project no longer stops at a polished single-neuron story. It now has a bounded but real task-level consequence with positive and negative regions, which materially strengthens benchmark credibility and manuscript logic. The ceiling remains limited by incomplete literature separation, lack of a cleaned reference ledger, and the fact that the new task result is still a stylized surrogate rather than a fully trained end-to-end network study.

## Last update
2026-04-25: built the first real task-level benchmark from the existing workspace by mapping the Figure-3 boundary-error models onto a fixed-budget random-feature classifier, saving reproducible CSV and JSON outputs, and writing `figure4_minimal_benchmark_package.md`. This closes the previous bottleneck around missing task-level consequence and shifts the next bottleneck to verified literature positioning and manuscript integration of the new mixed task-level result.
