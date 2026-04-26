# Theory Note V1

Last updated: 2026-04-26

## Scope

This note records the part of the theory that is already defensible from the current project state. It should be used to prevent the manuscript from overstating what has actually been proven.

## 1. Activation Approximation Cost

For a target nonlinear response `sigma(x)` and a physical activation family `A_theta(x)`, define the approximation error

`E_act(theta) = integral |A_theta(x) - sigma(x)|^2 p(x) dx`

where `p(x)` is the chosen input prior. The optimization-based activation cost at tolerance `epsilon` is then

`C_act(sigma, epsilon) = min n_bar`

subject to `E_act(theta) <= epsilon`.

Current status:

- Numerically implemented for proxy models.
- Not yet proven as a closed-form lower bound in general.

## 2. Binary Discrimination Cost Under Poisson Counting

For binary discrimination between a dark input and an illuminated input with mean detected signal `gamma n`, where

`gamma = eta * 10^(-L/10)`,

and with dark count `d`, the signal-to-noise ratio under Poisson statistics is

`D = (gamma n) / sqrt(gamma n + 2 d)`.

To require `D >= D0`, let `y = gamma n`. Then

`y / sqrt(y + 2 d) >= D0`

implies

`y^2 - D0^2 y - 2 D0^2 d >= 0`.

Solving the quadratic inequality gives

`y >= 0.5 * [ D0^2 + D0 * sqrt(D0^2 + 8 d) ]`.

Therefore the minimum required input photons satisfy

`n_min(D0, eta, L, d) >= { 0.5 * [ D0^2 + D0 * sqrt(D0^2 + 8 d) ] } / ( eta * 10^(-L/10) )`.

## 3. Interpretation

This bound is rigorous only for the stated discrimination setting. It does not yet prove a universal lower bound for arbitrary activation-function approximation. What it does prove is:

1. efficiency and optical loss enter multiplicatively and directly inflate the required input-photon floor
2. dark counts matter weakly at low discrimination targets but become increasingly costly at higher `D0`
3. any claim that binary-like activation is cheap in the low-photon regime must confront this floor

## 4. Numerical Examples Already Backed By Code

At `eta = 0.9`, `L = 3 dB`, `d = 0.01`, the current code gives:

1. `D0 = 1` -> `n_min = 2.2604`
2. `D0 = 2` -> `n_min = 8.9120`
3. `D0 = 3` -> `n_min = 19.9969`
4. `D0 = 5` -> `n_min = 55.4683`

These values are written to `/workspace/results/discrimination_bounds.csv`.

## 5. Manuscript Guardrail

Until a broader theorem is derived, the paper should use the following language discipline:

1. use "quantum resource floor" or "Poisson discrimination lower bound" when referring to the proven result
2. use "numerical lower envelope" or "optimization-based activation cost" for the scan-based results
3. reserve "quantum limit" for carefully scoped statements, not the whole manuscript in a blanket way
