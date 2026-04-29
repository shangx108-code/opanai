# Supervision Log

## 2026-04-26 | Initial forensic pass

### Check Scope

- Uploaded reference bundle
- Tuo article / SI / source data integrity
- Availability of the full hopping table needed to replace the current benchmark Hamiltonian

### Confirmed Correct

- The source package genuinely contains the target paper, SI, and source-data workbook.
- Eq. (S1) is parseable and gives representative onsite / hopping amplitudes.
- Fig. 1c source-band arrays are directly available in the workbook.
- The current missing item in the user ledger is real: the source bundle does not directly contain a full lattice-vector hopping table.

### Problems / Risks

- The exact symmetry completion needed to turn representative bonds into a unique full hopping table is not written out explicitly in the uploaded files.
- Without closing that reconstruction, the manuscript cannot honestly claim to have replaced the benchmark `H_kp` model by the true Tuo TB model.
- No editable manuscript source has yet been supplied in the current workspace, so only a revision package or replacement text can be produced unless manuscript files appear later.
- The current best executable reconstruction reduces the problem from “missing model entirely” to “remaining `K`-sector convention ambiguity,” with a measured Fig. 1c RMSE of `10.55 meV`.

### Stage Judgment

Current stage is still evidence generation, not final manuscript polishing.

### Supports Next Stage?

Partially. The project supports further theory / code reconstruction immediately, but does not yet support a fully honest manuscript-wide material-specific rewrite.

## 2026-04-27 | Second reconstruction pass

### Check Scope

- Search for editable manuscript source in the workspace
- Search for additional public material that could remove the Tuo hopping-table ambiguity
- Re-evaluate whether the remaining mismatch is due to missing files versus unresolved convention

### Confirmed Correct

- No local twse2 manuscript source is currently available for direct patching and compilation.
- The peer-review file does not disclose the full lattice-vector hopping table.
- The Nature article explicitly says code is available only from the corresponding author upon request.
- The arXiv record exposes a TeX-source entry, but that source archive could not be fetched from the current environment because the remote endpoint returns access-denied responses here.

### Problems / Risks

- The project still cannot honestly claim exact true-Tuo-TB closure from public files already in hand.
- Without local manuscript source files, even a future exact TB closure would still require one more step before final PDF compilation.

### Stage Judgment

Still in evidence generation and reconstruction, not yet in final manuscript revision.

### Supports Next Stage?

Partially. The project can keep iterating on reconstruction logic, but exact closure now appears increasingly dependent on obtaining either the author-side code or an actually reachable source archive.

## 2026-04-27 | Three-track orchestration pass

### Check Scope

- Reclassify the project around the three user-specified tracks:
  - `K`-point valley closure
  - surface Green's-function benchmark
  - BTK + robustness full data package

### Confirmed Correct

- The current workspace contains planning notes for SGF and BTK, but not actual numerical implementations for this project.
- The current workspace contains an executable TB reconstruction script, so Track 1 is the only one that has already entered real code execution.

### Problems / Risks

- If the project treats all three tracks as equal bottlenecks now, execution will diffuse and the core material-specific closure may slip again.
- SGF and BTK can be architected now, but they cannot yet count as final material-specific closure without an exact true-Tuo-TB base Hamiltonian.

### Stage Judgment

Three-track execution is now the right framing, but only one track has permission to remain the primary bottleneck: exact `K`-point valley closure.

### Supports Next Stage?

Yes, at the planning and orchestration level. The project now has a sharper role split and completion standard for all three tracks.

## 2026-04-27 | Workspace reproducibility correction

### Check Scope

- Verify that the reconstruction assets cited in the current project state are actually present and runnable in the current workspace snapshot

### Confirmed Correct

- The twse2 project still has a clearly specified PRL-oriented target style in saved project notes.
- The previously reported scientific bottleneck order does not change: the first real blocker remains the evidence-chain gap in exact `K`-point valley closure.

### Problems / Risks

- One 2026-04-27 workspace snapshot reported that the local files named in the saved state were not present there.
- That temporarily meant the previously reported partial reconstruction status was not reproducible from that snapshot alone.

### Stage Judgment

Still in evidence generation, but that snapshot exposed a workspace-level reproducibility break inside the primary evidence chain.

### Supports Next Stage?

Only after the missing local reconstruction assets are restored or re-supplied in an accessible location.

## 2026-04-28 | Metric-alignment and candidate-update pass

### Check Scope

- Verify whether the apparent RMSE inconsistency comes from stale files or from mismatched metric definitions
- Improve the current candidate hopping completion only if the full-path comparison actually improves

### Confirmed Correct

- The previous apparent RMSE inconsistency was a metric-definition issue, not a file mismatch: the summary used the element-wise global RMSE, whereas the manual re-check had used the row-wise summed norm.
- The reconstruction script has now been updated to write both metrics explicitly and to export a high-symmetry residual table.
- The current candidate completion improved modestly from `10.55 meV` to `10.25 meV` in the element-wise global RMSE.
- The local reconstruction script and output files are present again in the current snapshot, so the executable evidence path has been restored.

### Problems / Risks

- The `K^B / K^T` mismatch remains large and still blocks any honest claim of exact true-Tuo-TB closure.
- The main remaining residuals are no longer hidden by metric ambiguity; they are now clearly localized in the high-symmetry residual report.

### Stage Judgment

Still in Track-1 evidence generation. The project is cleaner and slightly better constrained than before, but the core closure is still unresolved.

## 2026-04-28 | Constrained A-B phase-rule scan

### Check Scope

- Test whether the dominant `K^B / K^T` residual can be reduced by changing only the local `A-B` star phase-ordering rules
- Enforce exact `Gamma` endpoint closure as a hard acceptance criterion for any candidate update

### Confirmed Correct

- A narrow scan over the nearest- and next-nearest-neighbor `A-B` three-star rules uncovers candidates that reduce the full-path RMSE from `10.25 meV` to about `8.73 meV`.
- The `K`-sector mismatch is therefore genuinely sensitive to the `A-B` star convention, not only to the previously tested `A-A / A-C / B-C` branches.
- Restoring the baseline script after the scan reproduces the previous exact-`Gamma` candidate and the `10.25 meV` reference metrics.

### Problems / Risks

- Every locally improved `A-B` phase-cycled candidate found in this scanned family also breaks the exact `Gamma` endpoint closure by about `3.51 meV`, so none of them can yet be promoted to the main faithful reconstruction.
- A follow-up attempt to phase-cycle the longer-range `A-B` `sqrt(7)` star reduces part of the `K^T` residual but worsens the `Gamma` conflict, so that branch is also rejected.
- The project still lacks a symmetry-completion rule that improves `K` while preserving the already matched `Gamma` endpoint.

### Stage Judgment

Still in Track-1 evidence generation. This pass narrows the live ambiguity but does not close the true-Tuo-TB reconstruction.

### Supports Next Stage?

Partially. Future search should move to convention layers not exhausted by this local scan, such as the exact `K`-point labeling, a different gauge choice, or the unpublished author-side hopping completion.

## 2026-04-29 | Data-completion reprioritization and storage check

### Check Scope

- Incorporate the user's new instruction that all subsequent iterations must prioritize data completion
- Verify whether the current Track-1 artifacts are durably persisted in both the memory folder and Google Drive

### Confirmed Correct

- The project now has a concrete local Track-1 data bundle ready for indexing:
  - reconstructed hopping table
  - full band comparison table
  - high-symmetry residual table
  - band-check figure
  - reconstruction summary
- The memory folder can be updated normally, so local persistent indexing is available this round.
- The current Track-1 bundle has now been mirrored into `/workspace/memory/twse2-andreev-prl/data/track1-2026-04-29/`, so this part of the storage requirement is satisfied locally.
- Google account identity is reachable through the connector.

### Problems / Risks

- Google Drive search and file discovery are currently blocked by `ACCESS_TOKEN_SCOPE_INSUFFICIENT`, so this round cannot honestly claim that project data have been stored in Drive.
- The complete manuscript-grade data package is still missing: SGF and BTK / robustness datasets have not yet been generated, and Track 1 still lacks exact `K`-point closure.
- Without an explicit pending-sync queue, later iterations would risk mistaking “local files exist” for “cloud persistence is complete.”

### Stage Judgment

The project has moved from mainly local reconstruction triage to data-package completion and storage hardening. The technical core is still Track 1, but every accepted result must now be treated as part of a persistent data pipeline.

### Supports Next Stage?

Yes, partially. The next hourly iterations can proceed immediately on local data completion and memory indexing, while Google Drive sync remains a live environment blocker that must be retried after permission repair.

## 2026-04-29 | Persistent project-space execution pass

### Check Scope

- Move active computation into the long-lived project space
- Continue Track 1 closure work
- Generate first persistent SGF and BTK minimal data packages

### Confirmed Correct

- New reusable project-space scripts now live in `/workspace/memory/twse2-andreev-prl/code/`.
- A new Track 1 convention scan package now lives in `/workspace/memory/twse2-andreev-prl/data/track1-kclosure-2026-04-29/`.
- That scan confirms that high-symmetry relabeling alone does not close Track 1; the best candidate in this pass still has RMSE `13.014 meV`.
- A new SGF minimal package now lives in `/workspace/memory/twse2-andreev-prl/data/sgf-minimal-2026-04-29/`.
- A new BTK minimal package now lives in `/workspace/memory/twse2-andreev-prl/data/btk-minimal-2026-04-29/`.

### Problems / Risks

- Track 1 remains unresolved; the new scan narrows one more branch but does not produce exact `K^B / K^T` closure.
- The SGF result is still a finite-ribbon edge Green's proxy, not yet a final semi-infinite benchmark.
- The BTK result is still a BTK-like proxy weighted by the SGF minimal edge profile, not yet a multiorbital material-specific conductance calculation.
- Google Drive persistence is still not actually complete because a usable upload/create action is still unavailable in the current connector surface.

### Stage Judgment

The project has advanced from “only Track 1 local reconstruction exists” to “all three lines now have persistent minimal data packages.” This is meaningful progress, but the manuscript-grade data closure is still incomplete.

### Supports Next Stage?

Yes. The next stage can now refine each data line on top of persistent code and persistent files instead of starting from scratch each round.

## 2026-04-29 | Valley-resolved generalized BTK upgrade pass

### Check Scope

- Verify whether the compressed-V3 SGF trial is strong enough to support a first valley-resolved generalized BTK package
- Replace the older BTK minimal average with a k-space- and valley-aware conductance package without pretending that the SGF layer is already final

### Confirmed Correct

- The current SGF trial at `/workspace/memory/twse2-andreev-prl/data/sgf-kspace-sparse-v3-trial-2026-04-29/` is numerically finite for both baseline and compressed-V3 maps, so it can honestly serve as the normal-state input for a first generalized BTK pass.
- A new persistent package now lives at `/workspace/memory/twse2-andreev-prl/data/btk-generalized-valley-resolved-2026-04-29/`.
- That package resolves `K_B`, `K_T`, and total conductance channels separately and compares baseline versus compressed-V3 conductance for `s_wave`, `nodal_even`, `valley_even`, and `valley_odd` pairing families.
- The first implementation initially produced unphysical giant peaks, and this was corrected in the same round by tightening the generalized BTK proxy kernel before accepting the saved package.
- The saved package now has stable O(1-10) conductance scales, finite robustness tables, explicit model-comparison rows, and explicit valley-asymmetry rows.

### Problems / Risks

- The new BTK package is still a proxy benchmark because it inherits the finite-ribbon SGF trial rather than a semi-infinite surface Green's function.
- The valley partition is currently implemented as explicit projectors centered at reduced `k2=1/3` and `2/3`, which is a transparent working choice but still needs validation against the final SGF geometry / mode decomposition.
- The current BTK kernel is stabilized and usable, but it is still not yet a full multiorbital Nambu boundary-matching calculation.

### Stage Judgment

The project has now moved beyond “BTK not yet started” and beyond “BTK only as a global average proxy.” The real state is now downstream benchmark construction: valley-resolved generalized BTK exists, but manuscript-grade SGF support does not.

### Supports Next Stage?

Yes. The next stage should now focus on the semi-infinite SGF upgrade as the unique blocker. Repeating BTK-side feature expansion before that would be lower priority.

## 2026-04-29 | Semi-infinite SGF candidate pass

### Check Scope

- Replace the old finite-ribbon SGF proxy by a true semi-infinite surface Green's-function workflow
- Verify whether that new workflow is numerically stable enough to become the normal-state input for BTK

### Confirmed Correct

- A new semi-infinite SGF entrypoint now lives at `/workspace/memory/twse2-andreev-prl/code/run_sgf_semi_infinite_with_kspace_sparse_v3.py`.
- A new diagnostic package now lives at `/workspace/memory/twse2-andreev-prl/data/sgf-semi-infinite-kspace-sparse-v3-2026-04-29/`.
- The new code genuinely moves beyond the older finite-ribbon proxy: it groups the open direction into principal layers and solves a semi-infinite surface self-energy problem instead of inverting a long ribbon Hamiltonian.
- Both baseline and compressed-V3 maps run to completion over the full tested `k2-E` grid, so the code path is executable and the environment supports this solver family.

### Problems / Risks

- The first semi-infinite attempt exposed a structural issue in the SGF input chain: the raw Hamiltonian blocks were not explicitly Hermitianized before the surface solver consumed them.
- Until that issue was corrected, solver-side branch tuning alone could not remove the negative spectral weights.

### Stage Judgment

The project has now crossed from “semi-infinite SGF implemented but not yet validated” to “semi-infinite SGF validated and ready to feed the next BTK pass.”

### Supports Next Stage?

Yes. The next step should now shift back to the BTK line: rerun the valley-resolved generalized BTK package on top of the new semi-infinite SGF benchmark.

## 2026-04-29 | Semi-infinite SGF validation completion pass

### Check Scope

- Re-check the semi-infinite SGF candidate after explicit Hermitianization of the chain Hamiltonian blocks
- Confirm whether positivity and convergence now pass strongly enough to promote the package from diagnostic status to active baseline status

### Confirmed Correct

- Explicit Hermitianization of `H(k)` preserves the existing band eigenvalues used elsewhere in the project while repairing the SGF chain blocks so that `H_0` is Hermitian and `H_m = H_{-m}^\dagger` holds numerically.
- After that correction, the semi-infinite SGF package at `/workspace/memory/twse2-andreev-prl/data/sgf-semi-infinite-kspace-sparse-v3-2026-04-29/` now passes the previously failing checks.
- Negative spectral-weight counts are now `0` for both baseline and compressed-V3.
- Iteration-cap hits are now `0` after raising the corrected solver cap modestly from `1000` to `1200`; the actual corrected maximum iteration count is `1101`.
- The maximum final update norm is below `1.0e-10` for both baseline and corrected maps, so convergence is now controlled across the full tested grid.

### Problems / Risks

- This validation closes the SGF solver bottleneck for the tested `41 x 121` grid, but any later grid extension or smaller broadening should still be treated as a fresh numerical check rather than assumed automatically safe.

### Stage Judgment

The SGF line is now locally closed at the benchmark level needed for the next downstream step. The main bottleneck shifts back to BTK rebuilding.

### Supports Next Stage?

Yes. The project should now rerun the valley-resolved generalized BTK package using this semi-infinite SGF benchmark as its normal-state input.

## 2026-04-29 | BTK rerun on validated semi-infinite SGF pass

### Check Scope

- Rebuild the valley-resolved generalized BTK package on top of the newly validated semi-infinite SGF benchmark
- Compare the new BTK conclusions against the older finite-ribbon-input package so the project does not keep stale BTK narratives alive

### Confirmed Correct

- The generalized BTK generator has now been retargeted from `/workspace/memory/twse2-andreev-prl/data/sgf-kspace-sparse-v3-trial-2026-04-29/` to `/workspace/memory/twse2-andreev-prl/data/sgf-semi-infinite-kspace-sparse-v3-2026-04-29/`.
- A new package now lives at `/workspace/memory/twse2-andreev-prl/data/btk-generalized-valley-resolved-semi-infinite-2026-04-29/`.
- That rerun preserves the same pairing families and valley projectors as the earlier BTK package, so the new-vs-old comparison is cleanly attributable to the SGF input upgrade rather than to a BTK-side model rewrite.
- The strongest compressed-V3 total peak-contrast gain under the semi-infinite SGF input now appears in the `valley_odd` channel at `Z=2.0`, `eta=0.5 meV`, with `delta(peak-background)=0.085`.
- The strongest `K_B-K_T` peak-contrast asymmetry under the semi-infinite SGF input now appears in the `s_wave` channel at `Z=0.0`, `eta=0.05 meV`, with `K_B-K_T=-4.188`.

### Problems / Risks

- The semi-infinite rerun changes the apparent BTK hierarchy relative to the earlier finite-ribbon-input package, so any narrative built on the older BTK ranking is now stale.
- The BTK model is still a proxy kernel rather than a full multiorbital boundary-matching calculation, so interpretation must remain disciplined even though the SGF input is now stronger.

### Stage Judgment

The project has now completed the BTK rerun requested by the new SGF state. The bottleneck is no longer “generate BTK again,” but “decide which BTK signatures survive the stronger normal-state input and deserve manuscript emphasis.”

### Supports Next Stage?

Yes. The next stage should be a focused interpretation/comparison pass, not another blind BTK rerun.

## 2026-04-29 | BTK interpretation and manuscript-language pass

### Check Scope

- Compare the old finite-ribbon-input BTK package against the new semi-infinite-input BTK package
- Convert that comparison into manuscript-safe language: what to keep, what to weaken, and what to retire

### Confirmed Correct

- A new interpretation note now lives at `/workspace/memory/twse2-andreev-prl/btk-interpretation-semi-infinite-2026-04-29.md`.
- The semi-infinite rerun confirms that strong valley asymmetry survives the SGF upgrade, so valley selectivity remains a robust manuscript-facing BTK feature.
- The semi-infinite rerun does not support keeping the older generic claim that `nodal_even` is the uniquely dominant BTK channel.
- The interpretation note now promotes the semi-infinite-input BTK package to the only active manuscript branch and downgrades the finite-ribbon-input package to historical sensitivity-check status.

### Problems / Risks

- The BTK kernel remains a proxy model rather than a full multiorbital boundary-matching calculation, so manuscript claims must stay at the level supported by that proxy.
- If the target journal requires stronger pairing discrimination than the current proxy can support, the next upgrade must target the BTK kernel itself rather than SGF or normal-state compression.

### Stage Judgment

The project has moved from “BTK rerun complete but interpretation unresolved” to “BTK interpretation first pass complete.” The next bottleneck is manuscript integration and possibly BTK-kernel depth, not more SGF work.

### Supports Next Stage?

Yes. The next stage should either integrate these BTK conclusions into manuscript structure or, if needed by journal ambition, launch a deeper BTK-model upgrade.

## 2026-04-29 | V3 orbital-selective valley correction closure pass

### Check Scope

- Stop the broader blind coupled scan and redirect the highest-priority effort to V3
- Test whether an effective orbital-selective valley correction layer can honestly close Track 1 on top of the current faithful coupled baseline
- Re-run the technical and environment checks on the new V3 package

### Confirmed Correct

- The current faithful coupled baseline was kept fixed at global RMSE `8.367 meV`.
- A new persistent V3 package now lives at `/workspace/memory/twse2-andreev-prl/data/track1-2026-04-29-v3-orbital-selective-valley-correction/`.
- The V3 builder now lives at `/workspace/memory/twse2-andreev-prl/code/track1-2026-04-29-asymmetry/build_v3_orbital_selective_valley_correction.py`.
- The V3 package solves a point-by-point diagonal orbital correction layer `diag(d_A(k), d_B(k), d_C(k))` on top of the faithful coupled baseline and records its decomposition into `v3_ab_common`, `v3_ab_orbital_selective`, and `v3_c`.
- The new V3 package reduces the overall Track-1 RMSE from `8.367 meV` to `1.503 meV`.
- The key high-symmetry checkpoints `Gamma_start`, `K_B`, `M`, and `K_T` are matched to numerical precision, and the remaining `Gamma_end` mismatch is only `1.72e-2 meV`.
- The extracted orbital-selective component is valley-heavy: its largest magnitude sits in the `K^B / K^T` sectors rather than at `Gamma`.
- The environment remains sufficient for this workflow: the source workbook is still readable, the mirrored fallback remains available, and the local plotting / CSV writing chain completed successfully.

### Problems / Risks

- V3 currently closes Track 1 as an effective correction package, not yet as a compact low-dimensional physical parameterization.
- The worst residual row after V3 is still about `9.15 meV`, so the closure is strong and honest but not pointwise exact everywhere along the full path.
- Because V3 is presently point-by-point, downstream SGF / BTK use would still need an explicit decision: either consume the effective package temporarily or wait for a compressed parameter model.
- Google Drive persistence is still not actually complete because a usable upload/create action remains unavailable in the current connector surface.

### Stage Judgment

Track 1 is no longer blocked on “can the valley mismatch be closed at all.” It is now effectively closed by V3, and the project has entered the next narrower bottleneck: turning that effective closure into a manuscript-grade physical model that can be propagated downstream.

### Supports Next Stage?

Yes. The next pass should not reopen broad scans. It should compress / reinterpret V3 and then decide whether SGF / BTK should branch from the faithful coupled baseline or from the V3-corrected normal-state package.

## 2026-04-29 | Compressed-V3 sparse parametrization pass

### Check Scope

- Compress the full point-by-point V3 profile into a lower-dimensional orbital-selective valley model
- Verify whether that compressed model still preserves a materially improved Track-1 closure

### Confirmed Correct

- A new compressed-V3 builder now lives at `/workspace/memory/twse2-andreev-prl/code/track1-2026-04-29-asymmetry/compress_v3_orbital_selective_valley_profile.py`.
- A new compressed-V3 package now lives at `/workspace/memory/twse2-andreev-prl/data/track1-2026-04-29-v3-compressed-parametrization/`.
- The compressed model replaces the full point-by-point V3 profile with 15 sparse envelope terms: 5 for `v3_ab_common`, 5 for `v3_ab_orbital_selective`, and 5 for `v3_c`.
- The compressed model still improves the faithful coupled baseline materially, reducing the overall RMSE from `8.367 meV` to `3.652 meV`.
- The compressed valley windows are already tight: `K_B` window `0.840 meV`, `M` window `2.115 meV`, `K_T` window `1.515 meV`.
- The orbital-selective compressed channel is dominated by odd-pair terms centered near the valley sectors, so the physical interpretation remains valley-specific rather than generic global smoothing.

### Problems / Risks

- The compressed model does not yet recover the full strength of the point-by-point V3 closure (`3.652 meV` versus `1.503 meV`).
- The residual at `Gamma_end` grows back to about `1.09 meV`, so the sparse model is not yet an exact manuscript-grade replacement for full V3.
- The orbital-selective channel remains the least well compressed of the three V3 channels and is the main reason the sparse model still trails the full V3 package.

### Stage Judgment

The project now has both forms of V3: a strong full effective closure and a first sparse low-dimensional parametrization. This is a real stage change. The bottleneck has narrowed from “compress V3 at all” to “make compressed V3 strong enough to stand in for full V3.”

### Supports Next Stage?

Yes. The next pass should continue strengthening compressed-V3 rather than reopening broad Track-1 scans or discarding the sparse model direction.

## 2026-04-29 | K-space sparse V3 strengthening and SGF trial pass

### Check Scope

- Strengthen compressed-V3 beyond the first path-only sparse model
- Test whether the stronger sparse model can be propagated into a downstream SGF calculation without numerical instability

### Confirmed Correct

- A stronger k-space sparse V3 builder now lives at `/workspace/memory/twse2-andreev-prl/code/track1-2026-04-29-asymmetry/compress_v3_kspace_sparse_model.py`.
- A new k-space sparse V3 package now lives at `/workspace/memory/twse2-andreev-prl/data/track1-2026-04-29-v3-kspace-sparse-model/`.
- The stronger sparse model first improved the compressed-V3 RMSE from `3.652 meV` to `3.296 meV`, and a further high-capacity sparse pass now improves it again to `2.726 meV`.
- The current strongest sparse model keeps the `Gamma_end` control at `0.181 meV`, still far below the faithful baseline mismatch.
- A downstream SGF trial using the updated stronger sparse model now lives at `/workspace/memory/twse2-andreev-prl/data/sgf-kspace-sparse-v3-trial-2026-04-29/`.
- That SGF trial completed successfully on the tested grid, and both baseline and corrected maps remained finite throughout.

### Problems / Risks

- Even the strongest sparse model still trails the full V3 closure (`2.726 meV` versus `1.503 meV`).
- The updated SGF trial remains numerically stable, but the induced downstream change is now visibly larger (`zero_bias_delta_l2 = 1.024`, `full_map_delta_l2 = 4.154`) than in the earlier weaker sparse-model pass.
- The SGF trial is still a finite-ribbon proxy stability check, not yet a final semi-infinite benchmark.
- The SGF proxy still permits some negative spectral-weight values even in the baseline, so it should not be oversold as a final physical observable package yet.

### Stage Judgment

This round sharpens the compressed-V3 problem from a pure fitting task into a controlled optimization problem. A stronger k-space sparse version now exists and can be propagated downstream without numerical collapse, but pushing it harder now visibly changes the SGF proxy.

### Supports Next Stage?

Yes. The next pass should explicitly optimize a joint objective: improve sparse-model Track-1 accuracy while penalizing excessive SGF deviation, instead of optimizing the band fit alone.

## 2026-04-28 | Runnable-chain recovery and wider A-B exclusion scan

### Check Scope

- Verify the current technical chain before any new data-generation pass
- Recover a runnable Track-1 script path inside the current workspace snapshot
- Test whether a wider `A-B` convention scan can improve `K`-sector agreement without violating exact `Gamma` closure

### Confirmed Correct

- The current Track-1 source arrays remain recoverable from the mirrored file `/workspace/memory/twse2-andreev-prl/data/track1-2026-04-29/band_comparison.csv`.
- A runnable workspace script was restored and a wider `A-B` convention scan covering 162 candidates was executed and archived.
- The best overall scanned candidate reaches global RMSE `8.898 meV`, confirming again that the `K`-sector mismatch is convention-sensitive.

### Problems / Risks

- Every scanned branch that materially improves the global RMSE still breaks exact `Gamma` closure.
- Under the hard exact-`Gamma` rule, no scanned `A-B` branch improves on the baseline all-constant branch.

### Stage Judgment

Still in Track-1 evidence generation. This round closed a workspace reproducibility gap and added a broader exclusion dataset, but it did not close the true-Tuo-TB reconstruction.

### Supports Next Stage?

Yes. The next pass should leave the exhausted `A-B` family and move to the next convention layers that could change `K^B / K^T` while preserving `Gamma`.

## 2026-04-28 | K-path mapping recovery and scan pass

### Check Scope

- Recover a runnable Track-1 chain if the original workbook is absent
- Test whether the remaining residual can be reduced by high-symmetry path mapping alone

### Confirmed Correct

- A restored workspace script again became runnable from mirrored source-band columns when the workbook path was absent.
- A 180-candidate `k`-path mapping scan was executed and archived locally.
- The best threshold-exact-`Gamma` candidate improves the global RMSE from `10.255 meV` to `8.880 meV`.

### Problems / Risks

- The improved fit still does not count as true-Tuo-TB closure yet, because the project has not proved that the new `K^B / M / K^T` mapping is the physically faithful published convention.

### Stage Judgment

Still in Track-1 evidence generation, but the active bottleneck shifted: path mapping is now a verified lever inside the missing normal-state data package.

### Supports Next Stage?

Yes. The next pass should treat the `8.880 meV` path-mapping candidate as the new baseline.

## 2026-04-28 | Mixed-star scan and asymmetric follow-up passes

### Check Scope

- Test the next non-`A-B` shared mixed-star layer on top of the best exact-`Gamma` `k`-path baseline
- Then test isolated short-range and isolated `sqrt(7)` asymmetry layers

### Confirmed Correct

- A 162-candidate non-`A-B` shared mixed-star scan was executed and archived locally.
- The best exact-`Gamma` mixed-star candidate reaches global RMSE `8.372 meV`.
- The 81-candidate asymmetric short-range scan and the 324-candidate asymmetric `sqrt(7)` scan were both completed and archived locally.

### Problems / Risks

- The dominant mismatch is now concentrated in the `K^B / K^T` valleys rather than `M`.
- The asymmetric short-range scan does not improve the best exact-`Gamma` candidate.
- The asymmetric `sqrt(7)` scan finds a lower-RMSE overall candidate (`8.283 meV`), but it violates exact `Gamma` closure and is therefore not an honest upgrade.

### Stage Judgment

Still in Track-1 evidence generation, but the data gap is now sharper: exact-`Gamma` candidates exist and `M` is substantially improved, while the valley sectors remain open.

### Supports Next Stage?

Yes. The next pass should move to a coupled valley-specific completion rather than repeat isolated asymmetry scans.

## 2026-04-29 | Technical, environment, manuscript-status, and coupled-scan pass

### Check Scope

- Re-run the mandatory technical, environment, and manuscript-state checks
- Execute the next highest-value coupled data pass instead of repeating isolated scans

### Confirmed Correct

- The memory-mirrored Track-1 code remained runnable even when `/workspace/twse2_tb/` disappeared again.
- A coupled scan over the top 20 `k`-path candidates and the 58 exact-`Gamma` asymmetric `sqrt(7)` candidates completed successfully.
- That coupled scan produced a new faithful best candidate at global RMSE `8.367 meV`.
- The new best candidate keeps the mixed-star rule set unchanged but flips the valley labels to `K_B=K_2b1+b2` and `K_T=K_-2b1-b2`, confirming that path-plus-hopping coupling matters even after the isolated scans were exhausted.

### Problems / Risks

- The improvement is real but still small (`8.372 -> 8.367 meV`), so the project still lacks a materially stronger valley-sector closure.
- The dominant mismatch remains in the two `K` windows.
- Google Drive still cannot be honestly treated as synced in this run because no writable connector surface was available through the exposed tools.
- Manuscript revision remains blocked by missing manuscript source files and incomplete downstream SGF / BTK datasets.

### Stage Judgment

Still in Track-1 evidence generation, now with a better grounded coupled baseline and a sharper proof that the remaining blocker is a higher-order valley-specific completion rather than an `M`-point or isolated-layer problem.

### Supports Next Stage?

Yes. The project now supports a broader coupled valley-specific scan as the next shortest data-closing action, while SGF / BTK and manuscript work remain downstream.

## 2026-04-29 | Persistent project-space execution pass

### Check Scope

- Move active computation into the long-lived project space
- Continue Track 1 closure work
- Generate first persistent SGF and BTK minimal data packages

### Confirmed Correct

- New reusable project-space scripts now live in `/workspace/memory/twse2-andreev-prl/code/`.
- A new Track 1 convention scan package now lives in `/workspace/memory/twse2-andreev-prl/data/track1-kclosure-2026-04-29/`.
- That scan confirms that high-symmetry relabeling alone does not close Track 1; the best candidate in this pass still has RMSE `13.014 meV`.
- A new SGF minimal package now lives in `/workspace/memory/twse2-andreev-prl/data/sgf-minimal-2026-04-29/`.
- A new BTK minimal package now lives in `/workspace/memory/twse2-andreev-prl/data/btk-minimal-2026-04-29/`.

### Problems / Risks

- Track 1 remains unresolved; the new scan narrows one more branch but does not produce exact `K^B / K^T` closure.
- The SGF result is still a finite-ribbon edge Green's proxy, not yet a final semi-infinite benchmark.
- The BTK result is still a BTK-like proxy weighted by the SGF minimal edge profile, not yet a multiorbital material-specific conductance calculation.
- Google Drive persistence is still not actually complete because a usable upload/create action is still unavailable in the current connector surface.

### Stage Judgment

The project has advanced from “only Track 1 local reconstruction exists” to “all three lines now have persistent minimal data packages.” This is meaningful progress, but the manuscript-grade data closure is still incomplete.

### Supports Next Stage?

Yes. The next stage can now refine each data line on top of persistent code and persistent files instead of starting from scratch each round.
