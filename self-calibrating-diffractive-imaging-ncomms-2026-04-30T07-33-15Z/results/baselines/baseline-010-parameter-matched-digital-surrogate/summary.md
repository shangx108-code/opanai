# Baseline 010 Parameter-Matched Digital Surrogate

Goal: provide a digital-only comparator with the same trainable digital parameter count used by the downstream ridge stage of `phase_only_stack`.

## Design

- Same training object family and same two held-out ledgers as the unified benchmark
- Same low-resolution target grid: `12 x 12`
- Zero optical trainable parameters
- Digital trainable parameters: `145296`
- Derived channels: `noisy_lowres, reference_lowres, difference, sum, product, noisy_square, reference_square`

## Mean PSNR gain over fixed baseline by ledger

| Method | Ledger | Mean PSNR gain | Std PSNR gain | CI low | CI high | Better-than-fixed fraction | n seeds | n samples |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| parameter_matched_digital_surrogate | same_family_heldout_aberration | 4.326442 | 0.091952 | 4.269450 | 4.383435 | 1.000000 | 10 | 1440 |
| parameter_matched_digital_surrogate | new_family_heldout_object_family | 0.459808 | 0.059292 | 0.423058 | 0.496557 | 0.500000 | 10 | 960 |

## Interpretation boundary

This comparator is intentionally simple: it expands the distorted and reference channels into a fixed seven-channel image-domain feature bank and trains only the final linear readout. It tests whether the phase-only result can be explained by downstream digital capacity alone after parameter matching.
