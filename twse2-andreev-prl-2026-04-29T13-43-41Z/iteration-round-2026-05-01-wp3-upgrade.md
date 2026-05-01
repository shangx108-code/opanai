# Iteration Round 2026-05-01 WP3 Upgrade

## Scope

Upgraded the WP3 generalized BTK kernel from a pure transparency-decay form to a
competition-aware form with an explicit mid-barrier interface resonance term,
then reran the same `alpha-Z-phi` scan grid.

## New Artifacts

- `code/wp3_alpha_z_phi_btk.py` updated in place
- `data/wp3-alpha-z-phi-generalized-btk-upgraded-2026-05-01/conductance_curves.csv`
- `data/wp3-alpha-z-phi-generalized-btk-upgraded-2026-05-01/metrics_summary.csv`
- `data/wp3-alpha-z-phi-generalized-btk-upgraded-2026-05-01/parameters.json`
- `data/wp3-alpha-z-phi-generalized-btk-upgraded-2026-05-01/summary.md`

## What Changed Quantitatively

- In the old WP3 package, all three candidate families were monotonic in `Z`.
- In the upgraded package, `s_wave` stays monotonic and `chiral` stays monotonic
  on the tested grid, but `s_pm` no longer does.
- The per-configuration monotonic fraction for `s_pm` drops from `1.00` to
  `0.56` when checked configuration-by-configuration over `(eta, alpha, phi)`.
- The strongest `s_pm` peak contrast shifts away from `Z=0.0` and now occurs at
  `eta=1.00`, `alpha=0.000`, `phi=1.571`, `Z=0.5`, with peak-minus-background
  contrast `2.364`.

## Example Non-Monotonic Case

For `s_pm` at `eta=0.5`, `alpha=0.0`, `phi=0.0`, the subgap average over
`Z=[0.0, 0.5, 1.0, 2.0, 3.0]` becomes:

`[0.9414, 0.9692, 0.8169, 0.5459, 0.4384]`

which is explicitly non-monotonic because the conductance first rises from
`Z=0.0` to `Z=0.5` before decreasing.

## Interpretation Boundary

This upgrade is enough to show that the earlier all-monotonic `Z` behavior was
not a fundamental outcome of the candidate library; it was a kernel limitation.
At the same time, the current non-monotonicity is only verified for the
`s_pm`-like sign-changing family on the tested grid, not yet for the chiral
family.

## Shortest Next Action

Use the upgraded kernel as the active WP3 branch, then decide whether the next
round should target:

1. a stronger chiral-sensitive interface term, or
2. direct manuscript integration of the now-verified `s_pm` barrier
   non-monotonicity result.
