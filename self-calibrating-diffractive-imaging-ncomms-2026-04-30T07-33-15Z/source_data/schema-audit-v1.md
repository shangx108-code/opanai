# Schema Audit v1

## Scope

This audit covers the current CSV files that support the main benchmark, the dual-ledger split, proxy natural-image stress tests, tolerance diagnosis, robust-mask mitigation, fairness accounting, and failure-case packaging.

## Audited files

- `results/unified_comparison/unified_comparison_detail.csv`
- `results/unified_comparison/unified_comparison_per_seed.csv`
- `results/unified_comparison_ci.csv`
- `results/tables/unified_comparison_by_ledger.csv`
- `results/tables/method_fairness_table.csv`
- `results/natural_objects/natural_object_metrics.csv`
- `results/natural_objects/mixed_train_natural_object_metrics.csv`
- `results/natural_objects/mixed_train_natural_object_thickstats_metrics.csv`
- `results/tolerance/mixed_train_tolerance_metrics.csv`
- `results/tolerance/robust_mask_tolerance_metrics.csv`
- `results/tolerance/robust_mask_tolerance_compare.csv`
- `results/failure_cases/object_shift_failure_cases.csv`

## Current finding

The project does not yet use one canonical result schema. Current tables are internally usable, but they diverge in field naming, role labeling, and detail depth. This is manageable for the manuscript draft, but it is not yet strong enough for submission-grade source-data packaging without one normalization pass.

## Canonical field targets

The following fields should become the shared target schema wherever they are meaningful:

- `seed`
- `dataset_name`
- `dataset_version`
- `ledger`
- `method`
- `sample_id`
- `object_family`
- `aberration_id`
- `condition`
- `condition_family`
- `condition_level`
- `psnr_fixed`
- `psnr_method`
- `psnr_gain`
- `ssim_fixed`
- `ssim_method`
- `ssim_gain`
- `better_than_fixed`

Not every table needs every field. Summary tables may omit sample-level fields, but any omitted field should be unavailable by design rather than by inconsistent export naming.

## File-by-file audit

### `results/unified_comparison/unified_comparison_detail.csv`

Current fields:

- `method`
- `seed`
- `ledger`
- `case_id`
- `object_id`
- `fixed_psnr_lowres`
- `method_psnr_lowres`
- `psnr_gain_over_fixed_lowres`
- `better_than_fixed`

Needed normalization:

- rename `case_id` to `aberration_id` or document if it is not purely aberration keyed
- rename `fixed_psnr_lowres` to `psnr_fixed`
- rename `method_psnr_lowres` to `psnr_method`
- rename `psnr_gain_over_fixed_lowres` to `psnr_gain`
- add explicit `dataset_name` if relevant

### `results/unified_comparison/unified_comparison_per_seed.csv`

Current fields:

- `method`
- `seed`
- `mean_psnr_gain`
- `better_than_fixed_fraction`

Needed normalization:

- add `ledger` if this table is retained as a pooled per-seed table
- add `n_samples`
- keep this table as a summary table, not a detail table

### `results/unified_comparison_ci.csv`

Current fields:

- `method`
- `mean_psnr_gain`
- `std`
- `95% CI`
- `better_than_fixed_fraction`

Needed normalization:

- replace `95% CI` string column with numeric `ci_low` and `ci_high`
- add `n_seeds`
- add `n_samples`

### `results/tables/unified_comparison_by_ledger.csv`

Current fields:

- `method`
- `ledger`
- `mean_psnr_gain`
- `better_than_fixed_fraction`

Needed normalization:

- add `std_psnr_gain`
- add `ci_low`
- add `ci_high`
- add `n_seeds`
- add `n_samples`

### `results/tables/method_fairness_table.csv`

Current fields:

- `method`
- `optical_trainable_parameters`
- `digital_trainable_parameters`
- `uses_reference_psf_at_test_time`
- `retrained_for_heldout_objects`
- `input_channels`
- `training_samples`
- `evaluation_protocol`

Needed normalization:

- add `comparator_role`
- add `total_trainable_parameters`
- add `uses_reference_channel_at_test_time`
- rename `training_samples` to `train_data_count`
- add `notes`

### `results/natural_objects/natural_object_metrics.csv`

Current fields:

- `case_id`
- `object_id`
- `fixed_psnr_lowres`
- `guided_psnr_lowres`
- `pipeline_psnr_lowres`
- `psnr_gain_over_fixed_lowres`
- `psnr_gap_to_guided_lowres`
- `dataset_name`
- `dataset_version`

Needed normalization:

- rename `case_id` to `aberration_id`
- rename `fixed_psnr_lowres` to `psnr_fixed`
- rename `pipeline_psnr_lowres` to `psnr_method`
- rename `guided_psnr_lowres` to `psnr_guided`
- rename `psnr_gain_over_fixed_lowres` to `psnr_gain`
- add `training_regime`
- add `seed` if repeated execution is performed

### `results/natural_objects/mixed_train_natural_object_metrics.csv`

Current fields:

- `case_id`
- `object_id`
- `fixed_psnr_lowres`
- `guided_psnr_lowres`
- `pipeline_psnr_lowres`
- `psnr_gain_over_fixed_lowres`
- `psnr_gap_to_guided_lowres`
- `dataset_name`
- `dataset_version`
- `training_regime`

Needed normalization:

- same renaming rules as above
- add `seed` if the table is reused after multi-seed aggregation

### `results/natural_objects/mixed_train_natural_object_thickstats_metrics.csv`

Current fields:

- `case_id`
- `object_id`
- `fixed_psnr_lowres`
- `guided_psnr_lowres`
- `pipeline_psnr_lowres`
- `psnr_gain_over_fixed_lowres`
- `psnr_gap_to_guided_lowres`
- `dataset_name`
- `dataset_version`
- `seed`
- `training_regime`

Needed normalization:

- same renaming rules as above
- add `better_than_fixed`
- add `sample_id` if `object_id` is not globally unique

### `results/tolerance/mixed_train_tolerance_metrics.csv`

Current fields:

- `method`
- `object_id`
- `fixed_psnr_lowres`
- `guided_psnr_lowres`
- `method_psnr_lowres`
- `psnr_gain_over_fixed_lowres`
- `seed`
- `dataset_name`
- `dataset_version`
- `perturbation_family`
- `level`
- `training_regime`

Needed normalization:

- rename `object_id` to `sample_id` or add `sample_id`
- rename `fixed_psnr_lowres` to `psnr_fixed`
- rename `method_psnr_lowres` to `psnr_method`
- rename `guided_psnr_lowres` to `psnr_guided`
- rename `psnr_gain_over_fixed_lowres` to `psnr_gain`
- rename `level` to `condition_level`
- add `condition_family`
- add `better_than_fixed`

### `results/tolerance/robust_mask_tolerance_metrics.csv`

Current fields:

- `object_id`
- `fixed_psnr_lowres`
- `robust_method_psnr_lowres`
- `psnr_gain_over_fixed_lowres`
- `seed`
- `dataset_name`
- `dataset_version`
- `perturbation_family`
- `level`
- `training_regime`

Needed normalization:

- add `method` with a stable label
- rename `object_id` to `sample_id` or add `sample_id`
- rename `fixed_psnr_lowres` to `psnr_fixed`
- rename `robust_method_psnr_lowres` to `psnr_method`
- rename `psnr_gain_over_fixed_lowres` to `psnr_gain`
- rename `level` to `condition_level`
- add `condition_family`
- add `better_than_fixed`

### `results/tolerance/robust_mask_tolerance_compare.csv`

Current fields:

- `perturbation_family`
- `level`
- `dataset_name`
- `robust_mean_psnr_gain_over_fixed_lowres`
- `robust_better_than_fixed_fraction`
- `baseline_mean_psnr_gain_over_fixed_lowres`
- `baseline_better_than_fixed_fraction`
- `gain_delta_vs_baseline`

Needed normalization:

- rename `level` to `condition_level`
- add `condition_family`
- split into long-form comparison if reuse across figures is planned
- add uncertainty columns if this file is used in the main text

### `results/failure_cases/object_shift_failure_cases.csv`

Current fields:

- `seed`
- `case_id`
- `object_id`
- `object_label`
- `defocus`
- `astig_x`
- `coma_x`
- `fixed_psnr_lowres`
- `phase_psnr_lowres`
- `psnr_gain_over_fixed_lowres`
- `failure_reason`

Needed normalization:

- rename `case_id` to `aberration_id`
- rename `object_label` to `object_family`
- rename `fixed_psnr_lowres` to `psnr_fixed`
- rename `phase_psnr_lowres` to `psnr_method`
- rename `psnr_gain_over_fixed_lowres` to `psnr_gain`
- add `method` with stable label `phase_only_stack`

## Cross-file inconsistencies that must be fixed first

1. `case_id` is used in some tables, while `seed + object_id` is used in others, and neither is consistently labeled as sample identifier versus aberration identifier.
2. `method_psnr_lowres`, `pipeline_psnr_lowres`, `phase_psnr_lowres`, and `robust_method_psnr_lowres` all represent the same conceptual field but use different names.
3. Confidence intervals are stored as a string field in one summary file and as absent fields elsewhere.
4. `level` is too generic for tolerance work and should become `condition_level`.
5. No current detailed table contains SSIM fields, even though the desired submission-grade schema reserves them.

## Immediate normalization priority

Do in this order:

1. Harmonize PSNR field names across all detailed files.
2. Harmonize identifier fields: `sample_id`, `object_family`, `aberration_id`.
3. Expand ledger and tolerance summary files with explicit uncertainty columns.
4. Add `method` and comparator labels to files that currently imply them.
5. Decide whether SSIM is available enough to be required now or should be marked as a planned field.

## Recommendation

The next concrete step should be a canonical field dictionary in CSV form, followed by either:

- script-level export updates for future reruns, or
- a normalization script that rewrites the current files into canonical tables without touching the original raw outputs.
