# Project State

Project: `twse2-andreev-prl`
Last updated: 2026-04-29

## Current Stage

Track-1 normal-state data completion, coupled path-plus-hopping refinement, and storage hardening for a PRL-oriented twisted bilayer WSe2 Andreev manuscript.

## Current Overall Goal

Complete a manuscript-grade data package for the twse2-Andreev project: reconstruct the true-or-closest faithful Tuo tight-binding input, then generate and durably store the Fig. 1-4 evidence chain, including normal-state band benchmarks, downstream SGF / BTK / robustness arrays, and their file-level indexes in both the memory folder and Google Drive.

## Single Main Bottleneck

The project still does not have a complete, manuscript-grade normal-state data package. A new coupled `k`-path plus exact-`Gamma` asymmetric `sqrt(7)` scan has now improved the faithful candidate slightly, so the bottleneck is no longer whether path-plus-hopping coupling matters. The remaining highest-value gap is a broader coupled valley-specific completion that can beat the new swapped-valley exact-`Gamma` baseline by more than a marginal `0.006 meV` and materially reduce the persistent `K`-sector mismatch without breaking `Gamma`.

## Newly Verified Facts

- The uploaded `04-ws2.zip` originally contained the Tuo article, SI, and source data; in the current 2026-04-28 UTC workspace snapshot, the original archive and workbook paths are absent, so execution cannot assume they are still present locally.
- The mirrored source-band columns in `/workspace/memory/twse2-andreev-prl/data/track1-2026-04-29/band_comparison.csv` are sufficient to keep Track 1 executable without inventing data.
- On 2026-04-28 UTC, the runnable workspace script was restored again at `/workspace/twse2_tb/reconstruct_tuo_tb.py`, and a new scan driver was added at `/workspace/twse2_tb/scan_mixed_star_gauges.py`.
- The current Python environment has `numpy`, `pandas`, and `Pillow`; `matplotlib` and `scipy` are absent, but they are not required for the current Track-1 scripts.
- In the current 2026-04-28 UTC workspace snapshot, no editable manuscript source for this project is present outside memory state files, so manuscript revision remains gated by data completion plus future source-material recovery.
- The earlier 162-candidate `A-B` convention scan remains valid as a local exclusion dataset, but every materially improved branch in that family still breaks the accepted exact-`Gamma` tolerance.
- On 2026-04-28 UTC, a 180-candidate `k`-path mapping scan was executed at `/workspace/output/twse2_k_path_scan/` and mirrored into `/workspace/memory/twse2-andreev-prl/data/track1-2026-04-28-kpath-scan/`.
- The best threshold-exact-`Gamma` candidate in the `k`-path scan uses `path_mode=exclusive_150`, `K_B=K_-2b1-b2`, `M=M_b2`, and `K_T=K_2b1+b2`, with global RMSE `8.880 meV` and `Gamma_end` max-abs residual `0.0132 meV`.
- On 2026-04-28 UTC, a 162-candidate non-`A-B` shared mixed-star scan was executed at `/workspace/output/twse2_mixed_star_scan/` and mirrored into `/workspace/memory/twse2-andreev-prl/data/track1-2026-04-28-mixed-star-scan/`.
- The best exact-`Gamma` mixed-star candidate uses `c1=cyc`, `c2=anti`, `c7_first=cyc`, `c7_second=anti`, and `c7_second_conjugated=False`, reaching global RMSE `8.372 meV` with `Gamma_end` max-abs residual `0.0362 meV`.
- Relative to the previous best path-only candidate, the new mixed-star candidate improves the global RMSE by `0.508 meV`, improves the `M`-window RMSE by `4.951 meV`, and modestly improves the `K^B` / `K^T` windows while keeping the hard exact-`Gamma` acceptance threshold satisfied.
- The mixed-star scan yields 24 candidates within the `0.05 meV` exact-`Gamma` threshold, so the current ambiguity has narrowed from “whether any non-`A-B` layer helps honestly” to “which valley-specific or asymmetric mixed-star rule closes the remaining `K`-sector mismatch.”
- On 2026-04-28 UTC, Google Drive profile lookup and project search were both reachable, but no existing project folder or file was found for this project, and the current connector surface still does not expose a generic file-upload / folder-placement path for the full CSV + PNG + Python artifact bundle.
- On 2026-04-28 UTC, a new 81-candidate asymmetric short-range scan was executed at `/workspace/output/twse2_asymmetric_short_range_scan/` and mirrored into `/workspace/memory/twse2-andreev-prl/data/track1-2026-04-29-asymmetric-short-range/`.
- The asymmetric short-range scan confirms that breaking only the `A-C / B-C` first- and second-neighbor sharing does not improve the best exact-`Gamma` candidate: the previous shared baseline (`ac1=bc1=cyc`, `ac2=bc2=anti`) remains the best exact-`Gamma` result at global RMSE `8.372 meV`.
- The best near-threshold alternative from the short-range scan (`ac1=bc1=cyc`, `ac2=cyc`, `bc2=anti`) reaches exact-`Gamma` tolerance but worsens the global RMSE to `8.401 meV`, so short-range asymmetry is now an exclusion dataset, not an upgrade path.
- On 2026-04-28 UTC, a new 324-candidate asymmetric `sqrt(7)` scan was executed at `/workspace/output/twse2_asymmetric_c7_scan/` and mirrored into `/workspace/memory/twse2-andreev-prl/data/track1-2026-04-29-asymmetric-c7/`.
- The best overall asymmetric `sqrt(7)` candidate (`ac7_first=const`, `bc7_first=cyc`, `ac7_second=anti`, `bc7_second=const`, both non-conjugated) lowers the global RMSE to `8.283 meV`, but it breaks exact-`Gamma` closure by `7.885 meV`, so it cannot be promoted honestly.
- Within the hard exact-`Gamma` tolerance, the asymmetric `sqrt(7)` scan also leaves the previous shared mixed-star baseline unchanged as the best faithful candidate at global RMSE `8.372 meV`.
- The current workspace runnable chain has been restored again at `/workspace/twse2_tb/`, now including `reconstruct_tuo_tb.py`, `scan_asymmetric_short_range.py`, and `scan_asymmetric_c7.py`, all mirrored into `/workspace/memory/twse2-andreev-prl/code/track1-2026-04-29-asymmetry/`.
- In the current 2026-04-29 UTC workspace snapshot, `/workspace/twse2_tb/` is absent again; the runnable Track-1 code now lives only in the memory mirror under `/workspace/memory/twse2-andreev-prl/code/track1-2026-04-29-asymmetry/`.
- On 2026-04-29 UTC, a new 1160-candidate coupled scan over the top 20 `k`-path mappings and the 58 exact-`Gamma` asymmetric `sqrt(7)` candidates was executed at `/workspace/output/twse2_coupled_path_c7_scan/` and mirrored into `/workspace/memory/twse2-andreev-prl/data/track1-2026-04-29-coupled-path-c7/`.
- The coupled scan verifies that path-plus-hopping coupling is a real improvement path: the best exact-`Gamma` candidate switches the valley labels to `K_B=K_2b1+b2`, `M=M_b2`, `K_T=K_-2b1-b2` while keeping the same shared mixed-star rule set (`c1=cyc`, `c2=anti`, `c7_first=cyc`, `c7_second=anti`, non-conjugated), improving the global RMSE from `8.372 meV` to `8.367 meV`.
- Relative to the previous faithful baseline, the new coupled candidate improves `Gamma_end` max-abs residual from `0.03618 meV` to `0.03506 meV` and improves the `K_B`-window RMSE from `15.056 meV` to `14.950 meV`, while leaving the `M` window unchanged and slightly worsening the opposite valley window. The dominant unresolved mismatch therefore remains a valley-sector closure problem, not an `M`-point problem.
- No editable manuscript source was found for this project in the current 2026-04-29 UTC workspace scan, so manuscript revision is still blocked by both missing source files and incomplete downstream data.

## Current Best Reconstruction Status

- Real-space geometry still most consistently matches a three-color triangular-lattice embedding of the A/B/C Wannier centers.
- A symmetry-completed candidate hopping table exists locally and remains executable through `/workspace/twse2_tb/reconstruct_tuo_tb.py`.
- The previous exact-`Gamma` baseline was the all-constant `A-B` branch at global RMSE `10.255 meV`.
- The best exact-`Gamma` path-mapping candidate improves that to `8.880 meV`.
- The best exact-`Gamma` shared mixed-star candidate improved that further to `8.372 meV`.
- A new coupled path-plus-hopping candidate now improves the faithful exact-`Gamma` baseline again to `8.367 meV`.
- The dominant remaining residual is still no longer at `M`; it remains concentrated in the `K^B / K^T` valleys even after the coupled scan.
- Independent short-range `A-C / B-C` asymmetry and independent `sqrt(7)` asymmetry have now both been tested as isolated layers and neither improves the best exact-`Gamma` candidate.
- The honest status is therefore no longer “only path labeling remains.” The path-label / indexing layer and the shared non-`A-B` mixed-star convention are verified contributors, and the new coupled scan confirms that their interaction matters, but the broader valley-specific completion is still open.

## Evidence Ledger Snapshot

- Tuo article / SI / Source Data ingestion: closed
- Tuo Eq. S1 representative hopping parameters parsing: closed
- Source-band fallback mirror for Track 1: closed
- Full lattice-vector hopping table: in progress
- Reconstructed `H_TB(k)` from hopping table: in progress
- `A-B` convention exclusion scan package: closed locally, pending cloud sync
- `k`-path mapping exclusion / candidate scan package: closed locally, pending cloud sync
- non-`A-B` mixed-star exclusion / candidate scan package: closed locally, pending cloud sync
- asymmetric short-range exclusion / candidate scan package: closed locally, pending cloud sync
- asymmetric `sqrt(7)` exclusion / candidate scan package: closed locally, pending cloud sync
- coupled path + exact-`Gamma` asymmetric `sqrt(7)` scan package: closed locally, pending cloud sync
- Manuscript-grade normal-state data package with indexed artifacts: partial
- SGF benchmark data package: not started
- BTK / robustness data package: not started
- Memory-folder persistence for current Track-1 artifacts: closed
- Memory-folder persistence for current `k`-path mapping artifacts: closed
- Memory-folder persistence for current mixed-star artifacts: closed
- Memory-folder persistence for current coupled path + exact-`Gamma` asymmetric `sqrt(7)` artifacts: closed
- Google Drive persistence for current Track-1 artifacts: blocked by connector write-surface limits
- Replace current `H_kp` with true Tuo TB in local manuscript files: not started
- Rerun Fig. 1-4 with true Tuo TB in local manuscript files: not started

## Immediate Next Action

Promote the new `8.367 meV` coupled path-plus-hopping candidate as the faithful Track-1 baseline. The next data pass should stay on the coupled valley-specific completion line and test whether broader coupled short-range plus `sqrt(7)` asymmetry can reduce the remaining `K`-sector mismatch beyond the current marginal gain, rather than reopening exhausted isolated scans or drifting into SGF / BTK before Track 1 is strong enough. Every newly accepted artifact should continue to be mirrored into the memory folder immediately, and Google Drive sync should remain an explicit pending queue item until a writable connector surface becomes available again.
