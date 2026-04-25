# Minimal Task-Level Benchmark Summary

## Benchmark definition
- Small-network surrogate: one random linear feature layer plus one physical threshold-activation layer plus ridge readout.
- Tasks: two-moons and concentric circles.
- Activation noise model: per-neuron output flips with probability given directly by the Figure-3 boundary-error curves.
- Constraint: fixed total activation photon budget per inference, so wider hidden layers reduce photons per neuron.
- This benchmark is intentionally narrow and only tests whether the single-neuron frontier changes the preferred activation choice in a reproducible toy-network setting.

## Linear no-activation baseline
- two_moons: test accuracy 0.882
- concentric_circles: test accuracy 0.484

## Best implementable route by task, detector efficiency, and total activation budget
| task | eta | budget | best route | width | test acc | linear acc | margin | oracle ceiling |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| concentric_circles | 0.50 | 1.0 | homodyne | 32 | 0.554 | 0.484 | 0.071 | 0.598 |
| concentric_circles | 0.50 | 2.0 | homodyne | 8 | 0.577 | 0.484 | 0.094 | 0.668 |
| concentric_circles | 0.50 | 4.0 | homodyne | 32 | 0.626 | 0.484 | 0.142 | 0.732 |
| concentric_circles | 0.50 | 8.0 | on_off | 8 | 0.654 | 0.484 | 0.170 | 0.806 |
| concentric_circles | 0.50 | 16.0 | homodyne | 32 | 0.751 | 0.484 | 0.267 | 0.903 |
| concentric_circles | 0.70 | 1.0 | homodyne | 32 | 0.572 | 0.484 | 0.089 | 0.584 |
| concentric_circles | 0.70 | 2.0 | homodyne | 32 | 0.593 | 0.484 | 0.109 | 0.652 |
| concentric_circles | 0.70 | 4.0 | homodyne | 32 | 0.657 | 0.484 | 0.173 | 0.731 |
| concentric_circles | 0.70 | 8.0 | homodyne | 32 | 0.714 | 0.484 | 0.230 | 0.802 |
| concentric_circles | 0.70 | 16.0 | homodyne | 32 | 0.795 | 0.484 | 0.311 | 0.906 |
| concentric_circles | 0.99 | 1.0 | homodyne | 8 | 0.566 | 0.484 | 0.082 | 0.596 |
| concentric_circles | 0.99 | 2.0 | homodyne | 32 | 0.616 | 0.484 | 0.132 | 0.650 |
| concentric_circles | 0.99 | 4.0 | homodyne | 32 | 0.682 | 0.484 | 0.199 | 0.734 |
| concentric_circles | 0.99 | 8.0 | homodyne | 32 | 0.766 | 0.484 | 0.283 | 0.826 |
| concentric_circles | 0.99 | 16.0 | on_off | 32 | 0.857 | 0.484 | 0.373 | 0.900 |
| two_moons | 0.50 | 1.0 | homodyne | 4 | 0.622 | 0.882 | -0.260 | 0.697 |
| two_moons | 0.50 | 2.0 | homodyne | 4 | 0.661 | 0.882 | -0.222 | 0.734 |
| two_moons | 0.50 | 4.0 | on_off | 4 | 0.711 | 0.882 | -0.172 | 0.794 |
| two_moons | 0.50 | 8.0 | homodyne | 32 | 0.764 | 0.882 | -0.118 | 0.849 |
| two_moons | 0.50 | 16.0 | homodyne | 32 | 0.815 | 0.882 | -0.067 | 0.894 |
| two_moons | 0.70 | 1.0 | homodyne | 4 | 0.644 | 0.882 | -0.239 | 0.695 |
| two_moons | 0.70 | 2.0 | on_off | 4 | 0.690 | 0.882 | -0.192 | 0.731 |
| two_moons | 0.70 | 4.0 | on_off | 4 | 0.743 | 0.882 | -0.140 | 0.791 |
| two_moons | 0.70 | 8.0 | homodyne | 32 | 0.791 | 0.882 | -0.092 | 0.852 |
| two_moons | 0.70 | 16.0 | on_off | 32 | 0.847 | 0.882 | -0.036 | 0.903 |
| two_moons | 0.99 | 1.0 | homodyne | 4 | 0.667 | 0.882 | -0.215 | 0.704 |
| two_moons | 0.99 | 2.0 | on_off | 4 | 0.715 | 0.882 | -0.168 | 0.741 |
| two_moons | 0.99 | 4.0 | on_off | 4 | 0.754 | 0.882 | -0.129 | 0.793 |
| two_moons | 0.99 | 8.0 | homodyne | 32 | 0.825 | 0.882 | -0.058 | 0.850 |
| two_moons | 0.99 | 16.0 | on_off | 32 | 0.878 | 0.882 | -0.005 | 0.902 |

## Design consequences observed in this run
- On-off beats homodyne in 9 of 30 matched task/eta/budget comparisons.
- Physical activation beats the linear no-activation baseline by more than 0.02 accuracy in 15 of 30 scanned conditions.
- In the remaining 15 scanned conditions, paying for activation is not yet justified by this minimal benchmark.

## Conditions where activation is clearly worth paying for in this benchmark
- concentric_circles, eta=0.99, budget=1.0: homodyne reaches 0.566 vs linear 0.484 (margin 0.082) with width 8.
- concentric_circles, eta=0.99, budget=2.0: homodyne reaches 0.616 vs linear 0.484 (margin 0.132) with width 32.
- concentric_circles, eta=0.99, budget=4.0: homodyne reaches 0.682 vs linear 0.484 (margin 0.199) with width 32.
- concentric_circles, eta=0.99, budget=8.0: homodyne reaches 0.766 vs linear 0.484 (margin 0.283) with width 32.
- concentric_circles, eta=0.99, budget=16.0: on_off reaches 0.857 vs linear 0.484 (margin 0.373) with width 32.
- concentric_circles, eta=0.70, budget=1.0: homodyne reaches 0.572 vs linear 0.484 (margin 0.089) with width 32.
- concentric_circles, eta=0.70, budget=2.0: homodyne reaches 0.593 vs linear 0.484 (margin 0.109) with width 32.
- concentric_circles, eta=0.70, budget=4.0: homodyne reaches 0.657 vs linear 0.484 (margin 0.173) with width 32.
- concentric_circles, eta=0.70, budget=8.0: homodyne reaches 0.714 vs linear 0.484 (margin 0.230) with width 32.
- concentric_circles, eta=0.70, budget=16.0: homodyne reaches 0.795 vs linear 0.484 (margin 0.311) with width 32.
- concentric_circles, eta=0.50, budget=1.0: homodyne reaches 0.554 vs linear 0.484 (margin 0.071) with width 32.
- concentric_circles, eta=0.50, budget=2.0: homodyne reaches 0.577 vs linear 0.484 (margin 0.094) with width 8.
- concentric_circles, eta=0.50, budget=4.0: homodyne reaches 0.626 vs linear 0.484 (margin 0.142) with width 32.
- concentric_circles, eta=0.50, budget=8.0: on_off reaches 0.654 vs linear 0.484 (margin 0.170) with width 8.
- concentric_circles, eta=0.50, budget=16.0: homodyne reaches 0.751 vs linear 0.484 (margin 0.267) with width 32.

## Conditions where activation is not yet justified in this benchmark
- two_moons, eta=0.99, budget=1.0: best physical route homodyne reaches 0.667 vs linear 0.882 (margin -0.215).
- two_moons, eta=0.99, budget=2.0: best physical route on_off reaches 0.715 vs linear 0.882 (margin -0.168).
- two_moons, eta=0.99, budget=4.0: best physical route on_off reaches 0.754 vs linear 0.882 (margin -0.129).
- two_moons, eta=0.99, budget=8.0: best physical route homodyne reaches 0.825 vs linear 0.882 (margin -0.058).
- two_moons, eta=0.99, budget=16.0: best physical route on_off reaches 0.878 vs linear 0.882 (margin -0.005).
- two_moons, eta=0.70, budget=1.0: best physical route homodyne reaches 0.644 vs linear 0.882 (margin -0.239).
- two_moons, eta=0.70, budget=2.0: best physical route on_off reaches 0.690 vs linear 0.882 (margin -0.192).
- two_moons, eta=0.70, budget=4.0: best physical route on_off reaches 0.743 vs linear 0.882 (margin -0.140).
- two_moons, eta=0.70, budget=8.0: best physical route homodyne reaches 0.791 vs linear 0.882 (margin -0.092).
- two_moons, eta=0.70, budget=16.0: best physical route on_off reaches 0.847 vs linear 0.882 (margin -0.036).
- two_moons, eta=0.50, budget=1.0: best physical route homodyne reaches 0.622 vs linear 0.882 (margin -0.260).
- two_moons, eta=0.50, budget=2.0: best physical route homodyne reaches 0.661 vs linear 0.882 (margin -0.222).
- two_moons, eta=0.50, budget=4.0: best physical route on_off reaches 0.711 vs linear 0.882 (margin -0.172).
- two_moons, eta=0.50, budget=8.0: best physical route homodyne reaches 0.764 vs linear 0.882 (margin -0.118).
- two_moons, eta=0.50, budget=16.0: best physical route homodyne reaches 0.815 vs linear 0.882 (margin -0.067).

## Interpretation bounds
- This result is real and reproducible, but it is still a stylized random-feature benchmark rather than a trained end-to-end photonic network.
- The benchmark therefore supports a bounded claim: the Figure-3 frontier can change whether activation is worth paying for and which measurement route is preferred under fixed total photon budget.
- It does not yet prove full-network optimality, hardware superiority over electronic activation, or broad task generality.
