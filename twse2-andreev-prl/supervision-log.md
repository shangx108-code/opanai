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
