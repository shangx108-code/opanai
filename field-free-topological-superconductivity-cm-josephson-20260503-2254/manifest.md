# Manifest

## Canonical project root

- `field-free-topological-superconductivity-cm-josephson-20260503-2254/`

## Key files

- `README.md`: project summary and canonical structure
- `project-state.md`: current stage and single bottleneck
- `iteration-log.md`: per-round progress record
- `archive-checklist.md`: archive completion status
- `drive-index.md`: Drive collaboration mapping
- `configs/project.yaml`: project metadata and execution defaults
- `requirements.txt`: Python dependency record
- `scripts/bootstrap_env.sh`: environment setup entrypoint
- `scripts/check_environment.py`: environment verification script
- `manuscript/main.tex`: manuscript skeleton aligned to the current target journal

## Current round artifacts

- `scripts/run_channel_filtered_round4_scan.py`: fourth coarse scan with hard channel/orbital filtering
- `results/channel-filtered-round4-scan-20260504/summary.md`: quantitative round-four result summary
- `results/channel-filtered-round4-scan-20260504/channel_filtered_round4_near_closing_points.csv`: near-closing subset for the fourth scan
- `results/channel-filtered-round4-scan-20260504/channel_filtered_round4_gap_scan.csv`: full fourth-scan coarse grid output, currently still local-only and pending GitHub writeback
- `scripts/run_round5_recoupled_family_scan.py`: fifth scan testing small recoupling on the three residual round-four families
- `results/round5-recoupled-family-scan-20260504/summary.md`: round-five quantitative tradeoff summary
- `results/round5-recoupled-family-scan-20260504/candidate_scores.csv`: round-five candidate ranking table
- `results/round5-recoupled-family-scan-20260504/family_gap_traces.csv`: round-five family trace table, currently still local-only and pending GitHub writeback
- `results/round5-recoupled-family-scan-20260504/best_recoupled_full_scan.csv`: full fifth-scan coarse grid output, currently still local-only and pending GitHub writeback
- `results/round5-recoupled-family-scan-20260504/best_recoupled_near_closing.csv`: fifth-scan near-closing subset, currently still local-only and pending GitHub writeback

## Current archive expectation

- All files above should be written to `shangx108-code/opanai` on branch `open-ai` under the same project root.
