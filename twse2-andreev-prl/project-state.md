# Project State

Project: `twse2-andreev-prl`
Last updated: 2026-04-28

## Current Stage

Track-1 normal-state data completion, executable-chain recovery, and storage hardening for a PRL-oriented twisted bilayer WSe2 Andreev manuscript.

## Current Overall Goal

Complete a manuscript-grade data package for the twse2-Andreev project: reconstruct the true-or-closest faithful Tuo tight-binding input, then generate and durably store the Fig. 1-4 evidence chain, including normal-state band benchmarks, downstream SGF / BTK / robustness arrays, and their file-level indexes in both the memory folder and Google Drive.

## Single Main Bottleneck

The project still does not have a complete, manuscript-grade normal-state data package. After the new `k`-path mapping scan, the sharpest unresolved data gap is now whether the improved low-RMSE path-mapping candidate is a physically faithful reading of the published Fig. 1c path; until that is settled and then combined with the next non-`A-B` mixed-star / gauge layer, the normal-state foundation is still not closed enough to start the SGF / BTK / robustness packages honestly.

## Newly Verified Facts

- The uploaded `04-ws2.zip` originally contained the Tuo article, SI, and source data; in the current 2026-04-28 UTC workspace snapshot, the original archive and workbook paths are absent, so execution cannot assume they are still present locally.
- The mirrored source-band columns in `/workspace/memory/twse2-andreev-prl/data/track1-2026-04-29/band_comparison.csv` are sufficient to keep Track 1 executable without inventing data.
- On 2026-04-28 UTC, a restored runnable script was created at `/workspace/twse2_tb/reconstruct_tuo_tb.py`; it falls back to the mirrored source-band CSV when `/workspace/tmp/ws2/41467_2025_64519_MOESM3_ESM.xlsx` is missing.
- The current Python environment has `numpy`, `pandas`, and `Pillow`; `matplotlib` and `scipy` are absent, but they are not required for the current Track-1 scripts.
- The earlier 162-candidate `A-B` convention scan remains valid as a local exclusion dataset, but every materially improved branch in that family still breaks the accepted exact-`Gamma` tolerance.
- On 2026-04-28 UTC, a new 180-candidate `k`-path mapping scan was executed at `/workspace/output/twse2_k_path_scan/` and mirrored into `/workspace/memory/twse2-andreev-prl/data/track1-2026-04-28-kpath-scan/`.
- The best threshold-exact-`Gamma` candidate in the new `k`-path scan uses `path_mode=exclusive_150`, `K_B=K_-2b1-b2`, `M=M_b2`, and `K_T=K_2b1+b2`, with global RMSE `8.880 meV` and `Gamma_end` max-abs residual `0.0132 meV`.
- A source-compatible duplicated-boundary variant using `path_mode=duplicated_150`, `K_B=K_2b1+b2`, `M=M_b2`, and `K_T=K_-2b1-b2` reaches global RMSE `8.900 meV` while restoring the final `Gamma` row exactly to numerical precision.
- The improved exact-`Gamma` candidate package has been mirrored into `/workspace/memory/twse2-andreev-prl/data/track1-2026-04-28-kpath-best/`, and the reproducible scripts have been mirrored into `/workspace/memory/twse2-andreev-prl/code/track1-2026-04-28-kpath/`.
- On 2026-04-28 UTC, Google Drive profile lookup and project search were both reachable, but no existing project folder or file was found for this project, and the current connector surface still does not expose a generic file-upload / folder-placement path for the full CSV + PNG + Python artifact bundle.

## Current Best Reconstruction Status

- Real-space geometry still most consistently matches a three-color triangular-lattice embedding of the A/B/C Wannier centers.
- A symmetry-completed candidate hopping table exists locally and remains unchanged in this round; the main new gain came from path-mapping rather than new hopping amplitudes.
- The restored Track-1 executable path is now `/workspace/twse2_tb/reconstruct_tuo_tb.py`.
- The previous exact-`Gamma` baseline was the all-constant `A-B` branch at global RMSE `10.255 meV`.
- The new best threshold-exact-`Gamma` path-mapping candidate improves that to `8.880 meV`.
- The best duplicated-boundary source-compatible candidate reaches `8.900 meV` with exact final-`Gamma` recovery.
- The honest status is therefore no longer “only hopping convention ambiguity remains.” The path-label / indexing layer is now a verified contributor to the residual mismatch, but exact full-band closure is still open.

## Evidence Ledger Snapshot

- Tuo article / SI / Source Data ingestion: closed
- Tuo Eq. S1 representative hopping parameters parsing: closed
- Source-band fallback mirror for Track 1: closed
- Full lattice-vector hopping table: in progress
- Reconstructed `H_TB(k)` from hopping table: in progress
- `A-B` convention exclusion scan package: closed locally, pending cloud sync
- `k`-path mapping exclusion / candidate scan package: closed locally, pending cloud sync
- Manuscript-grade normal-state data package with indexed artifacts: partial
- SGF benchmark data package: not started
- BTK / robustness data package: not started
- Memory-folder persistence for current Track-1 artifacts: closed
- Memory-folder persistence for current `k`-path mapping artifacts: closed
- Google Drive persistence for current Track-1 artifacts: blocked by connector write-surface limits
- Replace current `H_kp` with true Tuo TB in local manuscript files: not started
- Rerun Fig. 1-4 with true Tuo TB in local manuscript files: not started

## Immediate Next Action

Use the improved `k`-path candidate as the new Track-1 baseline, then rerun the next highest-value non-`A-B` mixed-star / gauge scan on top of that baseline rather than revisiting the exhausted old path / old `A-B` baseline. Every newly accepted artifact should continue to be mirrored into the memory folder immediately, and Google Drive sync should remain an explicit pending queue item until a generic upload surface becomes available.
