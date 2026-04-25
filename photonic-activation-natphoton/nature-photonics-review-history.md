# Nature Photonics Review History

## 2026-04-25 | Pre-manuscript triage baseline

### Reviewer-style verdict
- Major revision before a full draft exists

### Baseline reviewer estimates
- Reviewer 1 (novelty-focused): 18%
- Reviewer 2 (theory-rigor-focused): 16%
- Reviewer 3 (device/implementation-focused): 14%
- Reviewer 4 (broad-reader clarity-focused): 22%
- Reviewer 5 (benchmark/comparison-focused): 15%

## 2026-04-25 | Post-derivation micro-update

### New evidence reviewed
- One explicit derivation reducing threshold-like activation to a coherent-state binary discrimination problem and proving
  `n_bar >= (1/4) ln(1 / (4 epsilon (1 - epsilon)))`
  for the mean boundary-state photon cost under the stated assumptions.

### Review impact
- This is genuine progress on theory rigor.
- It does not yet materially solve the novelty, benchmark, or device-relevance objections.

### Updated reviewer interpretation
- Reviewer 1 (novelty-focused): stays effectively unchanged. A bound alone does not yet show field-changing consequence.
- Reviewer 2 (theory-rigor-focused): improves modestly because one central quantity is now explicitly defined and derived.
- Reviewer 3 (device/implementation-focused): unchanged until hardware-parameter mapping exists.
- Reviewer 4 (broad-reader clarity-focused): slight improvement because the activation-cost narrative is now more concrete.
- Reviewer 5 (benchmark/comparison-focused): unchanged until real comparison curves exist.

### Working reviewer estimates after this run
- Reviewer 1: 18-20%
- Reviewer 2: 20-24%
- Reviewer 3: 14-16%
- Reviewer 4: 22-25%
- Reviewer 5: 15-17%

### Current conclusion
- All five reviewer acceptance estimates remain far below 70%.
- The project must continue iterative advancement.

### Immediate upgrade condition
- Produce at least one real numerical regime map from the new bound and use it to state where measurement-induced activation could plausibly approach the boundary and where it cannot.

## 2026-04-25 | Post-scan micro-update

### New evidence reviewed
- A real numerical scan was run from the proved lower bound
  `n_bar >= (1/4) ln(1 / (4 epsilon (1 - epsilon)))`.
- Verified points include
  `n_bar^min = 0.255413` at `epsilon = 0.10`,
  `0.415183` at `epsilon = 0.05`,
  and `0.807232` at `epsilon = 0.01`.
- Under the local encoding model `alpha(x)=g(x-x_th)`, the minimum gain required at `delta = 0.10` rises to
  `g_min = 5.053838, 6.443468, 7.977987, 8.984607`
  for `epsilon = 0.10, 0.05, 0.02, 0.01`, respectively.

### Review impact
- Reviewer 2 and Reviewer 5 should move modestly upward because the project now has a true theory-to-numerics link.
- Reviewer 3 remains skeptical because no architecture comparison or hardware mapping exists yet.
- Reviewer 1 still lacks a reason to view the work as field-shifting rather than analytically tidy.

### Working reviewer estimates after this run
- Reviewer 1: 19-21%
- Reviewer 2: 24-29%
- Reviewer 3: 15-18%
- Reviewer 4: 24-28%
- Reviewer 5: 20-25%

### Current conclusion
- All five reviewer acceptance estimates remain far below 70%.
- The project must continue iterative advancement.

### Immediate upgrade condition
- Put one explicit measurement-induced activation model on the same axes as the lower-bound curve and show whether it approaches, misses, or crosses into an excluded regime.

## 2026-04-25 | Post-homodyne-comparison micro-update

### New evidence reviewed
- One explicit homodyne-conditioned AQMA proxy was computed on the same axes as the coherent-state discrimination lower bound.
- Verified same-axis results include:
  at `epsilon = 0.10`, `n_bar^lb = 0.255413` while `n_bar^hom = 0.414741` at `eta = 0.99` and `0.821187` at `eta = 0.50`;
  at `epsilon = 0.01`, `n_bar^lb = 0.807232` while `n_bar^hom = 1.366640` at `eta = 0.99` and `2.705947` at `eta = 0.50`.
- The homodyne-to-bound photon-cost ratio stays near `1.6-1.7x` for `eta = 0.99` but grows to about `3.2-3.35x` for `eta = 0.50` over `epsilon = 0.10-0.01`.

### Review impact
- Reviewer 2 and Reviewer 5 should rise meaningfully because the project now has a genuine lower-bound-versus-architecture comparison.
- Reviewer 3 should also rise because detector efficiency now enters as an explicit device-facing control axis.
- Reviewer 1 still remains cautious because one worked route is not yet a full novelty-separating comparison set.

### Five-reviewer dimension estimates
- Reviewer 1:
  innovation/significance `34/100`; theory rigor `45/100`; method reliability `42/100`; data/results `37/100`; figure quality `20/100`; writing `28/100`; journal fit `44/100`; acceptance estimate `26%`.
- Reviewer 2:
  innovation/significance `36/100`; theory rigor `58/100`; method reliability `49/100`; data/results `40/100`; figure quality `20/100`; writing `30/100`; journal fit `45/100`; acceptance estimate `34%`.
- Reviewer 3:
  innovation/significance `33/100`; theory rigor `46/100`; method reliability `47/100`; data/results `39/100`; figure quality `20/100`; writing `27/100`; journal fit `43/100`; acceptance estimate `27%`.
- Reviewer 4:
  innovation/significance `35/100`; theory rigor `46/100`; method reliability `43/100`; data/results `41/100`; figure quality `22/100`; writing `33/100`; journal fit `47/100`; acceptance estimate `30%`.
- Reviewer 5:
  innovation/significance `35/100`; theory rigor `50/100`; method reliability `48/100`; data/results `45/100`; figure quality `21/100`; writing `29/100`; journal fit `45/100`; acceptance estimate `33%`.

### Current conclusion
- All five reviewer acceptance estimates remain far below 70%.
- The project must continue iterative advancement.

### Immediate upgrade condition
- Add either a second activation route on the same axes or a figure-grade accessible-region panel strong enough to make the new comparison feel definitive rather than illustrative.
