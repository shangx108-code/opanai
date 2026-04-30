# Project State

- Project: Phase-sensitive Andreev fingerprints of unconventional pairing in twisted bilayer WSe2
- Long-term project space: `phase-sensitive-andreev-fingerprints-twisted-bilayer-wse2-20260430-091002-CST`
- Target journal: Physical Review Letters
- Article type: Theory Letter
- Last updated: 2026-04-30 09:10:02 CST

## Research Goal

Turn the current concept package into a reproducible PRL-ready theory paper that introduces a phase-sensitive Andreev diagnostic framework for twisted bilayer WSe2 and uses it to exclude ordinary same-sign s-wave under a coupled set of experimentally readable constraints.

## Current Stage

Project takeover and executable scaffold initialization.

## Current Main Bottleneck

Data truth and computational reproducibility gap: the project has a strong concept and work-package design, but it still lacks a versioned executable theory workflow that can start producing traceable evidence for the inner-gap selectivity and ordinary s-wave exclusion claims.

## Authoritative Sources In This Round

1. `inputs/01-markdown-3-.md`
2. `inputs/02-markdown-4-.md`
3. `results/initial_gap_summary.json`
4. `results/initial_gap_summary.csv`

## What Was Completed In This Round

1. Locked the project identity and target journal from the uploaded materials.
2. Created a dedicated timestamped long-term project space in the GitHub repository.
3. Initialized project-state, role, review, journal, archive, manifest, and iteration files for cross-round continuity.
4. Added a runnable minimal BdG scaffold to encode the normal-state toy model and three candidate pairing families.
5. Ran the scaffold once and generated the first machine-readable summary tables for candidate-state gap statistics.

## Current Evidence Snapshot

- The current numerical layer is only a v0 scaffold, not yet publication-grade evidence.
- The initial run confirms that the code path for normal-state plus candidate-pairing evaluation is reproducible and archived.
- The present outputs are enough to anchor future rounds, but not enough to support any journal-facing physics claim beyond "workflow initialized."

## Current Acceptance Estimate

12-18%.

## Stop Condition

Acceptance forecast above 80%, with all main evidence-chain blocks closed:

1. inner-gap selectivity quantitatively demonstrated
2. ordinary same-sign s-wave exclusion supported by coupled constraints
3. robustness checks completed
4. manuscript-ready figure logic and claim boundaries locked

## Next Highest-Priority Goal

Upgrade the minimal scaffold into the first evidence-producing calculation: a parameterized inner-gap versus outer-feature toy study that can test whether Andreev-selective behavior survives basic sweeps over barrier strength, intervalley mixing, and candidate pairing family.

## Immediate Plan

1. Extend the current scaffold from bulk gap statistics to a minimal Andreev-like response surrogate.
2. Define the first strict decision metrics for inner-gap selectivity and ordinary s-wave failure.
3. Produce the first figure-grade parameter scan tables.
4. Update the acceptance estimate only after real exclusion or robustness evidence appears.
