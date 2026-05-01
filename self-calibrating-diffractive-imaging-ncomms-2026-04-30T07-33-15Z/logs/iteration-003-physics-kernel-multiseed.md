# Iteration 003 Physics Kernel And Multiseed

- Timestamp: `2026-04-30T08:20:00Z`
- Action type: `physics_kernel_and_multiseed_hardening`
- Stage: `active calculation/verification`
- Single bottleneck addressed: `missing explicit propagation kernel and minimum multiseed statistics`

## Executed action

1. Added `scripts/optics_propagation.py` with an explicit angular-spectrum propagation kernel and a Fresnel kernel helper.
2. Updated `run_baseline_reference_psf.py` so the physical baseline now declares and uses:
   - sample spacing `Δx`
   - wavelength `λ`
   - propagation distance `z`
   - frequency coordinates `fx, fy`
3. Implemented `run_baseline_reference_psf_multiseed.py` and ran the physical baseline for 5 seeds.
4. Generated:
   - `multiseed_summary.csv`
   - `metrics_by_sample_seed_0.csv` through `metrics_by_sample_seed_4.csv`
   - `run_log_seed_0.txt` through `run_log_seed_4.txt`
   - `sha256_manifest.txt`

## Verified result

- Angular-spectrum baseline single-seed mean PSNR gain: `1.493 dB`
- Angular-spectrum baseline single-seed mean SSIM gain: `0.1022`
- Multi-seed mean PSNR gain: `1.661 dB`
- Multi-seed PSNR gain std: `0.139`
- Multi-seed PSNR gain 95% CI half-width: `0.122`
- Multi-seed mean SSIM gain: `0.1133`
- Multi-seed SSIM gain std: `0.0085`
- Multi-seed SSIM gain 95% CI half-width: `0.0075`
- Guided better fraction by PSNR across seeds: `1.0`
- Guided better fraction by SSIM across seeds: `1.0`

## Interpretation boundary

This closes the minimum reviewer-facing requirement that the propagation kernel be explicit and that the baseline be statistically repeated across multiple seeds. It still does not close the stronger manuscript requirement of object-family generalization or a passive differentiable optical frontend.

## Next shortest-path action

Introduce held-out object families into both the physical baseline and the trainable surrogate evaluation ledger before advancing to a more optical-faithful differentiable frontend.
