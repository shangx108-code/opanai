# Main-Space Alignment Report

## Scope

This report records the current alignment status of the active project against its canonical long-term root:

- `self-calibrating-diffractive-imaging-ncomms-2026-04-30T07-33-15Z`
- canonical GitHub repository: `shangx108-code/opanai`
- canonical GitHub branch: `open-ai`

For this project, the only valid long-term main space is:

- `shangx108-code/opanai` / `open-ai` / `self-calibrating-diffractive-imaging-ncomms-2026-04-30T07-33-15Z`

The local directory under `/workspace/memory/` should be interpreted as the current working mirror of that canonical path, not as a separate long-term root.

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

GitHub archival closure into the canonical `open-ai` branch path is now complete for the current local working mirror, excluding non-authoritative Python cache files under `scripts/__pycache__/`.

The remaining highest-priority gaps are:

1. licensed benchmark-root `ImageNet-1k / ILSVRC2012 validation` files are still missing
2. licensed benchmark-root `COCO 2017 validation` files are still missing
3. benchmark-root natural-image result files are still absent:
   - `results/natural_objects/benchmark_root_metrics.csv`
   - `results/natural_objects/benchmark_root_per_seed.csv`
4. authoritative LaTeX manuscript files are still absent:
   - `manuscript/main.tex`
   - `manuscript/supplement.tex`
5. experimental and physics-validity narrative closures are still absent:
   - `results/experimental/device_description.md`
   - `manuscript/propagation-validity-note.md`

## Authoritative gap list

The current file-by-file missing-data checklist remains:

- `indexes/data-gap-inventory-v1.csv`

The GitHub-backed main-space consistency audit remains:

- `indexes/github-main-space-gap-audit-v1.md`

## Shortest next executable action

Prioritize the `P1.1` benchmark-root natural-image files because they are now the single strongest remaining evidence blocker.
