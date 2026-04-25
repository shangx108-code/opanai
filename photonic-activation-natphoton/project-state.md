# Project State

## Project
- Working title: Quantum limits of nonlinear activation in photonic neural networks
- Target journal: Nature Photonics
- Source note: initialized from `/workspace/user_files/01-1-.txt` on 2026-04-25

## Research goal
Build a publishable theory-and-simulation paper that turns the vague claim "photonic neural networks need nonlinearity" into a journal-grade result: a quantitative resource framework for nonlinear activation under quantum noise, finite shots, detector inefficiency and loss, together with a near-limit measurement-induced activation architecture and a device-level design map.

## Current stage
Figure-consolidation and manuscript-integration stage. The project now has a submission-grade Figure-3 candidate package built around the three-curve same-axis comparison: one proved lower bound, one homodyne-conditioned measurement route, and one displaced on-off counting route.

## Current main bottleneck
The main bottleneck is now the absence of task-level evidence showing whether the single-neuron activation frontier changes system-level design choices. The paper can now state the single-neuron design law clearly, but Nature Photonics acceptance will still be capped if the story stops before a network-level consequence.

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

## This run's concrete result
### Goal
- Convert the completed three-curve comparison into a main-text Figure-3 object with reviewer-safe wording.

### Real outputs completed in this run
- Refined the plotting code in `figure3_same_axis_panel.py` and regenerated:
  - `figure3_same_axis_panel.svg`
  - `figure3_same_axis_panel.png`
  - `figure3_same_axis_panel.pdf`
  - `figure3_same_axis_panel_data.csv`
- Added regime annotations in the lower panel to separate:
  - near-frontier operation `1.0-1.4`
  - moderate overhead `1.4-2.0`
  - detector-limited operation `> 2.0`
- Added a submission-ready package in `figure3_submission_package.md` containing:
  - caption draft
  - insertable Results subsection text
  - allowed versus disallowed claims
  - provenance checklist

### Figure-supported numerical anchors now packaged for the manuscript
- At `epsilon = 0.01`, the displaced on-off route requires `1.224 x`, `1.731 x`, and `2.423 x` the lower-bound photon cost for `eta = 0.99`, `0.70`, and `0.50`, respectively.
- At the same target, the homodyne route requires `1.693 x`, `2.394 x`, and `3.352 x`.
- At `epsilon = 0.10`, the displaced on-off route requires `1.591 x`, `2.250 x`, and `3.151 x` the lower-bound photon cost for `eta = 0.99`, `0.70`, and `0.50`, while the homodyne route requires `1.624 x`, `2.297 x`, and `3.215 x`.

### Design-relevant interpretation now locked
- Detector efficiency controls the shared global accessibility of the frontier in the computed measurement-induced routes.
- Measurement choice controls the remaining constant-factor overhead above that frontier.
- The Figure-3 package is now strong enough to support this bounded design-law statement without claiming global optimality of either route.

## What is still missing
- Task-level evidence showing whether the single-neuron frontier matters for network utility
- A verified literature-positioning paragraph against 2024-2025 photonic nonlinearity papers
- A confirmed reference ledger separating verified citations from placeholders
- The first paper-integrated draft that places Figure 3 into the main Results flow with Figure 4 level follow-through

## Acceptance probability (stage estimate)
- Nature Photonics: 38-48% after assembling the Figure-3 package and Results-ready text
- Reason: the project now has a persuasive main-text comparison object rather than scattered internal notes, which materially improves clarity, figure quality, and reviewer confidence. The ceiling remains limited by the lack of task-level evidence and incomplete literature separation.

## Last update
2026-04-25: converted the completed same-axis comparison into a true Figure-3 submission package by improving the figure layout, adding regime annotations, regenerating SVG/PNG/PDF outputs, and writing a caption-plus-Results draft with explicit claim boundaries in `figure3_submission_package.md`. This closes the previous bottleneck around figure-grade assembly and shifts the project bottleneck to missing task-level evidence.
