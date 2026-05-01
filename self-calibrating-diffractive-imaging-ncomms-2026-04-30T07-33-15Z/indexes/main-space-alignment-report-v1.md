# Main-Space Alignment Report

## Scope

This report records the current alignment status of the active project against its canonical long-term root:

- `self-calibrating-diffractive-imaging-ncomms-2026-04-30T07-33-15Z`

## What was aligned in this round

Historical project materials scattered across related directories were imported into the canonical root under:

- `archive/legacy_imports/`
- `archive/input_sources/`

The file-level record is:

- `archive/legacy_import_alignment_manifest.csv`

The summary is:

- total manifest rows: `208`
- newly copied files: `174`

Imported sources:

- `memory-self-calibrating-diffractive-ncomms`
- `tmp-self-calibrating-diffractive-ncomms`
- `tmp-self-calibrating-diffractive-ncomms-20260429-134216`
- `tmp-self-calibrating-diffractive-ncomms-20260430T010105Z`
- `user_files`

These imports now preserve:

- earlier manuscript drafts and review materials
- round6 code and outputs
- historical submission-package files
- early project state and supervision notes
- user-provided concept and review-source texts

## What is now true

The canonical long-term root now contains the currently visible project history that was previously spread across temporary or predecessor locations. In that sense, the project data are now locally aligned to the canonical long-term root.

## What is still not complete

Local alignment does **not** yet mean full GitHub archival closure.

The remaining highest-priority gaps are:

1. the project root is still not tracked in the git-backed repository state
2. licensed benchmark-root `ImageNet-1k / ILSVRC2012 validation` files are still missing
3. licensed benchmark-root `COCO 2017 validation` files are still missing
4. benchmark-root natural-image result files are still absent:
   - `results/natural_objects/benchmark_root_metrics.csv`
   - `results/natural_objects/benchmark_root_per_seed.csv`
5. tolerance-closure exports are still absent:
   - `results/tolerance/tolerance_curve_summary.csv`
   - `results/tolerance/tolerance_curve_detail.csv`
   - `results/tolerance/tolerance_plot_manifest.csv`
   - `results/tolerance/hardware_tolerance_metrics.csv`
6. figure-level source-data folders are still absent
7. authoritative LaTeX manuscript files are still absent:
   - `manuscript/main.tex`
   - `manuscript/supplement.tex`

## Authoritative gap list

The current file-by-file missing-data checklist remains:

- `indexes/data-gap-inventory-v1.csv`

The GitHub-backed main-space consistency audit remains:

- `indexes/github-main-space-gap-audit-v1.md`

## Shortest next executable action

Track the canonical project root inside the git-backed repository state, then prioritize the `P1.1` benchmark-root natural-image files because they are the strongest remaining evidence blocker.
