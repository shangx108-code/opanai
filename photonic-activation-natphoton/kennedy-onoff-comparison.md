# Displaced On-Off Comparison

## Purpose
- Add a second concrete architecture on the same boundary-discrimination axes as the coherent-state lower bound and the homodyne-conditioned AQMA proxy.
- Use a physically distinct and experimentally familiar route: a Kennedy-type displaced on-off receiver.

## Model fixed in this run
- Boundary states are the coherent pair `|+a>` and `|-a>` with symmetric mean photon number `n_bar = a^2`.
- Apply a fixed displacement that nulls the `|+a>` hypothesis so the two post-displacement states are `|0>` and `|-2a>`.
- Use an on-off detector with efficiency `eta` and dark-count probability `p_d` per activation event.
- Decision rule: `no click -> |+a>`, `click -> |-a>`.

## Analytic comparison quantities
- Lower bound:
  `epsilon_lb(n_bar) = 1/2 * (1 - sqrt(1 - exp(-4 n_bar)))`.
- Kennedy/on-off error:
  `epsilon_ken(n_bar, eta, p_d) = 1/2 * [p_d + (1 - p_d) exp(-4 eta n_bar)]`.
- In the no-dark-count limit:
  `epsilon_ken(n_bar, eta, 0) = 1/2 * exp(-4 eta n_bar)`.
- The inverse photon cost for the no-dark-count model is closed form:
  `n_bar^ken(epsilon, eta) = [ln(1 / (2 epsilon))] / (4 eta)`.
- With dark counts:
  `n_bar^ken(epsilon, eta, p_d) = [ln((1 - p_d) / (2 epsilon - p_d))] / (4 eta)`,
  valid only when `2 epsilon > p_d`.

## Verified numerical results for `p_d = 0`

### Required photon number to reach target boundary error
| `epsilon` | `n_bar^lb` | `n_bar^ken(eta=0.99)` | ratio | `n_bar^ken(eta=0.85)` | ratio | `n_bar^ken(eta=0.70)` | ratio | `n_bar^ken(eta=0.50)` | ratio |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.10 | 0.255413 | 0.406424 | 1.591 | 0.473364 | 1.853 | 0.574799 | 2.250 | 0.804719 | 3.151 |
| 0.05 | 0.415183 | 0.581461 | 1.400 | 0.677231 | 1.631 | 0.822352 | 1.981 | 1.151293 | 2.773 |
| 0.02 | 0.636483 | 0.812847 | 1.277 | 0.946728 | 1.487 | 1.149599 | 1.806 | 1.609438 | 2.529 |
| 0.01 | 0.807232 | 0.987885 | 1.224 | 1.150595 | 1.425 | 1.397151 | 1.731 | 1.956012 | 2.423 |

### Comparison against the homodyne proxy
- Over the same `epsilon = 0.10-0.01` range, the ratio `n_bar^hom / n_bar^ken` is:
  - `1.020-1.383` for `eta = 0.99`
  - `1.020-1.383` for `eta = 0.85`
  - `1.020-1.383` for `eta = 0.70`
  - `1.020-1.383` for `eta = 0.50`
- Interpretation: both measurement routes degrade as `1/eta`, but the Kennedy/on-off route becomes increasingly closer to the lower bound at lower target error, while homodyne keeps a larger asymptotic penalty.

### Direct comparison at a fixed photon budget
- At `n_bar = 0.25`, the coherent-state lower bound gives `epsilon_lb = 0.102470`.
- At the same photon budget, the Kennedy/on-off baseline gives:
  - `eta = 0.99 -> epsilon_ken = 0.185788`
  - `eta = 0.95 -> epsilon_ken = 0.193371`
  - `eta = 0.85 -> epsilon_ken = 0.213707`
  - `eta = 0.70 -> epsilon_ken = 0.248293`
  - `eta = 0.50 -> epsilon_ken = 0.303265`
- For reference, the homodyne proxy at the same `n_bar` gives:
  - `eta = 0.99 -> epsilon_hom = 0.159871`
  - `eta = 0.95 -> epsilon_hom = 0.164860`
  - `eta = 0.85 -> epsilon_hom = 0.178276`
  - `eta = 0.70 -> epsilon_hom = 0.201392`
  - `eta = 0.50 -> epsilon_hom = 0.239750`

## Dark-count sensitivity
- Dark counts introduce a hard floor: this model cannot reach target error `epsilon <= p_d / 2`.
- For `p_d = 1e-4`, the required `n_bar^ken` shifts only slightly in the `epsilon = 0.10-0.01` range.
- For `p_d = 1e-3`, the shift remains modest at `epsilon >= 0.01`, but this parameter will matter more strongly if the paper pushes into `epsilon << 10^-2`.

## What this run establishes
- The project now has a second concrete same-axis activation route beside the lower bound and homodyne proxy.
- A displaced on-off route is generally closer to the lower bound than homodyne in the low-error regime, especially as `epsilon` approaches `0.01`.
- The second baseline sharpens the design message: detector inefficiency hurts both routes similarly through `1/eta`, but measurement choice still changes the prefactor substantially.
- The comparison is now broad enough to support a more decisive Figure-3 panel: lower bound, homodyne family, and displaced on-off family.

## What this run does not establish
- No claim yet that the displaced on-off receiver is globally optimal over all displacement or adaptive-receiver designs.
- No claim yet that this single-neuron comparison directly predicts full-network task accuracy.
- No direct Kerr, saturable, or electronic baseline has been placed on the same axes yet.

## Immediate use in the manuscript
- Result 3 can now compare two distinct measurement-induced routes against the lower bound without pretending either route is globally optimal.
- The strongest defensible text is now:
  for realistic measurement-induced activations, detector efficiency controls the global energy penalty, while the choice of measurement architecture sets an additional constant-factor overhead above the quantum limit.
