# Detailed Data Completion Plan

## Purpose

This document expands the earlier brief checklist into a full execution blueprint for closing every planned `P0`, `P1`, and `P2` evidence item. The objective is not to reach a minimal submission threshold, but to build a reviewer-resistant package in which every headline claim, figure, and supplementary statement can be traced to raw data, scripts, configs, and bounded interpretation.

## Governing principle

The evidence layer must not lag behind the narrative layer. Every added result should be filed into one of four evidence statuses:

- `complete`: fully auditable and acceptable for headline claims
- `proxy-only`: real execution but still limited to project-local proxy evidence
- `simulation-only`: physically informative but not yet hardware-validating
- `missing`: still absent and cannot be implied in the text

The manuscript, supplementary note, figure captions, and source-data index must use the same status labels.

## Current script inventory

The present project already contains the following executable assets that should be reused rather than replaced:

- `scripts/run_unified_comparison_ci.py`
- `scripts/run_natural_object_evaluation.py`
- `scripts/run_mixed_train_natural_object_rerun.py`
- `scripts/run_mixed_train_natural_object_thickstats.py`
- `scripts/run_mixed_train_tolerance.py`
- `scripts/run_robust_mask_tolerance_compare.py`
- `scripts/run_real_pipeline.py`
- `scripts/generate_submission_gap_packages.py`
- `scripts/generate_object_shift_failure_cases.py`
- `scripts/check_environment.py`

New work should extend this script family with clear naming rather than introduce parallel, untracked analysis paths.

## Execution policy

- Every new result table must be reproducible from a named script and config.
- Every new figure panel must have one summary file and one raw-data file.
- Every summary CSV must have a corresponding detailed CSV or a documented reason why detail is unavailable.
- Every new evidence package must be added to the source-data index before manuscript language is strengthened.
- No result should be promoted from proxy-only to complete without changing the underlying data status.

## P0. Submission-critical work

### P0.1 Source-data index and panel ledger

#### Objective

Create a complete crosswalk between manuscript panels and the exact files that support them.

#### Required file

- `source_data/source_data_index.csv`

#### Required columns

- `figure`
- `panel`
- `section`
- `claim_supported`
- `evidence_status`
- `summary_file`
- `raw_file`
- `plot_script`
- `analysis_script`
- `config_file`
- `checksum_summary`
- `checksum_raw`
- `last_verified_utc`
- `notes`

#### Required figure coverage

- Main benchmark summary figure
- Dual-ledger split figure
- Proxy natural-image transfer figure
- Tolerance figure
- Robust-mask mitigation figure
- Failure-case figure
- All supplementary tables that directly support discussion claims

#### Detailed execution steps

1. Freeze the current figure inventory and assign provisional identifiers: `Fig1`, `Fig2`, `Fig3`, `Fig4`, `FigS1`, `TableS1`, `TableS2`.
2. For each panel, identify the exact claim sentence in the manuscript that depends on it.
3. Map each panel to:
   - one summary table used by plotting
   - one raw or detailed table containing the underlying observations
   - one analysis script
   - one plotting script if plotting is separate
   - one config file or config snapshot
4. Compute SHA-256 checksums for summary and raw files.
5. Fill `evidence_status` with `complete`, `proxy-only`, `simulation-only`, or `missing`.
6. Add a one-line `notes` field for any panel that cannot yet be promoted to headline evidence.

#### Acceptance criteria

- Every figure cited in text has a row in the index.
- Every row has non-empty `summary_file`, `raw_file`, and `analysis_script`.
- No panel in the manuscript lacks an evidence status.

### P0.2 Schema normalization for all current result families

#### Objective

Normalize current CSV and JSON outputs so reviewers do not see one naming scheme in one figure and a different naming scheme in another.

#### Required result families

- unified comparison
- dual-ledger split
- natural-object proxy rerun
- natural-object proxy thickstats
- mixed-train tolerance
- robust-mask mitigation
- failure-case package

#### Mandatory detailed fields

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

#### Detailed execution steps

1. Audit headers in:
   - `results/unified_comparison/unified_comparison_detail.csv`
   - `results/unified_comparison/unified_comparison_per_seed.csv`
   - `results/natural_objects/mixed_train_natural_object_thickstats_metrics.csv`
   - `results/tolerance/mixed_train_tolerance_metrics.csv`
   - `results/tolerance/robust_mask_tolerance_metrics.csv`
   - `results/failure_cases/object_shift_failure_cases.csv`
2. Create a canonical field dictionary.
3. For each script, update the export layer so future runs write canonical columns directly.
4. For legacy files, generate one normalization pass that rewrites them into canonical tables without altering numeric content.
5. Add a short README noting which fields are unavailable historically and why.

#### Acceptance criteria

- All detailed CSVs share the same core field names.
- A downstream plotting script can load any result family without hand-written column renaming.
- No result file used in the source-data index depends on ambiguous field meaning.

### P0.3 Full dual-ledger decomposition package

#### Objective

Make the “best average dual-ledger trade-off” claim auditable without forcing a reviewer to reconstruct the harder-ledger story from the supplement.

#### Required files

- `results/tables/unified_comparison_by_ledger.csv`
- `results/tables/unified_comparison_by_ledger_detail.csv`

#### Required summary fields

- `ledger`
- `method`
- `mean_psnr_gain`
- `std_psnr_gain`
- `ci_low`
- `ci_high`
- `better_than_fixed_fraction`
- `n_seeds`
- `n_samples`

#### Required detail fields

- `ledger`
- `seed`
- `method`
- `sample_id`
- `psnr_fixed`
- `psnr_method`
- `psnr_gain`
- `better_than_fixed`

#### Detailed execution steps

1. Re-export current unified comparison outputs from `scripts/run_unified_comparison_ci.py`.
2. Split results by ledger before any pooled aggregation.
3. Compute confidence intervals separately for each ledger and method.
4. Produce one publication-ready summary CSV and one long-form detail CSV.
5. Update the manuscript figure plan so the harder ledger can be displayed directly.

#### Acceptance criteria

- The object-family-shift weakness is visible directly in a standalone table.
- `reference_psf_deconvolution` being stronger on the harder ledger is explicit.
- The pooled result no longer hides ledger asymmetry.

### P0.4 Expanded method fairness accounting

#### Objective

Turn fairness from a qualitative defense into a quantitative, reviewer-checkable table.

#### Required file

- `results/tables/method_fairness_table.csv`

#### Required columns

- `method`
- `comparator_role`
- `optical_trainable_parameters`
- `digital_trainable_parameters`
- `total_trainable_parameters`
- `uses_reference_psf_at_test_time`
- `uses_reference_channel_at_test_time`
- `train_data_count`
- `input_channels`
- `retrained_for_heldout_objects`
- `preprocessing_shared`
- `evaluation_protocol`
- `notes`

#### Required interpretation changes

- `reference_psf_deconvolution` must be labeled `reference-guided classical comparator`
- `phase_only_stack` must state the optical versus digital split explicitly
- all models must indicate whether test-time PSF information is available

#### Detailed execution steps

1. Derive exact parameter counts for all current comparators.
2. Add a column for whether explicit test-time PSF or reference information is used.
3. Add a column for comparator role so “baseline” is not overloaded.
4. Create a supplementary interpretation paragraph keyed to the table.

#### Acceptance criteria

- Reviewers can see immediately that optical and digital degrees of freedom are separated.
- The special status of `reference_psf_deconvolution` is explicit.
- The table can stand alone without narrative rescue.

### P0.5 Parameter-matched digital surrogate

#### Objective

Add the missing fairness control that wording alone cannot replace.

#### Deliverable

A digital-only comparator with approximately matched trainable capacity to the digital stage used by `phase_only_stack`.

#### New scripts expected

- `scripts/run_parameter_matched_digital_surrogate.py`
- optional helper config under `config/`

#### Required outputs

- per-seed result CSV
- sample-level detailed CSV
- ledger-resolved summary
- fairness-table row
- source-data index entries

#### Design requirements

- same training data
- same two ledgers
- same low-resolution target size
- no optical trainable parameters
- digital trainable parameter count matched as closely as practical

#### Detailed execution steps

1. Fix the target parameter budget from the current ridge stage.
2. Choose the simplest digital surrogate architecture that matches capacity without introducing a new modeling story.
3. Run the same seed schedule and aggregation rules as the main benchmark.
4. Export results into the same canonical schema as the other methods.
5. Insert the comparator into pooled and ledger-resolved benchmark tables.

#### Acceptance criteria

- The fairness table has no missing comparator slot.
- The main results can discuss whether the optical frontend still helps after capacity matching.
- This comparator is available before any stronger optical-advantage claim is made.

## P1. Strongly recommended evidence upgrades

### P1.1 Licensed benchmark-root natural-image evaluation

#### Objective

Replace proxy-only realism evidence with actual benchmark-root execution.

#### Required inputs

- licensed `ImageNet-1k / ILSVRC2012 validation`
- licensed `COCO 2017 validation`

#### Required outputs

- frozen subset manifest
- license note
- preprocessing log
- per-image metrics CSV
- per-seed summary CSV
- benchmark-root summary table
- source-data index entries marked `complete`

#### Recommended file targets

- `results/natural_objects/benchmark_root_subset_manifest.csv`
- `results/natural_objects/benchmark_root_metrics.csv`
- `results/natural_objects/benchmark_root_per_seed.csv`
- `results/natural_objects/benchmark_root_summary.csv`
- `results/natural_objects/benchmark_root_readme.md`

#### Detailed execution steps

1. Verify availability and path of licensed dataset roots.
2. Freeze subset-selection logic before running any method.
3. Ensure preprocessing is identical across all methods.
4. Run the baseline and mixed-training pipeline on the frozen benchmark-root subsets.
5. Export per-image and per-seed metrics in canonical schema.
6. Compare benchmark-root results to proxy-only results and explicitly record where the proxy was faithful or misleading.

#### Acceptance criteria

- The manuscript can say `ImageNet-1k` and `COCO` without the word `proxy`.
- A reviewer can inspect the subset manifest and preprocessing parity directly.
- Benchmark-root results either support the current text or force a documented claim narrowing.

### P1.2 Full tolerance matrix closure

#### Objective

Upgrade the current first-pass simulated tolerance diagnosis into a systematic tolerance package.

#### Required branches

- reference-channel intensity noise
- reference-channel misregistration
- propagation-distance error
- phase-mask quantization
- phase-mask lateral shift
- finer subpixel shift sweep

#### Required outputs

- `results/tolerance/tolerance_curve_summary.csv`
- `results/tolerance/tolerance_curve_detail.csv`
- `results/tolerance/tolerance_plot_manifest.csv`
- figure-ready panel data files

#### Detailed execution steps

1. Extend `scripts/run_mixed_train_tolerance.py` to support denser level sweeps.
2. Add uncertainty estimation at each perturbation level.
3. Ensure common perturbations and phase-mask-only perturbations remain separated.
4. Export both summary and detail tables in canonical schema.
5. Re-run `scripts/run_robust_mask_tolerance_compare.py` against the expanded tolerance grid.

#### Acceptance criteria

- Every plotted tolerance branch has confidence intervals.
- The unresolved `2 px` shift failure is quantified rather than only mentioned.
- The package can support one main-text figure and one supplementary detail figure.

### P1.3 Figure-level source-data folders

#### Objective

Package source data the way high-standard journals expect to receive it.

#### Required folder structure

- `source_data/Fig1/`
- `source_data/Fig2/`
- `source_data/Fig3/`
- `source_data/Fig4/`
- `source_data/FigS1/`

#### Required contents in each folder

- panel-level CSVs
- plotting script
- config snapshot
- short README
- checksum manifest

#### Detailed execution steps

1. Build each folder directly from the source-data index.
2. Copy only final files, not exploratory intermediates.
3. Add a one-paragraph README explaining what each file supports.
4. Verify that every manuscript panel can be rebuilt from its folder alone.

#### Acceptance criteria

- A reviewer or editor can navigate figure-by-figure evidence without reading code first.
- The source-data package mirrors the manuscript structure.

### P1.4 Figure-ready benchmark narrative package

#### Objective

Prevent the main figures from carrying hidden interpretation burdens.

#### Required outputs

- figure-specific caption note
- one-sentence claim boundary per figure
- cross-reference from figure to source-data folder

#### Detailed execution steps

1. For each figure, write one approved claim sentence.
2. For each figure, write one forbidden overclaim sentence.
3. Store both in a figure-note file adjacent to the source-data folder.

#### Acceptance criteria

- Future caption edits cannot accidentally outrun the evidence.

## P2. Optional but high-value strengthening

### P2.1 Fabricated-device or experimental closure

#### Objective

Provide at least one real-world anchor so the optics story is not entirely simulation-defined.

#### Minimum acceptable package

- device description
- fabrication note
- alignment procedure note
- one representative restoration comparison
- one tolerance-relevant observation

#### Suggested outputs

- `results/experimental/device_description.md`
- `results/experimental/alignment_log.csv`
- `results/experimental/restoration_comparison.csv`
- `results/experimental/experimental_summary.md`

#### Acceptance criteria

- Even if small, the package must be real enough to support a bounded experimental statement.

### P2.2 Physical-validity supplement note

#### Objective

Close the “simulation-defined optics” criticism without pretending to solve full high-NA physics.

#### Required file

- `manuscript/propagation-validity-note.md`

#### Required contents

- Fresnel approximation statement
- sampling choices
- numerical regime
- why vectorial or higher-NA corrections are not claimed here
- explicit validity boundary

#### Acceptance criteria

- A physics-facing reviewer can see that the approximation is deliberate and bounded.

### P2.3 Reproducibility manifest

#### Objective

Make the whole project easier to audit and rerun.

#### Required file

- `archive/reproducibility_manifest.json`

#### Required fields

- environment
- python version
- package versions
- script inventory
- config inventory
- result inventory
- hash inventory

## Phase order and dependency graph

### Phase A. Traceability lock

- P0.1 source-data index
- P0.2 schema normalization
- P0.3 ledger decomposition

Reason:

- no later evidence should be added before traceability is fixed

### Phase B. Fairness closure

- P0.4 expanded fairness table
- P0.5 parameter-matched digital surrogate

Reason:

- closes the most direct reviewer criticism against the current benchmark

### Phase C. Realism closure

- P1.1 benchmark-root natural-image evaluation
- P1.2 tolerance matrix closure

Reason:

- upgrades realism from proxy-only to more submission-grade evidence

### Phase D. Packaging closure

- P1.3 figure-level source-data folders
- P1.4 figure-ready narrative package
- P2.3 reproducibility manifest

### Phase E. Physics and experiment strengthening

- P2.1 experimental closure
- P2.2 physical-validity supplement note

## Recommended execution order

1. Create `source_data/source_data_index.csv`.
2. Normalize schemas across all existing result exports.
3. Finalize `unified_comparison_by_ledger` and fairness table updates.
4. Implement and run the parameter-matched digital surrogate.
5. Stage licensed benchmark-root datasets and run real natural-image evaluation.
6. Expand tolerance sweeps with uncertainty export.
7. Build figure-level source-data folders and manifests.
8. Add experimental and physical-validity strengthening if feasible.

## Reviewer-risk mapping

### Risk 1. “Overall best” is driven by the easier ledger

Closed by:

- P0.3 dual-ledger decomposition
- P0.5 parameter-matched surrogate

### Risk 2. Proxy-natural evidence is too central

Closed by:

- P1.1 benchmark-root natural-image execution
- figure-level evidence status labeling

### Risk 3. Hardware robustness is overstated

Closed by:

- P1.2 full tolerance matrix closure
- P2.1 experimental closure

### Risk 4. Optical contribution is confounded by digital capacity

Closed by:

- P0.4 expanded fairness table
- P0.5 parameter-matched digital surrogate

### Risk 5. Optics model is too simulation-defined

Closed by:

- P2.2 physical-validity supplement note
- P2.1 experimental closure

## Immediate owner checklist

- [ ] Build `source_data/source_data_index.csv`
- [ ] Audit and normalize all existing CSV schemas
- [ ] Finalize `results/tables/unified_comparison_by_ledger.csv`
- [ ] Expand `results/tables/method_fairness_table.csv`
- [ ] Implement `scripts/run_parameter_matched_digital_surrogate.py`
- [ ] Prepare benchmark-root subset manifest and license note
- [ ] Run benchmark-root natural-image evaluation
- [ ] Expand tolerance sweeps and export uncertainty tables
- [ ] Build figure-level source-data folders
- [ ] Draft propagation-validity note
- [ ] Scope experimental closure package
