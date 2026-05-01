# GitHub Main-Space Gap Audit

## Scope

This audit answers two questions for the active project:

1. Has the project actually landed in the GitHub-backed long-term space?
2. Which data packages are still missing or not yet promotable inside that long-term space?

## Result summary

The answer to the first question is currently **no**.

The canonical project root exists locally at:

- `/workspace/memory/self-calibrating-diffractive-imaging-ncomms-2026-04-30T07-33-15Z`

but it is not yet tracked in the git-backed long-term repository state that currently contains:

- tracked file: `CURRENT-PROJECT-SPACE.md`
- branch present locally: `master`
- remote branch observed locally: `origin/master`

The machine-readable project manifest still declares:

- repository: `shangx108-code/opanai`
- branch: `open-ai`
- GitHub root: `self-calibrating-diffractive-imaging-ncomms-2026-04-30T07-33-15Z`

However, the current local git state shows:

- the project directory is untracked
- no local `open-ai` branch exists
- no remote `origin/open-ai` branch is visible in the current checkout

An additional GitHub-side search for the project root string and related file paths returned no matches. Therefore the current project is **not yet fully present in the GitHub-backed long-term main space**, even though the canonical path and manifest already claim that it should be.

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

1. The project root itself is not yet committed into the GitHub-backed long-term repository state.
2. Licensed benchmark-root natural-image files are absent for both `ImageNet-1k` and `COCO`.
3. The true benchmark-root output files are still missing:
   - `results/natural_objects/benchmark_root_metrics.csv`
   - `results/natural_objects/benchmark_root_per_seed.csv`
4. The tolerance package remains simulation-only and still lacks:
   - `results/tolerance/tolerance_curve_summary.csv`
   - `results/tolerance/tolerance_curve_detail.csv`
   - `results/tolerance/tolerance_plot_manifest.csv`
   - `results/tolerance/hardware_tolerance_metrics.csv`
5. The figure-level source-data folders and narrative note package are still absent.

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

The current main-space problem is not only “some data are missing.” It is a two-layer issue:

1. the GitHub-backed long-term space is not yet actually carrying this project root as tracked project content
2. even inside the canonical local project root, the benchmark-root natural-image and tolerance-closure packages are still incomplete

That means the next corrective work should happen in this order:

1. make the project root itself truly live in the GitHub-backed main space
2. stage licensed benchmark-root natural-image files
3. run benchmark-root natural-image evaluation
4. expand tolerance sweeps into uncertainty-resolved export tables
5. build figure-level source-data folders and reproducibility packaging

## Shortest next executable action

The shortest action that fixes the largest structural problem is:

1. add the full project root `self-calibrating-diffractive-imaging-ncomms-2026-04-30T07-33-15Z` into the git-backed repository state
2. keep `indexes/data-gap-inventory-v1.csv` as the authoritative missing-data checklist inside that tracked project root

Only after the project root is truly inside the GitHub-backed main space does it make sense to treat later data additions as long-term archival closure rather than local-only progress.
