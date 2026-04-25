# Project State

## Project
- Working title: Quantum limits of nonlinear activation in photonic neural networks
- Target journal: Nature Photonics
- Source note: initialized from `/workspace/user_files/01-1-.txt` on 2026-04-25

## Research goal
Build a publishable theory-and-simulation paper that turns the vague claim "photonic neural networks need nonlinearity" into a journal-grade result: a quantitative resource framework for nonlinear activation under quantum noise, finite shots, detector inefficiency and loss, together with a near-limit measurement-induced activation architecture and a device-level design map.

## Current stage
Verified novelty-positioning and manuscript-integration stage. The project now has a citation-checked literature-positioning package and direct manuscript text that connect the Figure-3 activation frontier and the first real Figure-4 task-level benchmark to the 2024-2025 Nature-family photonic-nonlinearity landscape.

## Current main bottleneck
The main bottleneck is now the absence of a stronger end-to-end task benchmark beyond the current random-feature surrogate. The literature-positioning bottleneck is now materially reduced, but reviewers can still argue that the system-level consequence remains too stylized for Nature Photonics unless one tighter trainable-network benchmark is added under the same photon-budget accounting.

## Highest-priority objective for the current round
Build a citation-verified literature-positioning package that explains, in reviewer-safe language, why the mixed Figure-3/Figure-4 result is distinct from recent 2024-2025 photonic nonlinearity papers and can be integrated directly into the manuscript.

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
- Remove the novelty-positioning bottleneck by converting the current literature placeholders into verified manuscript-ready positioning text.

### Real outputs completed in this run
- Added a citation-verified literature-positioning brief in `verified-literature-positioning.md`.
- Added a checked reference ledger in `verified-reference-ledger.md`.
- Added direct manuscript prose blocks in `manuscript-integration-draft.md`.
- Updated `manuscript-spine.md` so the prior-work gap and preview logic now align with verified comparator papers rather than placeholder novelty language.

### Literature-positioning conclusions now locked
- The manuscript can now state a reviewer-safe novelty claim:
  the contribution is not generic photonic nonlinearity or generic programmability, but a common resource-and-regime framework for nonlinear activation cost.
- The strongest comparator papers now have explicit claim boundaries:
  - Bandyopadhyay et al. 2024 for integrated on-chip nonlinear ONNs
  - Yildirim et al. 2024 for nonlinear processing with nominally linear optics
  - Wu et al. 2025 for programmable nonlinear photonic hardware
  - Wang et al. 2022 and Ma et al. 2025 for low-photon optical-computing and low-photon activation demonstrations
- The project can now argue, with checked citations, that its distinct result is the combination of:
  - a common lower-bound-plus-implementable-route comparison
  - explicit detector-efficiency and sampling penalties
  - a mixed task-level worth-it criterion showing that paying for activation is regime dependent rather than universally beneficial

## What is still missing
- At least one tighter trainable-network benchmark beyond the current random-feature surrogate under the same photon-budget accounting
- A full manuscript draft that incorporates the new literature-positioning and integration text across Introduction, Results, and Discussion
- A final cleaned reference ledger covering all non-core citations, not only the key comparator set
- A clear archive-ready manuscript package with main text, supplementary text, and figure callouts

## Acceptance probability (stage estimate)
- Nature Photonics: 50-60% after adding verified literature positioning and manuscript-ready integration text
- Reason: the project has now closed a major reviewer-facing weakness by replacing placeholder novelty rhetoric with checked comparator papers and bounded manuscript text. The ceiling remains limited by the lack of a stronger end-to-end task benchmark and by the absence of a full integrated draft.

## Last update
2026-04-25: converted the literature-positioning bottleneck into checked manuscript assets by writing `verified-literature-positioning.md`, `verified-reference-ledger.md`, and `manuscript-integration-draft.md`, and by updating `manuscript-spine.md` to align the claimed advance with verified 2024-2025 comparator papers. This shifts the next bottleneck to a stronger end-to-end task benchmark beyond the current random-feature surrogate.
