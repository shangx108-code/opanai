# Supplementary Methods and Tables

## Scope

This supplementary note supports `main-manuscript-v2-strict.md` and is limited to claims that are backed by files present in the active long-term project space.

## Supplementary Methods S1. Unified dual-ledger evaluation

The unified comparison was executed by `scripts/run_unified_comparison_ci.py`. The pipeline uses 10 seeds (`0-9`) and two fixed evaluation ledgers:

- `same_family_heldout_aberration`
- `new_family_heldout_object_family`

For every method, the evaluation uses the same seed set, the same held-out aberration schedule, the same held-out object-family ledger, the same low-resolution target grid (`12 x 12`), and the same aggregation rule. Per-seed outputs are first averaged within each ledger and then averaged across ledgers so that one ledger does not dominate the overall method score merely by sample count.

## Supplementary Methods S2. Fresnel propagation and sampling conventions

The optical propagation model uses a scalar Fresnel transfer function of the form

`H(f_x, f_y) = exp(-i * pi * lambda * z * (f_x^2 + f_y^2))`

with the following active configuration in the unified comparison:

- wavelength `lambda = 532e-9 m`
- native sample spacing `dx = 8e-6 m`
- propagation distance `z = 12e-3 m`
- low-resolution frontend grid `12 x 12`
- phase-only layer count `5`
- phase basis count per layer `10`

The frequency coordinates are generated through the shared `PropagationConfig` and `frequency_coordinates` utilities in `scripts/optics_propagation.py`. The manuscript should describe this model as a scalar Fresnel approximation with explicit sampling choices, not as a general high-NA vectorial propagation model. The active project space does not yet contain a finalized supplement-level derivation of validity bounds, so the main text should keep the physical claim bounded to the current numerical regime.

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

Interpretation note: the current phase-only method should be described as a hybrid optical-digital system because the optical frontend has only 50 trainable optical parameters while the downstream ridge reconstruction stage contains 145296 digital trainable weights. The updated fairness table also makes the role of `reference_psf_deconvolution` explicit: it is not a generic baseline, but a reference-guided classical comparator that receives explicit test-time PSF information. The newly added `parameter_matched_digital_surrogate` closes the strongest remaining fairness gap at the digital-capacity level: it matches the digital parameter count of the `phase_only_stack` ridge stage exactly, yet still trails the hybrid method in the pooled benchmark.

## Supplementary Methods S4. Seed-level and raw-result availability

The current active project space contains the following auditable outputs:

- overall comparison table: `results/unified_comparison_ci.csv`
- per-seed table: `results/unified_comparison/unified_comparison_per_seed.csv`
- sample-level table: `results/unified_comparison/unified_comparison_detail.csv`
- execution metadata: `results/unified_comparison/unified_comparison_summary.json`

These files should be cited explicitly in the manuscript as the source-data path for the current unified comparison.

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

- `phase_only_stack` is strongest in overall average gain because it dominates the held-out aberration ledger.
- `parameter_matched_digital_surrogate` closes most of the object-family gap but remains well below `phase_only_stack` on the held-out aberration ledger.
- `reference_psf_deconvolution`, a reference-guided classical comparator with test-time PSF information, is stronger on the held-out object-family ledger.
- `trainable_surrogate_ridge` does not retain a positive average gain under object-family shift.
- Therefore the object-family result for the phase-only stack should be written as modest but positive, not as strong universal generalization or uniform superiority across regimes.

## Supplementary Discussion S1. Strict wording rules for the current manuscript

The following expressions should be avoided in the present round because they exceed the current evidence:

- `all-optical reconstruction`
- `purely optical inference`
- `fully autonomous self-calibrating optical network`
- `strong generalization to unseen object families`

Preferred wording:

- `hybrid optical-digital phase-only frontend`
- `pre-registered dual-ledger evaluation`
- `large and stable gain under held-out aberrations`
- `modest but positive mean gain under held-out object-family shift`

## Supplementary Discussion S2. Remaining unresolved reviewer risks

The current revision materially improves claim discipline and fairness transparency, but the following items remain open blockers for a stronger submission package:

1. The executed natural-image evidence now comes from staged public Kodak/UCID subsets rather than from benchmark-root `ImageNet-1k` or `COCO`, so it should be presented explicitly as a public-open-data protocol with dataset-dependent outcomes, not as finalized benchmark-root evidence.
2. The executed tolerance evidence supports a constrained engineering conclusion, but it does not yet justify a broad hardware-robustness claim. The linked fabrication-style scan shows that robust-mask training raises the clean `UCID` margin but does not widen the pass region beyond the clean `UCID` branch, and the `2 px` lateral-shift failure mode also remains unresolved.
3. The current project space does not yet contain a fabricated-device experiment.

These items should appear as explicit future-work or revision requirements rather than being implied as already complete.

## Supplementary Figure Candidate S1. Failure cases under object-family shift

The active project space now includes a dedicated failure-case package:

- panel image: `results/failure_cases/object_shift_failure_cases_panel.png`
- case table: `results/failure_cases/object_shift_failure_cases.csv`
- narrative note: `results/failure_cases/object_shift_failure_cases.md`

The current representative failures show three distinct modes:

1. `diag_x` is the most consistently negative held-out object family, reaching `-4.402 dB` in the selected representative case.
2. `checker_blocks` produces negative cases consistent with alias-prone repeated edges and boundary leakage, with the selected representative case at `-2.350 dB`.
3. `crescent` produces a mixed negative tail associated with asymmetric curved boundaries and hollow subtraction, with the selected representative case at `-2.463 dB`.

These cases strengthen the reviewer-facing interpretation that the new-family ledger is limited by structured shape-dependent failures rather than by uniform collapse across all held-out objects. The caption and surrounding text should not describe this panel as evidence of complete failure under object-family shift; instead, it should be used to explain why the mean gain on `new_family_heldout_object_family` remains modest even though the aggregate sign stays positive.
