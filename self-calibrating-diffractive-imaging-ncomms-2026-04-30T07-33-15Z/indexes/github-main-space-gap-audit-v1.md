# GitHub Main-Space Gap Audit

## Scope

This audit answers two questions for the active project:

1. Has the project actually landed in the GitHub-backed long-term space?
2. Which data packages are still missing or not yet promotable inside that long-term space?

## Result summary

The answer to the first question is now **yes**.

The canonical project root exists locally at:

- `/workspace/memory/self-calibrating-diffractive-imaging-ncomms-2026-04-30T07-33-15Z`

and it is now tracked in the GitHub-backed long-term repository state at:

- repository: `shangx108-code/opanai`
- branch: `open-ai`
- GitHub root: `self-calibrating-diffractive-imaging-ncomms-2026-04-30T07-33-15Z`

The machine-readable project manifest declares:

- repository: `shangx108-code/opanai`
- branch: `open-ai`
- GitHub root: `self-calibrating-diffractive-imaging-ncomms-2026-04-30T07-33-15Z`

The current alignment check shows:

- local project files: `475`
- GitHub-tracked project files: `465`
- missing GitHub-side substantive files: `0`
- local-only non-authoritative files: `10` under `scripts/__pycache__/`

Blob-hash comparison across the shared file set shows that the substantive tracked project files are now aligned between the active local mirror and the GitHub long-term main space. Therefore the current project **is now present in the GitHub-backed long-term main space**.

## Natural-image validation-file check

The benchmark-root validation-file search is also negative in the current long-term space.

### What exists

- `data/natural_objects/imagenet-1k-ilsvrc2012-validation`
- `data/natural_objects/coco-2017-validation`

### What is inside

Only proxy placeholder PNG files:

- `imagenet_proxy_000.png` through `imagenet_proxy_011.png`
- `coco_proxy_000.png` through `coco_proxy_011.png`

### What does not exist

- licensed `ImageNet-1k / ILSVRC2012 validation` benchmark-root files
- licensed `COCO 2017 validation` benchmark-root files

Therefore the current benchmark-root natural-image branch remains `proxy-only`, not `complete`.

## Still-missing data in the project main space

The current missing-data inventory is recorded in:

- `indexes/data-gap-inventory-v1.csv`

The highest-priority gaps are:

1. Licensed benchmark-root natural-image files are absent for both `ImageNet-1k` and `COCO`.
2. The true benchmark-root output files are still missing:
   - `results/natural_objects/benchmark_root_metrics.csv`
   - `results/natural_objects/benchmark_root_per_seed.csv`
3. The tolerance package remains simulation-only and still lacks:
   - `results/tolerance/tolerance_curve_summary.csv`
   - `results/tolerance/tolerance_curve_detail.csv`
   - `results/tolerance/tolerance_plot_manifest.csv`
   - `results/tolerance/hardware_tolerance_metrics.csv`
4. The figure-level source-data folders and narrative note package are still absent.

## Evidence-status view

From `source_data/source_data_index.csv`, the current evidence-status distribution is:

- `complete`: 6 items
- `proxy-only`: 3 items
- `simulation-only`: 4 items

The non-complete items are:

- `Fig2A`: synthetic-only proxy natural-image failure package
- `Fig2B`: mixed-train proxy natural-image recovery package
- `Fig3A`: common-perturbation tolerance package
- `Fig3B`: dominant-vulnerability tolerance package
- `Fig4A`: robust-mask mitigation package
- `Fig4B`: residual `2 px` shift failure package
- `TableS4A`: benchmark-root natural-image blocker audit

## Practical interpretation

The current main-space problem is no longer GitHub placement. It is now a data-completeness issue:

1. the benchmark-root natural-image branch is still proxy-only
2. the tolerance-closure exports are still incomplete

That means the next corrective work should happen in this order:

1. stage licensed benchmark-root natural-image files
2. run benchmark-root natural-image evaluation
3. expand tolerance sweeps into uncertainty-resolved export tables
4. build figure-level source-data folders and reproducibility packaging

## Shortest next executable action

The shortest action that fixes the largest remaining evidence problem is:

1. stage licensed benchmark-root natural-image files into the audited dataset roots
2. keep `indexes/data-gap-inventory-v1.csv` as the authoritative missing-data checklist for the remaining evidence gaps

From this point onward, later data additions can be treated as normal long-term archival updates rather than recovery of a missing GitHub project root.
