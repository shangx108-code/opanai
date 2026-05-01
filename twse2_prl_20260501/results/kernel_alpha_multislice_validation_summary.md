# Kernel-alpha multislice validation summary

## Selected fixed-(Z, phi, eta) slices
- S1: eta=1.00, phi=1.571, Z=2.0, score=0.2994, alpha-split coupling=0.1888
- S2: eta=1.00, phi=1.178, Z=2.0, score=0.2991, alpha-split coupling=0.1888
- S3: eta=1.00, phi=1.963, Z=2.0, score=0.2991, alpha-split coupling=0.1888
- S4: eta=1.00, phi=0.785, Z=2.0, score=0.2969, alpha-split coupling=0.1888

## Branch invariance check
- S1 chiral: alpha-split coupling=0.1888, mean collapse RMS=0.1880, max collapse RMS=0.4245
- S2 chiral: alpha-split coupling=0.1888, mean collapse RMS=0.1502, max collapse RMS=0.2493
- S3 chiral: alpha-split coupling=0.1888, mean collapse RMS=0.1503, max collapse RMS=0.2495
- S4 chiral: alpha-split coupling=0.1888, mean collapse RMS=0.1613, max collapse RMS=0.1876
- S1 control: alpha-split coupling=0.0000, mean collapse RMS=5.9493e-17, max collapse RMS=5.9493e-17
- S2 control: alpha-split coupling=0.0000, mean collapse RMS=5.9493e-17, max collapse RMS=5.9493e-17
- S3 control: alpha-split coupling=0.0000, mean collapse RMS=5.9493e-17, max collapse RMS=5.9493e-17
- S4 control: alpha-split coupling=0.0000, mean collapse RMS=5.9493e-17, max collapse RMS=5.9493e-17

## Verdict
- Control collapse invariant across tested slices: yes
- Phase-sensitive non-collapse invariant across tested slices: yes
- Operational criterion: control should retain near-zero alpha-split coupling and near-zero collapse RMS, while chiral should retain nonzero alpha-split coupling together with a nonzero collapse RMS after common recentering and normalization.

## Files
- `kernel_alpha_multislice_curves.csv`
- `kernel_alpha_multislice_metrics.csv`
- `kernel_alpha_multislice_summary.csv`
- `kernel_alpha_multislice_validation_figure.svg`
