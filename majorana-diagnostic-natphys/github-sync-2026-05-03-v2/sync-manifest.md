# CMJJ sync manifest - 2026-05-03

## Verification hashes

```text
5e6ed1fcf1804a338ebe083a49b37a68d110334ded7f590a895fcdec1f1536c8  cmjj-project-space-2026-05-03.tar.gz
2f9ca6173a4e8f8c4a10ebfa8114d455c316da5ff502d909e4ed734cf524f20c  source-data-only-2026-05-03.tar.gz
```

## Source roots included in the prepared archive

```text
/workspace/memory/majorana-diagnostic-natphys
/workspace/submission_draft_main.tex
/workspace/submission_draft_main.pdf
/workspace/supplementary_information.tex
/workspace/supplementary_information.pdf
/workspace/references_verified.bib
/workspace/submission_pack_latex_ready.tex
/workspace/submission_pack_rewrite.md
/workspace/fig45_and_reviewer_pressure_pack.md
/workspace/figures/Fig4_negative_controls.{png,pdf}
/workspace/figures/Fig5_nonlocal_transport.{png,pdf}
```

## Long-term project-space source data included

```text
majorana-diagnostic-natphys/data/cmjj-source-data-2026-05-01/README.md
majorana-diagnostic-natphys/data/cmjj-source-data-2026-05-01/manifest.json
source_data_fig2/fig2a_normal_state_spin_splitting.csv
source_data_fig2/fig2b_bulk_gap_mu_phi.csv
source_data_fig2/fig2c_ring_invariant_mu_phi.csv
source_data_fig2/fig2d_refined_phi_cut_mu_1p0.csv
source_data_fig3/fig3a_open_boundary_spectrum_vs_phi.csv
source_data_fig3/fig3b_topological_wavefunction_profile.csv
source_data_fig3/fig3c_trivial_dot_mimic_profile.csv
source_data_fig3/fig3d_isolation_endweight_vs_phi.csv
source_data_fig4/fig4a_dot_control_sweep.csv
source_data_fig4/fig4b_impurity_control_sweep.csv
source_data_fig4/fig4c_disorder_ensemble.csv
source_data_fig4/fig4d_control_summary_table.csv
source_data_fig5/fig5a_positive_transport_heatmap.csv
source_data_fig5/fig5b_dot_transport_heatmap.csv
source_data_fig5/fig5c_impurity_transport_heatmap.csv
source_data_fig5/fig5d_disorder_robustness.csv
```

## Recovery commands after binary upload

```bash
sha256sum cmjj-project-space-2026-05-03.tar.gz
sha256sum source-data-only-2026-05-03.tar.gz
tar -xzf cmjj-project-space-2026-05-03.tar.gz
```

## Status

- Metadata and manifest synced to GitHub using the connector.
- Full binary/source-data archives prepared locally.
- Large archive upload should be completed by git/Git LFS or GitHub Releases because the current connector is text-file oriented.
