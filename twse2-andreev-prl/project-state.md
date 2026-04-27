# Project State

Project: `twse2-andreev-prl`
Last updated: 2026-04-27

## Current Stage

Theory strengthening and evidence-ledger closure for a PRL-oriented twisted bilayer WSe2 Andreev manuscript.

## Current Overall Goal

Replace the current `H_kp` benchmark with a symmetry-completed tight-binding Hamiltonian reconstructed from the Tuo et al. three-band Wannier model, then rerun the manuscript-facing Fig. 1-4 evidence chain with the true-or-closest faithful Tuo TB input.

## Single Main Bottleneck

The uploaded Tuo supplementary package provides only representative hopping parameters in Eq. (S1), not the full lattice-vector hopping table. The current round must therefore reconstruct the full real-space hopping table from geometry and symmetry before the manuscript can honestly claim use of the true Tuo TB model.

## Newly Verified Facts

- The uploaded `04-ws2.zip` contains the Tuo article, SI, and source data.
- `41467_2025_64519_MOESM3_ESM.xlsx` contains Fig. 1c energy-band arrays and Fig. 2/4 source data, but not a full hopping table.
- Supplementary Eq. (S1) lists representative onsite and hopping amplitudes for the K valley.
- Fig. S1 shows representative bonds up to fifth-nearest neighbor.
- The SI explicitly states that the full model is obtained by symmetry completion from these representative bonds.
- The Nature page states that code is only available from the corresponding author upon request.
- The arXiv preprint `2409.06779` exposes a TeX-source entry publicly, but the source archive is not retrievable from the current container due remote access restrictions.
- No editable local manuscript source for this twse2-Andreev project has appeared in the workspace as of 2026-04-27.

## Current Best Reconstruction Status

- Real-space geometry most consistently matches a three-color triangular-lattice embedding of the A/B/C Wannier centers.
- A symmetry-completed candidate hopping table has been reconstructed locally.
- A reproducible reconstruction script now exists at `/workspace/twse2_tb/reconstruct_tuo_tb.py`.
- The current best reconstructed `H_TB(k)` reproduces the exact `Gamma`-point energies of Tuo Fig. 1c and the full-band endpoint closure, but still shows nontrivial mismatch near `K^B` and `K^T`.
- The current quantitative check gives an overall band RMSE of `10.55 meV` against the uploaded Fig. 1c source arrays.
- Additional 2026-04-27 inspection confirms that the remaining mismatch is not explained by a missing source-data sheet or an obvious alternate peer-review attachment; the ambiguity is still in the unpublished full hopping convention / code path.
- Therefore the honest status is: partial reconstruction achieved; exact full-band reproduction not yet closed.

## Evidence Ledger Snapshot

- Tuo article / SI / Source Data uploaded: closed
- Tuo Eq. S1 representative hopping parameters parsed: closed
- Tuo Source Data Fig. 1c energy bands imported: closed
- Full lattice-vector hopping table: in progress
- Reconstructed `H_TB(k)` from hopping table: in progress
- Reproduced Tuo TB bands from hopping table: in progress
- Replace current `H_kp` with true Tuo TB: not started in local manuscript files
- Rerun Fig. 1-4 with true Tuo TB: not started in local manuscript files

## Immediate Next Action

Either obtain the author-side full hopping table / code, or recover the exact full star ordering and phase convention from a newly accessible source archive, before any manuscript text is upgraded from “candidate reconstruction” to “true Tuo TB”.
