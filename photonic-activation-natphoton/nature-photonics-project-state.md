# Nature Photonics Project State

## Current stage
- Result generation

## Current total goal
- Build a Nature Photonics-competitive theory-and-simulation paper on quantum limits of nonlinear activation in photonic neural networks, with a quantitative resource framework, realistic measurement-induced activation route, and figure-ready evidence.

## Core bottleneck
- The project now has a first validated numerical boundary curve, but it still lacks a device-interpretable comparison showing where a concrete measurement-induced activation route can approach or miss this lower bound.

## Highest-priority action completed in this run
- Ran the first real numerical scan from the completed lower bound and converted it into reproducible boundary-cost data for a figure-ready panel candidate.

## This run's concrete computation
### Goal
- Turn the completed lower bound
  `n_bar >= (1/4) ln(1 / (4 epsilon (1 - epsilon)))`
  into referee-checkable numerical data rather than leaving it as a text-only formula.

### Parameterization used
- Allowed boundary decision error `epsilon` sampled at
  `0.01, 0.02, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40`.
- Threshold margin parameter `delta` sampled at
  `0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50`
  under the local linear encoding model
  `alpha(x) = g (x - x_th)`,
  so that `Delta alpha = 2 g delta`.

### Quantities computed
1. Minimum mean boundary-state photon cost:
   `n_bar^min(epsilon) = (1/4) ln(1 / (4 epsilon (1 - epsilon)))`.
2. Minimum encoder gain required to resolve a threshold margin `delta` at target error `epsilon`:
   `g_min(delta, epsilon) = sqrt(ln(1 / (4 epsilon (1 - epsilon)))) / (2 delta)`.

### Verified numerical outputs
- Photon-cost lower bound:
  `epsilon = 0.40 -> n_bar^min = 0.010205`
- Photon-cost lower bound:
  `epsilon = 0.20 -> n_bar^min = 0.111572`
- Photon-cost lower bound:
  `epsilon = 0.10 -> n_bar^min = 0.255413`
- Photon-cost lower bound:
  `epsilon = 0.05 -> n_bar^min = 0.415183`
- Photon-cost lower bound:
  `epsilon = 0.02 -> n_bar^min = 0.636483`
- Photon-cost lower bound:
  `epsilon = 0.01 -> n_bar^min = 0.807232`
- At fixed `delta = 0.10`, the minimum encoding gain rises as:
  `g_min = 1.010223, 3.340236, 5.053838, 6.443468, 7.977987, 8.984607`
  for `epsilon = 0.40, 0.20, 0.10, 0.05, 0.02, 0.01`, respectively.

### Design-relevant interpretation
- The bound is numerically weak only when one tolerates very high decision error near the activation boundary.
- Once the target boundary error drops below `10%`, even the lower bound already requires a quarter-photon-scale average boundary cost.
- For a narrow normalized threshold margin `delta = 0.10`, the encoding slope required by the lower bound grows sharply as one asks for sharper activation decisions, which gives a direct axis for a figure panel and later hardware comparison.

## This run's concrete derivation
### Goal
- Formalize one non-rhetorical quantity behind "activation quantum cost" for a threshold-like activation implemented from an optical signal.

### Setup
- Let the scalar pre-activation input be encoded into a coherent state `|alpha(x)>`.
- Consider the critical threshold pair `x_- = x_th - delta` and `x_+ = x_th + delta`.
- Any activation that outputs different branches for these two inputs must, explicitly or implicitly, distinguish the optical states `|alpha_->` and `|alpha_+>`, where `alpha_± = alpha(x_±)`.
- Assume equal prior probability for the two boundary cases and define the allowed decision error as `epsilon < 1/2`.

### Derivation
1. For coherent states, the state overlap satisfies
   `|<alpha_-|alpha_+>|^2 = exp(-|Delta alpha|^2)`,
   where `Delta alpha = alpha_+ - alpha_-`.
2. The minimum achievable binary decision error for two pure states with equal priors is the Helstrom bound
   `P_e^min = 1/2 * (1 - sqrt(1 - exp(-|Delta alpha|^2)))`.
3. Requiring `P_e^min <= epsilon` gives
   `sqrt(1 - exp(-|Delta alpha|^2)) >= 1 - 2 epsilon`.
4. Squaring both sides yields
   `exp(-|Delta alpha|^2) <= 1 - (1 - 2 epsilon)^2 = 4 epsilon (1 - epsilon)`.
5. Therefore the minimum boundary-state separation needed for an error-controlled activation decision is
   `|Delta alpha|^2 >= ln(1 / (4 epsilon (1 - epsilon)))`.

### Consequence for activation cost
- For a symmetric boundary pair centered to minimize average optical energy in the decision mode, the mean photon number across the pair is
  `n_bar = (|alpha_-|^2 + |alpha_+|^2) / 2 >= |Delta alpha|^2 / 4`.
- Combining with the inequality above gives the lower bound
  `n_bar >= (1/4) ln(1 / (4 epsilon (1 - epsilon)))`.
- This is a real lower bound, not a performance claim for AQMA.
- It shows that any threshold-like activation requiring binary separation at error `epsilon` must pay a nonzero discrimination-energy cost even before hardware inefficiency, dark counts, loss, or feedback overhead are added.

### Interpretation
- The result turns one part of "activation quantum cost" into an operational discrimination problem.
- It supports a clean statement for the paper: sharp activation is limited not only by nonlinear material response, but also by the information-theoretic cost of deciding which side of the activation boundary the optical signal occupies.
- The bound is architecture-agnostic at this level. It does not yet prove AQMA superiority, but it does give a referee-checkable floor that later benchmarks can compare against.

### Validity conditions
- Coherent-state input model for the boundary states
- Equal-prior binary boundary decision
- Threshold-like local activation behavior
- No claim yet about global network optimality, multi-class decisions, or full task accuracy

## What is genuinely completed
- One explicit derivation now exists for a lower bound on boundary discrimination cost.
- The project now has a mathematically checkable quantity that can appear in the theory section or Methods.
- The previous supervision demand to avoid rhetorical "quantum limit" language has been partially addressed for one local activation decision primitive.
- One real computation has been run from that derivation.
- The project now has verified numerical values for a first boundary-cost curve and a first gain-versus-margin map.
- A figure candidate can now be defined around exact computed values rather than around a symbolic expression alone.

## What is still incomplete
- No full unified activation framework yet across Kerr, saturable, electronic, homodyne, photon-counting, and AQMA routes
- No comparison to a concrete AQMA or other measurement-induced activation model has yet been derived or computed
- No finalized figure panel has yet been drawn from the computed tables
- No manuscript PDF or supplementary PDF exists
- No verified literature-positioning text has yet been rewritten around this derivation

## Current acceptance estimate
- The project is still far below submission readiness, but the evidence base is now stronger than in the derivation-only state.
- Working Nature Photonics stage estimate after this run: 19-28%.
- Reason: the project now has both an explicit lower bound and real numeric consequences, but it still lacks architecture comparison, device relevance, manuscript integration, and literature separation.

## Latest update
- 2026-04-25: completed the first manuscript-usable derivation for activation quantum cost by reducing threshold activation to a coherent-state discrimination bound and established the lower bound `n_bar >= (1/4) ln(1 / (4 epsilon (1 - epsilon)))` under the stated assumptions.
- 2026-04-25: ran the first numerical scan from that bound and verified that the lower-bound mean boundary photon cost rises from `0.010205` at `epsilon = 0.40` to `0.807232` at `epsilon = 0.01`; under the local encoding model `alpha(x)=g(x-x_th)`, the required minimum gain at `delta = 0.10` rises from `1.010223` to `8.984607` over the same error range.

## Next immediate action
- Define one explicit AQMA-inspired measurement model with stated assumptions and compute where its effective boundary error and photon usage sit relative to the new lower-bound curves.
