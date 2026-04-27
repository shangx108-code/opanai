# Theory Note V2

Last updated: 2026-04-27

## New rigor gain in this round

In addition to the binary Poisson discrimination bound, we now have a corollary that converts a threshold-activation approximation requirement into a photon-floor statement.

## Corollary: threshold activation floor from binary discrimination

Consider a binary-like target activation on two input regions separated by a positive normalized margin `m`. If a physical activation mechanism achieves mean output error at most `epsilon < 1/2` on those two regions, then the induced binary decision problem must attain a minimum signal-to-noise ratio

`D0 >= (1 - 2 epsilon) / sqrt(2 epsilon (1 - epsilon))`.

Combining this with the previously derived Poisson discrimination bound yields

`n_min >= { 0.5 * [ D0^2 + D0 * sqrt(D0^2 + 8 d) ] } / ( eta * 10^(-L/10) * m )`.

This corollary is now implemented in `/workspace/quantum_activation/theory/threshold_bound.py` and tabulated in `/workspace/results/threshold_activation_bounds.csv`.

## What this proves

1. achieving a sharper threshold-like activation requires rapidly increasing photon budget as `epsilon` decreases
2. detector inefficiency and loss penalize threshold-like activation directly and multiplicatively
3. dark counts matter increasingly as the required threshold sharpness grows

## What this still does not prove

1. a universal closed-form lower bound for arbitrary smooth activations such as sigmoid or tanh
2. optimality of AQMA relative to all conceivable physical nonlinear mechanisms
3. a theorem that directly predicts benchmark accuracy from the lower bound

## Numerically backed examples

For margin `m = 0.5`, efficiency `eta = 0.82`, loss `L = 3 dB`, and dark count `d = 0.01`, the current implementation gives:

1. `epsilon = 0.2` -> `n_min = 5.57`
2. `epsilon = 0.1` -> `n_min = 17.40`
3. `epsilon = 0.05` -> `n_min = 41.59`

These values are useful because they place a quantitative floor under increasingly sharp binary-like activations in a realistic detector regime.
