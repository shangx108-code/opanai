# Methods Note V2

Last updated: 2026-04-26

## Simulation Layers

The current project uses three evidence layers that should be kept conceptually distinct in the paper:

1. function-level scans:
   numerical approximation of target nonlinear responses under idealized and device-constrained activation models
2. task-level benchmarks:
   Monte Carlo inference studies using sampled measurement outcomes and finite-dimensional linear projections
3. analytic floor:
   a closed-form lower bound for binary discrimination in the Poisson counting regime

## Why This Separation Matters

The manuscript should not imply that a theorem on binary discrimination automatically proves the full optimization-based activation-cost landscape. Instead:

1. the theorem constrains one important regime
2. the scans map achievable envelopes for specific model families
3. the benchmarks test whether those envelopes correlate with usable inference behavior

## Recommended Claim Structure

Use the following hierarchy in the paper:

1. strongest claim:
   binary-like activation in counting-limited settings obeys a rigorous resource floor that increases with loss, reduced efficiency and dark counts
2. medium claim:
   numerical optimization indicates that sigmoid-like measurement-induced activation can remain low-budget across a realistic device window
3. task claim:
   benchmark gains are task-dependent, with strong benefits on curved-separation toy data and weaker gains on the current weak-signal discrimination task

## Immediate Methods Additions Still Needed

1. explicit symbol table
2. precise prior choice `p(x)` for activation-cost integration
3. reproducibility note for random seeds and parameter grids
4. one paragraph explaining why the weak-signal benchmark is intentionally difficult and why its modest gains are informative rather than contradictory
5. add the new threshold-activation corollary as a separate proposition beneath the Poisson discrimination theorem
