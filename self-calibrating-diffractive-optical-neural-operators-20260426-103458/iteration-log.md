# Iteration Log

## 2026-05-03 Project Canonicalization
- Locked the project identity to:
  `self-calibrating-diffractive-optical-neural-operators-20260426-103458`
- Mapped the old non-canonical memory directory into the new canonical memory
  root as historical archive material.
- Created the new local project workspace with stable subdirectories:
  `manuscript`, `results`, `scripts`, `configs`, `logs`, `archive`, `indexes`
- Added the minimum runtime verification script:
  `scripts/environment_smoke_test.py`
- Imported the user brief into `archive/project-brief-2026-05-03.txt`
- Executed the smoke test successfully with:
  - Python `3.12.13`
  - `numpy 2.3.5`
  - `Pillow 12.2.0`
  - output folder:
    `results/environment_smoke_test_2026-05-03/`

## Pending
- Upload the user project brief and smoke test outputs to GitHub when the next
  project update is pushed
- Continue project execution from this canonical root only

## 2026-05-03 Round 1 Intake to Draft
- Current stage: full draft assembly with strict evidence boundary control
- Single bottleneck: Figure 5 still cannot support a robust processor-level
  common-path advantage over ordinary D2NN
- This round completed:
  - `manuscript/round1-intake-draft.md`
  - `manuscript/round1-complete-skeleton.tex`
  - `manuscript/round1-complete-skeleton.pdf`
- This round decision:
  - The manuscript structure is now fixed enough for iterative section updates.
  - The next quantitative round should touch only the Figure 5 result package
    and its immediately dependent prose unless new evidence breaks the current
    claim boundary.

## 2026-05-14 Round24 Writer-Facing Numeric Short Table
- Current stage: writer-facing packaging closure after the evidence pack
- This round completed:
  - `results/round24_figure5_boundary_numeric_short_table.csv`
  - `submission-package/05-figure5-boundary-short-insert.tex`
  - `manuscript/round24-manuscript-absorption-note.md`
- Key quantitative anchors locked for the current writing pass:
  - round14 `CMO 0.786 +- 0.050`, `CMN/control 0.788 +- 0.031`
  - round15 `CMO 0.312 +- 0.026`, `CMN/control 0.348 +- 0.043`
  - round16 `CMO 0.542 +- 0.024`, `CMN/control 0.378 +- 0.057`
  - round17 `CMO 0.542 +- 0.024`, `CMN/control 0.464 +- 0.082`
- Reviewer-safe audit compressed to:
  - `0/4` alternate anchors changed manuscript role
  - Round17 fully stable threshold pairs `3/9`

## 2026-05-14 Submission-Package Consistency Cleanup And Backfill
- Current stage: final package naming, pointer, and wording cleanup
- This round completed:
  - created `submission-package/00-submission-package-index.md`
  - created `submission-package/01-manuscript-main.md`
  - created `submission-package/02-cover-letter-main.md`
  - created `submission-package/03-reviewer-response-main.md`
  - created `submission-package/04-language-lock.md`
  - backfilled `submission-package/05-figure5-boundary-short-insert.tex`
  - backfilled `results/round24_figure5_boundary_numeric_short_table.csv`
  - backfilled `manuscript/round24-manuscript-absorption-note.md`
- Package-level decision:
  - `00-submission-package-index.md` is now the canonical package entrypoint
  - `05-figure5-boundary-short-insert.tex` is a support insert, not a separate manuscript version
  - round24 reviewer-safe robustness wording is now part of the package primary files
