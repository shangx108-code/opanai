# Method-Fair Hardware-Tolerance Package

## Status

- Package type: `fairness protocol scaffold plus executed proxy-tolerance boundary note`
- Execution status: `first-pass proxy-tolerance execution completed; broad hardware-robustness claim not yet supported`

## Fairness rule

- Use common perturbations for headline cross-method comparison.
- Report phase-mask-specific perturbations separately as engineering diagnostics for the phase-only stack.

## Frozen perturbation matrix

- `method_fair_tolerance_matrix.csv` records perturbation family, units, applied location, method scope, and fairness class.
- Executed proxy-tolerance files now also exist in the active root:
  - `mixed_train_tolerance_summary.json`
  - `robust_mask_tolerance_compare.json`
  - `robust_mask_tolerance_metrics.csv`

## Interpretation boundary

This package does not by itself establish hardware robustness. It freezes a reviewer-safe protocol so later runs cannot quietly mix common-input perturbations with phase-mask-only perturbations. The active root now contains executed proxy-tolerance results, but those results support only a constrained engineering conclusion: mild shared perturbations preserve positive gain, robust-mask training repairs first-order `1 px` shift and `3/4`-bit quantization failures, and `2 px` lateral shift remains a clear failure mode.

## True blocker

- No fabricated-device tolerance evidence is present in the active root.
- Therefore the remaining blocker is no longer the absence of any executed tolerance result, but the absence of stronger hardware-facing validation beyond the current proxy-tolerance regime.
