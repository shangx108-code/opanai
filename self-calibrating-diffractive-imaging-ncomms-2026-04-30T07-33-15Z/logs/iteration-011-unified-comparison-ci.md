# Iteration 011 Unified Comparison CI

- Timestamp: `2026-05-01T00:00:00Z`
- Action type: `unified_four_method_comparison`
- Stage: `active calculation/verification`
- Single bottleneck addressed: `missing one shared multi-seed comparison across all required methods`

## Executed action

1. Added `scripts/run_unified_comparison_ci.py`.
2. Ran one unified comparison with:
   - seeds `0-9`
   - the same dual held-out ledgers:
     - `same_family_heldout_aberration`
     - `new_family_heldout_object_family`
   - one shared confidence-interval aggregation pipeline
3. Included four methods in the same table:
   - `phase_only_stack`
   - `trainable_surrogate_ridge`
   - `reference_psf_deconvolution`
   - `spectral_frontend`
4. Wrote the required output file:
   - `results/unified_comparison_ci.csv`

## Verified result

- `phase_only_stack`: mean PSNR gain `4.0571 dB`, std `0.2032 dB`, 95% CI `[3.9312, 4.1830]`, better-than-fixed fraction `0.7786`
- `reference_psf_deconvolution`: mean PSNR gain `2.7061 dB`, std `0.1016 dB`, 95% CI `[2.6432, 2.7691]`, better-than-fixed fraction `1.0000`
- `spectral_frontend`: mean PSNR gain `1.8912 dB`, std `0.0749 dB`, 95% CI `[1.8448, 1.9376]`, better-than-fixed fraction `0.7438`
- `trainable_surrogate_ridge`: mean PSNR gain `1.3795 dB`, std `0.0463 dB`, 95% CI `[1.3509, 1.4082]`, better-than-fixed fraction `0.7448`

## Interpretation boundary

This unified experiment closes the comparison-format gap: all four methods now sit on the same seed set, the same two held-out ledgers, and the same CI pipeline. Under that shared protocol, the current phase-only stack is the strongest method by mean PSNR gain, while the reference-PSF deconvolution remains the only method with a perfect better-than-fixed fraction.

## Output package

- `results/unified_comparison_ci.csv`
- `results/unified_comparison/unified_comparison_per_seed.csv`
- `results/unified_comparison/unified_comparison_detail.csv`
- `results/unified_comparison/unified_comparison_summary.json`

## Next shortest-path action

The next clean move is no longer format unification. It is to raise the phase-only stack's better-than-fixed fraction on the new-family ledger without giving back too much of its current mean-gain lead.
