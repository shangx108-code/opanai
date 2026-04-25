# Nature Photonics Project State

## Current stage
- Result generation, now specifically first comparison generation

## Current total goal
- Build a Nature Photonics-competitive theory-and-simulation paper on quantum limits of nonlinear activation in photonic neural networks, with a quantitative resource framework, realistic measurement-induced activation route, and figure-ready evidence.

## Core bottleneck
- The project now has one device-interpretable comparison, but it still lacks a multi-route same-axis comparison and a figure-ready panel that would let a referee judge whether the result is a real design law rather than a single worked example.

## Highest-priority action completed in this run
- Computed the first concrete homodyne-conditioned AQMA proxy on the same axes as the completed lower bound and quantified how detector efficiency moves it away from the frontier.

## This run's concrete computation
### Goal
- Put one concrete measurement-induced activation architecture on the same axes as the proved lower bound
  `n_bar >= (1/4) ln(1 / (4 epsilon (1 - epsilon)))`.

### Architecture fixed in this run
- Use the homodyne-conditioned AQMA proxy already defined in the theory framework.
- Model the boundary states as the coherent pair `|+a>` and `|-a>` with symmetric mean photon number `n_bar = a^2`.
- Use single-shot homodyne along the signal quadrature with detector efficiency `eta`.
- Use zero-threshold boundary decision on the homodyne outcome.

### Quantities computed
1. Lower-bound decision error:
   `epsilon_lb(n_bar) = 1/2 * (1 - sqrt(1 - exp(-4 n_bar)))`.
2. Lower-bound inverse photon cost:
   `n_bar^lb(epsilon) = (1/4) ln(1 / (4 epsilon (1 - epsilon)))`.
3. Homodyne proxy decision error:
   `epsilon_hom(n_bar, eta) = 1/2 * erfc(sqrt(2 eta n_bar))`.
4. Minimum homodyne photon cost `n_bar^hom(epsilon, eta)` from direct numerical inversion.

### Verified numerical outputs
- At `epsilon = 0.10`:
  `n_bar^lb = 0.255413`,
  `n_bar^hom = 0.414741` at `eta = 0.99`,
  `0.483051` at `eta = 0.85`,
  `0.586562` at `eta = 0.70`,
  `0.821187` at `eta = 0.50`.
- At `epsilon = 0.01`:
  `n_bar^lb = 0.807232`,
  `n_bar^hom = 1.366640` at `eta = 0.99`,
  `1.591734` at `eta = 0.85`,
  `1.932819` at `eta = 0.70`,
  `2.705947` at `eta = 0.50`.
- The photon-cost ratio `n_bar^hom / n_bar^lb` stays at about
  `1.624-1.693` for `eta = 0.99`,
  `1.891-1.972` for `eta = 0.85`,
  `2.297-2.394` for `eta = 0.70`,
  and `3.215-3.352` for `eta = 0.50`
  over `epsilon = 0.10-0.01`.
- At fixed `n_bar = 0.25`, the lower bound gives `epsilon_lb = 0.102470`, while the homodyne proxy gives
  `0.159871` at `eta = 0.99`,
  `0.178276` at `eta = 0.85`,
  `0.201392` at `eta = 0.70`,
  `0.239750` at `eta = 0.50`.

### Design-relevant interpretation
- The project now has a real accessible-region comparison, not just a formal floor.
- Near-unity-efficiency homodyne stays within about a `1.6-1.7x` photon penalty above the discrimination lower bound in the low-error regime.
- Detector inefficiency rapidly widens that penalty, which produces the first device-facing message of the paper:
  measurement-induced activation can stay near the frontier only when detector efficiency is very high.

## What is genuinely completed
- One explicit lower bound exists for boundary discrimination cost.
- One concrete measurement-induced activation route now sits on the same axes as that bound.
- The project now has verified numerical evidence for how detector efficiency changes the distance from an accessible route to the lower-bound frontier.
- A figure candidate can now show both the excluded region and a concrete accessible-route family.

## What is still incomplete
- No second physical activation family has yet been compared on the same axes
- No finalized figure panel has yet been drawn from the computed tables
- No manuscript PDF or supplementary PDF exists
- No verified literature-positioning text has yet been rewritten around this comparison
- No task-level evidence yet links the single-neuron frontier to network benefit

## Current acceptance estimate
- The project is still far below submission readiness, but the evidence base is now materially stronger than in the lower-bound-only state.
- Working Nature Photonics stage estimate after this run: 24-34%.
- Reason: the project now has a same-axis lower-bound-versus-architecture comparison with explicit detector-efficiency dependence, but it still lacks a second baseline, figure-grade assembly, manuscript integration, and literature separation.

## Latest update
- 2026-04-25: computed the first concrete homodyne-conditioned AQMA proxy on the same axes as the coherent-state discrimination lower bound.
- 2026-04-25: verified that the homodyne route stays within about `1.6-1.7x` of the lower-bound photon cost for `eta = 0.99`, but widens to about `3.2-3.35x` for `eta = 0.50` over `epsilon = 0.10-0.01`.

## Next immediate action
- Add one second concrete activation family on the same axes and assemble the first figure-ready panel showing lower bound, homodyne-accessible region, and the new comparison trace with full caption logic.
