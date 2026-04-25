# Project State

## Project
- Working title: Quantum limits of nonlinear activation in photonic neural networks
- Target journal: Nature Photonics
- Source note: initialized from `/workspace/user_files/01-1-.txt` on 2026-04-25

## Research goal
Build a publishable theory-and-simulation paper that turns the vague claim "photonic neural networks need nonlinearity" into a journal-grade result: a quantitative resource framework for nonlinear activation under quantum noise, finite shots, detector inefficiency and loss, together with a near-limit measurement-induced activation architecture and a device-level design map.

## Current stage
Result-generation stage. The project has now moved beyond pure formalization into first comparison generation: one proved lower bound and one concrete measurement-induced route have been placed on the same boundary-discrimination axes.

## Current main bottleneck
The project still has only one explicit architecture trace on those axes. The leading blocker is now the absence of a multi-route same-axis comparison and figure-ready panel that would let a Nature Photonics referee judge whether the result is a real photonic design law rather than a single illustrative example.

## Highest-priority objective for the current round
Turn the proved lower bound into a device-relevant comparison by computing where a concrete homodyne-conditioned AQMA proxy sits relative to that bound under finite detector efficiency.

## Proposed central claim
The real scalability bottleneck of photonic neural networks is not linear optics but the physical cost of nonlinear activation; this cost can be cast as a quantum resource problem, and measurement-induced adaptive activation can approach the low-energy Pareto frontier only inside explicitly quantified detector-, loss-, and sampling-limited regimes.

## Mandatory evidence package
- Formal definition of activation quantum cost, discrimination cost, and task-level energy-accuracy cost
- Unified activation model covering electronic, Kerr-like, saturable, photon-counting, homodyne, and AQMA-style measurement-feedback activation
- Single-neuron approximation benchmark for at least five target activation families
- Small-network task benchmark showing when measurement-induced nonlinearity is useful and when it is not
- Robustness scans over detector efficiency, dark count, optical loss, and finite-shot sampling
- Clear separation from closely related literature in Nature Photonics, Nature Communications, and adjacent photonic-AI work

## What is already strong
- The question is pitched at a field level rather than as one more classifier demo
- The project now has one explicit lower bound for boundary discrimination cost
- The project now also has one concrete same-axis comparison for a measurement-induced activation route
- The target venue is scope-compatible with nonlinear optics, quantum optics, optoelectronic components, and photonic AI
- The paper can be framed as design rules plus limits, which fits a theory-heavy route better than a hardware-claim route

## This run's concrete result
### Goal
- Compute the first concrete measurement-induced activation curve on the same axes as the proved coherent-state discrimination lower bound.

### Architecture fixed in this run
- Use the homodyne-conditioned AQMA proxy already named in the theory framework.
- Boundary states are the coherent pair `|+a>` and `|-a>` with symmetric mean photon number `n_bar = a^2`.
- Single-shot homodyne is performed along the signal quadrature with detector efficiency `eta`.
- Boundary decision uses a zero-threshold rule on the homodyne outcome.

### Quantities computed
1. Lower-bound decision error:
   `epsilon_lb(n_bar) = 1/2 * (1 - sqrt(1 - exp(-4 n_bar)))`.
2. Lower-bound inverse cost:
   `n_bar^lb(epsilon) = (1/4) ln(1 / (4 epsilon (1 - epsilon)))`.
3. Homodyne proxy decision error:
   `epsilon_hom(n_bar, eta) = 1/2 * erfc(sqrt(2 eta n_bar))`.
4. Minimum homodyne photon cost `n_bar^hom(epsilon, eta)` obtained by direct numerical inversion for target error `epsilon`.

### Verified numerical outputs
- At target error `epsilon = 0.10`:
  `n_bar^lb = 0.255413`,
  `n_bar^hom = 0.414741` at `eta = 0.99`,
  `0.483051` at `eta = 0.85`,
  `0.586562` at `eta = 0.70`,
  `0.821187` at `eta = 0.50`.
- At target error `epsilon = 0.01`:
  `n_bar^lb = 0.807232`,
  `n_bar^hom = 1.366640` at `eta = 0.99`,
  `1.591734` at `eta = 0.85`,
  `1.932819` at `eta = 0.70`,
  `2.705947` at `eta = 0.50`.
- The ratio `n_bar^hom / n_bar^lb` is:
  `1.624-1.693` for `eta = 0.99`,
  `1.891-1.972` for `eta = 0.85`,
  `2.297-2.394` for `eta = 0.70`,
  and `3.215-3.352` for `eta = 0.50`
  over the target-error range `epsilon = 0.10-0.01`.
- At fixed photon budget `n_bar = 0.25`, the lower bound gives `epsilon_lb = 0.102470`, while the homodyne proxy gives:
  `0.159871` at `eta = 0.99`,
  `0.178276` at `eta = 0.85`,
  `0.201392` at `eta = 0.70`,
  `0.239750` at `eta = 0.50`.

### Design-relevant interpretation
- The project now has a real, same-axis comparison between a lower bound and a concrete measurement-induced route.
- Near-unity-efficiency homodyne remains within about a `1.6-1.7x` photon overhead above the coherent-state lower bound in the practically interesting low-error regime.
- Detector inefficiency rapidly widens that gap, which produces the first device-facing message of the paper:
  measurement-induced activation can stay near the frontier only when detector efficiency is very high.
- This is not yet a superiority claim, but it is already more journal-relevant than a bare lower-bound curve.

## What is still missing
- A sharp novelty statement against 2024-2025 photonic nonlinearity papers
- A second concrete activation baseline on the same axes as the lower bound and homodyne proxy
- A submission-grade figure panel and caption package
- A verified reference ledger separating confirmed citations from placeholders
- Task-level evidence showing whether the single-neuron frontier matters for network utility

## Acceptance probability (stage estimate)
- Nature Photonics: 24-34% after the first same-axis architecture comparison
- Reason: the project now has a lower bound plus one concrete accessible-route comparison, which materially improves theory-to-device relevance; however, the evidence package still lacks a second baseline, figure-grade assembly, manuscript integration, and verified literature separation.

## Last update
2026-04-25: computed the first concrete homodyne-conditioned AQMA proxy on the same axes as the coherent-state discrimination lower bound. Verified that near-unity detector efficiency keeps the route within about `1.6-1.7x` of the lower-bound photon cost across `epsilon = 0.10-0.01`, while `eta = 0.50` widens the penalty to about `3.2-3.35x`. The main bottleneck has therefore shifted from "no architecture comparison" to "no multi-route figure-ready comparison."
