# Project State

## Project
- Working title: Beyond zero-bias peaks: a nonlocal Green-function diagnostic for Majorana zero modes
- Target journal: Nature Physics
- Source note: initialized from `/workspace/user_files/01-1-.txt` on 2026-04-24

## Research goal
Build a publishable theory paper that does not merely restate that nonlocal conductance helps, but establishes a genuinely new and experimentally actionable diagnostic hierarchy that separates topological Majorana zero modes from trivial zero-energy states across multiple superconducting hybrid platforms. The project is not considered complete until the estimated Nature Physics acceptance probability exceeds 70% and all required evidence layers are closed with auditable support.

## Current stage
Pilot-manuscript stage with literature-verified repositioning, theory-standard fixing, and expanded transport numerics. The project now includes a draft manuscript package, an explicit diagnostic-hierarchy theory note, first real-data benchmark outputs, and a wider transport benchmark suite across positive, smooth-dot, impurity, disorder, and broadening scans. It is still below Nature Physics submission strength, but it is no longer only a concept note.

## Current main bottleneck
The main bottleneck is still selectivity under the stricter evidence-completion standard. The project now has broader result coverage, but the current false-positive parameter families do not yet produce the strongest misleading zero-bias behavior, and the topology layer remains weaker than the manuscript ultimately needs. Without a stronger disorder-robust discriminator and more convincing false-positive benchmarks, neither the >70% target nor the "all evidence completed" rule is reachable.

## Highest-priority objective for the current round
Lock the project around one original centerpiece and one auditable completion rule:

1. a universal diagnostic hierarchy with explicit failure boundaries for local tunnelling;
2. a cross-platform benchmark using at least three model families;
3. a disorder/impurity stress-test showing that zero-bias-peak probability and topology probability decouple;
4. an experimentally usable protocol window rather than only theoretical observables;
5. no success declaration before acceptance probability exceeds 70% and every required evidence layer is backed by real data or verified derivation.

## Proposed central claim
Local zero-bias peaks are neither sufficient nor stably informative in realistic hybrid superconductors; a topological diagnosis requires the joint consistency of end-to-end correlation, nonlocal transport, bulk-gap reopening, and scattering-matrix topology, and this hierarchy remains discriminating across dot-induced ABS, impurity-induced YSR-like states, and disorder-induced near-zero modes.

## Mandatory evidence package
- Positive control: topological Rashba nanowire
- Negative controls: dot/smooth-confinement ABS, impurity-driven subgap state, disorder-induced near-zero state
- Primary observables: `G_LL`, `G_RR`, `G_LR`, gap closing/reopening, scattering invariant
- Secondary observables: CAR/EC decomposition, LDOS/nonlocality metric, robustness under barrier/temperature/disorder
- Stretch layer: noise or cavity-response channel only if it materially sharpens the main claim
- Theory layer: explicit derivation note for conductance formulas, topology-sensitive label, and diagnostic-hierarchy logic
- Figure rule: only conceptual schematics may be image-generated; all data figures must come from real computed or verified data

## What is already strong
- Clear field-level problem selection
- Unified Green-function / BTK / self-energy / T-matrix technical spine
- Good instinct to include false positives instead of only ideal Majoranas
- Strong candidate visual centerpiece in the form of a diagnostic map
- A first manuscript package and LaTeX draft now exist in `/workspace/output`
- Literature positioning now reflects the 2026 TAJJ overlap explicitly
- A formal internal theory note now defines the diagnostic hierarchy and evidence-completion criteria
- A first real-data benchmark sweep now exists for a Rashba positive control and a smooth-dot false-positive control in one finite-chain BdG code path
- A wider transport benchmark bundle now exists with positive-control, smooth-dot, impurity, disorder, eta-broadening, and bias-trace outputs stored under `/workspace/output/transport-benchmark`

## What is still missing
- A verified novelty statement against 2019/2021/2024 nanowire-diagnostic literature
- A numerically validated disorder-robust inhomogeneous discriminator for false-positive controls
- Platform breadth sufficient for Nature Physics
- Real numerical results, figure-ready parameter scans, and robustness windows
- A citation-clean reference set
- A three-terminal transport benchmark with positive and false-positive controls from one code path
- A completed derivation note integrated into the manuscript rather than only the internal theory file
- Evidence-complete real data for every main-text data figure
- A benchmark where nonlocal transport, gap reopening, and topology label are evaluated together rather than only finite-chain spectral proxies
- One more false-positive family, preferably impurity- or YSR-like
- Stronger experimental observability windows for temperature and barrier scans
- Parameter tuning that produces genuinely persuasive false-positive zero-bias behavior rather than merely weak trivial responses

## Acceptance probability (stage estimate)
- Nature Physics: 10-18% in the current manuscript-package state
- Project success threshold: >70%
- Reason: numerical coverage improved, but the evidence is still not selective enough and the novelty separation remains below the top-tier threshold

## Last update
2026-04-27: expanded the numerical suite from the initial Rashba sweep to a shared transport-benchmark package containing positive-control, smooth-dot, impurity, disorder, eta-broadening, and bias-trace outputs. The new result classes are now available, but the present parameter family still does not generate convincingly strong false-positive zero-bias peaks, so scientific closure has not yet been reached.
