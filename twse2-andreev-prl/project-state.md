# Project State

Project: `twse2-andreev-prl`
Last updated: 2026-04-28

## Current Stage

Track-1 normal-state data completion, executable-chain recovery, and storage hardening for a PRL-oriented twisted bilayer WSe2 Andreev manuscript.

## Current Overall Goal

Complete a manuscript-grade data package for the twse2-Andreev project: reconstruct the true-or-closest faithful Tuo tight-binding input, then generate and durably store the Fig. 1-4 evidence chain, including normal-state band benchmarks, downstream SGF / BTK / robustness arrays, and their file-level indexes in both the memory folder and Google Drive.

## Single Main Bottleneck

The project still does not have a complete, manuscript-grade normal-state data package. After the new shared `A-C / B-C` mixed-star scan on top of the improved `k`-path baseline, the sharpest unresolved data gap is now the remaining `K^B / K^T` valley mismatch under candidates that already preserve exact-`Gamma` closure; the next highest-value data pass must therefore break the still-shared mixed-star assumptions or test the next valley-specific gauge layer rather than revisit `M`, the old path baseline, or exhausted `A-B` scans.

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

## Current Best Reconstruction Status

- Real-space geometry still most consistently matches a three-color triangular-lattice embedding of the A/B/C Wannier centers.
- A symmetry-completed candidate hopping table exists locally and remains executable through `/workspace/twse2_tb/reconstruct_tuo_tb.py`.
- The previous exact-`Gamma` baseline was the all-constant `A-B` branch at global RMSE `10.255 meV`.
- The best exact-`Gamma` path-mapping candidate improves that to `8.880 meV`.
- The best exact-`Gamma` shared mixed-star candidate improves that further to `8.372 meV`.
- The dominant remaining residual is no longer at `M`; it is now concentrated in the `K^B / K^T` valleys.
- The honest status is therefore no longer “only path labeling remains.” The path-label / indexing layer and the non-`A-B` mixed-star convention are both verified contributors to the residual mismatch, but exact valley closure is still open.

## Evidence Ledger Snapshot

- Tuo article / SI / Source Data ingestion: closed
- Tuo Eq. S1 representative hopping parameters parsing: closed
- Source-band fallback mirror for Track 1: closed
- Full lattice-vector hopping table: in progress
- Reconstructed `H_TB(k)` from hopping table: in progress
- `A-B` convention exclusion scan package: closed locally, pending cloud sync
- `k`-path mapping exclusion / candidate scan package: closed locally, pending cloud sync
- non-`A-B` mixed-star exclusion / candidate scan package: closed locally, pending cloud sync
- Manuscript-grade normal-state data package with indexed artifacts: partial
- SGF benchmark data package: not started
- BTK / robustness data package: not started
- Memory-folder persistence for current Track-1 artifacts: closed
- Memory-folder persistence for current `k`-path mapping artifacts: closed
- Memory-folder persistence for current mixed-star artifacts: closed
- Google Drive persistence for current Track-1 artifacts: blocked by connector write-surface limits
- Replace current `H_kp` with true Tuo TB in local manuscript files: not started
- Rerun Fig. 1-4 with true Tuo TB in local manuscript files: not started

## Immediate Next Action

Treat the `8.372 meV` mixed-star candidate as the new Track-1 baseline, then run the next smallest asymmetric scan that decouples the still-shared `A-C` and `B-C` phase rules or the next valley-specific gauge layer, because `M` has now improved sharply while `K^B / K^T` remains the dominant residual. Every newly accepted artifact should continue to be mirrored into the memory folder immediately, and Google Drive sync should remain an explicit pending queue item until a generic upload surface becomes available.
