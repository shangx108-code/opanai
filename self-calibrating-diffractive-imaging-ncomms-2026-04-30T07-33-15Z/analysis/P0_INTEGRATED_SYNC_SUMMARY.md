# P0 results integrated into manuscript and supplement

Generated: 2026-05-02T15:30:52.084718Z

## Scope
This record integrates the latest P0 evidence into the manuscript and supplementary material for the self-calibrating diffractive imaging Nature Communications project.

## Boundary statement
No external raw public PSF dataset was downloaded in this runtime. The available `measured_psf_or_speckle_dataset.npz` is used conservatively as a pseudo-experimental measured-PSF/speckle proxy. The manuscript addendum explicitly avoids presenting it as a completed real-device experiment.

## Key P0 results
- Mismatched PSF proxy PSNR gap vs clean simulation: `-0.314742 dB`
- Tolerance collapse level: `1.00`
- 2-bit phase quantization proxy degradation: `1.472450 dB`
- 2-bit lower 95% CI bound: `1.468161 dB`
- 4-bit phase quantization proxy degradation: `0.148322 dB`

## New manuscript/supplement assets
- `manuscript/p0_results_integration.tex`
- `supplement/p0_supplement_addendum.tex`
- `manuscript/main.pdf` (P0 addendum appended)
- `supplement/supplement.pdf` (P0 addendum appended)

## New source-data assets
- `source_data/psf_public_dataset_eval.csv`
- `source_data/psf_public_vs_simulated_gap.csv`
- `source_data/tolerance_reconstruction_collapse.csv`
- `source_data/tolerance_reconstruction_collapse_detail.csv`
- `source_data/phase_quantization_ci.csv`
- `source_data/phase_quantization_detail.csv`
- `source_data/evidence_ledger.csv`
- `source_data/figure_mapping_p0_public_psf_collapse_quantization.csv`
- `source_data/source_data_index.csv`
- `source_data/submission_artifact_checksums.csv`

## Figures
- `figures/figure_tolerance_collapse.png`
- `figures/figure_phase_quantization_failure.png`
- `figures/figure_psf_domain_gap.png`

## Evidence ledger snapshot

| claim_id   | claim                                                                                            | evidence_file                                     | key_value                                                              | status                        |
|:-----------|:-------------------------------------------------------------------------------------------------|:--------------------------------------------------|:-----------------------------------------------------------------------|:------------------------------|
| P0-1       | PSF proxy domain differs from simulated model and reveals reconstruction/correlation sensitivity | source_data/psf_public_vs_simulated_gap.csv       | mismatched PSNR gap vs clean = -0.315 dB                               | validated_with_proxy_boundary |
| P0-2       | Reconstruction zero-gain/collapse boundary is explicitly extracted from PSF-tolerance sweep      | source_data/tolerance_reconstruction_collapse.csv | first mean collapse level = 1.00                                       | validated                     |
| P0-3       | 2-bit quantization produces statistically stable proxy degradation relative to continuous phase  | source_data/phase_quantization_ci.csv             | 2-bit proxy drop = 1.472 dB, 95% CI low = 1.468; 4-bit drop = 0.148 dB | validated                     |

## Figure mapping snapshot

| figure   | panel                      | data_file                                         | script                                                    | metric                                                                   |
|:---------|:---------------------------|:--------------------------------------------------|:----------------------------------------------------------|:-------------------------------------------------------------------------|
| Fig5     | tolerance collapse         | source_data/tolerance_reconstruction_collapse.csv | scripts/generate_p0_results_and_manuscript_integration.py | PSNR gain vs mismatched baseline                                         |
| Fig5     | phase quantization failure | source_data/phase_quantization_ci.csv             | scripts/generate_p0_results_and_manuscript_integration.py | phase entropy; speckle correlation; proxy reconstruction drop            |
| Fig6     | PSF proxy domain gap       | source_data/psf_public_vs_simulated_gap.csv       | scripts/generate_p0_results_and_manuscript_integration.py | contrast; sparsity; high-frequency spectral fraction; reconstruction gap |
| Fig6     | PSF proxy evaluation       | source_data/psf_public_dataset_eval.csv           | scripts/generate_p0_results_and_manuscript_integration.py | PSNR; SSIM; correlation                                                  |

## Checksums snapshot

| file                                                      | sha256                                                           |   size_bytes |
|:----------------------------------------------------------|:-----------------------------------------------------------------|-------------:|
| source_data/psf_public_dataset_eval.csv                   | 0b7e28b5395c336c138d7e13e97fd921899600d7e0bd5be65f7969ee60fe1d16 |        33156 |
| source_data/psf_public_vs_simulated_gap.csv               | ba40fb76ba7581a1b975b13304729821b1aea544930d486922e973d31d0c374b |         1494 |
| source_data/psf_public_psf_stats_detail.csv               | 08732b02f7e0e68a208c0414381f4de886766524e6694d4cdfde642cdcc387b9 |         7925 |
| source_data/tolerance_reconstruction_collapse.csv         | 3736ca8596e403fd0c48ce6caf2464260d6cdd4a30569e0c50b3fd1eb7941179 |         1357 |
| source_data/tolerance_reconstruction_collapse_detail.csv  | 55ea10f97d9cf2afe6277761bf43fe06434b34df61420bb70042dae4ec209758 |       300899 |
| source_data/phase_quantization_ci.csv                     | ca4368e93a369219c03bbc2d4861031130382b7f0c84dc16e20c8fe6f63a31ed |          831 |
| source_data/phase_quantization_detail.csv                 | 069c6e7fc14d197e20a4361ac0c4ba649acc57397ad4ab2d29b8bce6e7088561 |        58291 |
| figures/figure_tolerance_collapse.png                     | e3919386b92447b91b34fdb6f8b640dc03682761b54a11eb57e464fd52d50690 |       107748 |
| figures/figure_phase_quantization_failure.png             | c57451e04fd63e5837dd0c5691a1f816e82e9c41cb31c7062069bd6f6a524fc6 |        77099 |
| figures/figure_psf_domain_gap.png                         | 173e26862b24cb6dd987b48f87ebe093353f343d161864d573aeb23707c246ef |        77037 |
| manuscript/main.pdf                                       | a57a5bf7f5bc580e07f6b6529a26a31c3d79d5000bc683b7dbdb4e2e2761cd03 |      1839377 |
| supplement/supplement.pdf                                 | 014437a1d298ebc8e8ebc22646c1dec9595bfd1a43187bcc110b09e89924fe57 |       152946 |
| manuscript/p0_results_integration.tex                     | 4bea39d92d95bf21b5928dccc2010328a000e7aa4d82cc79e0e0fb36ee00d563 |         2197 |
| supplement/p0_supplement_addendum.tex                     | 1613f4a2055383667b60d13d86e9d4abe5f639352117e1cd2e01c29ce853c3cf |         1088 |
| logs/p0_results_integration_run.log                       | 7c8a6837f3388dbdef1d61a57063d55baef1dabd7ba927937eed903fd157369d |          309 |
| scripts/generate_p0_results_and_manuscript_integration.py | 92228830438c2b8375976cea0c384d1e45a5d55eefd76c9429fbd5f890f62629 |        15725 |

## Local long-term mirror
The refreshed local mirror is stored at:

`/workspace/github-sync/open-ai/self-calibrating-diffractive-imaging-ncomms-2026-04-30T07-33-15Z`

The refreshed compressed mirror is:

`/workspace/github-sync/self-calibrating-diffractive-imaging-ncomms-2026-04-30T07-33-15Z-full.tar.gz`
