# Project State

## Project
- Working title: Beyond zero-bias peaks: a nonlocal Green-function diagnostic for Majorana zero modes
- Primary target journal: Nature Physics
- Secondary packaging path: Nature Communications
- Source note: initialized from `/workspace/user_files/01-1-.txt` on 2026-04-24

## Research goal
Build a publishable theory paper that does not merely restate that nonlocal conductance helps, but establishes a genuinely new and experimentally actionable diagnostic hierarchy that separates topological Majorana zero modes from trivial zero-energy states across multiple superconducting hybrid platforms. The project is not considered complete until the estimated Nature Physics acceptance probability exceeds 70% and all required evidence layers are closed with auditable support.

## Current stage
Application-and-venue repositioning with a first real CMJJ source-data bundle. On 2026-05-01, the project not only locked the compensated-magnetic Josephson-junction branch and the Nature Communications packaging path, but also generated the first auditable Figures 2-5 source-data package for that branch under `data/cmjj-source-data-2026-05-01/`. The package is built from a minimal executable effective model that runs in the current `numpy`-only environment and already covers bulk gap scans, finite-ring topology labels, open-boundary spectra, negative controls, and lead-attached transport proxies.

## Current main bottleneck
The main bottleneck has shifted from total absence of CMJJ evidence to selective upgrade of the weak panels. A first review pass over the new bundle shows that Figures 2 and 3 are already plausible manuscript-facing assets, while Figures 4 and 5 remain the limiting layer. The concrete bottleneck is now narrower than before: a targeted retune run identified dot and impurity control windows that recover `nu_ring = 1` while keeping `min|E|` in the near-zero regime, and a follow-up candidate rebuild regenerated the Fig. 4 control summary plus the Fig. 5 positive/dot/impurity heatmaps around those locked settings. A dedicated window-discrimination check now shows that the present proxy is substantially cleaner as a zero-bias or near-zero-bias discriminator than as a full-bias-window discriminator.

## Highest-priority objective for the current round
Convert the first CMJJ source-data bundle into a manuscript-facing package:

1. keep `A-compensated-magnetic-cmjj-blueprint-2026-05-01.md` as the fixed application brief;
2. keep `B-nc-repositioning-and-reproducibility-plan-2026-05-01.md` as the fixed packaging brief;
3. treat `data/cmjj-source-data-2026-05-01/` and `code/generate_cmjj_source_data.py` as the current reproducible baseline;
4. freeze the first-pass bundle as the baseline and treat `data/fig4-fig5-targeted-retune-2026-05-01/` plus `code/retune_fig4_fig5_targeted.py` as the current control-retune workspace;
5. treat `data/fig4-fig5-candidate-rebuild-2026-05-01/` as the current manuscript-facing weak-panel package for Figures 4 and 5;
6. treat the present Fig. 5 proxy as acceptable only for a zero-bias or tight near-zero-bias discriminator;
7. if a broader bias-window claim is still desired, upgrade the transport observable rather than reopening control-parameter scans;
8. only after that add plotting, captioning, and venue-specific figure selection.

## Proposed central claim
In a compensated-magnetic Josephson junction, field-free topological superconductivity should be diagnosed not from a local near-zero feature alone, but from the consistency of bulk topology, open-boundary spectra, and phase-resolved nonlocal response under explicit ABS, impurity, and disorder false-positive tests.

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
- The compensated-magnetic Josephson-junction application is now frozen as a reusable project branch rather than a vague future option
- A Nature Communications-safe claim stack and reproducibility plan are now frozen in long-term memory
- A first real CMJJ Figures 2-5 source-data bundle now exists under `memory/majorana-diagnostic-natphys/data/cmjj-source-data-2026-05-01/`
- The corresponding generator script and config now exist under `code/generate_cmjj_source_data.py` and `config/cmjj_source_data_config.json`
- A targeted Fig. 4 / Fig. 5 retune bundle now exists under `data/fig4-fig5-targeted-retune-2026-05-01/`, with ranked dot and impurity control candidates that stay topologically trivial while remaining near-zero
- A candidate-based Fig. 4 / Fig. 5 rebuild bundle now exists under `data/fig4-fig5-candidate-rebuild-2026-05-01/`, including the updated control summary table and regenerated positive/dot/impurity heatmaps
- A window-discrimination judgment now exists under `data/fig4-fig5-candidate-rebuild-2026-05-01/`, showing that the current Fig. 5 proxy is much stronger near zero bias than over the full bias window
- A first manuscript package and LaTeX draft now exist in `/workspace/output`
- Literature positioning now reflects the 2026 TAJJ overlap explicitly
- A formal internal theory note now defines the diagnostic hierarchy and evidence-completion criteria
- A first real-data benchmark sweep now exists for a Rashba positive control and a smooth-dot false-positive control in one finite-chain BdG code path
- A wider transport benchmark bundle now exists with positive-control, smooth-dot, impurity, disorder, eta-broadening, and bias-trace outputs stored under `/workspace/output/transport-benchmark`
- A first three-terminal benchmark package now exists under `/workspace/output/three-terminal-benchmark`, including selected operating points and rebuilt Figure 3/4 candidates

## What is still missing
- A verified novelty statement against both 2019/2021/2024 nanowire-diagnostic work and 2026 TAJJ overlap
- A numerically validated disorder-robust inhomogeneous discriminator for false-positive controls
- Final plotted and manuscript-vetted compensated-magnetic parameter scans and robustness windows
- A citation-clean reference set
- A fully convincing compensated-magnetic nonlocal transport benchmark with stronger topology discrimination than the current first-pass proxy implementation
- A completed derivation note integrated into the manuscript rather than only the internal theory file
- Final evidence-complete real data for every selected main-text data figure
- A benchmark where nonlocal transport, gap reopening, and a stronger topology label are evaluated together in the compensated-magnetic branch with the final chosen observable definitions
- One more false-positive family, preferably impurity- or YSR-like, implemented in the compensated-magnetic branch itself
- Stronger experimental observability windows for temperature and barrier scans
- A final choice on whether the manuscript will explicitly frame Fig. 5 around zero bias or a small near-zero-bias window
- If the manuscript insists on a broad-bias criterion, a stronger transport observable than the current proxy

## Acceptance probability (stage estimate)
- Nature Physics: 14-22% in the current manuscript-package state
- Nature Communications repack path: 15-25% if submitted immediately; 50-65% if the new required evidence-and-reproducibility package is actually completed
- Project success threshold: >70%
- Reason: the framing is now healthier, but the compensated-magnetic branch still lacks a real figure-grade evidence bundle and the reproducibility layer is not yet complete

## Last update
2026-05-01: completed a window-discrimination judgment for the candidate-based Fig. 5 rebuild and stored it under `data/fig4-fig5-candidate-rebuild-2026-05-01/`. The quantitative comparison shows that the current proxy supports a zero-bias or near-zero-bias discriminator much more convincingly than a full-bias-window discriminator, so the next writing and plotting pass should frame Fig. 5 around that narrower window unless the transport observable itself is upgraded.
