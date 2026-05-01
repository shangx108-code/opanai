# Data Status Audit

Project: `twse2-andreev-prl`  
Audit date: 2026-05-01

## Scope

This audit checks the canonical long-term project space
`/workspace/memory/twse2-andreev-prl-2026-04-29T13-43-41Z` against the current
project-state, archive checklist, and visible local data packages.

## Present and readable

- Track-1 baseline and all main exclusion / correction branches are present in
  `data/track1-*`.
- SGF packages are present:
  - `sgf-minimal-2026-04-29`
  - `sgf-kspace-sparse-v3-trial-2026-04-29`
  - `sgf-semi-infinite-kspace-sparse-v3-2026-04-29`
- BTK packages are present:
  - `btk-minimal-2026-04-29`
  - `btk-generalized-valley-resolved-2026-04-29`
  - `btk-generalized-valley-resolved-semi-infinite-2026-04-29`
- New WP3 packages are present:
  - `wp3-alpha-z-phi-generalized-btk-2026-05-01`
  - `wp3-alpha-z-phi-generalized-btk-upgraded-2026-05-01`
  - `wp3-control-discriminant-2026-05-01`
- Manuscript assets are now present locally:
  - `prl-manuscript-draft-2026-05-01.tex`
  - `prl-manuscript-draft-2026-05-01.bib`
  - Figure 4 replacement text blocks

## Still missing or not yet closed

1. No final manuscript-grade rerun of Fig. 1-4 with the true Tuo-TB input is
   present.
2. No final SGF manuscript-grade benchmark package is present under a dedicated
   finalized path.
3. No final BTK / robustness manuscript-grade benchmark package is present under
   a dedicated finalized path.
4. No actual figure asset files for the manuscript are present yet:
   `fig1_schematic.pdf`, `fig2_selectivity.pdf`, `fig3_fingerprints.pdf`,
   `fig4_control_discriminant.pdf` are all still placeholders in the draft.
5. Google Drive sync remains incomplete because no writable upload surface is
   available in this session.
6. Direct GitHub repository linkage is still absent in this session, so the
   long-term project space is local-only rather than verified as mirrored into a
   live GitHub branch.

## Items that were historically available but are not currently in the canonical root

1. The original source workbook and archive are not present as stable files in
   the canonical long-term project root, even though derivative mirrors and
   downstream outputs remain available.
2. The true manuscript main source before this round was absent; this is now
   partially repaired by the new PRL draft, but not by an inherited original
   author manuscript file.

## Practical conclusion

No core computed package from Track-1, SGF, BTK, or WP3 appears to have been
silently lost from the canonical local long-term space. The real gaps are not
random missing folders; they are higher-level missing closures:

- final figure-asset generation,
- final true-Tuo-TB reruns for manuscript figures,
- final manuscript-grade SGF and BTK benchmark bundles,
- and remote persistence to Google Drive / GitHub.
