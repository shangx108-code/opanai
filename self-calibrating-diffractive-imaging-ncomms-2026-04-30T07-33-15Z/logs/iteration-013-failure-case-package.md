# Iteration 013 Failure-Case Package

- Timestamp: `2026-05-01T00:00:00Z`
- Action type: `object_family_shift_failure_case_analysis`
- Stage: `active calculation/verification`
- Single bottleneck addressed: `the manuscript still lacked a concrete reviewer-facing failure-case package under object-family shift`

## Executed action

1. Added `scripts/generate_object_shift_failure_cases.py`.
2. Re-ran the phase-only stack only for the representative seeds needed to recover worst-case object-family failures.
3. Generated:
   - `results/failure_cases/object_shift_failure_cases.csv`
   - `results/failure_cases/object_shift_failure_cases_panel.png`
   - `results/failure_cases/object_shift_failure_cases.md`
   - `results/failure_cases/object_shift_failure_cases_summary.json`
4. Integrated the resulting pattern back into:
   - `manuscript/main-manuscript-v2-strict.md`
   - `manuscript/supplementary-methods-and-tables-v1.md`

## Verified failure pattern

- `diag_x` is the most consistently negative held-out object family.
- `checker_blocks` sits near the decision boundary but contains clear negative cases.
- `crescent` has a mixed but nontrivial negative tail.
- `triangle` remains comparatively stable and positive.

## Interpretation boundary

This round does not claim that the failure mechanism has been fully proved. It does close a reviewer-facing packaging gap by showing that the negative tail under object-family shift is structured and auditable rather than anecdotal.
