# Trainable Task-Level Benchmark Summary

## Benchmark definition
- Small-network surrogate: one trainable linear input layer plus one trainable physical threshold-activation layer plus trainable readout.
- Tasks: two-moons and concentric circles.
- Activation noise model: per-neuron output flips with probability given directly by the Figure-3 boundary-error curves.
- Constraint: fixed total activation photon budget per inference, so wider hidden layers reduce photons per neuron.
- Training rule: optimize a smooth noisy-activation surrogate, then evaluate with the actual threshold-and-flip activation used by the physical benchmark.
- This benchmark is still intentionally small, but it removes the largest reviewer objection to the earlier random-feature surrogate by letting the hidden layer adapt to the task.

## Trainable linear no-activation baseline
- two_moons: test accuracy 0.866
- concentric_circles: test accuracy 0.566

## Best implementable route by task, detector efficiency, and total activation budget
| task | eta | budget | best route | width | test acc | linear acc | margin | oracle ceiling |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| concentric_circles | 0.50 | 1.0 | homodyne | 32 | 0.632 | 0.566 | 0.066 | 0.699 |
| concentric_circles | 0.50 | 2.0 | homodyne | 4 | 0.686 | 0.566 | 0.120 | 0.864 |
| concentric_circles | 0.50 | 4.0 | on_off | 4 | 0.804 | 0.566 | 0.237 | 0.934 |
| concentric_circles | 0.50 | 8.0 | homodyne | 4 | 0.893 | 0.566 | 0.326 | 0.951 |
| concentric_circles | 0.50 | 16.0 | homodyne | 4 | 0.974 | 0.566 | 0.407 | 0.964 |
| concentric_circles | 0.70 | 1.0 | homodyne | 16 | 0.654 | 0.566 | 0.088 | 0.741 |
| concentric_circles | 0.70 | 2.0 | on_off | 4 | 0.749 | 0.566 | 0.183 | 0.907 |
| concentric_circles | 0.70 | 4.0 | homodyne | 4 | 0.849 | 0.566 | 0.283 | 0.907 |
| concentric_circles | 0.70 | 8.0 | on_off | 4 | 0.952 | 0.566 | 0.386 | 0.934 |
| concentric_circles | 0.70 | 16.0 | on_off | 16 | 0.985 | 0.566 | 0.419 | 0.980 |
| concentric_circles | 0.99 | 1.0 | homodyne | 16 | 0.677 | 0.566 | 0.111 | 0.710 |
| concentric_circles | 0.99 | 2.0 | on_off | 4 | 0.750 | 0.566 | 0.184 | 0.906 |
| concentric_circles | 0.99 | 4.0 | on_off | 4 | 0.939 | 0.566 | 0.373 | 0.937 |
| concentric_circles | 0.99 | 8.0 | homodyne | 4 | 0.974 | 0.566 | 0.407 | 0.984 |
| concentric_circles | 0.99 | 16.0 | on_off | 16 | 0.968 | 0.566 | 0.401 | 0.944 |
| two_moons | 0.50 | 1.0 | homodyne | 4 | 0.711 | 0.866 | -0.155 | 0.813 |
| two_moons | 0.50 | 2.0 | on_off | 4 | 0.789 | 0.866 | -0.077 | 0.887 |
| two_moons | 0.50 | 4.0 | on_off | 4 | 0.858 | 0.866 | -0.008 | 0.943 |
| two_moons | 0.50 | 8.0 | homodyne | 16 | 0.888 | 0.866 | 0.022 | 0.972 |
| two_moons | 0.50 | 16.0 | on_off | 16 | 0.952 | 0.866 | 0.086 | 0.988 |
| two_moons | 0.70 | 1.0 | homodyne | 32 | 0.802 | 0.866 | -0.064 | 0.846 |
| two_moons | 0.70 | 2.0 | homodyne | 16 | 0.831 | 0.866 | -0.035 | 0.858 |
| two_moons | 0.70 | 4.0 | on_off | 4 | 0.879 | 0.866 | 0.013 | 0.915 |
| two_moons | 0.70 | 8.0 | homodyne | 16 | 0.932 | 0.866 | 0.066 | 0.974 |
| two_moons | 0.70 | 16.0 | on_off | 16 | 0.981 | 0.866 | 0.115 | 0.980 |
| two_moons | 0.99 | 1.0 | homodyne | 32 | 0.784 | 0.866 | -0.083 | 0.849 |
| two_moons | 0.99 | 2.0 | on_off | 4 | 0.864 | 0.866 | -0.002 | 0.866 |
| two_moons | 0.99 | 4.0 | homodyne | 4 | 0.899 | 0.866 | 0.033 | 0.914 |
| two_moons | 0.99 | 8.0 | on_off | 16 | 0.974 | 0.866 | 0.108 | 0.979 |
| two_moons | 0.99 | 16.0 | homodyne | 16 | 0.987 | 0.866 | 0.121 | 0.988 |

## Design consequences observed in this run
- On-off beats homodyne in 14 of 30 matched task/eta/budget comparisons.
- Physical activation beats the trainable linear no-activation baseline by more than 0.02 accuracy in 22 of 30 scanned conditions.
- In the remaining 8 scanned conditions, paying for activation is not yet justified by this tighter benchmark.

## Conditions where activation is clearly worth paying for in this benchmark
- two_moons, eta=0.99, budget=4.0: homodyne reaches 0.899 vs trainable linear 0.866 (margin 0.033) with width 4.
- two_moons, eta=0.99, budget=8.0: on_off reaches 0.974 vs trainable linear 0.866 (margin 0.108) with width 16.
- two_moons, eta=0.99, budget=16.0: homodyne reaches 0.987 vs trainable linear 0.866 (margin 0.121) with width 16.
- two_moons, eta=0.70, budget=8.0: homodyne reaches 0.932 vs trainable linear 0.866 (margin 0.066) with width 16.
- two_moons, eta=0.70, budget=16.0: on_off reaches 0.981 vs trainable linear 0.866 (margin 0.115) with width 16.
- two_moons, eta=0.50, budget=8.0: homodyne reaches 0.888 vs trainable linear 0.866 (margin 0.022) with width 16.
- two_moons, eta=0.50, budget=16.0: on_off reaches 0.952 vs trainable linear 0.866 (margin 0.086) with width 16.
- concentric_circles, eta=0.99, budget=1.0: homodyne reaches 0.677 vs trainable linear 0.566 (margin 0.111) with width 16.
- concentric_circles, eta=0.99, budget=2.0: on_off reaches 0.750 vs trainable linear 0.566 (margin 0.184) with width 4.
- concentric_circles, eta=0.99, budget=4.0: on_off reaches 0.939 vs trainable linear 0.566 (margin 0.373) with width 4.
- concentric_circles, eta=0.99, budget=8.0: homodyne reaches 0.974 vs trainable linear 0.566 (margin 0.407) with width 4.
- concentric_circles, eta=0.99, budget=16.0: on_off reaches 0.968 vs trainable linear 0.566 (margin 0.401) with width 16.
- concentric_circles, eta=0.70, budget=1.0: homodyne reaches 0.654 vs trainable linear 0.566 (margin 0.088) with width 16.
- concentric_circles, eta=0.70, budget=2.0: on_off reaches 0.749 vs trainable linear 0.566 (margin 0.183) with width 4.
- concentric_circles, eta=0.70, budget=4.0: homodyne reaches 0.849 vs trainable linear 0.566 (margin 0.283) with width 4.
- concentric_circles, eta=0.70, budget=8.0: on_off reaches 0.952 vs trainable linear 0.566 (margin 0.386) with width 4.
- concentric_circles, eta=0.70, budget=16.0: on_off reaches 0.985 vs trainable linear 0.566 (margin 0.419) with width 16.
- concentric_circles, eta=0.50, budget=1.0: homodyne reaches 0.632 vs trainable linear 0.566 (margin 0.066) with width 32.
- concentric_circles, eta=0.50, budget=2.0: homodyne reaches 0.686 vs trainable linear 0.566 (margin 0.120) with width 4.
- concentric_circles, eta=0.50, budget=4.0: on_off reaches 0.804 vs trainable linear 0.566 (margin 0.237) with width 4.
- concentric_circles, eta=0.50, budget=8.0: homodyne reaches 0.893 vs trainable linear 0.566 (margin 0.326) with width 4.
- concentric_circles, eta=0.50, budget=16.0: homodyne reaches 0.974 vs trainable linear 0.566 (margin 0.407) with width 4.

## Conditions where activation is not yet justified in this benchmark
- two_moons, eta=0.99, budget=1.0: best physical route homodyne reaches 0.784 vs trainable linear 0.866 (margin -0.083).
- two_moons, eta=0.99, budget=2.0: best physical route on_off reaches 0.864 vs trainable linear 0.866 (margin -0.002).
- two_moons, eta=0.70, budget=1.0: best physical route homodyne reaches 0.802 vs trainable linear 0.866 (margin -0.064).
- two_moons, eta=0.70, budget=2.0: best physical route homodyne reaches 0.831 vs trainable linear 0.866 (margin -0.035).
- two_moons, eta=0.70, budget=4.0: best physical route on_off reaches 0.879 vs trainable linear 0.866 (margin 0.013).
- two_moons, eta=0.50, budget=1.0: best physical route homodyne reaches 0.711 vs trainable linear 0.866 (margin -0.155).
- two_moons, eta=0.50, budget=2.0: best physical route on_off reaches 0.789 vs trainable linear 0.866 (margin -0.077).
- two_moons, eta=0.50, budget=4.0: best physical route on_off reaches 0.858 vs trainable linear 0.866 (margin -0.008).

## Interpretation bounds
- This result is real and reproducible, but it is still a small one-hidden-layer benchmark rather than a full end-to-end photonic training study.
- The benchmark therefore supports a tighter claim than the random-feature surrogate: trainable task adaptation still leaves a route- and budget-dependent activation decision, rather than washing out the Figure-3 physics.
- It does not yet prove large-scale task generality, full hardware readiness, or superiority over electronic activation with complete detector and control overhead accounting.
