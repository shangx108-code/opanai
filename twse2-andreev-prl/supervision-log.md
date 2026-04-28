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
