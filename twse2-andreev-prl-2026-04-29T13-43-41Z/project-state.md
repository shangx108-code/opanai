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

Track-1 closure and semi-infinite SGF validation are already in place. The project has now moved into upgraded BTK discrimination work using a channel-resolved multiorbital kernel.

## Current Overall Goal

Complete a manuscript-grade data package for the twse2-Andreev project and convert the upgraded BTK line into a PRL-grade exclusion chain against ordinary same-sign `s`-wave.

## Single Main Bottleneck

The BTK kernel upgrade is now complete. The single active bottleneck is to use the upgraded kernel to construct a discriminating null-model scan that forces ordinary same-sign `s`-wave to fail on at least one robust observable.

## Newly Verified Facts

- The one-hour project schedule remains the only active schedule for this chat.
- The upgraded BTK engine has now been generated in `btk-channel-resolved-multiorbital-semi-infinite-2026-04-30`.
- This package replaces the scalar conductance proxy with channel-resolved reflection amplitudes, multiorbital BdG pairing matrices, explicit interface orientation `alpha`, and explicit interface mixing `mixing_lambda`.
- In the upgraded package, the strongest total peak contrast still appears in `s_wave`, while the strongest valley asymmetry shifts to `valley_odd`.
- Kernel existence is therefore no longer the blocker; discriminating exclusion is.

## Immediate Next Action

1. Treat `btk-channel-resolved-multiorbital-semi-infinite-2026-04-30` as the active BTK working package.
2. Use `btk-upgrade-result-2026-04-30.md` as the handoff note for what the upgraded kernel now establishes and what it still does not establish.
3. Run a selection-rule null-model scan with the upgraded kernel, targeting one observable on which ordinary same-sign `s`-wave fails robustly while at least one unconventional family survives.