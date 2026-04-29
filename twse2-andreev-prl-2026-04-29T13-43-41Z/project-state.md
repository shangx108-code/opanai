# Project State

Project: `twse2-andreev-prl`
Last updated: 2026-04-29

## Current Stage

Track-1 effective closure via V3 orbital-selective valley correction is in place, and the project is now in downstream BTK interpretation and hardening on top of a validated semi-infinite SGF benchmark for the PRL-oriented twisted bilayer WSe2 Andreev manuscript.

## Current Overall Goal

Complete a manuscript-grade data package for the twse2-Andreev project: reconstruct the true-or-closest faithful Tuo tight-binding input, then generate and durably store the Fig. 1-4 evidence chain, including normal-state band benchmarks, downstream SGF / BTK / robustness arrays, and their file-level indexes in both the memory folder and Google Drive.

## Single Main Bottleneck

The project now has a faithful coupled baseline, a full V3 closure, a portable k-space sparse compressed-V3 approximation, a verified SGF stability trial, a first valley-resolved generalized BTK package, a validated semi-infinite SGF benchmark, a new valley-resolved generalized BTK rerun anchored to that semi-infinite SGF data, and a manuscript-language interpretation note that separates robust BTK statements from obsolete proxy-era claims. The single main bottleneck has therefore shifted again: the next highest-priority task is manuscript integration and deciding whether the current BTK kernel itself needs a deeper upgrade for journal-standard claims.

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
- A new persistent V3 package now lives at `/workspace/memory/twse2-andreev-prl/data/track1-2026-04-29-v3-orbital-selective-valley-correction/`.
- That V3 package starts from the current best faithful coupled baseline and solves an effective diagonal orbital correction layer `diag(d_A(k), d_B(k), d_C(k))` point-by-point along the high-symmetry path.
- V3 reduces the Track-1 global RMSE from `8.367 meV` to `1.503 meV`.
- V3 matches the key high-symmetry checkpoints (`Gamma_start`, `K_B`, `M`, `K_T`) to numerical precision and leaves only a small `Gamma_end` mismatch (`1.72e-2 meV` max abs delta).
- The extracted V3 profile is genuinely valley-heavy: the largest `A/B` orbital-selective component sits in the `K^B / K^T` sectors rather than at `Gamma`.
- A new persistent compressed-V3 package now lives at `/workspace/memory/twse2-andreev-prl/data/track1-2026-04-29-v3-compressed-parametrization/`.
- That compressed package replaces the point-by-point V3 profile with a sparse low-dimensional envelope model: 5 even-pair terms for `v3_ab_common`, 5 odd-pair terms for `v3_ab_orbital_selective`, and 5 even/central terms for `v3_c`.
- The compressed-V3 model reduces the Track-1 global RMSE from `8.367 meV` to `3.652 meV`.
- The compressed-V3 valley-window errors are already much smaller than the baseline (`K_B` window `0.840 meV`, `K_T` window `1.515 meV`), but it does not yet match the full point-by-point V3 closure.
- A stronger k-space sparse compressed-V3 package now lives at `/workspace/memory/twse2-andreev-prl/data/track1-2026-04-29-v3-kspace-sparse-model/`.
- The current strongest k-space sparse model reduces the Track-1 global RMSE further to `2.726 meV` and keeps the `Gamma_end` mismatch down to `0.181 meV`.
- A downstream SGF trial using the k-space sparse compressed-V3 model now lives at `/workspace/memory/twse2-andreev-prl/data/sgf-kspace-sparse-v3-trial-2026-04-29/`.
- That SGF trial confirms numerical stability: both baseline and corrected spectral maps are finite throughout the tested grid, but the newer stronger sparse model produces a larger downstream SGF shift than the earlier `3.296 meV` version.
- A new persistent SGF minimal package now lives at `/workspace/memory/twse2-andreev-prl/data/sgf-minimal-2026-04-29/`.
- A new persistent BTK minimal package now lives at `/workspace/memory/twse2-andreev-prl/data/btk-minimal-2026-04-29/`.
- A new persistent valley-resolved generalized BTK package now lives at `/workspace/memory/twse2-andreev-prl/data/btk-generalized-valley-resolved-2026-04-29/`.
- That new BTK package is explicitly anchored to the SGF-verified compressed-V3 spectral map rather than the older SGF-minimal zero-bias average alone.
- The new BTK package resolves `K_B`, `K_T`, and total conductance channels separately for `s_wave`, `nodal_even`, `valley_even`, and `valley_odd` pairing families.
- For the current proxy benchmark, the strongest compressed-V3 enhancement of the total peak-minus-background contrast appears in the `nodal_even` channel at `Z=2.0`, `eta=0.5 meV`, with `delta(peak-background)=0.549`.
- The strongest compressed-V3 valley asymmetry in the current proxy benchmark also appears in the `nodal_even` channel, at `Z=0.5`, `eta=0.05 meV`, where the `K_B-K_T` peak-contrast difference reaches `-3.970`.
- A new semi-infinite SGF package now lives at `/workspace/memory/twse2-andreev-prl/data/sgf-semi-infinite-kspace-sparse-v3-2026-04-29/`.
- That package uses principal-layer decimation plus explicit Hermitianization of the chain Hamiltonian blocks, which preserves the existing band eigenvalues while repairing the SGF input model.
- The validated semi-infinite SGF map now passes the two hard checks that previously failed: negative spectral-weight counts are `0` for both baseline and compressed-V3, and iteration-cap hits are also `0`.
- The corrected semi-infinite SGF run converges everywhere with maximum iteration count `1101` and maximum final update norm below `1.0e-10`.
- A new semi-infinite-informed valley-resolved BTK package now lives at `/workspace/memory/twse2-andreev-prl/data/btk-generalized-valley-resolved-semi-infinite-2026-04-29/`.
- That rerun keeps the same pairing families and valley partition as the earlier BTK package, but swaps the normal-state input from the older finite-ribbon SGF proxy to the new validated semi-infinite SGF benchmark.
- Under the semi-infinite SGF input, the strongest compressed-V3 total peak-contrast gain shifts to the `valley_odd` channel at `Z=2.0`, `eta=0.5 meV`, with `delta(peak-background)=0.085`.
- Under the same semi-infinite SGF input, the strongest `K_B-K_T` peak-contrast asymmetry appears in the `s_wave` channel at `Z=0.0`, `eta=0.05 meV`, with `K_B-K_T=-4.188`.
- Compared with the older finite-ribbon-input BTK package, the semi-infinite rerun generally suppresses the apparent compressed-V3 gain in the `s_wave` family and changes which pairing channel looks most favorable.
- A new manuscript-facing BTK interpretation note now lives at `/workspace/memory/twse2-andreev-prl/btk-interpretation-semi-infinite-2026-04-29.md`.
- That note keeps the robust statement that strong valley asymmetry survives the semi-infinite upgrade, removes the older broad claim that `nodal_even` is generically the dominant BTK channel, and promotes the semi-infinite-input BTK package to the only active manuscript branch.

## Current Best Reconstruction Status

- Real-space geometry still most consistently matches a three-color triangular-lattice embedding of the A/B/C Wannier centers.
- The old exact-`Gamma` all-constant `A-B` baseline remains reproducible at `10.255 meV` global RMSE.
- The best exact-`Gamma` path-mapping candidate improved that to `8.880 meV`.
- The best exact-`Gamma` shared mixed-star candidate improved that further to `8.372 meV`.
- The current best faithful coupled path-plus-hopping candidate improves the exact-`Gamma` baseline again to `8.367 meV`.
- The new V3 orbital-selective valley correction package reduces the pathwise mismatch to `1.503 meV` overall RMSE while preserving the coupled baseline as the underlying faithful starting point.
- The strongest k-space sparse model now outperforms the earlier sparse versions (`2.726 meV` versus `3.296 meV` versus `3.652 meV`) while remaining portable away from the high-symmetry path.
- The dominant SGF-side numerical issue has now been resolved: the semi-infinite solver is stable and the SGF map is physically acceptable across the tested grid.
- The honest status is: Track 1 is effectively closed as a full V3-corrected path package, the semi-infinite SGF benchmark is validated, the valley-resolved generalized BTK package has been rerun on top of it, and a first manuscript-safe interpretation pass is complete. The remaining bottleneck is now whether the current proxy BTK kernel is already sufficient for the target journal standard or whether a deeper BTK model upgrade is required.

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
- V3 orbital-selective valley correction package: closed locally, pending cloud sync
- Compressed V3 sparse parametrization package: closed locally, pending cloud sync
- K-space sparse compressed-V3 package: closed locally, pending cloud sync
- SGF trial with k-space sparse compressed-V3: closed locally, pending cloud sync
- Manuscript-grade normal-state data package with indexed artifacts: partial
- SGF benchmark data package: closed locally, with validated semi-infinite baseline-vs-compressed-V3 comparison now available
- BTK / robustness data package: partial, with valley-resolved generalized BTK proxy now closed locally but final multiorbital benchmark still missing
- Semi-infinite-informed BTK comparison package: closed locally, pending interpretation and manuscript integration
- Memory-folder persistence for current Track-1, SGF, and BTK artifacts: closed
- Google Drive persistence for current artifacts: blocked by missing upload surface
- Replace current `H_kp` with true Tuo TB in manuscript files: not started
- Rerun Fig. 1-4 with true Tuo TB in manuscript files: not started

## Immediate Next Action

1. Keep the `8.367 meV` coupled path-plus-hopping candidate as the faithful baseline, the `1.503 meV` full V3 package as the strongest closure, and the `2.726 meV` k-space sparse model as the current best portable compressed approximation for downstream work.
2. Treat `/workspace/memory/twse2-andreev-prl/data/btk-generalized-valley-resolved-2026-04-29/` as the new BTK working package and retire the older minimal BTK package to historical-proxy status.
3. Compare the BTK observables from the old finite-ribbon proxy input versus the new semi-infinite SGF input, and preserve only the semi-infinite branch as the active manuscript path.
4. Integrate the surviving BTK statements into manuscript structure and figure logic, using `/workspace/memory/twse2-andreev-prl/btk-interpretation-semi-infinite-2026-04-29.md` as the active reference.
5. Then decide whether the BTK kernel itself must be upgraded beyond the current proxy model for the target journal standard.
