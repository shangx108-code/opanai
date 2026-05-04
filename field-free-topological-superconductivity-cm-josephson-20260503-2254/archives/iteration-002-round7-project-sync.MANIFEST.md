# iteration-002 round7 project sync archive manifest

Project: field-free-topological-superconductivity-cm-josephson-20260503-2254
Archive: iteration-002-round7-project-sync.zip
Created: 2026-05-04
Purpose: Consolidated project long-space snapshot through Round 7 global scoring.

## Package checks

- ZIP size: 68624 bytes
- base64 size: 92704 bytes
- base64 parts: 8
- part size target: 12000 bytes, except final part
- ZIP SHA256: 21188388dc5ded9c784a7198211d5f55048ab00d8cdbc7ac4024fed5cbe20ce0

## Included content

- Round 1 minimal BdG phase scan summaries and near-closing subset
- Round 2 planar junction coarse scan summaries and near-closing subset
- Round 3 selective weak-link scan summaries and near-closing subset
- Round 4 channel-filtered scan script, summary, and near-closing subset
- Round 5 recoupled-family scan script, summary, and candidate scores
- Round 6 row-asymmetric recoupling scan script, summary, and candidate scores
- Round 7 k-selective phase lever scan, best full scan, global scoring summary, ranked scores, and scoring script

## Included file list

- SYNC_MANIFEST.md
- results/channel-filtered-round4-scan-20260504/channel_filtered_round4_near_closing_points.csv
- results/channel-filtered-round4-scan-20260504/summary.md
- results/minimal-bdg-phase-scan-20260503/near_closing_points.csv
- results/minimal-bdg-phase-scan-20260503/summary.md
- results/planar-junction-coarse-scan-20260504/planar_junction_near_closing_points.csv
- results/planar-junction-coarse-scan-20260504/summary.md
- results/round5-recoupled-family-scan-20260504/candidate_scores.csv
- results/round5-recoupled-family-scan-20260504/summary.md
- results/round6-row-asymmetric-recoupling-20260504/candidate_scores.csv
- results/round6-row-asymmetric-recoupling-20260504/summary.md
- results/round7-k-selective-phase-lever-20260504/best_k_selective_full_scan.csv
- results/round7-k-selective-phase-lever-20260504/global_candidate_scores_ranked.csv
- results/round7-k-selective-phase-lever-20260504/global_scoring_summary.md
- results/round7-k-selective-phase-lever-20260504/summary.md
- results/selective-weak-link-scan-20260504/selective_weak_link_near_closing_points.csv
- results/selective-weak-link-scan-20260504/summary.md
- scripts/run_channel_filtered_round4_scan.py
- scripts/run_minimal_bdg_phase_scan.py
- scripts/run_planar_junction_coarse_scan.py
- scripts/run_round5_recoupled_family_scan.py
- scripts/run_round6_row_asymmetric_recoupling_scan.py
- scripts/run_round7_k_selective_phase_lever_scan.py
- scripts/run_selective_weak_link_scan.py
- scripts/score_round7_global_candidates.py

## Excluded content

- Python virtual environments
- bytecode/cache directories
- old archive/base64 sidecars, to avoid recursive packaging

## Restore command

Run inside the GitHub archive directory after all parts are present:

```bash
cat iteration-002-round7-project-sync.zip.base64.part-* | base64 -d > iteration-002-round7-project-sync.zip
sha256sum iteration-002-round7-project-sync.zip
unzip -t iteration-002-round7-project-sync.zip
```

Expected SHA256:

```text
21188388dc5ded9c784a7198211d5f55048ab00d8cdbc7ac4024fed5cbe20ce0
```

## Part status

- iteration-002-round7-project-sync.zip.base64.part-000
- iteration-002-round7-project-sync.zip.base64.part-001
- iteration-002-round7-project-sync.zip.base64.part-002
- iteration-002-round7-project-sync.zip.base64.part-003
- iteration-002-round7-project-sync.zip.base64.part-004
- iteration-002-round7-project-sync.zip.base64.part-005
- iteration-002-round7-project-sync.zip.base64.part-006
- iteration-002-round7-project-sync.zip.base64.part-007
