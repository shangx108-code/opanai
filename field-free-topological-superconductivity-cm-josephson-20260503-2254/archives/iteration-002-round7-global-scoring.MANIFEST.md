# iteration-002 round7 global scoring archive manifest

Project: field-free-topological-superconductivity-cm-josephson-20260503-2254
Archive: iteration-002-round7-global-scoring.zip
Iteration label: iteration-002
Created: 2026-05-04
Purpose: Round 7 k-selective phase lever results and global candidate scoring archive for later manuscript synthesis and project review.

## Contents

- results/round7-k-selective-phase-lever-20260504/summary.md
- results/round7-k-selective-phase-lever-20260504/best_k_selective_full_scan.csv
- results/round7-k-selective-phase-lever-20260504/global_scoring_summary.md
- results/round7-k-selective-phase-lever-20260504/global_candidate_scores_ranked.csv
- scripts/run_round7_k_selective_phase_lever_scan.py
- scripts/score_round7_global_candidates.py

## Scientific status

Round 7 introduced a k-selective phase lever and then fixed a global scoring rule to balance phase concentration against total low-gap clutter. The lead candidate is selected by an explicit threshold plus weighted global score rather than by family-level visual inspection alone.

Lead candidate:

- sigma = 0.18
- t_boost = 0.04
- alpha_boost = 0.06
- near-closing count = 47
- phi~pi fraction = 0.213
- low-phase fraction = 0.170

Selection rule:

1. Candidate must satisfy phi_pi_fraction > 0.154 and low_phi_fraction < 0.231.
2. Rank by global_score = 0.50 * clutter_recovery + 0.35 * phase_focus_gain + 0.15 * low_phi_suppression.

## Restore from base64 sidecar

After all parts are present in the same directory:

```bash
cat iteration-002-round7-global-scoring.zip.base64.part-* | base64 -d > iteration-002-round7-global-scoring.zip
unzip -t iteration-002-round7-global-scoring.zip
```

## Part status

- iteration-002-round7-global-scoring.zip.base64.part-000: pending
- iteration-002-round7-global-scoring.zip.base64.part-001: pending
- iteration-002-round7-global-scoring.zip.base64.part-002: pending
- iteration-002-round7-global-scoring.zip.base64.part-003: pending
- iteration-002-round7-global-scoring.zip.base64.part-004: pending
- iteration-002-round7-global-scoring.zip.base64.part-005: pending
