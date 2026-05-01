# Iteration 029 Device Tolerance Priors

- Timestamp: `2026-05-02T00:00:00Z`
- Action type: `literature_bound_device_prior_packaging`
- Stage: `active calculation/verification`
- Single bottleneck addressed: `the linked tolerance results existed, but the simulation-side variables were not yet packaged into a reusable literature-bound device mapping for manuscript-safe platform interpretation`

## Executed action

1. Executed `scripts/device_tolerance_priors.py`.
2. Generated:
   - `results/tolerance_device_priors/device_tolerance_prior_profiles.json`
   - `results/tolerance_device_priors/device_tolerance_prior_summary.csv`
   - `results/tolerance_device_priors/device_tolerance_prior_summary.md`
3. Bound the current tolerance variables to two explicit device classes:
   - single-plane reflective LCoS SLM
   - bilayer visible dielectric metasurface

## Verification result

- The result package now explicitly distinguishes which tolerance variables are device-native and which are only system-level surrogates.
- For the SLM profile:
  - `phase_noise_sigma_rad` is directly literature-bound
  - `shift_sigma_px` and `rotation_sigma_deg` are not fabrication-native for a single-plane panel
  - `wavelength_drift_fraction` remains calibration/source dependent rather than panel-fabrication native
- For the bilayer metasurface profile:
  - `phase_noise_sigma_rad`, `shift_sigma_px`, and `wavelength_drift_fraction` all admit direct literature anchors
  - `rotation_sigma_deg` is only partially bound and still needs device-specific overlay metrology for an exact degree-scale prior

## Interpretation boundary

The present linked phase-noise plus misalignment plus wavelength-drift simulation is a cleaner physical match to a stacked metasurface platform than to a single-plane SLM panel. The SLM interpretation remains usable for the phase-noise axis, but the current misalignment variables should not be overclaimed as panel-fabrication-native.

## Next shortest-path action

Use the new prior package to tighten manuscript wording around platform scope and to prevent overinterpreting the current hardware-tolerance simulation as a native SLM fabrication study.
