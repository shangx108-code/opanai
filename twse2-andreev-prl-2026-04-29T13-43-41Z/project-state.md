# Project State

Project: `twse2-andreev-prl`
Last updated: 2026-04-30

## Canonical Long-term Root

- Project slug: `twse2-andreev-prl-2026-04-29T13-43-41Z`
- First start time: `2026-04-29T13:43:41Z`
- GitHub repo / branch: `shangx108-code/opanai` @ `open-ai`
- GitHub root path: `twse2-andreev-prl-2026-04-29T13-43-41Z/`
- Local long-term root: `/workspace/memory/twse2-andreev-prl-2026-04-29T13-43-41Z`
- Active compute mirror: `/workspace/memory/twse2-andreev-prl`

## Iteration Control

- Cadence: once per hour
- Stop criterion:
  - Five reviewer-style acceptance estimates must all exceed `80%`
  - Evidence chain must be complete enough to produce the submission package, compiled main-text PDF, and compiled supplementary PDF

## Current Stage

Track-1 effective closure via V3 orbital-selective valley correction is in place, and the project is now in downstream BTK interpretation and hardening on top of a validated semi-infinite SGF benchmark for the PRL-oriented twisted bilayer WSe2 Andreev manuscript.

## Current Overall Goal

Complete a manuscript-grade data package for the twse2-Andreev project: reconstruct the true-or-closest faithful Tuo tight-binding input, then generate and durably store the Fig. 1-4 evidence chain, including normal-state band benchmarks, downstream SGF / BTK / robustness arrays, and their file-level indexes in both the memory folder and GitHub.

## Single Main Bottleneck

The project now has a faithful coupled baseline, a full V3 closure, a portable k-space sparse compressed-V3 approximation, a verified SGF stability trial, a first valley-resolved generalized BTK package, a validated semi-infinite SGF benchmark, a new valley-resolved generalized BTK rerun anchored to that semi-infinite SGF data, and a manuscript-language interpretation note that separates robust BTK statements from obsolete proxy-era claims. The single main bottleneck has therefore shifted again: the next highest-priority task is manuscript integration and deciding whether the current BTK kernel itself needs a deeper upgrade for journal-standard claims.

## Newly Verified Facts

- The user explicitly redirected the project so that `补齐所有数据` is the unique top priority.
- The user set the project iteration cadence to once per hour.
- The canonical GitHub long-term root has now been created under `shangx108-code/opanai` on branch `open-ai` at `twse2-andreev-prl-2026-04-29T13-43-41Z/`.
- The long-term root now includes a reproducible environment bootstrap script, a minimal requirements file, and an hourly iteration driver.
- The local hourly iteration driver now reports `ready_for_hourly_iteration: true`.
- An older overlapping two-hour schedule has been disabled so the new one-hour project loop is the only active cadence for this project.

## Immediate Next Action

1. Keep the `8.367 meV` coupled path-plus-hopping candidate as the faithful baseline, the `1.503 meV` full V3 package as the strongest closure, and the `2.726 meV` k-space sparse model as the current best portable compressed approximation for downstream work.
2. Treat the semi-infinite-informed BTK package as the only active manuscript branch.
3. Compare the BTK observables against the PRL claim boundary and decide whether the BTK kernel itself must be upgraded beyond the current proxy model before text integration.