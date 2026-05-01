# WP3 PRL Figure Slice

## Panel intent
- Single-panel comparison of the three best candidate-resolved conductance traces from the minimal WP3 proxy.
- Use `conductance_minus_one` for a raw BTK-style excess-conductance panel.
- Use `conductance_minus_curve_min` if a baseline-shifted visual comparison is preferred.

## Included traces
- s_wave: eta=0.00, alpha=1.047, Z=2.00, peak_bias=0.000, peak_split=0.004, signature=broad zero-bias enhancement without split finite-bias peaks
- s_pm: eta=1.00, alpha=0.000, Z=1.00, peak_bias=0.000, peak_split=0.004, signature=intervalley-activated zero-bias enhancement
- chiral: eta=0.00, alpha=1.047, Z=0.00, peak_bias=-0.026, peak_split=0.052, signature=finite-bias-dominant subgap response

## Recommended caption skeleton
- Representative conductance traces from the minimal candidate-resolved BTK proxy.
- The conventional s-wave case shows a broad zero-bias-centered enhancement without resolved finite-bias splitting.
- The s_pm case becomes strongly zero-bias-enhanced only in the intervalley-active limit.
- The chiral case instead develops a finite-bias-dominant subgap structure with a resolved split scale in the best slice.

## Files
- `wp3_prl_figure_slice_source_data.csv`: plot-ready traces.
- `wp3_prl_figure_slice_annotations.csv`: peak and parameter annotations.
