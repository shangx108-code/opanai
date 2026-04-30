# Project State

- Project: Phase-sensitive Andreev fingerprints of unconventional pairing in twisted bilayer WSe2
- Long-term project space: `phase-sensitive-andreev-fingerprints-twisted-bilayer-wse2-20260430-091002-CST`
- Target journal: Physical Review Letters
- Article type: Theory Letter
- Last updated: 2026-04-30 09:19:00 CST

## Research Goal

Turn the current concept package into a reproducible PRL-ready theory paper that introduces a phase-sensitive Andreev diagnostic framework for twisted bilayer WSe2 and uses it to exclude ordinary same-sign s-wave under a coupled set of experimentally readable constraints.

## Current Stage

First interface-sensitive surrogate scan completed.

## Current Main Bottleneck

Evidence-chain gap: the project now has a runnable interface-sensitive surrogate and an initial s-wave failure candidate, but still lacks a stronger quantitative bridge from this toy scan to a more physics-faithful Andreev/BTK-level exclusion argument.

## Authoritative Sources In This Round

1. `inputs/01-markdown-3-.md`
2. `inputs/02-markdown-4-.md`
3. `results/initial_gap_summary.json`
4. `results/initial_gap_summary.csv`
5. `results/interface_scan_metrics.csv`
6. `results/candidate_constraint_summary.csv`
7. `results/ordinary_s_wave_failure_candidate.json`

## What Was Completed In This Round

1. Locked the project identity and target journal from the uploaded materials.
2. Created a dedicated timestamped long-term project space in the GitHub repository.
3. Initialized project-state, role, review, journal, archive, manifest, and iteration files for cross-round continuity.
4. Added a runnable minimal BdG scaffold to encode the normal-state toy model and three candidate pairing families.
5. Upgraded the scaffold into an interface-sensitive surrogate scan over barrier strength, interface orientation, intervalley mixing, and in-plane field angle.
6. Generated candidate-level constraint summaries and the first machine-readable ordinary s-wave failure-candidate file.

## Current Evidence Snapshot

- The current numerical layer remains a toy surrogate rather than a full BTK calculation, so it cannot yet support journal-facing claims on its own.
- The first interface-sensitive scan now produces explicit inner-selectivity and contrast metrics for all three candidate families.
- In this scan, ordinary same-sign s-wave reaches strong raw inner-selectivity at low barrier, but fails the orientation, intervalley, and field-angle contrast thresholds that the best unconventional candidate satisfies.
- The present outputs are enough to justify the next evidence step: replacing the toy surrogate with a more physics-faithful response model while preserving the same saved metrics.

## Current Acceptance Estimate

20-28%.

## Stop Condition

Acceptance forecast above 80%, with all main evidence-chain blocks closed:

1. inner-gap selectivity quantitatively demonstrated
2. ordinary same-sign s-wave exclusion supported by coupled constraints
3. robustness checks completed
4. manuscript-ready figure logic and claim boundaries locked

## Next Highest-Priority Goal

Strengthen the current failure candidate into a more credible exclusion layer by upgrading the response surrogate toward a BTK-like calculation while keeping the same contrast-based decision metrics.

## Immediate Plan

1. Replace the current hand-built response surrogate with a closer interface-scattering approximation.
2. Stress-test the current s-wave failure candidate against broadening and parameter perturbations.
3. Convert the strongest surviving scan into a figure-ready panel map and caption skeleton.
4. Keep the acceptance estimate conservative until the failure candidate survives robustness checks.
