# Fig. 5 Observable Upgrade

This folder upgrades only the Fig. 5 readout layer while keeping the candidate
heatmaps and transport solver fixed.

## Selected observable

- Primary upgraded observable: `symmetric_nonlocal_score`

## Why it was selected

- It gave the strongest worst-case full-bias median separation across the two
  control families among the tested readouts.
- For `symmetric_nonlocal_score`, the positive/control median ratios are:
  - positive/dot = 9.980
  - positive/impurity = 9.128
- The worst of those two ratios is `9.128`.

## Interpretation

- The upgraded observable suppresses broad-bias leakage better than raw
  `|G_LR|`.
- This is a readout-layer upgrade, not a new transport simulation.

## Files

- `observable_selection_table.csv`
- `fig5a_positive_observable_heatmap.csv`
- `fig5b_dot_candidate_observable_heatmap.csv`
- `fig5c_impurity_candidate_observable_heatmap.csv`
