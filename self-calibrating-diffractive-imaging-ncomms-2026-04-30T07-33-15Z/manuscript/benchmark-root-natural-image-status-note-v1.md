# Benchmark-Root Natural-Image Status Note

## Historical status

This note is retained as a historical record of why the benchmark-root `ImageNet-1k` / `COCO` branch was not executable in the active root on `2026-05-01`. It is no longer the active natural-image execution path for the manuscript.

## Active replacement path

The active natural-image branch now uses staged public-open-data subsets from `Kodak-PCD0992` and `UCID-1338`, with frozen manifests under:

- `results/natural_objects/public_dataset_protocol.md`
- `results/natural_objects/public_dataset_download_manifest.csv`
- `results/natural_objects/public_dataset_download_manifest.json`

Current manuscript wording should therefore follow the public Kodak/UCID protocol rather than the old proxy-only benchmark-root contingency described below.

## Purpose

This note consolidates the current status of the planned benchmark-root natural-image evaluation for `ImageNet-1k / ILSVRC2012 validation` and `COCO 2017 validation`. It is intended to support manuscript-safe wording, supplementary clarification, and the next execution handoff.

## Search outcome as of 2026-05-01

On `2026-05-01`, a direct search of the active project root and the connected Google Drive workspace did not identify any licensed benchmark-root validation files for `ImageNet-1k / ILSVRC2012 validation` or `COCO 2017 validation`.

### Local project-root search

The expected staging directories exist:

- `data/natural_objects/imagenet-1k-ilsvrc2012-validation`
- `data/natural_objects/coco-2017-validation`

However, both directories currently contain only project-local placeholder PNG files:

- `imagenet_proxy_000.png` through `imagenet_proxy_011.png`
- `coco_proxy_000.png` through `coco_proxy_011.png`

The benchmark-root audit therefore classifies both staged roots as `proxy_only`, not as benchmark-root ready.

### Connected Drive search

Keyword searches for `ImageNet ILSVRC2012 validation`, `COCO 2017 validation`, `imagenet`, `ILSVRC`, `val2017`, and related variants returned no matching Drive results that could be used as licensed benchmark-root evaluation inputs.

## What has already been executed

The natural-image branch is not empty. It already contains three execution-valid but explicitly proxy-only result packages.

### 1. Synthetic-only proxy natural-object evaluation

Source: `logs/iteration-017-proxy-natural-object-eval.md`

- `ImageNet-1k` proxy subset:
  - mean PSNR gain over fixed: `-10.3924 dB`
  - better-than-fixed fraction: `0.0`
- `COCO` proxy subset:
  - mean PSNR gain over fixed: `-12.8547 dB`
  - better-than-fixed fraction: `0.0`

Interpretation: the original synthetic-only pipeline fails strongly on proxy natural images.

### 2. Mixed-train proxy natural rerun

Source: `logs/iteration-018-mixed-train-natural-rerun.md`

- `ImageNet-1k` proxy subset:
  - mean PSNR gain over fixed: `+0.7458 dB`
  - better-than-fixed fraction: `0.7639`
- `COCO` proxy subset:
  - mean PSNR gain over fixed: `+1.3334 dB`
  - better-than-fixed fraction: `0.8750`

Interpretation: adding proxy-natural images to the training distribution flips the sign from strongly negative to positive on both proxy datasets.

### 3. Mixed-train proxy natural thickened validation

Source: `logs/iteration-019-mixed-train-thickstats.md`

- `ImageNet-1k` proxy thickstats:
  - mean PSNR gain over fixed: `+0.9841 dB`
  - 95% CI half-width: `0.2501 dB`
  - mean better-than-fixed fraction: `0.7736`
- `COCO` proxy thickstats:
  - mean PSNR gain over fixed: `+1.4520 dB`
  - 95% CI half-width: `0.1370 dB`
  - mean better-than-fixed fraction: `0.9111`

Interpretation: the sign improvement remains positive after thickening and is not a one-seed artifact inside the proxy setup.

## What can be claimed now

The current project root supports the following narrower statement:

> Under project-local proxy natural-image stress tests, the baseline synthetic-only pipeline fails strongly, whereas mixed training with proxy natural images produces a reproducible positive mean PSNR gain over the fixed baseline on both `ImageNet-1k`-matched and `COCO`-matched proxy subsets.

The current project root does **not** support the following stronger statement:

> The method has been validated on licensed benchmark-root `ImageNet-1k` or `COCO` validation images.

That stronger statement remains unsupported because no licensed benchmark-root files are currently staged in the active execution root.

## Manuscript-safe wording

If the manuscript must mention the natural-image branch before benchmark-root execution is available, the wording should remain explicit and bounded.

### Safe version

> To probe whether the strong synthetic-only failure primarily reflected a training-distribution mismatch, we constructed project-local proxy natural-image subsets matched to the planned `ImageNet-1k` and `COCO` preprocessing protocol. Under this proxy-only stress test, the synthetic-only pipeline became strongly negative, whereas mixed training with proxy natural images restored a positive mean PSNR gain over the fixed baseline on both datasets. These results are informative about distribution alignment, but they do not constitute benchmark-root `ImageNet-1k` or `COCO` validation.

### Unsafe version to avoid

> We validated the method on `ImageNet-1k` and `COCO`.

## Planned benchmark-root upgrade path

According to `manuscript/data-completion-plan-v2-detailed.md`, the `P1.1` target remains:

1. stage licensed `ImageNet-1k / ILSVRC2012 validation` files
2. stage licensed `COCO 2017 validation` files
3. freeze subset selection before rerunning any method
4. rerun the natural-object pipeline on benchmark-root subsets
5. export:
   - `results/natural_objects/benchmark_root_subset_manifest.csv`
   - `results/natural_objects/benchmark_root_metrics.csv`
   - `results/natural_objects/benchmark_root_per_seed.csv`
   - `results/natural_objects/benchmark_root_summary.csv`
   - `results/natural_objects/benchmark_root_readme.md`
6. compare benchmark-root results against the proxy branch and document where the proxy branch was faithful or misleading

## Immediate blocker

The blocker is now precise and auditable:

- the expected dataset roots exist
- they are not empty
- but every staged file is still a project-local proxy placeholder

Therefore the bottleneck is no longer directory discovery or script readiness. It is the absence of licensed benchmark-root raw files in the audited staging roots.

## Next executable action

Copy or mount the licensed benchmark-root validation images into:

- `data/natural_objects/imagenet-1k-ilsvrc2012-validation`
- `data/natural_objects/coco-2017-validation`

and then rerun:

- `scripts/run_natural_object_evaluation.py`

Only after that rerun should the manuscript drop the `proxy-only` qualifier from the natural-image branch.
