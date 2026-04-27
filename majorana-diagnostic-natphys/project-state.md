# Project State

## Project
- Working title: Beyond zero-bias peaks: a nonlocal Green-function diagnostic for Majorana zero modes
- Target journal: Nature Physics
- Source note: initialized from `/workspace/user_files/01-1-.txt` on 2026-04-24

## Research goal
Build a publishable theory paper that does not merely restate that nonlocal conductance helps, but establishes a genuinely new and experimentally actionable diagnostic hierarchy that separates topological Majorana zero modes from trivial zero-energy states across multiple superconducting hybrid platforms. The project is not considered complete until the estimated Nature Physics acceptance probability exceeds 70% and all required evidence layers are closed with auditable support.

## Current stage
Pilot-manuscript stage with literature-verified repositioning, theory-standard fixing, and a first reliable topological layer for the clean homogeneous wire. The project now includes a draft manuscript package, an explicit diagnostic-hierarchy theory note, a compact real-data benchmark, figure assets, and an internal review package. It is still below Nature Physics submission strength, but it is no longer only a concept note.

## Current main bottleneck
The main bottleneck is now missing selectivity under the stricter evidence-completion standard. The clean-wire class-D invariant is explicit and reliable, and the inhomogeneous controls now have a quasi-topological layer based on end-to-end nonlocality and charge neutrality. However, that new layer rejects the dot-induced ABS but does not yet eliminate the disorder-generated false positive. Without a stronger disorder-robust discriminator, neither the >70% target nor the "all evidence completed" rule is reachable. Novelty also still needs sharper separation from the older nonlocal-Majorana diagnostic literature and from the 1 April 2026 *npj Quantum Materials* article on topological altermagnetic Josephson junctions.

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
- Full manuscript draft and internal review package now exist
- A compact numerical benchmark now exists for clean-wire, dot-ABS, and disorder-induced near-zero-state cases
- The clean homogeneous Rashba wire now has a reliable bulk class-D invariant in the benchmark
- A quasi-topological metric now exists for the inhomogeneous controls and already suppresses the dot-induced ABS case

## What is still missing
- A sharper novelty statement against 2019/2021/2024 nanowire-diagnostic literature
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

## Acceptance probability (stage estimate)
- Nature Physics: 24-34% after adding the quasi-topological control layer and keeping the stricter >70% completion rule
- Project success threshold: >70%
- Reason: the manuscript is now stronger on both the clean topological side and the local-ABS-control side, but the evidence package and novelty separation are still below top-tier threshold because the disorder false positive remains insufficiently filtered and the cross-platform breadth is missing

## Last update
2026-04-27: the project was advanced again by adding a quasi-topological inhomogeneous-control layer based on end-to-end nonlocality and charge neutrality. This new layer strongly suppresses the dot-induced ABS but does not yet eliminate the disorder-generated false positive. The manuscript and review package were updated accordingly. The next bottleneck is now a disorder-robust inhomogeneous discriminator and insufficient cross-platform evidence.
