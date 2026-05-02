# Manuscript-Facing Sync 2026-05-02

This archive snapshot records the manuscript-facing text sync performed on
2026-05-02 for the compensated-magnetic Majorana diagnostic project.

## Scope of this sync

- locked the Methods / Supplement boundary around the current Fig. 4 / Fig. 5
  story;
- synchronized duplicated Fig. 4 / Fig. 5 captions across the working main
  manuscript and the LaTeX-ready submission pack;
- upgraded the Fig. 4 language to a null-calibrated ensemble test;
- upgraded the Fig. 5 language to a single prespecified nonlocal decision rule.

## Important boundary

This sync is a manuscript-discipline update only. It does not resolve the
underlying numerical blocker for the full-device topology rerun. Any claim that
depends on refreshed `nu_ring` / `P_topo` outputs remains conditional on
recovering and rerunning the missing three-terminal benchmark bundle.

## Archived files

- `submission_draft_main.tex`
- `submission_pack_latex_ready.tex`
- `submission_draft_main.pdf`
- `supplementary_information.tex`
- `supplementary_information.pdf`
- `references_verified.bib`
- `document-plan.md`

## 2026-05-02 compile follow-up

This follow-up pass extended the same manuscript-facing sync with a compiled
main-manuscript PDF and a first compilable Supplementary Information entry.

- revised the Introduction paragraph-2 citation logic so each false-positive
  source is tied to its own supporting reference;
- created `supplementary_information.tex` as a clean SI entry distilled from the
  existing supplement-facing text pack;
- compiled both the main manuscript and the Supplementary Information into PDF;
- reduced the placeholder-figure overflow by constraining the main-text figure
  height during compilation.

The current PDFs are still manuscript-structure artifacts rather than
submission-final outputs because the live figure files remain placeholders, but
the LaTeX workflow is now closed enough to regenerate both documents on demand.
