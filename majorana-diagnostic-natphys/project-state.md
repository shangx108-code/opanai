# Project State

## Project
- Working title: Beyond zero-bias peaks: a nonlocal Green-function diagnostic for Majorana zero modes
- Target journal: Nature Physics
- Source note: initialized from `/workspace/user_files/01-1-.txt` on 2026-04-24

## Research goal
Build a publishable theory paper that does not merely restate that nonlocal conductance helps, but establishes a genuinely new and experimentally actionable diagnostic hierarchy that separates topological Majorana zero modes from trivial zero-energy states across multiple superconducting hybrid platforms.

## Current stage
Concept consolidation, literature-verified repositioning, and manuscript-package drafting. The project now has a sharper Nature-Physics-oriented claim architecture and first deliverables, but it is still below submission readiness.

## Current main bottleneck
The novelty bar is still not cleared. In addition to the older nonlocal-Majorana diagnostic literature, the paper must now explicitly separate itself from the 1 April 2026 *npj Quantum Materials* article on topological altermagnetic Josephson junctions. A generic field-free Majorana-platform claim is no longer sufficient.

## Highest-priority objective for the current round
Reframe the manuscript around one original centerpiece:

1. a universal diagnostic hierarchy with explicit failure boundaries for local tunnelling;
2. a cross-platform benchmark using at least three model families;
3. a disorder/impurity stress-test showing that zero-bias-peak probability and topology probability decouple;
4. an experimentally usable protocol window rather than only theoretical observables.

## Proposed central claim
Local zero-bias peaks are neither sufficient nor stably informative in realistic hybrid superconductors; a topological diagnosis requires the joint consistency of end-to-end correlation, nonlocal transport, bulk-gap reopening, and scattering-matrix topology, and this hierarchy remains discriminating across dot-induced ABS, impurity-induced YSR-like states, and disorder-induced near-zero modes.

## Mandatory evidence package
- Positive control: topological Rashba nanowire
- Negative controls: dot/smooth-confinement ABS, impurity-driven subgap state, disorder-induced near-zero state
- Primary observables: `G_LL`, `G_RR`, `G_LR`, gap closing/reopening, scattering invariant
- Secondary observables: CAR/EC decomposition, LDOS/nonlocality metric, robustness under barrier/temperature/disorder
- Stretch layer: noise or cavity-response channel only if it materially sharpens the main claim

## What is already strong
- Clear field-level problem selection
- Unified Green-function / BTK / self-energy / T-matrix technical spine
- Good instinct to include false positives instead of only ideal Majoranas
- Strong candidate visual centerpiece in the form of a diagnostic map
- A first manuscript package and LaTeX draft now exist in `/workspace/output`
- Literature positioning now reflects the 2026 TAJJ overlap explicitly

## What is still missing
- A verified novelty statement against 2019/2021/2024 nanowire-diagnostic literature
- A precise theorem-like or protocol-like new ingredient
- Quantitative completion criteria for each diagnostic observable
- Platform breadth sufficient for Nature Physics
- Real numerical results, figure-ready parameter scans, and robustness windows
- A citation-clean reference set
- A three-terminal transport benchmark with positive and false-positive controls from one code path

## Acceptance probability (stage estimate)
- Nature Physics: 10-18% in the current manuscript-package state
- Reason: topic importance and manuscript architecture improved, but the evidence chain remains incomplete and novelty separation is still below threshold

## Last update
2026-04-25: verified the direct overlap with Yang, Sun, Xie and Law's *Topological altermagnetic Josephson junctions* (*npj Quantum Materials*, published 1 April 2026), repositioned the project toward a diagnostic-hierarchy paper, generated a first manuscript package, and completed an honesty-check toy-model calculation that did not yet produce a robust topological zero-mode window.
