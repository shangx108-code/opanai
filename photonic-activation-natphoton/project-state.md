# Project State

## Project
- Working title: Quantum limits of nonlinear activation in photonic neural networks
- Target journal: Nature Photonics
- Source note: initialized from `/workspace/user_files/01-1-.txt` on 2026-04-25

## Research goal
Build a publishable theory-and-simulation paper that turns the vague claim "photonic neural networks need nonlinearity" into a journal-grade result: a quantitative resource framework for nonlinear activation under quantum noise, finite shots, detector inefficiency and loss, together with a near-limit measurement-induced activation architecture and a device-level design map.

## Current stage
Concept-to-manuscript architecture stage. The project now has a strong journal-facing paper concept, a candidate flagship architecture (AQMA), an initial figure storyboard, and a clear metrics stack, but it does not yet have validated numerics or a full manuscript package.

## Current main bottleneck
The evidence chain is still too conceptual for Nature Photonics. Right now the project lacks a quantitative proof package showing that the proposed framework yields a new and decision-relevant result beyond recent work on photonic nonlinearity, low-photon optical neural networks, and linear-scattering-based nonlinear encoding.

## Highest-priority objective for the current round
Convert the concept note into a falsifiable paper spine with one decisive main claim, one minimal mathematical framework, one benchmark plan, and one realistic venue-risk assessment.

## Proposed central claim
The real scalability bottleneck of photonic neural networks is not linear optics but the physical cost of nonlinear activation; this cost can be cast as a quantum resource problem, and measurement-induced adaptive activation can approach the low-energy Pareto frontier under realistic detector and loss constraints.

## Mandatory evidence package
- Formal definition of activation quantum cost, discrimination cost, and task-level energy-accuracy cost
- Unified activation model covering electronic, Kerr-like, saturable, photon-counting, homodyne, and AQMA-style measurement-feedback activation
- Single-neuron approximation benchmark for at least five target activation families
- Small-network task benchmark showing when measurement-induced nonlinearity is useful and when it is not
- Robustness scans over detector efficiency, dark count, optical loss, and finite-shot sampling
- Clear separation from closely related literature in Nature Photonics, Nature Communications, and adjacent photonic-AI work

## What is already strong
- The question is pitched at a field level rather than as one more classifier demo
- The proposed AQMA architecture is mechanistic, testable, and easy to explain
- The note already contains a credible figure storyboard for a selective photonics journal
- The target venue is scope-compatible with nonlinear optics, quantum optics, optoelectronic components, and photonic AI
- The paper can be framed as design rules plus limits, which fits a theory-heavy route better than a hardware-claim route

## What is still missing
- A sharp novelty statement against 2024-2025 photonic nonlinearity papers
- A mathematically clean formulation with assumptions and approximation regime stated explicitly
- Reproducible numerical benchmarks and figure-ready parameter scans
- A validated manuscript structure calibrated to Nature Photonics rather than to a broad review article
- A verified reference ledger separating confirmed citations from placeholders

## Acceptance probability (stage estimate)
- Nature Photonics: 12-20% at project start
- Reason: the concept is timely and well aimed, but currently it is still a strong proposal rather than a submission-grade evidence package

## Last update
2026-04-25: started autonomous project orchestration from the uploaded note, verified current Nature Photonics scope and several closely related 2024-2025 papers, identified evidence incompleteness as the lead blocker, and launched the first structured planning/review cycle plus scheduled 90-minute follow-up iterations.
