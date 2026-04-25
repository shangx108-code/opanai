# Trainable Task Benchmark Seed Robustness Summary

## Purpose
- Test whether the trainable-benchmark systems claim remains stable across independently reseeded data splits and training initializations.
- Repeats run: 3
- Positive-margin threshold: margin versus trainable linear baseline > 0.02

## Headline findings
- Activation beats the trainable linear baseline in 22.0 of 30 scanned conditions on average across repeats, with a range of 22 to 22.
- On-off beats homodyne in 14.7 of 30 matched task/eta/budget comparisons on average across repeats.
- 21 of 30 scanned conditions stay above the +0.02 margin threshold in all 3 repeats.
- 9 of 30 scanned conditions change sign or fall below the +0.02 threshold in at least one repeat.

## Per-repeat counts
| repeat | activation beats linear | not yet worth paying for | on_off beats homodyne |
| ---: | ---: | ---: | ---: |
| 0 | 22 | 8 | 20 |
| 1 | 22 | 8 | 13 |
| 2 | 22 | 8 | 11 |

## Conditions robustly above the positive-margin threshold in every repeat
- concentric_circles, eta=0.50, budget=1.0: mean margin 0.093 +/- 0.042, route wins on_off/homodyne = 0/3.
- concentric_circles, eta=0.50, budget=2.0: mean margin 0.148 +/- 0.039, route wins on_off/homodyne = 0/3.
- concentric_circles, eta=0.50, budget=4.0: mean margin 0.286 +/- 0.027, route wins on_off/homodyne = 2/1.
- concentric_circles, eta=0.50, budget=8.0: mean margin 0.386 +/- 0.053, route wins on_off/homodyne = 1/2.
- concentric_circles, eta=0.50, budget=16.0: mean margin 0.422 +/- 0.050, route wins on_off/homodyne = 1/2.
- concentric_circles, eta=0.70, budget=1.0: mean margin 0.103 +/- 0.043, route wins on_off/homodyne = 0/3.
- concentric_circles, eta=0.70, budget=2.0: mean margin 0.179 +/- 0.039, route wins on_off/homodyne = 1/2.
- concentric_circles, eta=0.70, budget=4.0: mean margin 0.359 +/- 0.043, route wins on_off/homodyne = 2/1.
- concentric_circles, eta=0.70, budget=8.0: mean margin 0.427 +/- 0.062, route wins on_off/homodyne = 2/1.
- concentric_circles, eta=0.70, budget=16.0: mean margin 0.409 +/- 0.042, route wins on_off/homodyne = 2/1.
- concentric_circles, eta=0.99, budget=1.0: mean margin 0.140 +/- 0.033, route wins on_off/homodyne = 1/2.
- concentric_circles, eta=0.99, budget=2.0: mean margin 0.298 +/- 0.039, route wins on_off/homodyne = 3/0.
- concentric_circles, eta=0.99, budget=4.0: mean margin 0.400 +/- 0.035, route wins on_off/homodyne = 3/0.
- concentric_circles, eta=0.99, budget=8.0: mean margin 0.407 +/- 0.054, route wins on_off/homodyne = 3/0.
- concentric_circles, eta=0.99, budget=16.0: mean margin 0.427 +/- 0.047, route wins on_off/homodyne = 1/2.
- two_moons, eta=0.50, budget=8.0: mean margin 0.021 +/- 0.000, route wins on_off/homodyne = 1/2.
- two_moons, eta=0.50, budget=16.0: mean margin 0.101 +/- 0.021, route wins on_off/homodyne = 2/1.
- two_moons, eta=0.70, budget=8.0: mean margin 0.060 +/- 0.019, route wins on_off/homodyne = 1/2.
- two_moons, eta=0.70, budget=16.0: mean margin 0.105 +/- 0.010, route wins on_off/homodyne = 2/1.
- two_moons, eta=0.99, budget=8.0: mean margin 0.083 +/- 0.009, route wins on_off/homodyne = 1/2.
- two_moons, eta=0.99, budget=16.0: mean margin 0.109 +/- 0.008, route wins on_off/homodyne = 3/0.

## Conditions that remain fragile under reseeding
- two_moons, eta=0.50, budget=1.0: mean margin -0.098 +/- 0.003, range [-0.101, -0.094], positive in 0/3 repeats.
- two_moons, eta=0.50, budget=2.0: mean margin -0.067 +/- 0.008, range [-0.078, -0.059], positive in 0/3 repeats.
- two_moons, eta=0.50, budget=4.0: mean margin -0.022 +/- 0.008, range [-0.034, -0.016], positive in 0/3 repeats.
- two_moons, eta=0.70, budget=1.0: mean margin -0.103 +/- 0.014, range [-0.123, -0.091], positive in 0/3 repeats.
- two_moons, eta=0.70, budget=2.0: mean margin -0.040 +/- 0.005, range [-0.046, -0.033], positive in 0/3 repeats.
- two_moons, eta=0.70, budget=4.0: mean margin 0.016 +/- 0.016, range [0.004, 0.039], positive in 1/3 repeats.
- two_moons, eta=0.99, budget=1.0: mean margin -0.066 +/- 0.013, range [-0.076, -0.047], positive in 0/3 repeats.
- two_moons, eta=0.99, budget=2.0: mean margin -0.021 +/- 0.017, range [-0.043, -0.004], positive in 0/3 repeats.
- two_moons, eta=0.99, budget=4.0: mean margin 0.035 +/- 0.026, range [0.013, 0.073], positive in 2/3 repeats.

## Interpretation bounds
- This is a real seed-robustness check of the existing small trainable benchmark, not a new large-scale learning study.
- It strengthens confidence only if the positive/negative regime split survives reseeding; it does not establish dataset generality, hardware feasibility, or full control-overhead accounting.
