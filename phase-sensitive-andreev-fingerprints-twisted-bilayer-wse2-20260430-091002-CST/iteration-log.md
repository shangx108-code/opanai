# Iteration Log

## 2026-04-30 09:10:02 CST

- Initialized the long-term GitHub project space.
- Archived the two uploaded planning md files into `inputs/`.
- Created state, review, role, journal, and archive tracking files.
- Added `scripts/minimal_bdg_scaffold.py`.
- Ran the scaffold and saved `results/initial_gap_summary.json` and `results/initial_gap_summary.csv`.
- Current bottleneck fixed as the lack of evidence-producing Andreev-selectivity calculations.
- Current acceptance estimate fixed at 12-18%.

## 2026-04-30 09:19:00 CST

- Upgraded `scripts/minimal_bdg_scaffold.py` from a bulk-only summary into an interface-sensitive surrogate scan.
- Added barrier, interface-orientation, intervalley, and in-plane-field scan dimensions in `config/default_scan_config.json`.
- Generated `results/interface_scan_metrics.csv`, `results/candidate_constraint_summary.csv`, and `results/ordinary_s_wave_failure_candidate.json`.
- First reusable numerical outcome: s-wave is now a failure candidate in the toy scan because it fails orientation, intervalley, and field-angle contrast thresholds simultaneously.
- Main bottleneck shifted from "no executable evidence path" to "need a more physics-faithful response model and robustness checks."
