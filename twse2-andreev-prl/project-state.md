# Project State

Project: `twse2-andreev-prl`
Last updated: 2026-04-29

## Current Stage

Track-1 normal-state data completion, coupled path-plus-hopping refinement, and persistent project-space build-out for a PRL-oriented twisted bilayer WSe2 Andreev manuscript.

## Current Overall Goal

Complete a manuscript-grade data package for the twse2-Andreev project: reconstruct the true-or-closest faithful Tuo tight-binding input, then generate and durably store the Fig. 1-4 evidence chain, including normal-state band benchmarks, downstream SGF / BTK / robustness arrays, and their file-level indexes in both the memory folder and Google Drive.

## Single Main Bottleneck

The project still does not have a complete, manuscript-grade normal-state data package. The current best faithful exact-`Gamma` candidate has improved to `8.367 meV` global RMSE, so the bottleneck is now a broader coupled valley-specific completion that can reduce the persistent `K^B / K^T` mismatch materially without breaking exact `Gamma` closure.

## Newly Verified Facts

- The uploaded Tuo bundle originally provided the article, SI, and source workbook.
- In later workspace snapshots, the original workbook paths were intermittently absent, so Track 1 can no longer rely on temporary workspace paths alone.
- Track 1 remains runnable because the source-band columns are mirrored in `/workspace/memory/twse2-andreev-prl/data/track1-2026-04-29/band_comparison.csv`.
- The user explicitly redirected the project so that “补齐所有数据” is the unique top priority.
- The user set the project iteration cadence to once per hour.
- All new computation and data generation in this round have been moved into the long-lived project space `/workspace/memory/twse2-andreev-prl/`.
- Google Drive read-side connectivity is available again, but the current connector surface still does not expose a usable generic upload / create path for the project artifact bundle.
- The broader `A-B` exclusion scan remains a valid local exclusion dataset, but no materially improved branch in that family satisfies the exact-`Gamma` acceptance rule.
- The `k`-path mapping scan improved the faithful candidate to `8.880 meV`.
- The shared mixed-star scan improved the faithful candidate further to `8.372 meV`.
- Independent short-range `A-C / B-C` asymmetry and independent `sqrt(7)` asymmetry were both tested as isolated layers and neither improved the best exact-`Gamma` candidate honestly.
- A coupled path-plus-hopping scan over the best path mappings and exact-`Gamma` asymmetric `sqrt(7)` branches improved the faithful baseline again to `8.367 meV`.
- A new persistent Track-1 convention scan now lives at `/workspace/memory/twse2-andreev-prl/data/track1-kclosure-2026-04-29/` and confirms that high-symmetry-point relabeling alone does not close Track 1; its best candidate still has `13.014 meV` high-symmetry RMSE.
- A new persistent SGF minimal package now lives at `/workspace/memory/twse2-andreev-prl/data/sgf-minimal-2026-04-29/`.
- A new persistent BTK minimal package now lives at `/workspace/memory/twse2-andreev-prl/data/btk-minimal-2026-04-29/`.

## Current Best Reconstruction Status

- Real-space geometry still most consistently matches a three-color triangular-lattice embedding of the A/B/C Wannier centers.
- The old exact-`Gamma` all-constant `A-B` baseline remains reproducible at `10.255 meV` global RMSE.
- The best exact-`Gamma` path-mapping candidate improved that to `8.880 meV`.
- The best exact-`Gamma` shared mixed-star candidate improved that further to `8.372 meV`.
- The current best faithful coupled path-plus-hopping candidate improves the exact-`Gamma` baseline again to `8.367 meV`.
- The dominant unresolved residual is no longer at `M`; it remains concentrated in the two valley windows `K^B / K^T`.
- The honest status is: Track 1 is materially stronger and much better indexed than before, but exact full-band faithful reproduction is still open.

## Evidence Ledger Snapshot

- Tuo article / SI / source-data ingestion: closed
- Source-band fallback mirror for Track 1: closed
- Full lattice-vector hopping table: in progress
- Reconstructed `H_TB(k)` from hopping table: in progress
- `A-B` convention exclusion scan package: closed locally, pending cloud sync
- `k`-path mapping scan package: closed locally, pending cloud sync
- Shared mixed-star scan package: closed locally, pending cloud sync
- Asymmetric short-range exclusion scan package: closed locally, pending cloud sync
- Asymmetric `sqrt(7)` exclusion scan package: closed locally, pending cloud sync
- Coupled path-plus-hopping scan package: closed locally, pending cloud sync
- Track-1 convention-scan package in persistent project space: closed locally, pending cloud sync
- Manuscript-grade normal-state data package with indexed artifacts: partial
- SGF benchmark data package: partial
- BTK / robustness data package: partial
- Memory-folder persistence for current Track-1, SGF, and BTK minimal artifacts: closed
- Google Drive persistence for current artifacts: blocked by missing upload surface
- Replace current `H_kp` with true Tuo TB in manuscript files: not started
- Rerun Fig. 1-4 with true Tuo TB in manuscript files: not started

## Immediate Next Action

1. Keep the `8.367 meV` coupled path-plus-hopping candidate as the faithful Track-1 baseline.
2. Continue coupled valley-specific completion in the persistent project space instead of reopening exhausted isolated scans.
3. Upgrade the SGF minimal package from a finite-ribbon edge proxy toward a manuscript-grade semi-infinite benchmark.
4. Upgrade the BTK minimal package from a proxy package toward a material-specific conductance benchmark.
5. Mirror every newly accepted artifact into memory immediately and keep Google Drive sync in the explicit pending queue until a writable connector surface becomes available.
