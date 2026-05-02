# Majorana Diagnostic Project-Space Index

Project key: `majorana-diagnostic-natphys`  
Target journal line: `Nature Physics`  
Index refresh date: `2026-05-02`

## Purpose

This index records the current GitHub-backed long-term project-space structure
for the compensated-magnetic / nonlocal Majorana diagnostic manuscript line.
It is meant to answer one practical question quickly: where do the manuscript,
code, results, and archived bundles now live?

## Top-level layout

- `code/`: reusable project scripts for source-data generation, Figure 4/5
  candidate rebuilds, targeted retuning, observable upgrades, and recovery
  bootstrap logic.
- `config/`: stable configuration files used by the source-data pipeline.
- `data/`: GitHub-backed numerical outputs, source-data packages, targeted
  retune tables, and figure-grade candidate bundles.
- `archive/`: zip-level long-term snapshot bundles.
- `manuscript-facing-sync-2026-05-02/`: current manuscript package snapshot,
  including main-text and supplementary PDFs, LaTeX sources, bibliography, and
  compilation placeholder figures.
- root-level markdown files: project state, archive checklist, review history,
  theory rewrite notes, upload records, and journal-positioning notes.

## Code bundle

- `code/generate_cmjj_source_data.py`
- `code/rebuild_fig4_fig5_from_candidates.py`
- `code/retune_fig4_fig5_targeted.py`
- `code/upgrade_fig5_observable_from_heatmaps.py`
- `code/majorana_recovery_bootstrap.py`

## Data bundle

- `data/cmjj-source-data-2026-05-01/`
  - figure-source subdirectories for Fig. 2 through Fig. 5
  - `manifest.json`
  - `README.md`
- `data/fig4-fig5-candidate-rebuild-2026-05-01/`
  - candidate transport heatmaps
  - window-discrimination tables
  - rebuild summary notes
- `data/fig4-fig5-targeted-retune-2026-05-01/`
  - full scan table
  - candidate-control table
  - retune summary
- `data/fig5-observable-upgrade-2026-05-01/`
  - observable heatmaps
  - observable selection table
  - upgrade summary

## Manuscript snapshot

The current compile-ready manuscript snapshot is:

- `manuscript-facing-sync-2026-05-02/submission_draft_main.tex`
- `manuscript-facing-sync-2026-05-02/submission_draft_main.pdf`
- `manuscript-facing-sync-2026-05-02/supplementary_information.tex`
- `manuscript-facing-sync-2026-05-02/supplementary_information.pdf`
- `manuscript-facing-sync-2026-05-02/submission_pack_latex_ready.tex`
- `manuscript-facing-sync-2026-05-02/references_verified.bib`
- `manuscript-facing-sync-2026-05-02/document-plan.md`
- `manuscript-facing-sync-2026-05-02/figures/`

## Important boundary

The project space is now structurally complete in the sense that manuscript
files, scripts, configurations, archived numerical outputs, and image assets are
all represented inside the same GitHub-backed directory. This does **not** mean
the scientific bottleneck is closed. The full-device topology rerun remains
blocked by the missing executable three-terminal benchmark path and dependency
barrier described in `project-state.md`.

## This round

The 2026-05-02 refresh did two things:

- extended the manuscript-facing sync to include a first clean Supplementary
  Information entry plus compiled PDFs;
- rehydrated the local long-term project space from the existing GitHub-backed
  code/data/archive directories so the local and remote project spaces again
  carry the same program/result/image structure.
