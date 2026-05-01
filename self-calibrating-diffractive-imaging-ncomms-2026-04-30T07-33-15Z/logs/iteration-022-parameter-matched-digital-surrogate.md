# Iteration 022 Parameter-Matched Digital Surrogate

- Timestamp: `2026-05-01T11:20:00Z`
- Action type: `fairness_control_execution`
- Stage: `active calculation/verification`
- Single bottleneck addressed: `missing parameter-matched digital-only fairness comparator`

## Executed action

1. Added `scripts/run_parameter_matched_digital_surrogate.py`.
2. Built a digital-only seven-channel image-domain feature bank from:
   - distorted low-resolution image
   - reference low-resolution image
   - difference
   - sum
   - product
   - distorted-image square
   - reference-image square
3. Matched the digital trainable parameter count exactly to the downstream ridge stage used by `phase_only_stack`:
   - `1008` input features
   - `144` output targets
   - `145296` digital trainable parameters including bias
4. Ran the same 10-seed dual-ledger schedule used by `scripts/run_unified_comparison_ci.py`.
5. Re-exported the unified benchmark and ledger-resolved submission tables with the new comparator included.

## Verified result

- Overall pooled dual-ledger mean PSNR gain over fixed: `+2.3931 dB`
- Overall pooled better-than-fixed fraction: `0.7500`
- Same-family held-out aberration mean PSNR gain: `+4.3264 dB`
- New-family held-out object-family mean PSNR gain: `+0.4598 dB`

## Interpretation boundary

This new comparator closes the strongest remaining fairness slot because it matches the digital parameter count of the `phase_only_stack` ridge stage exactly while using no optical trainable parameters. The result strengthens the hybrid-method interpretation on the held-out aberration ledger and in the pooled benchmark. However, it does not justify a broad optical-front-end superiority claim on the held-out object-family ledger, where the gap to `phase_only_stack` is only `~0.06 dB`.

## Output package

- `results/baselines/baseline-010-parameter-matched-digital-surrogate/detail_metrics.csv`
- `results/baselines/baseline-010-parameter-matched-digital-surrogate/per_seed_summary.csv`
- `results/baselines/baseline-010-parameter-matched-digital-surrogate/ledger_summary.csv`
- `results/baselines/baseline-010-parameter-matched-digital-surrogate/summary.json`
- `results/baselines/baseline-010-parameter-matched-digital-surrogate/summary.md`
- `results/unified_comparison_ci.csv`
- `results/tables/unified_comparison_by_ledger.csv`
- `results/tables/unified_comparison_by_ledger_detail.csv`

## Next shortest-path action

Promote the realism evidence chain from `proxy-only` to benchmark-root execution by staging licensed natural-image roots and rerunning the frozen natural-object evaluation pipeline.
