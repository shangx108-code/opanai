# Project State

## Project
- Working title: Beyond zero-bias peaks: a nonlocal Green-function diagnostic for Majorana zero modes
- Target journal: Nature Physics
- Source note: initialized from `/workspace/user_files/01-1-.txt` on 2026-04-24

## Research goal
Build a publishable theory paper that does not merely restate that nonlocal conductance helps, but establishes a genuinely new and experimentally actionable diagnostic hierarchy that separates topological Majorana zero modes from trivial zero-energy states across multiple superconducting hybrid platforms. The project is not considered complete until the estimated Nature Physics acceptance probability exceeds 70% and all required evidence layers are closed with auditable support.

## Current stage
Pilot-manuscript stage with literature-verified repositioning, theory-standard fixing, expanded transport numerics, a first three-terminal figure-grade benchmark, and a newly frozen topology-layer upgrade specification for the next Figure 4 rebuild. The project now includes a draft manuscript package, an explicit diagnostic-hierarchy theory note, broader transport benchmark suites, rebuilt Figure 3/4 candidates derived from real three-terminal data, and a manuscript-facing definition of the required full-device topological discriminator. It is still below Nature Physics submission strength, but it is no longer only a concept note.

## Current main bottleneck
The main bottleneck is the weak topology layer in the current manuscript-facing benchmark. The three-terminal figure package is now real enough to matter, but Figure 4 still relies on a clean-backbone criterion rather than a full-device inhomogeneous topological discriminator. Until transport and topology are evaluated on the same dot/impurity/disorder landscape, the paper cannot make a Nature Physics-level rescue claim.

## Highest-priority objective for the current round
Freeze the topology-layer upgrade path so the next numerical round is constrained to one auditable manuscript goal:

1. replace the clean-backbone criterion with a full-device inhomogeneous class-D invariant;
2. require transport, reopened-gap logic, and topology to be evaluated on the same operating points;
3. compare topological-consistency probability against local-peak prevalence for positive and false-positive families;
4. rebuild Figure 4 only after the dot and impurity false positives remain visually meaningful beside the disorder family;
5. keep the project below success status until the strengthened topology layer is backed by real rerun data.

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
- A first three-terminal benchmark package now exists under `/workspace/output/three-terminal-benchmark`, including selected operating points and rebuilt Figure 3/4 candidates

## What is still missing
- A verified novelty statement against 2019/2021/2024 nanowire-diagnostic literature
- A numerically validated disorder-robust inhomogeneous discriminator for false-positive controls
- Platform breadth sufficient for Nature Physics
- Real numerical results, figure-ready parameter scans, and robustness windows
- A citation-clean reference set
- A fully convincing three-terminal transport benchmark with stronger topology discrimination than the current backbone criterion
- A completed derivation note integrated into the manuscript rather than only the internal theory file
- Evidence-complete real data for every main-text data figure
- A benchmark where nonlocal transport, gap reopening, and a stronger topology label are evaluated together rather than only finite-chain spectral proxies plus backbone topology
- One more false-positive family, preferably impurity- or YSR-like
- Stronger experimental observability windows for temperature and barrier scans
- Additional tuning that reduces the current over-dominance of the disorder false positive and sharpens the smooth-dot and impurity comparison

## Acceptance probability (stage estimate)
- Nature Physics: 14-22% in the current manuscript-package state
- Project success threshold: >70%
- Reason: numerical coverage and figure readiness improved, but the evidence is still not selective enough, and the topology layer remains below the threshold needed for a top-tier theory paper

## Last update
2026-04-27: reviewed the post-three-terminal project state and froze a manuscript-facing topology-layer upgrade specification in `topology-layer-upgrade-spec-2026-04-27.md`. This round did not rerun the numerics because the current scheduled-run workspace contains only the memory files and not the benchmark scripts or output bundles. The project remains blocked on replacing the clean-backbone criterion with a full-device inhomogeneous topological discriminator and then rebuilding Figure 4 from real rerun data.
