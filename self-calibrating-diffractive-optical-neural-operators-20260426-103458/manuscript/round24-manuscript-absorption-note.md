# Round 24 manuscript absorption note

## Bottleneck

The scientific chain was already closed by rounds 18--23, but the current writing window still lacked one extreme-short quantitative table that could be pasted directly into the main text, SI, and reviewer response without reopening the larger ledgers.

## Chosen action

Compress the locked round18--19 numeric anchors and the round20--23 approved wording into one writer-facing numeric short table plus one LaTeX-safe insertion block.

## Required data / blocker status

- Required source tables were already available:
  - `archive/round18-codex-return/results/round18_boundary_synthesis_table.csv`
  - `archive/round19-codex-return/results/round19_threshold_robustness_table.csv`
  - `archive/round19-codex-return/results/round19_anchor_swap_audit.csv`
  - `archive/round20-codex-return/results/round20_figure5_claim_ledger.csv`
  - `archive/round23-codex-return/results/round23_writer_micro_tables.csv`
- No new model run, audit, threshold search, or sentence expansion was required.

## Execution

- Re-read the round23 writer handoff pack and traced each approved sentence back to the locked round18--19 numeric anchors.
- Extracted the minimum numeric rows needed for the writing pass:
  - round14 `very_weak`
  - round15 `minimal_image_bridge`
  - round16 `diag_minus_ordinary_readout`
  - round17 `spatial_scrambled_noncommon`
- Preserved the round19 robustness caveat as compact reviewer-facing audit numbers:
  - anchor-swap audit `0/4`
  - round17 fully stable threshold pairs `3/9`
- Wrote one CSV short table and one LaTeX-safe insertion block.

## Deliverable

- Numeric short table:
  - `results/round24_figure5_boundary_numeric_short_table.csv`
- LaTeX-safe insertion block:
  - `submission-package/05-figure5-boundary-short-insert.tex`

## Evidence status

verified

This round changes no scientific conclusion. It only compresses already locked evidence into a lower-friction writing artifact.

## Next step

Replace the current long-form Figure 5 boundary prose in the manuscript workflow with the round24 short insert, then run one final naming and consistency pass across `submission-package/`.
