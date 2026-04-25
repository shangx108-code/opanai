# AQMA Homodyne Comparison

## Purpose
- Put one concrete measurement-induced activation route on the same axes as the proved coherent-state discrimination lower bound.

## Model fixed in this run
- Boundary states are the coherent pair `|+a>` and `|-a>` with real amplitude `a`.
- The symmetric boundary-pair mean photon number is `n_bar = a^2`.
- The architecture proxy is the homodyne-conditioned AQMA variant already named in the theory framework.
- Measurement is single-shot homodyne along the signal quadrature with detector efficiency `eta`.
- Boundary decision uses the zero-threshold rule on the homodyne outcome.

## Analytic comparison quantities
- Lower bound:
  `epsilon_lb(n_bar) = 1/2 * (1 - sqrt(1 - exp(-4 n_bar)))`.
- Lower-bound inverse:
  `n_bar^lb(epsilon) = (1/4) ln(1 / (4 epsilon (1 - epsilon)))`.
- Homodyne proxy:
  `epsilon_hom(n_bar, eta) = 1/2 * erfc(sqrt(2 eta n_bar))`.
- The minimum homodyne photon cost `n_bar^hom(epsilon, eta)` was obtained by direct numerical inversion of the monotonic error curve.

## Verified numerical results

### Required photon number to reach target boundary error
| `epsilon` | `n_bar^lb` | `n_bar^hom(eta=0.99)` | ratio | `n_bar^hom(eta=0.85)` | ratio | `n_bar^hom(eta=0.70)` | ratio | `n_bar^hom(eta=0.50)` | ratio |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.10 | 0.255413 | 0.414741 | 1.624 | 0.483051 | 1.891 | 0.586562 | 2.297 | 0.821187 | 3.215 |
| 0.05 | 0.415183 | 0.683218 | 1.646 | 0.795748 | 1.917 | 0.966266 | 2.327 | 1.352772 | 3.258 |
| 0.02 | 0.636483 | 1.065122 | 1.673 | 1.240554 | 1.949 | 1.506387 | 2.367 | 2.108942 | 3.313 |
| 0.01 | 0.807232 | 1.366640 | 1.693 | 1.591734 | 1.972 | 1.932819 | 2.394 | 2.705947 | 3.352 |

### Direct comparison at a fixed photon budget
- At `n_bar = 0.25`, the coherent-state lower bound gives `epsilon_lb = 0.102470`.
- At the same photon budget, the homodyne proxy gives:
  - `eta = 0.99 -> epsilon_hom = 0.159871`
  - `eta = 0.95 -> epsilon_hom = 0.164860`
  - `eta = 0.85 -> epsilon_hom = 0.178276`
  - `eta = 0.70 -> epsilon_hom = 0.201392`
  - `eta = 0.50 -> epsilon_hom = 0.239750`

## What this run establishes
- A concrete measurement-induced activation route can be placed on the same boundary-cost axes as the proved lower bound.
- Near-unity-efficiency homodyne does not saturate the bound, but it stays within about a `1.6-1.7x` photon overhead over the `epsilon = 0.10-0.01` range.
- Detector inefficiency quickly widens the gap: at `eta = 0.50`, the same target boundary error requires about `3.2-3.35x` the lower-bound photon cost.
- This creates a design-relevant statement for the paper:
  the lower bound is not merely formal, but the accessible region for a realistic measurement-induced route narrows rapidly with detector loss.

## What this run does not establish
- No claim yet that the homodyne proxy is globally optimal among all AQMA architectures.
- No claim yet about task-level classification accuracy or full-network advantage.
- No claim yet about direct-counting AQMA, Kerr, saturable, or electronic baselines on the same axes.

## Immediate use in the manuscript
- This note can support a Figure-3-style panel:
  lower bound plus homodyne-accessible curves for several detector efficiencies.
- The most defensible main-text claim is regime-based:
  measurement-induced activation can stay near the discrimination-energy frontier only when detector efficiency is very high; otherwise the resource penalty grows quickly.
