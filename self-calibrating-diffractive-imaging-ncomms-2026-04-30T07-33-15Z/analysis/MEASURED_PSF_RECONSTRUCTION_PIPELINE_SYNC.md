# Measured PSF reconstruction pipeline sync

Generated UTC: `2026-05-03T01:04Z`

## Status

The measured PSF reconstruction pipeline was executed in the project runtime and synchronized into the local long-term project mirror. This record is committed to the GitHub long-term project space on branch `open-ai` as the remote audit index.

## Boundary statement

The input `source_data/measured_psf_or_speckle_dataset.npz` is treated as a pseudo-experimental measured-PSF/speckle proxy. This run does not claim a new hardware experiment or a newly downloaded public PSF dataset.

## Command

```bash
python scripts/run_measured_psf_reconstruction.py \
  --root /workspace/self-calibrating-diffractive-ncomms \
  --input source_data/measured_psf_or_speckle_dataset.npz \
  --output-dir results/measured_pipeline
```

## Outputs

- `scripts/run_measured_psf_reconstruction.py`
- `source_data/measured_psf_reconstruction_full.csv`
- `source_data/measured_psf_reconstruction_summary.csv`
- `source_data/measured_psf_reconstruction_full.npz`
- `source_data/measured_psf_reconstruction_figure_mapping.csv`
- `results/measured_pipeline/figure5_reconstruction_alignment_check.csv`
- `results/measured_pipeline/measured_reconstruction_run_log.md`
- `results/measured_pipeline/measured_reconstruction_checksums.csv`
- `results/measured_pipeline/measured_reconstruction_report.json`
- `results/measured_pipeline/measured_pipeline_summary.md`
- `results/measured_pipeline/measured_pipeline_bundle_checksums.csv`

## Key values

| metric | value |
|---|---:|
| sample_count | 48 |
| matched mean PSNR (dB) | 12.211602052052816 |
| mismatched mean PSNR (dB) | 12.00167719523112 |
| matched-minus-mismatch PSNR gain (dB) | 0.20992485682169715 |
| matched mean correlation | 0.3496704575082541 |
| mismatched mean correlation | 0.2880145289645076 |
| matched-minus-mismatch correlation gain | 0.06165592854374652 |
| measured-eval alignment PASS rows | 5 |
| Figure 5 context rows | 2 |

## Checksums

| path | size_bytes | sha256 |
|---|---:|---|
| `source_data/measured_psf_or_speckle_dataset.npz` | 11437001 | `b019caf44a3ba60d19c51e3ae6574bd7fe4d6852259ec3c4f583c879de31a53b` |
| `scripts/run_measured_psf_reconstruction.py` | 17367 | `ce8f684d3fb290b2a55f90c86a288f797d5104d7e4b4c959afaf6c66fd4e388c` |
| `source_data/measured_psf_reconstruction_full.csv` | 27390 | `6c3c3d16f37542f14f32478f0a35342401ced8516993cbefd449040f7ec0154b` |
| `source_data/measured_psf_reconstruction_summary.csv` | 1004 | `306bedf235f3eaf2f9ca7203d3675b2e2a96cd63184610effd7af25c1c5bce66` |
| `source_data/measured_psf_reconstruction_full.npz` | 11439372 | `fac6e5f2396dbfe9e1724e20c79899718979a70d42d4e73ec3b19d27d5d7c1a5` |
| `source_data/measured_psf_reconstruction_figure_mapping.csv` | 928 | `36a58b66b4470c7ac207d1eafd3847e3bd34594cb5a88a560eef6006a8cd7a56` |
| `results/measured_pipeline/figure5_reconstruction_alignment_check.csv` | 1543 | `de30c91f2f4380bc3cabb1fe42c7887f76bc9a42899f336ba33fe3ba1d76cc89` |
| `results/measured_pipeline/measured_reconstruction_run_log.md` | 1031 | `708842432034b74b03d4fada41a34261ca8392984af3da98d33cfdce140487e9` |
| `results/measured_pipeline/measured_reconstruction_checksums.csv` | 908 | `f741795fd695e63a0ce8fec0f64b81a8d891fb6e2bd04aa60fcd2fabf146c3ff` |
| `results/measured_pipeline/measured_reconstruction_report.json` | 2876 | `a70c1cfd728f5ae1d76477fa76bf7833773089fbd390976a2a3c06d54733d709` |
| `results/measured_pipeline/measured_pipeline_summary.md` | 1915 | `d7320a6126eb3fd03933fcff80f26e1f0a36d41bb8d86ae800a3494011a4282d` |
| `results/measured_pipeline/measured_pipeline_bundle_checksums.csv` | 1254 | `1b8371889dc85234509a851066b03696ac290a934c5aa7d86743ddc07c66e839` |
| refreshed local full tarball | 12505922 | `ae93bc92a9c0fbdbadd33358a180a5b2df7feb17fe5154a19417a4d9c75faedc` |

## Figure 5 alignment interpretation

- The released `measured_psf_reconstruction_eval.csv` table is reproduced within `2e-6` tolerance for mean PSNR, mean correlation, and mean PSNR drop.
- `figure5_reconstruction_summary.csv` is recorded as `REFERENCE_CONTEXT`: it uses the same PSNR/correlation definitions but a different family/tolerance experiment, so direct numerical equality is not expected.

## Local long-term mirror

The local long-term mirror was refreshed at:

`/workspace/github-sync/open-ai/self-calibrating-diffractive-ncomms-2026-04-27T00-00-00Z/project_workspace`

The refreshed compressed mirror is:

`/workspace/github-sync/self-calibrating-diffractive-imaging-ncomms-2026-04-30T07-33-15Z-full.tar.gz`

## Remote binary-upload boundary

The GitHub connector used in this environment can commit UTF-8 audit files such as this manifest. Native binary assets such as `.npz` and compiled PDFs remain in the local long-term mirror and are tracked here by checksum for a later native `git push` from a network-enabled Git environment.
