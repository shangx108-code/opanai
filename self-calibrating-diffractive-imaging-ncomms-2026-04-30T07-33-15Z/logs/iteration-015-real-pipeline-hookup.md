# Iteration 015 Real Pipeline Hookup

- Timestamp: `2026-05-01T00:00:00Z`
- Action type: `real_pipeline_hookup`
- Stage: `active calculation/verification`
- Single bottleneck addressed: `the active project root still lacked a single runnable entry that exposed load_dataset -> forward_diffractive -> model -> compute_psnr`

## Executed action

1. Reused the already validated Fresnel, phase-only frontend, and ridge reconstruction components from the active scripts.
2. Added `scripts/run_real_pipeline.py` as the unified executable path.
3. Exposed the following real functions in one place:
   - `load_dataset(...)`
   - `fit_pipeline(...)`
   - `forward_diffractive(...)`
   - `model(...)`
   - `compute_psnr(...)`
4. Wired the outputs to:
   - `results/pipeline/pipeline_smoke/pipeline_metrics.csv`
   - `results/pipeline/pipeline_smoke/pipeline_summary.json`
   - `results/pipeline/pipeline_smoke/pipeline_runtime.json`

## Expected execution chain

```python
data = load_dataset(...)
state = fit_pipeline(data["train"], ...)
optical_output = forward_diffractive(...)
recon = model(...)
psnr_gain = compute_psnr(...)
```

## Interpretation boundary

This iteration is about pipeline closure, not about claiming a new manuscript result yet. The next required step is to run the script, verify the outputs, and then decide whether to scale it to the next ledger or realism package.

## Verification result

- `scripts/check_environment.py` passed with all required modules available.
- `scripts/run_real_pipeline.py` executed successfully on `2026-05-01T08:07:32Z`.
- Smoke-run configuration:
  - seed: `0`
  - training cases: `24`
  - evaluation cases: `6`
  - evaluation split: `new_family_heldout_object_family`
- Runtime footprint:
  - training samples: `1200`
  - evaluation samples: `24`
  - feature shape: `24 x 1008`
  - phase-plane tensor shape: `24 x 5 x 12 x 12`
- Smoke-run summary:
  - mean fixed PSNR: `17.5701 dB`
  - mean guided PSNR: `19.8360 dB`
  - mean pipeline PSNR: `17.7550 dB`
  - mean PSNR gain over fixed: `+0.1849 dB`
  - better-than-fixed fraction: `0.4167`
