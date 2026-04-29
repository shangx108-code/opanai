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

## 2026-04-28 | Runnable-chain recovery and wider A-B exclusion scan

### Check Scope

- Verify the current technical chain before any new data-generation pass
- Recover a runnable Track-1 script path inside the current workspace snapshot
- Test whether a wider `A-B` convention scan can improve `K`-sector agreement without violating exact `Gamma` closure

### Confirmed Correct

- The current workspace snapshot does not contain the earlier local paths `/workspace/tmp/ws2/41467_2025_64519_MOESM3_ESM.xlsx` or `/workspace/user_files/04-ws2.zip`, so direct dependence on those paths would currently break execution.
- The current Track-1 source arrays remain recoverable from the mirrored file `/workspace/memory/twse2-andreev-prl/data/track1-2026-04-29/band_comparison.csv`, so Track 1 can continue honestly without inventing data.
- A runnable workspace script has now been restored at `/workspace/twse2_tb/reconstruct_tuo_tb.py`, and it reproduces the baseline Track-1 package while falling back to the mirrored source arrays if the original workbook is absent.
- A wider `A-B` convention scan covering 162 candidates has now been executed and archived.
- The best overall scanned candidate reaches global RMSE `8.898 meV`, confirming again that the `K`-sector mismatch is convention-sensitive.

### Problems / Risks

- Every scanned branch that materially improves the global RMSE still breaks exact `Gamma` closure, with the best overall branch missing the `Gamma` constraint by about `8.19 meV`.
- Under the hard acceptance rule `max abs delta < 0.05 meV` at both `Gamma` endpoints, no scanned `A-B` branch improves on the current baseline; the best exact-`Gamma` candidate is still the baseline all-constant branch at `10.255 meV`.
- Google Drive still lacks a usable generic upload path in this session, so the new scan artifacts can only be claimed as locally archived, not cloud-synced.

### Stage Judgment

Still in Track-1 evidence generation. This round closed a workspace reproducibility gap and added a broader exclusion dataset, but it did not close the true-Tuo-TB reconstruction.

### Supports Next Stage?

Yes. The next pass should leave the exhausted `A-B` family and move to the next convention layers that could change `K^B / K^T` while preserving `Gamma`, such as non-`A-B` mixed-star gauge choices or explicit high-symmetry path mapping checks.

## 2026-04-28 | K-path mapping recovery and scan pass

### Check Scope

- Verify the current technical chain before any new data-generation pass
- Recover a runnable Track-1 script path inside the current workspace snapshot if the original workbook is absent
- Test whether the remaining residual can be reduced by high-symmetry path mapping alone before changing the hopping table again

### Confirmed Correct

- In this workspace snapshot, the previously cited `/workspace/twse2_tb` and `/workspace/output` tree were absent, so the runnable chain did need to be rebuilt before further data work.
- A restored workspace script now exists at `/workspace/twse2_tb/reconstruct_tuo_tb.py`, and it runs from the mirrored source-band columns when `/workspace/tmp/ws2/41467_2025_64519_MOESM3_ESM.xlsx` is missing.
- The current Python environment has `numpy`, `pandas`, and `Pillow`; `matplotlib` and `scipy` are absent, but they do not block the present Track-1 scripts.
- A 180-candidate `k`-path mapping scan has now been executed and archived locally.
- The best threshold-exact-`Gamma` candidate in that scan improves the global RMSE from `10.255 meV` to `8.880 meV` with `Gamma_end` max abs residual `0.0132 meV`.
- A duplicated-boundary source-compatible variant reaches `8.900 meV` while restoring the final `Gamma` row exactly to numerical precision.
- Google Drive profile lookup and project search are working again.

### Problems / Risks

- The improved fit still does not count as true-Tuo-TB closure yet, because the project has not proved that the new `K^B / M / K^T` mapping is the physically faithful published convention rather than an equally plausible relabeling.
- The hopping-table ambiguity is therefore narrowed but not removed; the next scan still has to move into non-`A-B` mixed-star / gauge choices on top of the improved path baseline.
- The current Google Drive connector surface still does not expose a generic file-upload / folder-placement path for the full CSV + PNG + Python artifact bundle, so this round can only claim local archival, not cloud sync.

### Stage Judgment

Still in Track-1 evidence generation, but the active bottleneck has shifted. The project is no longer justified in treating the old path convention as fixed; path mapping is now a verified lever inside the missing normal-state data package.

### Supports Next Stage?

Yes. The next pass should treat the `8.880 meV` path-mapping candidate as the new baseline and rerun the next non-`A-B` mixed-star / gauge layer rather than revisiting the exhausted old baseline.

## 2026-04-28 | Mixed-star scan and state-hardening pass

### Check Scope

## 2026-04-28 | Technical / environment / manuscript check plus asymmetric follow-up scans

### Check Scope

- Re-run the required technical state check before generating new data
- Re-run the environment and Google Drive availability check
- Re-run the manuscript-state check
- Test whether the remaining `K^B / K^T` mismatch can be improved by breaking `A-C / B-C` sharing in two isolated layers:
  - short-range (`|R|=1, 2`)
  - `sqrt(7)` mixed-star layer

### Confirmed Correct

- The current workspace snapshot initially lacked `/workspace/twse2_tb`, so the runnable Track-1 chain did need to be restored again before the new scan pass.
- The current Python environment still has `numpy`, `pandas`, and `Pillow`, while `matplotlib` and `scipy` remain absent; the present Track-1 scans do not require the missing packages.
- No editable manuscript source for this project is present in the current workspace snapshot, so manuscript revision remains gated by data completion plus future source recovery.
- Google Drive profile lookup and project search are still readable in this session, and the project still has no existing Drive folder or file returned by the current searches.
- The 81-candidate asymmetric short-range scan is now complete and archived locally.
- The 324-candidate asymmetric `sqrt(7)` scan is now complete and archived locally.

### Problems / Risks

- The asymmetric short-range scan does not improve the best exact-`Gamma` candidate; the previous shared baseline remains the faithful best point.
- The asymmetric `sqrt(7)` scan finds a lower-RMSE overall candidate (`8.283 meV`), but it violates exact `Gamma` closure by `7.885 meV`, so it is not an honest upgrade.
- The current unresolved bottleneck is therefore no longer generic `A-C / B-C` sharing. It is a narrower coupled valley-specific gauge / path-plus-hopping ambiguity that has not yet been closed by any isolated asymmetry layer.
- Google Drive still does not offer a generic binary upload / folder-placement path for the full CSV + PNG + Python bundle, so this round cannot honestly claim cloud archival.

### Stage Judgment

Still in Track-1 evidence generation, but the exclusion logic is now materially stronger. Two more plausible ambiguity layers have been closed as local exclusion datasets.

### Supports Next Stage?

Yes. The next data pass should move to a coupled valley-specific gauge / indexing completion rather than re-scanning any isolated `A-C / B-C` asymmetry layer.

- Perform the required technical status check, environment check, and manuscript-status check before generating new data
- Restore the runnable Track-1 chain in the current workspace snapshot
- Test the next non-`A-B` shared mixed-star layer on top of the best exact-`Gamma` `k`-path baseline

### Confirmed Correct

- The current workspace snapshot again lacked an active `/workspace/twse2_tb` chain at the start of the round, but the runnable script has now been restored at `/workspace/twse2_tb/reconstruct_tuo_tb.py`.
- A new reproducible scan entrypoint now exists at `/workspace/twse2_tb/scan_mixed_star_gauges.py`.
- The current Python environment still has `numpy`, `pandas`, and `Pillow`, while `matplotlib` and `scipy` remain absent; that does not block the present Track-1 scripts.
- No editable manuscript source for this project is present in the current workspace snapshot, so this round still belongs to data completion rather than manuscript patching.
- A 162-candidate non-`A-B` shared mixed-star scan has now been executed and archived locally.
- The best exact-`Gamma` mixed-star candidate uses `c1=cyc`, `c2=anti`, `c7_first=cyc`, `c7_second=anti`, and `c7_second_conjugated=False`, reaching global RMSE `8.372 meV` with `Gamma_end` max abs delta `0.0362 meV`.
- Relative to the previous best `k`-path-only candidate, this new candidate improves the global RMSE by `0.508 meV` and cuts the `M`-window RMSE from `8.237 meV` to `3.286 meV`.
- The new mixed-star scan package and the updated scripts have been mirrored into the memory folder and indexed for later cloud sync.
- Google Drive profile lookup and project search still work, but searches for `twse2 andreev prl` and `ws2 tuo andreev` continue to return no project folder or file.

### Problems / Risks

- The dominant mismatch is now concentrated in the `K^B / K^T` valleys rather than `M`, so the next scan must explicitly target valley-specific asymmetry instead of repeating shared mixed-star rules.
- The current mixed-star scan still keeps `A-C` and `B-C` tied together within each distance shell; that shared assumption may be the remaining reason exact valley closure is not yet reached.
- The current Google Drive connector surface still does not expose a generic binary upload / folder-placement path, so this round can only claim local archival plus a pending-sync queue, not cloud completion.

### Stage Judgment

Still in Track-1 evidence generation, but the data gap is now sharper. This round converts the old broad “mixed-star / gauge ambiguity” into a much narrower residual problem: exact-`Gamma` candidates exist and `M` is substantially improved, but the `K^B / K^T` valley sectors are still not closed.

### Supports Next Stage?

Yes. The next pass should start from the `8.372 meV` mixed-star baseline and run the smallest asymmetric scan that decouples the still-shared `A-C` and `B-C` phase rules or otherwise tests the next valley-specific gauge layer.

## 2026-04-29 | Technical, environment, manuscript-status, and coupled-scan pass

### Check Scope

- Re-run the mandatory technical status check, environment check, and manuscript-status check before starting a new data pass
- Verify whether the current workspace still exposes the runnable Track-1 directory and whether the Python stack remains sufficient
- Execute the next highest-value coupled data pass instead of repeating isolated scans

### Confirmed Correct

- The current Python environment still supports the active Track-1 chain with `numpy`, `pandas`, and `Pillow`; `scipy` and `matplotlib` remain absent but are not required for the current scripts.
- The current workspace snapshot no longer contains `/workspace/twse2_tb/`, but the memory-mirrored code under `/workspace/memory/twse2-andreev-prl/code/track1-2026-04-29-asymmetry/` remains runnable.
- No editable manuscript source was found for this project in the current workspace scan, so manuscript modification is still not the active work surface.
- A new coupled scan over the top 20 `k`-path candidates and the 58 exact-`Gamma` asymmetric `sqrt(7)` candidates completed successfully and produced a new faithful best candidate at global RMSE `8.367 meV`.
- The new best candidate keeps the mixed-star rule set unchanged but flips the valley labels to `K_B=K_2b1+b2` and `K_T=K_-2b1-b2`, confirming that path-plus-hopping coupling matters even after the isolated scans were exhausted.

### Problems / Risks

- The improvement is real but small (`8.372 -> 8.367 meV`), so the project still lacks a materially stronger valley-sector closure.
- The dominant mismatch remains in the two `K` windows; the coupled scan improved one valley window and slightly worsened the other, rather than closing both.
- Google Drive still cannot be honestly treated as synced in this run because no writable connector surface was available through the exposed tools.
- Manuscript revision remains blocked by missing manuscript source files and incomplete downstream SGF / BTK datasets.

### Stage Judgment

Still in Track-1 evidence generation, now with a better grounded coupled baseline and a sharper proof that the remaining blocker is a higher-order valley-specific completion rather than an `M`-point or isolated-layer problem.

### Supports Next Stage?

Yes. The project now supports a broader coupled valley-specific scan as the next shortest data-closing action, while SGF / BTK and manuscript work remain downstream.
