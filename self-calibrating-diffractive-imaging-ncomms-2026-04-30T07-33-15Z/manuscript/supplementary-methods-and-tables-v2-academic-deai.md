# Supplementary Methods and Tables

## Scope

This supplementary note supports `main-manuscript-v3-academic-deai.md` and is limited to claims backed by files present in the active long-term project space.

## Supplementary Methods S1. Unified dual-ledger evaluation

The unified comparison was executed by `scripts/run_unified_comparison_ci.py`. The pipeline uses `10` seeds (`0-9`) and two fixed evaluation ledgers:

- `same_family_heldout_aberration`
- `new_family_heldout_object_family`

For every method, the evaluation uses the same seed set, held-out aberration schedule, held-out object-family ledger, low-resolution target grid (`12 x 12`), and aggregation rule. Per-seed outputs are first averaged within each ledger and then averaged across ledgers so that one ledger does not dominate the overall score merely by sample count.

## Supplementary Methods S2. Fresnel propagation and sampling conventions

The optical propagation model uses a scalar Fresnel transfer function

`H(f_x, f_y) = exp(-i * pi * lambda * z * (f_x^2 + f_y^2))`

with the following active configuration in the unified comparison:

- wavelength `lambda = 532e-9 m`
- native sample spacing `dx = 8e-6 m`
- propagation distance `z = 12e-3 m`
- low-resolution frontend grid `12 x 12`
- phase-only layer count `5`
- phase basis count per layer `10`

The frequency coordinates are generated through the shared `PropagationConfig` and `frequency_coordinates` utilities in `scripts/optics_propagation.py`. The manuscript should therefore describe this model as a scalar Fresnel approximation in the present sampling regime, not as a general high-NA vectorial propagation model.

## Supplementary Methods S3. Method fairness accounting

Table S1 separates optical and digital degrees of freedom for the methods in the unified comparison.

### Table S1. Method fairness table

| Method | Comparator role | Optical trainable parameters | Digital trainable parameters | Total trainable parameters | Uses reference PSF at test time | Uses reference channel at test time | Retrained for held-out objects | Training samples | Evaluation protocol |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | ---: | --- |
| `phase_only_stack` | proposed hybrid | 50 | 145296 | 145346 | Yes | Yes | No | 4800 | same dual-ledger protocol |
| `reference_psf_deconvolution` | reference-guided classical comparator | 0 | 0 | 0 | Yes | Yes | No | 0 | same dual-ledger protocol |
| `parameter_matched_digital_surrogate` | parameter-matched digital comparator | 0 | 145296 | 145296 | Yes | Yes | No | 4800 | same dual-ledger protocol |
| `spectral_frontend` | learned spectral comparator | 0 | 20880 | 20880 | Yes | Yes | No | 4800 | same dual-ledger protocol |
| `trainable_surrogate_ridge` | digital comparator | 0 | 41616 | 41616 | Yes | Yes | No | 4800 | same dual-ledger protocol |

Interpretation note: `phase_only_stack` should be described as a hybrid optical-digital method because the optical frontend has only `50` trainable optical parameters while the downstream ridge stage contains `145296` digital trainable weights. `reference_psf_deconvolution` is not a generic baseline but a reference-guided classical comparator with explicit test-time PSF information. `parameter_matched_digital_surrogate` closes the main digital-capacity fairness gap and still trails the hybrid method in the pooled benchmark.

## Supplementary Methods S4. Seed-level and raw-result availability

The active project space contains the following auditable outputs:

- overall comparison table: `results/unified_comparison_ci.csv`
- per-seed table: `results/unified_comparison/unified_comparison_per_seed.csv`
- sample-level table: `results/unified_comparison/unified_comparison_detail.csv`
- execution metadata: `results/unified_comparison/unified_comparison_summary.json`

These files should be cited explicitly as the source-data path for the current unified comparison.

## Supplementary Methods S5. Literature-bound device-prior package

The active project space now includes an explicit device-prior package in `results/tolerance_device_priors/`:

- `device_tolerance_prior_profiles.json`
- `device_tolerance_prior_summary.csv`
- `device_tolerance_prior_summary.md`

This package distinguishes which simulation variables can be interpreted as device-native for different platform classes.

For a single-plane reflective LCoS SLM:

- `phase_noise_sigma_rad` is literature-bound
- `shift_sigma_px` is not fabrication-native for a single-plane panel
- `rotation_sigma_deg` is not fabrication-native for a single-plane panel
- `wavelength_drift_fraction` is better interpreted as source or recalibration dependent

For a stacked dielectric metasurface:

- `phase_noise_sigma_rad` is literature-bound
- `shift_sigma_px` is literature-bound through bilayer overlay tolerance
- `rotation_sigma_deg` is only partially bound and still requires device-specific overlay metrology
- `wavelength_drift_fraction` is literature-bound through geometry-induced resonance shift

The linked phase-noise plus misalignment plus wavelength-drift scan should therefore be written as a cleaner physical match to a stacked metasurface interpretation than to a single-plane SLM fabrication interpretation.

## Supplementary Results S1. Ledger-resolved unified comparison

Table S2 reports the current ledger-resolved PSNR gains.

### Table S2. Mean PSNR gain over the fixed baseline by ledger

| Method | same-family held-out aberration | new-family held-out object family |
| --- | ---: | ---: |
| `phase_only_stack` | 7.5931 | 0.5211 |
| `reference_psf_deconvolution` | 2.9015 | 2.5108 |
| `parameter_matched_digital_surrogate` | 4.3264 | 0.4598 |
| `spectral_frontend` | 3.7016 | 0.0807 |
| `trainable_surrogate_ridge` | 2.8978 | -0.1387 |

Reviewer-facing interpretation:

- `phase_only_stack` is strongest in pooled average gain because it dominates the held-out aberration ledger.
- `parameter_matched_digital_surrogate` closes most of the object-family gap but remains much weaker on the held-out aberration ledger.
- `reference_psf_deconvolution` is stronger on the held-out object-family ledger.
- `trainable_surrogate_ridge` does not retain a positive average gain under object-family shift.
- The object-family result for the phase-only stack should therefore be written as modest but positive, not as universal generalization.

## Supplementary Results S2. Public-open-data natural-image protocol

The current real-data branch uses frozen public subsets from `Kodak-PCD0992` and `UCID-1338`, with traceability files in:

- `results/natural_objects/public_dataset_download_manifest.csv`
- `results/natural_objects/public_dataset_download_manifest.json`
- `results/natural_objects/public_dataset_protocol.md`
- `archive/reproducibility_manifest.json`

The active thickened mixed-training results are:

- `Kodak-PCD0992`: `-1.0544 ± 0.1434 dB` mean PSNR gain over fixed
- `UCID`: `+1.7261 ± 0.2319 dB` mean PSNR gain over fixed

This branch supports a statement about dataset-dependent recovery under mixed training. It does not support a benchmark-root `ImageNet-1k` or `COCO` claim.

## Supplementary Results S3. Linked fabrication-style tolerance boundary

The linked scan in `results/tolerance_joint/` varies:

- phase-noise RMS: `0`, `0.05`, `0.10`, `0.20 rad`
- layer misalignment levels:
  - clean: `0 px`, `0 deg`
  - mild: `0.25 px`, `0.5 deg`
  - moderate: `0.50 px`, `1.0 deg`
  - severe: `1.0 px`, `2.0 deg`
- wavelength drift: `0`, `0.5%`, `1%`, `2%`

Key outcomes:

- `UCID` remains positive only on the clean-mask branch
- `Kodak-PCD0992` has no positive branch even at the clean point
- wavelength drift up to `2%` is comparatively mild when the hardware is otherwise clean
- phase noise and layer misalignment dominate the failure boundary

These data support a constrained engineering conclusion rather than a broad tolerance claim.

## Supplementary Results S4. Robust-mask and second-generation mitigation comparison

The matched robust-mask version in `results/tolerance_joint_robust/` improves the clean branch but does not expand the pass region:

- `UCID`, clean, `0%` drift: `+2.5993 ± 0.0812 dB`
- `UCID`, clean, `2%` drift: `+2.5192 ± 0.1570 dB`
- `Kodak-PCD0992`, clean, `0%` drift: `-0.2182 ± 0.0935 dB`

The first second-generation objective in `results/tolerance_joint_secondgen/` also fails to expand the pass region:

- `UCID`, clean, `0%` drift: `+2.3951 ± 0.2853 dB`
- `UCID`, clean, `2%` drift: `+2.3037 ± 0.3357 dB`
- `UCID`, phase noise only `0.05 rad`: `-4.7289 ± 1.9562 dB`
- `UCID`, mild misalignment only `0.25 px / 0.5 deg`: `-8.3056 ± 2.1266 dB`
- `Kodak-PCD0992`, clean, `0%` drift: `-0.4409 ± 0.1989 dB`

Interpretation note: the robust-mask package is the stronger current mitigation result, and the second-generation objective should be retained as a meaningful negative result rather than treated as a hidden failed branch.

## Supplementary Discussion S1. Strict wording rules for the current manuscript

The following expressions should be avoided because they exceed the current evidence:

- `all-optical reconstruction`
- `purely optical inference`
- `fully autonomous self-calibrating optical network`
- `strong generalization to unseen object families`
- `broad hardware robustness`
- `fabrication-tolerant SLM implementation`

Preferred wording:

- `hybrid optical-digital phase-only frontend`
- `pre-registered dual-ledger evaluation`
- `large and stable gain under held-out aberrations`
- `modest but positive mean gain under held-out object-family shift`
- `dataset-dependent public-data transfer`
- `stacked-metasurface-aligned interpretation of the linked tolerance variables`

## Supplementary Discussion S2. Remaining reviewer-facing risks

The current revision substantially improves claim discipline, fairness transparency, and hardware-interpretation clarity, but the following issues remain active:

1. The natural-image evidence uses staged public Kodak/UCID subsets rather than benchmark-root `ImageNet-1k` or `COCO`.
2. The executed tolerance package does not justify a broad hardware-robustness claim.
3. The second-generation joint-training objective remains a negative result and does not rescue the linked failure boundary.
4. The current project space still lacks a fabricated-device experiment.

These issues should appear as explicit limitations or future work, not as implied achievements.
