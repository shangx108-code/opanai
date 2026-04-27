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

- Verify that the reconstruction assets cited in the current project state are actually present and runnable in this workspace snapshot

### Confirmed Correct

- The twse2 project still has a clearly specified PRL-oriented target style in saved project notes.
- The previously reported scientific bottleneck order does not change: the first real blocker remains the evidence-chain gap in exact `K`-point valley closure.

### Problems / Risks

- The local files named in the saved state are not present in the current workspace snapshot: `/workspace/user_files/04-ws2.zip`, `/workspace/tmp/ws2/...`, and `/workspace/twse2_tb/reconstruct_tuo_tb.py` could not be found in this run.
- This means the previously reported partial reconstruction status is not currently reproducible from the available local files.
- Until those assets are restored, the project is blocked one layer earlier than before: not only on unresolved `K`-sector convention, but on missing executable reconstruction inputs in the current workspace.

### Stage Judgment

Still in evidence generation, but now with a newly verified workspace-level reproducibility break inside the primary evidence chain.

### Supports Next Stage?

Only after the missing local reconstruction assets are restored or re-supplied in an accessible location.
