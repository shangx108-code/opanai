# XOR Geometry Extension Summary

## Purpose
- Add one intermediate-complexity nonlinear classification task under the same activation-photon accounting as the saved trainable benchmark.
- Test whether the current design rule remains selective beyond the existing positive (`concentric_circles`) and fragile (`two_moons`) pair.

## Task definition
- Task: noisy XOR quadrants in two dimensions.
- Input-noise scale: 0.18
- Repeats: 3
- Positive-margin threshold: margin versus the trainable linear baseline > 0.02

## Headline findings
- Physical activation beats the trainable linear baseline in 14.0 of 15 scanned `(eta, budget)` settings on average across repeats.
- On-off beats homodyne in 8.7 of 15 matched `(eta, budget)` settings on average across repeats.
- 12 of 15 scanned settings stay above the +0.02 margin threshold in all 3 repeats.

## Per-repeat counts
| repeat | activation beats linear | not yet worth paying for | on_off beats homodyne |
| ---: | ---: | ---: | ---: |
| 0 | 15 | 0 | 9 |
| 1 | 15 | 0 | 9 |
| 2 | 12 | 3 | 8 |

## Robustly positive conditions
| eta | budget | mean best test acc | mean linear acc | mean margin | route wins on_off/homodyne |
| ---: | ---: | ---: | ---: | ---: | --- |
| 0.50 | 4.0 | 0.743 | 0.579 | 0.164 | 3/0 |
| 0.50 | 8.0 | 0.802 | 0.579 | 0.224 | 3/0 |
| 0.50 | 16.0 | 0.818 | 0.579 | 0.239 | 2/1 |
| 0.70 | 2.0 | 0.706 | 0.579 | 0.128 | 0/3 |
| 0.70 | 4.0 | 0.775 | 0.579 | 0.197 | 1/2 |
| 0.70 | 8.0 | 0.820 | 0.579 | 0.241 | 3/0 |
| 0.70 | 16.0 | 0.806 | 0.579 | 0.227 | 2/1 |
| 0.99 | 1.0 | 0.665 | 0.579 | 0.086 | 1/2 |
| 0.99 | 2.0 | 0.740 | 0.579 | 0.162 | 3/0 |
| 0.99 | 4.0 | 0.786 | 0.579 | 0.207 | 3/0 |
| 0.99 | 8.0 | 0.804 | 0.579 | 0.225 | 2/1 |
| 0.99 | 16.0 | 0.806 | 0.579 | 0.227 | 1/2 |

## Interpretation bounds
- This extension strengthens geometry breadth by one task only; it does not convert the paper into a general benchmark survey.
- The XOR result should therefore be used to support a bounded three-regime narrative: weak-linear-baseline tasks can be strongly positive, strong-linear-baseline tasks can remain fragile, and an intermediate nonlinear task can still remain robustly activation-positive under the same photon accounting.
