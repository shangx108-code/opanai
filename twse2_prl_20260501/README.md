# tWSe2 PRL WP1-WP2 Minimal Engine

This directory contains a minimum runnable theory scaffold for the first two
work packages in the uploaded PRL planning notes:

- WP1: normal-state plus correlated-background calibration
- WP2: pairing-candidate library and symmetry screening

The goal is not a publication-grade final calculation yet. The goal is to turn
the paper outline into an executable starting point that already produces:

- a two-scale DOS summary for a minimal normal-plus-superconducting model
- a first-pass screening table for three pairing families at an interface

## Layout

- `config/default_params.json`: shared parameters
- `src/twse2_minimal.py`: model helpers
- `scripts/run_wp1_wp2.py`: runs the first two work packages
- `scripts/update_sync_status.py`: refreshes the project sync audit
- `results/`: generated summary tables and markdown
- `prl-manuscript-draft-v1.md`: PRL-style manuscript draft based on the current minimal results
- `sync-status.md`: current sync checklist for the long-term project space

## Run

```bash
python scripts/run_wp1_wp2.py
```
