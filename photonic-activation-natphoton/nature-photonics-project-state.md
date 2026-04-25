# Nature Photonics Project State

## Current stage
- Theoretical strengthening

## Current total goal
- Build a Nature Photonics-competitive theory-and-simulation paper on quantum limits of nonlinear activation in photonic neural networks, with a quantitative resource framework, realistic measurement-induced activation route, and figure-ready evidence.

## Core bottleneck
- The project still lacks a sufficiently complete mathematical framework plus validated numerics that would let a referee see a decisive, decision-relevant result rather than a well-written concept.

## Highest-priority action completed in this run
- Completed one manuscript-usable derivation: a lower bound linking threshold-like activation to binary coherent-state discrimination cost.

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

## What is still incomplete
- No full unified activation framework yet across Kerr, saturable, electronic, homodyne, photon-counting, and AQMA routes
- No numerical benchmark has yet been run from this bound
- No figure-ready parameter scan has yet been produced
- No manuscript PDF or supplementary PDF exists
- No verified literature-positioning text has yet been rewritten around this derivation

## Current acceptance estimate
- Not enough new evidence exists for a major probability upgrade.
- Working Nature Photonics stage estimate after this run: 15-23%.
- Reason: theory rigor improved slightly, but novelty separation, numerics, figure package, and manuscript completeness remain below submission bar.

## Latest update
- 2026-04-25: completed the first manuscript-usable derivation for activation quantum cost by reducing threshold activation to a coherent-state discrimination bound and established the lower bound `n_bar >= (1/4) ln(1 / (4 epsilon (1 - epsilon)))` under the stated assumptions.

## Next immediate action
- Extend this local bound into a figure-producing computation: choose one encoded activation family and numerically map required boundary photon cost versus target decision error `epsilon` and boundary margin `delta`, then compare that curve to one AQMA-inspired measurement model.
