# Project State

## Project
- Working title: Quantum limits of nonlinear activation in photonic neural networks
- Target journal: Nature Photonics
- Source note: initialized from `/workspace/user_files/01-1-.txt` on 2026-04-25

## Research goal
Build a publishable theory-and-simulation paper that turns the vague claim "photonic neural networks need nonlinearity" into a journal-grade result: a quantitative resource framework for nonlinear activation under quantum noise, finite shots, detector inefficiency and loss, together with a near-limit measurement-induced activation architecture and a device-level design map.

## Current stage
Result-generation and figure-consolidation stage. The project now has a three-curve same-axis comparison set: one proved lower bound, one homodyne-conditioned measurement route, and one displaced on-off counting route.

## Current main bottleneck
The leading blocker is no longer the lack of a second architecture. The main bottleneck is now the absence of a submission-grade Figure-3 package and integrated Results text that convert the new three-curve comparison into an unmistakable design law for Nature Photonics readers.

## Highest-priority objective for the current round
Turn the completed lower-bound plus homodyne plus displaced-counting comparison into a figure-ready main-text panel with caption logic, claim boundaries, and manuscript-ready Results prose.

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
- The project now has a second concrete same-axis baseline using a displaced on-off counting route
- The target venue is scope-compatible with nonlinear optics, quantum optics, optoelectronic components, and photonic AI
- The paper can be framed as design rules plus limits, which fits a theory-heavy route better than a hardware-claim route

## This run's concrete result
### Goal
- Add a second concrete architecture on the same discrimination-cost axes so the paper no longer rests on a single illustrative route.

### Architecture fixed in this run
- Use a Kennedy-type displaced on-off route as the second same-axis baseline.
- Boundary states are the coherent pair `|+a>` and `|-a>` with symmetric mean photon number `n_bar = a^2`.
- Apply a fixed displacement that nulls the `|+a>` hypothesis, producing post-displacement states `|0>` and `|-2a>`.
- Detection uses an on-off detector with efficiency `eta` and dark-count probability `p_d`.
- Decision rule is `no click -> |+a>`, `click -> |-a>`.

### Quantities computed
1. Lower-bound decision error:
   `epsilon_lb(n_bar) = 1/2 * (1 - sqrt(1 - exp(-4 n_bar)))`.
2. Lower-bound inverse cost:
   `n_bar^lb(epsilon) = (1/4) ln(1 / (4 epsilon (1 - epsilon)))`.
3. Kennedy/on-off error:
   `epsilon_ken(n_bar, eta, p_d) = 1/2 * [p_d + (1 - p_d) exp(-4 eta n_bar)]`.
4. In the no-dark-count limit:
   `n_bar^ken(epsilon, eta) = [ln(1 / (2 epsilon))] / (4 eta)`.
5. With dark counts:
   `n_bar^ken(epsilon, eta, p_d) = [ln((1 - p_d) / (2 epsilon - p_d))] / (4 eta)`,
   valid only when `2 epsilon > p_d`.

### Verified numerical outputs
- At target error `epsilon = 0.10`:
  `n_bar^lb = 0.255413`,
  `n_bar^ken = 0.406424` at `eta = 0.99`,
  `0.473364` at `eta = 0.85`,
  `0.574799` at `eta = 0.70`,
  `0.804719` at `eta = 0.50`.
- At target error `epsilon = 0.01`:
  `n_bar^lb = 0.807232`,
  `n_bar^ken = 0.987885` at `eta = 0.99`,
  `1.150595` at `eta = 0.85`,
  `1.397151` at `eta = 0.70`,
  `1.956012` at `eta = 0.50`.
- The ratio `n_bar^ken / n_bar^lb` is:
  `1.224-1.591` for `eta = 0.99`,
  `1.425-1.853` for `eta = 0.85`,
  `1.731-2.250` for `eta = 0.70`,
  and `2.423-3.151` for `eta = 0.50`
  over the target-error range `epsilon = 0.01-0.10`.
- Relative to the homodyne proxy, the ratio `n_bar^hom / n_bar^ken` is:
  `1.020-1.383` across the same error range, independent of `eta` in the idealized no-dark-count model because both routes scale as `1 / eta`.
- At fixed photon budget `n_bar = 0.25`, the lower bound gives `epsilon_lb = 0.102470`, while the displaced on-off route gives:
  `0.185788` at `eta = 0.99`,
  `0.213707` at `eta = 0.85`,
  `0.248293` at `eta = 0.70`,
  `0.303265` at `eta = 0.50`.
- Dark-count sensitivity check:
  the route cannot reach `epsilon <= p_d / 2`; for `p_d = 1e-4` and `1e-3`, the cost shift is still modest in the current `epsilon = 0.10-0.01` window but becomes a hard floor below that range.

### Design-relevant interpretation
- The project now has three real same-axis curves: a lower bound plus two physically distinct measurement-induced routes.
- Detector inefficiency remains the dominant global penalty because both measurement routes scale as `1 / eta`.
- Measurement architecture still matters strongly at fixed `eta`: displaced on-off counting is noticeably closer to the lower bound than homodyne at low target error.
- This sharpens the paper's design message from a single-route observation into a comparative law:
  detector quality sets the global accessibility of the frontier, while measurement choice sets the constant-factor overhead above it.

## What is still missing
- A sharp novelty statement against 2024-2025 photonic nonlinearity papers
- A submission-grade figure panel and caption package built from the three-curve same-axis comparison
- A verified reference ledger separating confirmed citations from placeholders
- A main-text Results subsection that states the new comparison sharply but without overclaiming
- Task-level evidence showing whether the single-neuron frontier matters for network utility

## Acceptance probability (stage estimate)
- Nature Photonics: 31-41% after adding the second same-axis architecture baseline
- Reason: the project now has a lower bound plus two concrete measurement routes and can articulate a stronger design law. The ceiling remains limited by the absence of a figure-ready panel, manuscript-integrated Results text, verified literature separation, and task-level evidence.

## Last update
2026-04-25: added a Kennedy-type displaced on-off baseline on the same axes as the lower bound and homodyne route, and saved a reproducible calculation script in `/workspace/memory/photonic-activation-natphoton/same_axis_metrics.py`. Verified that the displaced on-off route sits closer to the lower bound than homodyne in the low-error regime, while both measurement routes inherit a strong `1 / eta` penalty from detector inefficiency. The main bottleneck has therefore shifted from "missing second architecture" to "missing Figure-3-grade assembly and manuscript integration."
