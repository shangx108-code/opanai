# Project State

## Project
- Working title: Quantum limits of nonlinear activation in photonic neural networks
- Target journal: Nature Photonics
- Source note: initialized from `/workspace/user_files/01-1-.txt` on 2026-04-25

## Research goal
Build a publishable theory-and-simulation paper that turns the vague claim "photonic neural networks need nonlinearity" into a journal-grade result: a quantitative resource framework for nonlinear activation under quantum noise, finite shots, detector inefficiency and loss, together with a near-limit measurement-induced activation architecture and a device-level design map.

## Current stage
Formalization stage. The project now has a strong journal-facing concept plus a first-pass theory framework, benchmark specification, and manuscript spine. It still lacks validated numerics and a full draft, but it is no longer only a concept note.

## Current main bottleneck
The framework is now defined, but it remains untested. The leading blocker is the absence of numerical evidence showing a real regime boundary or superiority window that would make the framework decision-relevant rather than merely well organized.

## Highest-priority objective for the current round
Turn the new framework into a falsifiable evidence program by generating the first benchmark-grade numerical plan and then using it to build the manuscript's first technical results section.

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
- Reproducible numerical benchmarks and figure-ready parameter scans
- A verified reference ledger separating confirmed citations from placeholders
- A first technical result demonstrating either a regime boundary or a superiority window

## Acceptance probability (stage estimate)
- Nature Photonics: 18-26% after formalization
- Reason: the project now has a paper-grade framework and clearer editorial positioning, but the decisive evidence package is still absent

## Last update
2026-04-25: converted the concept into a formal project package by adding a theory framework, benchmark specification, and manuscript spine; the main bottleneck has shifted from conceptual vagueness to missing benchmark evidence. The automation cadence is now being updated from 90-minute runs to hourly runs.
