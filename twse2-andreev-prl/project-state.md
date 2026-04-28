# Project State

Project: `twse2-andreev-prl`
Last updated: 2026-04-28

## Current Stage

Results generation, data-package completion, and storage hardening for a PRL-oriented twisted bilayer WSe2 Andreev manuscript.

## Current Overall Goal

Complete a manuscript-grade data package for the twse2-Andreev project: reconstruct the true-or-closest faithful Tuo tight-binding input, then generate and durably store the Fig. 1-4 evidence chain, including normal-state band benchmarks, downstream SGF / BTK / robustness arrays, and their file-level indexes in both the memory folder and Google Drive.

## Single Main Bottleneck

The project still does not have a complete, manuscript-grade data package. The sharpest unresolved data gap remains exact `K`-point valley closure of the true Tuo TB model under the hard constraint that exact `Gamma` closure must survive, and until that normal-state foundation is closed the later SGF / BTK / robustness datasets cannot be completed honestly or archived as final evidence.

## Newly Verified Facts

- The uploaded `04-ws2.zip` contains the Tuo article, SI, and source data.
- `41467_2025_64519_MOESM3_ESM.xlsx` contains Fig. 1c energy-band arrays and Fig. 2/4 source data, but not a full hopping table.
- Supplementary Eq. (S1) lists representative onsite and hopping amplitudes for the K valley.
- Fig. S1 shows representative bonds up to fifth-nearest neighbor.
- The SI explicitly states that the full model is obtained by symmetry completion from these representative bonds.
- The Nature page states that code is only available from the corresponding author upon request.
- The arXiv preprint `2409.06779` exposes a TeX-source entry publicly, but the source archive is not retrievable from the current container due remote access restrictions.
- No editable local manuscript source for this twse2-Andreev project has appeared in the workspace as of 2026-04-27.
- On 2026-04-29, the user explicitly redirected the project so that “补齐所有数据” is the unique top priority.
- On 2026-04-29, the user set the project iteration cadence to once per hour.
- On 2026-04-29, Google account identity was reachable, but Google Drive file search failed with `ACCESS_TOKEN_SCOPE_INSUFFICIENT`, so cloud indexing / sync is currently blocked by connector permissions rather than by missing local data files.
- The current local Track-1 data bundle already available for indexing includes:
  - `/workspace/output/twse2_tb_reconstruction/reconstructed_hopping_table.csv`
  - `/workspace/output/twse2_tb_reconstruction/band_comparison.csv`
  - `/workspace/output/twse2_tb_reconstruction/high_symmetry_residuals.csv`
  - `/workspace/output/twse2_tb_reconstruction/band_reconstruction_check.png`
  - `/workspace/output/twse2_tb_reconstruction/summary.md`
- On 2026-04-29, the current Track-1 data bundle and reconstruction script were copied into the memory folder at `/workspace/memory/twse2-andreev-prl/data/track1-2026-04-29/`, so local persistent storage is now in place for the current normal-state package.
- In the 2026-04-28 UTC workspace snapshot, the original source-workbook path `/workspace/tmp/ws2/41467_2025_64519_MOESM3_ESM.xlsx` and the uploaded archive path `/workspace/user_files/04-ws2.zip` are absent, so the current executable path cannot assume those files still exist locally.
- On 2026-04-28 UTC, a runnable workspace script was restored at `/workspace/twse2_tb/reconstruct_tuo_tb.py` with a verified fallback that reads mirrored source-band columns from `/workspace/memory/twse2-andreev-prl/data/track1-2026-04-29/band_comparison.csv` when the original workbook is missing.
- On 2026-04-28 UTC, a new 162-candidate `A-B` convention scan was executed and archived at `/workspace/output/twse2_ab_scan/` and `/workspace/memory/twse2-andreev-prl/data/track1-2026-04-28-ab-scan/`.
- The best overall `A-B` scan candidate lowers the global RMSE to `8.898 meV`, but it breaks `Gamma` closure by about `8.19 meV`, so it is a rejected branch rather than a new faithful reconstruction.
- Under the exact-`Gamma` tolerance used in this round (`max abs delta < 0.05 meV` at both `Gamma` endpoints), the baseline all-constant `A-B` branch remains the best exact-`Gamma` candidate with RMSE `10.255 meV`.

## Current Best Reconstruction Status

- Real-space geometry most consistently matches a three-color triangular-lattice embedding of the A/B/C Wannier centers.
- A symmetry-completed candidate hopping table has been reconstructed locally.
- A reproducible reconstruction script now exists at `/workspace/twse2_tb/reconstruct_tuo_tb.py`.
- The current best reconstructed `H_TB(k)` reproduces the exact `Gamma`-point energies of Tuo Fig. 1c and the full-band endpoint closure, but still shows nontrivial mismatch near `K^B` and `K^T`.
- As of 2026-04-28, the RMSE definition has been aligned explicitly with `band_comparison.csv`. The summary metric now uses the element-wise global RMSE `sqrt(mean((E_rec - E_src)^2))`, while the larger row-wise sum metric is recorded separately for clarity.
- The current quantitative check gives an element-wise global band RMSE of `10.25 meV` and a row-wise summed RMSE of `17.76 meV` against the uploaded Fig. 1c source arrays.
- A new high-symmetry residual file now exists at `/workspace/output/twse2_tb_reconstruction/high_symmetry_residuals.csv`.
- A previous 2026-04-27 workspace snapshot briefly reported a reproducibility break because the local reconstruction assets were missing there. In the current workspace snapshot, those assets are present again, so the executable evidence path is restored.
- Additional 2026-04-27 inspection confirms that the remaining mismatch is not explained by a missing source-data sheet or an obvious alternate peer-review attachment; the ambiguity is still in the unpublished full hopping convention / code path.
- A new 2026-04-28 constrained phase scan over the `A-B` three-star families shows that several local phase-ordering choices can reduce the global band RMSE from `10.25 meV` to about `8.73 meV`, but every such candidate found in the scanned family also breaks the exact `Gamma` endpoint closure by about `3.51 meV`.
- Therefore the apparent `K`-sector improvement from those `A-B` phase-cycled candidates is currently classified as a rejected branch, not a new best faithful reconstruction.
- A wider 2026-04-28 UTC `A-B` convention scan over 162 candidates confirms the same pattern at larger scope: better global RMSE is available only by giving up `Gamma` closure, and no exact-`Gamma` branch beats the current baseline.
- Therefore the honest status is: partial reconstruction has been restored and modestly improved, but exact full-band reproduction remains open.

## Evidence Ledger Snapshot

- Tuo article / SI / Source Data uploaded: closed
- Tuo Eq. S1 representative hopping parameters parsed: closed
- Tuo Source Data Fig. 1c energy bands imported: closed
- Full lattice-vector hopping table: in progress
- Reconstructed `H_TB(k)` from hopping table: in progress
- Reproduced Tuo TB bands from hopping table: in progress
- Manuscript-grade normal-state data package with indexed artifacts: partial
- SGF benchmark data package: not started
- BTK / robustness data package: not started
- Memory-folder persistence for current Track-1 data artifacts: closed for current Track-1 bundle
- Google Drive persistence for current Track-1 data artifacts: blocked by permissions
- `A-B` convention exclusion scan package: closed locally, pending cloud sync
- Replace current `H_kp` with true Tuo TB: not started in local manuscript files
- Rerun Fig. 1-4 with true Tuo TB: not started in local manuscript files

## Immediate Next Action

Use the “data completion first” policy for every subsequent hourly iteration:

1. close the highest-value missing dataset, starting with exact `K^B / K^T` closure under the exact-`Gamma` constraint;
2. archive every newly verified artifact in the memory folder with an explicit index entry;
3. attempt Google Drive sync / indexing whenever connector permissions allow it;
4. if Drive remains blocked, keep an explicit pending-sync queue rather than claiming cloud persistence is complete.

The next technical move inside Track 1 is therefore: move beyond the exhausted `A-B` convention family and test the next highest-value convention layers that can still preserve exact `Gamma` closure, starting with non-`A-B` mixed-star gauge / labeling rules and exact `k`-path mapping checks, while treating every accepted result as part of a manuscript-grade data package instead of an isolated exploratory scan.
