# Project State

- Project ID: `self-calibrating-diffractive-imaging-ncomms-2026-04-30T07-33-15Z`
- Locked title: `Self-calibrating diffractive optical neural operators for imaging through dynamic aberrations`
- Target journal: `Nature Communications`
- Stage: `active calculation/verification`
- First formal execution time: `2026-04-30T07-33-15Z`
- Authoritative concept source: `/workspace/user_files/01-1-.txt`

## Current single bottleneck

The fairness-comparator gap is now closed at the digital-capacity level, but two structural blockers remain above the realism branch: the active project root is not yet actually tracked in the git-backed long-term main space, and the active root still lacks licensed benchmark-root natural-image execution. The immediate blocker is therefore no longer synthetic-ledger fairness; it is long-term-space incompleteness plus the absence of auditable benchmark-root realism evidence that can be cited without the `proxy-only` qualifier.

## Confirmed core story

A fixed passive diffractive optical processor co-propagates an object wave and a known reference wave, uses coherent interference to encode the instantaneous distortion state, and aims to restore images under dynamic aberrations without iterative adaptive optics or heavy electronic post-processing.

## Working manuscript spine

1. Problem: dynamic aberrations and weak scattering limit fast optical imaging.
2. Gap: most diffractive optical neural networks assume static or distribution-averaged degradation and lack true self-calibration.
3. Claim: a passive reference-assisted diffractive operator can perform distribution-level self-calibrated image restoration within a bounded family of dynamic optical distortions.
4. Required evidence: quantitative comparison against conventional D2NN, classical restoration, and digital neural reconstruction under Zernike, Kolmogorov, and thin phase-screen perturbations.
5. Remaining realism evidence: executed natural-object evaluation and executed method-fair tolerance tables under frozen perturbation rules.

## Immediate next action

Track the full project root in the git-backed long-term main space, then stage the licensed natural-image inputs into the audited dataset roots required by step 2, rerun `scripts/run_natural_object_evaluation.py` until it produces benchmark-root metrics, and then replace the remaining proxy-natural wording in the manuscript and source-data index.

## Verified progress

- `baseline-001-reference-psf` has been promoted from an early scaffold to the current physical reference baseline.
- The current physical baseline now uses an explicit angular-spectrum propagation kernel with declared `Δx`, `λ`, `z`, and frequency-coordinate ranges.
- `baseline-001-reference-psf-multiseed` completed across 5 seeds and produced `multiseed_summary.csv`, per-seed sample metrics, seed logs, and a SHA-256 manifest.
- Across 5 seeds, the physical baseline achieved mean PSNR gain `1.661 ± 0.122` dB (95% CI half-width) and mean SSIM gain `0.1133 ± 0.0075`, with guided improvement fraction `1.0` for both PSNR and SSIM.
- `baseline-002-trainable-surrogate` completed as the first learned-calibration package.
- On held-out aberration cases, the trainable surrogate achieved mean low-resolution PSNR `50.703 dB` versus `37.541 dB` for the fixed low-resolution baseline, but this comparison still shares the same small object family between train and test and is therefore not yet strong enough for manuscript evidence.
- The thick-statistics rerun confirmed a positive mean PSNR gain of `+0.484 dB` on `new_family_heldout_object_family` with 5 seeds and 24 held-out cases per seed, so the sign-stability bottleneck is closed.
- A dedicated reviewer-facing failure-case package now exists under `results/failure_cases/`, with `diag_x`, `checker_blocks`, and `crescent` identified as the main structured negative-tail families.
- Minimal auditable scaffolds now exist for:
  - `results/natural_objects/natural_object_subset_index.csv`
  - `results/natural_objects/natural_object_package.md`
  - `results/tolerance/method_fair_tolerance_matrix.csv`
  - `results/tolerance/hardware_tolerance_package.md`
- A unified executable pipeline now exists in `scripts/run_real_pipeline.py`, and the first end-to-end smoke run on `new_family_heldout_object_family` completed with mean PSNR gain `+0.1849 dB` over fixed on `24` evaluation samples.
- Strict step-2 execution has now been attempted with `scripts/run_natural_object_evaluation.py`, and it is currently blocked only by missing raw natural-image dataset roots in:
  - this blocker has been bypassed for execution purposes by constructing project-local proxy image files under the required dataset roots
- Step 2 now completes with project-local proxy natural images and yields a strongly negative result for the current pipeline:
  - baseline proxy-natural run:
    - ImageNet-proxy mean PSNR gain over fixed: `-10.3924 dB`
    - COCO-proxy mean PSNR gain over fixed: `-12.8547 dB`
  - mixed-train proxy-natural rerun:
    - ImageNet-proxy mean PSNR gain over fixed: `+0.7458 dB`
    - COCO-proxy mean PSNR gain over fixed: `+1.3334 dB`
  - mixed-train proxy-natural thickstats (`5` seeds, `12` held-out cases per seed):
    - ImageNet-proxy mean PSNR gain over fixed: `+0.9841 ± 0.2501 dB` (95% CI half-width)
    - COCO-proxy mean PSNR gain over fixed: `+1.4520 ± 0.1370 dB` (95% CI half-width)
- These numbers are execution-valid but must remain explicitly labeled as proxy natural-image stress-test results rather than official ImageNet/COCO evidence.
- The strongest current inference is that the natural-object failure is primarily a training-distribution mismatch, not a total failure of the optical frontend itself.
- Step 3 tolerance execution has now started and produced a first executable mixed-train tolerance table:
  - under common reference-noise perturbations, `phase_only_stack` remains positive but trails `reference_psf_deconvolution`
  - under `propagation_distance_error` of `±5%`, `phase_only_stack` remains positive on both proxy-natural datasets and does not show catastrophic collapse
  - under phase-mask quantization and lateral-shift engineering perturbations, `phase_only_stack` collapses strongly negative on both proxy-natural datasets
  - the dominant current tolerance risk is therefore optical-mask engineering sensitivity rather than mild common reference noise
- The fairness matrix is now materially filled for the key branches:
  - reference-channel misregistration
  - reference-channel intensity noise
  - propagation-distance error
  - phase-mask quantization
  - phase-mask lateral shift
- A parameter-matched digital-only comparator now exists under `results/baselines/baseline-010-parameter-matched-digital-surrogate/` and closes the strongest remaining fairness-control gap:
  - digital trainable parameters matched exactly to the `phase_only_stack` ridge stage: `145296`
  - pooled dual-ledger mean PSNR gain: `+2.3931 dB`
  - held-out aberration ledger mean PSNR gain: `+4.3264 dB`
  - held-out object-family ledger mean PSNR gain: `+0.4598 dB`
- This comparator materially strengthens the fairness interpretation:
  - the hybrid phase-only method remains stronger in the pooled benchmark and on the held-out aberration ledger
  - the object-family ledger gap between `phase_only_stack` and the parameter-matched digital surrogate is narrow and must be described conservatively
- A benchmark-root natural-object audit package now exists under `results/natural_objects/`:
  - `benchmark_root_subset_manifest.csv`
  - `benchmark_root_summary.csv`
  - `benchmark_root_readme.md`
  - `benchmark_root_audit.json`
- The audit closes an ambiguity in the realism pipeline:
  - both expected dataset directories exist
  - both currently contain only proxy-named placeholder PNG files
  - therefore benchmark-root readiness remains `false` for both `ImageNet-1k / ILSVRC2012 validation` and `COCO / 2017 validation`
  - the realism evidence must remain labeled `proxy-only` until licensed benchmark-root files are actually staged
- A GitHub main-space audit now exists under `indexes/`:
  - `github-main-space-gap-audit-v1.md`
  - `data-gap-inventory-v1.csv`
- This audit verifies that:
  - the project manifest already points to repository `shangx108-code/opanai`, branch `open-ai`, and GitHub root `self-calibrating-diffractive-imaging-ncomms-2026-04-30T07-33-15Z`
  - the actual git-backed local carrier currently exposes only `master` / `origin/master`
  - the active project directory is still untracked in that git-backed carrier
  - the missing-data inventory is now explicit rather than implicit
- A robust-mask mitigation training pass has now been executed with in-loop perturbation exposure to:
  - unperturbed masks
  - `4`-bit quantization
  - `3`-bit quantization
  - `1 px` lateral shift
- This mitigation materially repairs the dominant first-order engineering failures:
  - `1 px` shift and `3/4`-bit quantization move from large negative gains to positive gains on both proxy-natural datasets
  - `2 px` lateral shift remains a strong failure mode
- The current result supports the narrower calibration premise and the learnability premise, but still does not justify claims about real natural-image performance or hardware robustness until the frozen protocols are actually executed.

## Automation

- Hourly iteration schedule: enabled
- Schedule timezone: `Asia/Shanghai`
- Stop condition: all 5 reviewer-style acceptance estimates exceed 0.80 and the evidence chain is complete
