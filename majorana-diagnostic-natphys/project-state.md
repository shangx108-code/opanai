# Project State

## Project
- Working title: Beyond zero-bias peaks: a nonlocal Green-function diagnostic for Majorana zero modes
- Target journal: Nature Physics
- Source note: initialized from `/workspace/user_files/01-1-.txt` on 2026-04-24

## Research goal
Build a publishable theory paper that does not merely restate that nonlocal conductance helps, but establishes a genuinely new and experimentally actionable diagnostic hierarchy that separates topological Majorana zero modes from trivial zero-energy states across multiple superconducting hybrid platforms.

## Current stage
Concept consolidation and venue-fit triage. The project already has a strong conceptual direction and a plausible computational toolbox, but it is not yet at the level of a Nature Physics submission package.

## Current main bottleneck
The novelty bar is not yet cleared. Existing literature already covers end-to-end nonlocal correlations, three-terminal nonlocal conductance under disorder, and local-conductance-based topology probes in Majorana nanowires. The current draft idea is still too close to that literature and too centered on a qualitative program rather than a sharply new principle with a closed evidence chain.

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

## What is still missing
- A verified novelty statement against 2019/2021/2024 nanowire-diagnostic literature
- A precise theorem-like or protocol-like new ingredient
- Quantitative completion criteria for each diagnostic observable
- Platform breadth sufficient for Nature Physics
- Real numerical results, figure-ready parameter scans, and robustness windows
- A citation-clean reference set

## Acceptance probability (stage estimate)
- Nature Physics: 8-15% in the current concept-only state
- Reason: important problem and promising architecture, but novelty and evidence are both currently below threshold

## Last update
2026-04-24: initialized project memory, identified novelty-overlap as the main rejection risk, and set the next round around a cross-platform diagnostic hierarchy with quantitative failure tests.
