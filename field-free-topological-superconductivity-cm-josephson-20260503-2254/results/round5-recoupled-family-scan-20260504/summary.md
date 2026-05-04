# Round-5 Recoupled Family Scan

## Goal

Restore phi sensitivity in the three residual round-four families by adding only a small amount of recoupling rather than reopening the full low-gap manifold.

## Best candidate

- `t_interface = 0.2`
- `t_junction_y = 0.14`
- `alpha_junction_x = 0.1`
- `alpha_junction_y = 0.06`
- `channel_filter_strength = 0.55`
- family-level `phi~pi` wins: `3/3`
- mean phase-gain score: `0.344360`
- mean family gap spread: `0.000108`

## Full-scan result for the best candidate

- total points: `936`
- near-closing points: `204`
- near-closing `phi~pi` fraction: `0.147`
- near-closing low-phase fraction: `0.235`
- smallest gap: `0.000000` at `mu=1.500`, `M0=0.400`, `phi/pi=0.500`

## Interpretation

- This round tests only small recoupling moves on top of the hard filter, so any change in phi sensitivity can be attributed to restored phase leverage rather than a full model reset.
- Family-level phi leverage does come back: the best candidate makes all three residual round-four families favor `phi=pi` over `phi=0`.
- The global tradeoff is unfavorable in its current form: once the best family-level candidate is restored to the full coarse scan, near-closing points grow from the round-four baseline `39` to the measured value in this run.
- The remaining phase-allocation metrics barely improve at the full-grid level, so this is not yet the right manuscript branch.

## Evidence status

- `tradeoff verified but globally unfavorable`: small recoupling can restore phase preference locally in the residual families, but the current recoupling knobs reopen too much global low-gap clutter.
