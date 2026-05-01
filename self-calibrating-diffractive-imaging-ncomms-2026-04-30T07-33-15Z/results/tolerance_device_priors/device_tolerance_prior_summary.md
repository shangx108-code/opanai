# Literature-Bound Device Tolerance Priors

This package binds the current simulation variables to actual device classes where the literature supports a defensible mapping.

## Core rule

- `phase_noise_sigma_rad` can be device-native for both LCoS-SLM and metasurface platforms.
- `shift_sigma_px` and `rotation_sigma_deg` are device-native for stacked metasurfaces but not for a single-plane SLM panel.
- `wavelength_drift_fraction` is device-native for metasurface resonance shift, but SLM wavelength behavior is primarily a calibration and source issue rather than a fabricated-panel tolerance by itself.

## slm_lcos_visible_reflective

- Device class: `single-plane reflective LCoS SLM`
- Binding status:
  - `phase_noise_sigma_rad`: `bound`
  - `shift_sigma_px`: `not_fabrication_native_for_single_plane_device`
  - `rotation_sigma_deg`: `not_fabrication_native_for_single_plane_device`
  - `wavelength_drift_fraction`: `external_source_or_recalibration_dependent`
- Prior anchors:
  - `phase_noise_sigma_rad`: {"family": "lognormal", "median_sigma_rad": 0.19477874452256716, "p95_sigma_rad": 0.6108652381980153, "mu_log": -1.6358910080876454, "sigma_log": 0.6949020179106618, "derivation": "Median from 3.1% average phase stability times 2pi; 95th anchor from 35 degree maximum flicker."}
  - `wavelength_drift_fraction`: {"family": "qualitative_close_wavelength_recalibration_regime", "status": "not numerically fixed from panel fabrication alone", "note": "Panel calibration must be wavelength-specific; close calibrated wavelengths can remain similar, but the relevant quantitative prior belongs to the source and calibration stack rather than the fabricated panel itself."}
- Sources:
  - `slm_flicker_2021`: Fast measurement of the phase flicker of a digitally addressable LCoS-SLM | https://www.sciencedirect.com/science/article/abs/pii/S0030402621009219
    - Average phase stability about 3.1%; maximal phase flicker about 30 degrees for a HOLOEYE Pluto device at 633 nm.
  - `slm_photonics_2017`: LCoS SLM Study and Its Application in Wavelength Selective Switch | https://www.mdpi.com/2304-6732/4/2/22
    - GAEA device with 3.74 um pitch shows maximum flicker about 35 degrees; cooling to -8 C can reduce flicker by up to 80%.
  - `slm_nonuniformity_2021`: Phase Compensation of the Non-Uniformity of the Liquid Crystal on Silicon Spatial Light Modulator at Pixel Level | https://www.mdpi.com/1424-8220/21/3/967
    - HOLOEYE device with 8 um pitch and 87% fill factor; phase response must be recalibrated across wavelength and temperature.
  - `slm_close_wavelength_2019`: Liquid Crystal Spatial Light Modulator with Optimized Phase Modulation Ranges to Display Multiorder Diffractive Elements | https://www.mdpi.com/2076-3417/9/13/2592/html
    - Phase response does not vary remarkably for a different but close illuminating wavelength after calibration.

## bilayer_tio2_metasurface_visible

- Device class: `stacked dielectric metasurface`
- Binding status:
  - `phase_noise_sigma_rad`: `bound`
  - `shift_sigma_px`: `bound`
  - `rotation_sigma_deg`: `partially_bound_via_stacked_layer_alignment_class`
  - `wavelength_drift_fraction`: `bound`
- Prior anchors:
  - `phase_noise_sigma_rad`: {"family": "gaussian_pushforward", "sigma_rad": 0.7853981633974483, "physical_origin": "10 nm diameter variation mapped to about pi/4 dephasing."}
  - `shift_sigma_px`: {"family": "gaussian_pushforward", "sigma_nm": 50.0, "sigma_pitch_fraction": 0.11904761904761904, "stress_anchors_pitch_fraction": {"100nm": 0.23809523809523808, "250nm": 0.5952380952380952}, "physical_origin": "50 nm bilayer misalignment tolerance; 100 nm and 250 nm explicitly studied as stronger displacement cases."}
  - `rotation_sigma_deg`: {"family": "surrogate_from_lateral_registration_class", "status": "requires device-specific overlay metrology for exact degree-scale calibration", "note": "Current simulation rotation term should be interpreted as a companion variable to bilayer overlay error rather than as an independently measured literature distribution."}
  - `wavelength_drift_fraction`: {"family": "gaussian_pushforward", "sigma_fraction": 0.03333333333333333, "sigma_nm_at_750nm": 25.0, "physical_origin": "10 nm geometry error induces about 25 nm shift of the wavelength of maximum diffraction efficiency at 750 nm."}
- Sources:
  - `meta_fabrication_2021`: Challenges in nanofabrication for efficient optical metasurfaces | https://www.nature.com/articles/s41598-021-84666-z
    - 10 nm diameter error yields dephasing close to pi/4 and about 25 nm peak-wavelength shift at 750 nm; high-performance devices require better than 10 nm precision.
  - `meta_bilayer_visible_2025`: Free-standing bilayer metasurfaces in the visible | https://www.nature.com/articles/s41467-025-58205-7
    - Bilayer structures show robust performance under misalignment tolerance within 50 nm; unit-cell size is 420 nm.
  - `meta_bilayer_nonlinear_2025`: Bilayer optical metasurfaces with multiple broken symmetries for nonlinear wavelength generation | https://www.nature.com/articles/s44455-025-00016-3
    - Controlled horizontal-displacement studies explicitly evaluate 100 nm and 250 nm layer offsets in a bilayer metasurface.

## Interpretation boundary

- The metasurface profile is the cleaner match to the current linked phase-noise plus misalignment plus wavelength-drift simulation.
- The SLM profile is still useful, but only the phase-noise term maps directly to fabricated-panel behavior. The current misalignment variable should not be overinterpreted as an SLM fabrication prior.
