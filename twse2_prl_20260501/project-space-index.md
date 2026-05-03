# Long-Term Project Space Index

Project: `twse2_prl_20260501`
Created: `2026-05-01T00:00:00Z`
Canonical project space: `/workspace/memory/twse2_prl_20260501`
Source snapshot copied from: `/workspace/twse2_prl_20260501`
Active target journal: `Nature Communications`

## Purpose

This folder is the long-term project space for the current tWSe2 transport
project. It now serves the `Nature Communications` revision line, while still
retaining the earlier PRL-oriented scaffold and intermediate artifacts as
source material.

## Current contents

- runnable source code for the minimal model
- shared parameter configuration
- generated WP1 and WP2 result files
- a first WP3 conductance-proxy follow-up for candidate-resolved observable screening
- a PRL-style manuscript draft derived from the current minimal outputs
- a slice-matched alpha-rule to semi-infinite BTK correlation package dated `2026-05-02`
- a channel-resolved multiorbital BTK verification package dated `2026-05-02`
- an internal `r_he(E)` onset-tracking package dated `2026-05-02` that shows
  `Delta_in` tracking from the anomalous-reflection kernel itself
- a kernel-invariance proof package dated `2026-05-02` for orbital-basis and
  interface-mixing robustness of the alpha-window
- a transport-validation package dated `2026-05-03` that closes threshold,
  broadening, barrier, and internal `r_he` particle-hole consistency checks
- a full-S normal-incidence transport audit dated `2026-05-03` that adds
  explicit `r_ee/r_eh/r_he/r_hh` blocks plus unitarity and particle-hole
  closure tables
- a Nature Communications revision tracker dated `2026-05-03` that maps the
  detailed revision memo to current evidence, missing controls, and execution
  order
- a Nature Communications execution-status check dated `2026-05-03` that
  records what has already been executed, what remains partial, and what is
  still missing for the current revision line
- an observable / constraint / negative-control audit dated `2026-05-03` that
  defines `G(E)=int dk_y Tr(r_he^dagger r_he)`, builds an executable
  `W_alpha(E)` proxy, and checks the same-pipeline trivial `s`-wave failure
- a convergence and reproducibility suite dated `2026-05-03` under
  `results/convergence_reproducibility_suite_2026-05-03/`, including explicit
  energy-grid scans, Fermi-surface / angular discretization scans, runtime
  manifest, rerun commands, and file inventory
- an E4-to-E11 manuscript-support package dated `2026-05-03` under
  `results/e4_to_e11_package_2026-05-03/`, tying the saved transport,
  invariance, convergence, negative-control, methods, reviewer-response,
  and submission-checklist lines into one continuous NC-facing ledger
- a full Nature Communications submission package dated `2026-05-03` under
  `submission_package_nc_2026-05-03/`, including revised main text,
  supplementary information, figures, source-data workbook, response summary,
  and compiled PDFs
- a manuscript-ready transport result patch dated `2026-05-02` that merges the
  internal `r_he(E)` onset proof with the kernel-invariance closure
- a full PRL-style manuscript draft v2 dated `2026-05-03` with the transport
  closure integrated into the main text
- a PRL-compressed manuscript draft v3 dated `2026-05-03` with tighter title,
  abstract, lead introduction, and Results compression
- top-level README for rerunning the scaffold

## Working rule

From this point onward, new project data for this chat should be saved here
first, then mirrored elsewhere only when needed.

All future iterations for this project should prioritize strictly completing
the missing checks, controls, and revisions required by reviewer-style comments
or formal review feedback, rather than opening new side branches.

All future data, scripts, results, notes, manuscript files, and other project
artifacts generated in this chat must be synchronized into this directory as
the canonical GitHub-backed long-term project space.

After every substantive run, the newly generated scripts, tables, figures,
markdown notes, and summary files should be copied or written back into this
long-term project space before the turn is considered closed.

All substantive project data updates in this directory should also be committed
and pushed to the attached GitHub remote, so later sessions can inspect the
latest available files directly from the long-term project space.

The file `sync-status.md` should be refreshed after each substantive turn by
running `python scripts/update_sync_status.py`, so this project always carries a
local audit of its GitHub sync state.
