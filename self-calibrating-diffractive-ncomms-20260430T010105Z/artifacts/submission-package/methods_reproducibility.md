# Methods Reproducibility

## Round6 baseline
The restored round6 processor-level baseline was rerun from `code/project-scripts/round6_numpy_passive_d2nn.py` inside this long-term project space. The script writes all primary outputs to `artifacts/project-outputs/`.

## Verified outputs from this project space
- ordinary OOD mean PSNR: 11.884343 dB
- common-path OOD mean PSNR: 10.753760 dB
- non-common-path OOD mean PSNR: 10.690498 dB
- wrong-reference OOD mean PSNR: 10.830944 dB
- common minus ordinary: -1.130583 dB
- common minus non-common-path: 0.063262 dB
- common minus wrong-reference: -0.077184 dB

## Reproducibility boundary
This restored round6 baseline is a minimal NumPy-based passive D2NN rebuild. It closes the raw-output chain for Fig. 5 source-data generation, but the summary note in the script explicitly marks it as a reproducible baseline rather than a submission-grade final result.
