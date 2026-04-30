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

The BTK adequacy check is now closed. The current semi-infinite-informed BTK package preserves a real valley-resolved response, but the kernel is still a proxy benchmark and cannot yet support PRL-grade phase-sensitive exclusion claims. The single active bottleneck is therefore a deeper BTK kernel upgrade before manuscript-level exclusion of ordinary same-sign `s`-wave.

## Newly Verified Facts

- The user explicitly redirected the project so that `补齐所有数据` is the unique top priority.
- The user set the project iteration cadence to once per hour.
- The canonical GitHub long-term root has now been created under `shangx108-code/opanai` on branch `open-ai` at `twse2-andreev-prl-2026-04-29T13-43-41Z/`.
- The long-term root now includes a reproducible environment bootstrap script, a minimal requirements file, and an hourly iteration driver.
- The local hourly iteration driver now reports `ready_for_hourly_iteration: true`.
- An older overlapping two-hour schedule has been disabled so the new one-hour project loop is the only active cadence for this project.
- The BTK adequacy review is now closed: the present semi-infinite-informed BTK package is scientifically usable as a proxy diagnostic, but not yet strong enough for PRL-grade phase-sensitive exclusion wording.
- The strongest current valley peak-contrast asymmetry still appears in the `s_wave` channel inside the proxy kernel, so the current BTK line does not yet exclude ordinary same-sign `s`-wave.

## Immediate Next Action

1. Keep the `8.367 meV` coupled path-plus-hopping candidate as the faithful baseline, the `1.503 meV` full V3 package as the strongest closure, and the `2.726 meV` k-space sparse model as the current best portable compressed approximation for downstream work.
2. Treat the semi-infinite-informed BTK package as the only active manuscript branch.
3. Use `btk-kernel-prl-adequacy-assessment-2026-04-30.md` as the ruling memo for what the current BTK package can and cannot claim.
4. Upgrade the BTK kernel from the current scalar proxy into a channel-resolved multiorbital generalized BTK engine before attempting PRL-grade exclusion wording.