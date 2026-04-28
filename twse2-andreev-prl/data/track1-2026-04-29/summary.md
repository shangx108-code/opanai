# Tuo TB Reconstruction Summary

- Overall RMSE against source Fig. 1c arrays: 10.255 meV
- Row-wise summed RMSE against source Fig. 1c arrays: 17.762 meV
- Per-band RMSE: [6.007, 13.737, 9.523] meV
- Exact endpoint match at Gamma is recovered.
- The summary uses the element-wise global RMSE definition `sqrt(mean((E_rec - E_src)^2))`; this differs from the larger row-wise sum metric by a factor of `sqrt(3)` and resolves the earlier apparent inconsistency with `band_comparison.csv`.
- Remaining mismatch is concentrated near the K-point sectors, indicating that the symmetry-completed star ordering or phase convention is still not uniquely fixed by the uploaded files alone.
- This output should therefore be treated as a reproducible partial reconstruction, not yet a fully closed exact reproduction of the published Tuo tight-binding bands.

Generated files:
- reconstructed_hopping_table.csv
- band_comparison.csv
- high_symmetry_residuals.csv
- band_reconstruction_check.png