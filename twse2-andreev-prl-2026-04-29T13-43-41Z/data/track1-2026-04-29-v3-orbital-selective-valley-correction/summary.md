# V3 Orbital-Selective Valley Correction Summary

## Baseline
- Source origin: workbook:/workspace/tmp/ws2/41467_2025_64519_MOESM3_ESM.xlsx
- Path mode: exclusive_150
- K_B label: K_2b1+b2
- M label: M_b2
- K_T label: K_-2b1-b2
- Mixed-star config: {'ac1_pattern': 'cyc', 'bc1_pattern': 'cyc', 'ac2_pattern': 'anti', 'bc2_pattern': 'anti', 'ac7_first_pattern': 'cyc', 'bc7_first_pattern': 'cyc', 'ac7_second_pattern': 'anti', 'bc7_second_pattern': 'anti', 'ac7_second_conjugated': False, 'bc7_second_conjugated': False}
- Baseline overall RMSE: 8.366681 meV

## V3 closure result
- Definition: solve a diagonal orbital correction layer `diag(d_A(k), d_B(k), d_C(k))` point-by-point on the coupled baseline.
- Decomposition:
  - `v3_ab_common = (d_A + d_B) / 2`
  - `v3_ab_orbital_selective = (d_A - d_B) / 2`
  - `v3_c = d_C`
- Corrected overall RMSE: 1.503154374257 meV
- Gamma-end max abs delta after V3: 1.720306874197e-02 meV
- Max solver residual norm: 9.149288849689e+00 meV

## Valley localization check
- Max |v3_ab_orbital_selective| over points 140-160 and 440-460: 23.052668 meV
- Max |v3_ab_common| over points 140-160 and 440-460: 9.008285 meV
- Max |v3_c| over points 140-160 and 440-460: 17.897181 meV
- Global max |v3_ab_orbital_selective|: 26.206664 meV
- Global max |v3_ab_common|: 12.790562 meV
- Global max |v3_c|: 24.019572 meV

Generated files:
- band_comparison_v3.csv
- v3_correction_profile.csv
- high_symmetry_residuals_v3.csv
- band_reconstruction_check_v3.png