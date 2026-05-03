# tWSe2 project long-term-space sync manifest

Project: `twse2_prl_20260501`
Source: `/workspace/memory/twse2_prl_20260501`
Date: 2026-05-03

This manifest records the current local long-term project space synchronized to GitHub through the connector. A full zip snapshot is split into base64 chunks under `twse2_prl_20260501/github_sync/full_snapshot_20260503_parts/`.

## Snapshot

- archive: `twse2_prl_20260503_fullsync.zip`
- archive sha256: `f1ccb6ff8996de9bb3b7bad32962ee2914f69a76b76ec7836c0ba5fcfefc0094`
- archive size bytes: `2537021`
- part count: 3

## Parts

| part | raw bytes | sha256 | stored file |
|---|---:|---|---|
| `twse2_prl_20260503_fullsync.part.aa` | 921600 | `7602902bfb994011c0466047bddd77dff2eb751093b00447a506a90cc2065eb9` | `twse2_prl_20260503_fullsync.part.aa.b64` |
| `twse2_prl_20260503_fullsync.part.ab` | 921600 | `9472a920d6dc617d30929d5fd94ad2c018b098be0de6ccacf7bfdcc443fe7ad0` | `twse2_prl_20260503_fullsync.part.ab.b64` |
| `twse2_prl_20260503_fullsync.part.ac` | 693821 | `198db5946fecc3709e4aea001bb5684227089e792e3d1dbf0e9d986b82f6eed7` | `twse2_prl_20260503_fullsync.part.ac.b64` |

## Reassembly

```bash
cd twse2_prl_20260501/github_sync/full_snapshot_20260503_parts
base64 -d twse2_prl_20260503_fullsync.part.aa.b64 > twse2_prl_20260503_fullsync.part.aa
base64 -d twse2_prl_20260503_fullsync.part.ab.b64 > twse2_prl_20260503_fullsync.part.ab
base64 -d twse2_prl_20260503_fullsync.part.ac.b64 > twse2_prl_20260503_fullsync.part.ac
cat twse2_prl_20260503_fullsync.part.aa twse2_prl_20260503_fullsync.part.ab twse2_prl_20260503_fullsync.part.ac > twse2_prl_20260503_fullsync.zip
sha256sum twse2_prl_20260503_fullsync.zip
unzip -t twse2_prl_20260503_fullsync.zip
```

## File manifest

```text
README.md	3284
ncomms-execution-status-2026-05-03.md	3214
project-space-index.md	1369
results/alpha_btk_correlation_2026-05-02/alpha_btk_correlation_figure.png	48015
results/alpha_btk_correlation_2026-05-02/alpha_btk_correlation_summary.csv	99078
results/alpha_btk_correlation_2026-05-02/alpha_btk_pairing_slice_dataset.csv	407169
results/alpha_btk_correlation_2026-05-02/alpha_btk_valley_asymmetry_correlation.csv	5193
results/alpha_btk_correlation_2026-05-02/alpha_rule_family_slices.csv	2613
results/alpha_btk_correlation_2026-05-02/summary.md	1480
results/channel_resolved_multiorbital_btk_2026-05-02/ar_onset_alignment.csv	1599
results/channel_resolved_multiorbital_btk_2026-05-02/ar_peak_vs_delta_in_alignment.png	22957
results/channel_resolved_multiorbital_btk_2026-05-02/channel_resolved_conductance.csv	1937421
results/channel_resolved_multiorbital_btk_2026-05-02/channel_weights_vs_alpha.csv	2651
results/channel_resolved_multiorbital_btk_2026-05-02/channel_weights_vs_alpha.png	22547
results/channel_resolved_multiorbital_btk_2026-05-02/pairing_symmetry_comparison.png	39725
results/channel_resolved_multiorbital_btk_2026-05-02/summary.md	1359
results/channel_resolved_multiorbital_btk_2026-05-02/summed_conductance.csv	387394
results/channel_resolved_multiorbital_btk_2026-05-02/verification_metrics.csv	393
results/convergence_reproducibility_suite_2026-05-03/summary.md	4677
results/e4_to_e11_package_2026-05-03/e10_reviewer_response_map.md	1812
results/e4_to_e11_package_2026-05-03/e11_submission_package_audit.md	825
results/e4_to_e11_package_2026-05-03/e4_inner_gap_selectivity.md	1198
results/e4_to_e11_package_2026-05-03/e5_pairing_negative_controls.md	1239
results/e4_to_e11_package_2026-05-03/e7_methods_strengthening.md	1202
results/e4_to_e11_package_2026-05-03/e8_material_priority.md	520
results/e4_to_e11_package_2026-05-03/e9_reference_positioning.md	1404
results/e4_to_e11_package_2026-05-03/summary.md	514
results/e5_e8_package_2026-05-02/e5_swave_failure_map.csv	1449
results/e5_e8_package_2026-05-02/e6_decision_tree.md	1984
results/e5_e8_package_2026-05-02/e7_prl_gate.md	1585
results/e5_e8_package_2026-05-02/e8_manuscript_scaffold.md	2032
results/e5_e8_package_2026-05-02/summary.md	534
results/e5_to_e8_package_2026-05-02/summary.md	698
results/kernel_invariance_tests_2026-05-02/invariance_summary.csv	627
results/kernel_invariance_tests_2026-05-02/kernel_invariance_alpha_window.png	21403
results/kernel_invariance_tests_2026-05-02/manuscript_ready_kernel_invariance_patch.md	2405
results/kernel_invariance_tests_2026-05-02/summary.md	1499
results/observable_constraint_negative_control_2026-05-03/constraint_summary.csv	2407
results/observable_constraint_negative_control_2026-05-03/manuscript_ready_observable_definition_patch.md	3551
results/observable_constraint_negative_control_2026-05-03/manuscript_ready_trivial_control_patch.md	5305
results/observable_constraint_negative_control_2026-05-03/summary.md	4484
results/xi_ar_zeeman_scan_2026-05-02/metrics.json	386
results/xi_ar_zeeman_scan_2026-05-02/summary.md	952
results/xi_ar_zeeman_scan_2026-05-02/xi_ar_scan.csv	611
revision-tracker-ncomms-2026-05-03.md	8743
scripts/build_alpha_btk_correlation.py	21741
scripts/build_channel_resolved_multiorbital_btk.py	28537
scripts/build_e4_e11_package.py	26122
scripts/build_e5_e8_package.py	18420
scripts/build_xi_ar_scan.py	7183
scripts/run_kernel_invariance_tests.py	12665
scripts/run_observable_constraint_negative_control.py	17765
scripts/update_sync_status.py	4120
submission_package_nc_2026-05-03/main.pdf	339759
submission_package_nc_2026-05-03/response_to_reviewers_summary.md	1597
submission_package_nc_2026-05-03/source_data/SourceData_NC_revision.xlsx	93731
submission_package_nc_2026-05-03/supplementary_information.pdf	160586
submission_package_nc_2026-05-03_clean.zip	734880
submission_package_nc_2026-05-03_rev2.zip	759602
sync-status.md	2237
```
