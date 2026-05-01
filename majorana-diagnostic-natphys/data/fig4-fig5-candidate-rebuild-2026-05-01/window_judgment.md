# Fig. 5 Window Judgment

Decision date: 2026-05-01

Question:

Should the current Fig. 5 transport discriminator be defined on the full bias
window, or should the manuscript-facing criterion be restricted to a zero-bias
or near-zero-bias window?

## Verdict

Use a zero-bias or near-zero-bias window as the main manuscript-facing Fig. 5
criterion. Do not use the full bias window as the decisive discriminator with
the current proxy observable.

## Why

The rebuilt candidate heatmaps show a strong separation improvement once the
window is restricted toward zero bias:

- At zero bias, the positive-to-dot ratio in `max |G_LR|` is about `17.7`, and
  the positive-to-impurity ratio is about `7.1`.
- In the `|V| <= 0.02` window, the positive-to-dot ratio in `mean |G_LR|` is
  about `10.3`, and the positive-to-impurity ratio is about `4.4`.
- Over the full bias window, those `mean |G_LR|` ratios collapse to about
  `2.7` and `3.4`, while the `max |G_LR|` ratios fall further to about `1.49`
  and `1.91`.

So the current proxy already supports a near-zero-bias discriminator much more
cleanly than a full-window discriminator.

## Practical implication

- The current candidate-based rebuild is good enough to support a Fig. 5 story
  centered on zero bias or a tight near-zero window.
- If the manuscript needs a broad-bias transport discriminator, the next change
  should be an observable-definition upgrade, not another control-parameter
  scan.

## Supporting file

- `window_discrimination_metrics.csv`
