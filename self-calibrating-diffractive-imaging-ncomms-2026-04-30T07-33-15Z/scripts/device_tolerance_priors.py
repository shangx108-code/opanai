#!/usr/bin/env python3
"""Literature-bound tolerance prior package for actual device mappings.

This module binds the simulation-side tolerance variables to device-facing
literature anchors for:
1. LCoS / SLM platforms
2. Bilayer dielectric metasurfaces

The goal is not to claim that every parameter is fabrication-native for every
platform. Instead, the package states explicitly which current simulation
variables map naturally to a given device class, which require a system-level
reinterpretation, and which remain external-source dependent.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import pandas as pd


@dataclass(frozen=True)
class LiteratureSource:
    short_name: str
    title: str
    url: str
    note: str


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def output_root() -> Path:
    return project_root() / "results" / "tolerance_device_priors"


def slm_sources() -> list[LiteratureSource]:
    return [
        LiteratureSource(
            short_name="slm_flicker_2021",
            title="Fast measurement of the phase flicker of a digitally addressable LCoS-SLM",
            url="https://www.sciencedirect.com/science/article/abs/pii/S0030402621009219",
            note="Average phase stability about 3.1%; maximal phase flicker about 30 degrees for a HOLOEYE Pluto device at 633 nm.",
        ),
        LiteratureSource(
            short_name="slm_photonics_2017",
            title="LCoS SLM Study and Its Application in Wavelength Selective Switch",
            url="https://www.mdpi.com/2304-6732/4/2/22",
            note="GAEA device with 3.74 um pitch shows maximum flicker about 35 degrees; cooling to -8 C can reduce flicker by up to 80%.",
        ),
        LiteratureSource(
            short_name="slm_nonuniformity_2021",
            title="Phase Compensation of the Non-Uniformity of the Liquid Crystal on Silicon Spatial Light Modulator at Pixel Level",
            url="https://www.mdpi.com/1424-8220/21/3/967",
            note="HOLOEYE device with 8 um pitch and 87% fill factor; phase response must be recalibrated across wavelength and temperature.",
        ),
        LiteratureSource(
            short_name="slm_close_wavelength_2019",
            title="Liquid Crystal Spatial Light Modulator with Optimized Phase Modulation Ranges to Display Multiorder Diffractive Elements",
            url="https://www.mdpi.com/2076-3417/9/13/2592/html",
            note="Phase response does not vary remarkably for a different but close illuminating wavelength after calibration.",
        ),
    ]


def metasurface_sources() -> list[LiteratureSource]:
    return [
        LiteratureSource(
            short_name="meta_fabrication_2021",
            title="Challenges in nanofabrication for efficient optical metasurfaces",
            url="https://www.nature.com/articles/s41598-021-84666-z",
            note="10 nm diameter error yields dephasing close to pi/4 and about 25 nm peak-wavelength shift at 750 nm; high-performance devices require better than 10 nm precision.",
        ),
        LiteratureSource(
            short_name="meta_bilayer_visible_2025",
            title="Free-standing bilayer metasurfaces in the visible",
            url="https://www.nature.com/articles/s41467-025-58205-7",
            note="Bilayer structures show robust performance under misalignment tolerance within 50 nm; unit-cell size is 420 nm.",
        ),
        LiteratureSource(
            short_name="meta_bilayer_nonlinear_2025",
            title="Bilayer optical metasurfaces with multiple broken symmetries for nonlinear wavelength generation",
            url="https://www.nature.com/articles/s44455-025-00016-3",
            note="Controlled horizontal-displacement studies explicitly evaluate 100 nm and 250 nm layer offsets in a bilayer metasurface.",
        ),
    ]


def build_profiles() -> dict[str, object]:
    # SLM phase-noise prior from literature anchors:
    # typical flicker scale = 3.1% of 2pi; high tail = 35 deg
    slm_typical_phase_sigma_rad = 0.031 * 2.0 * math.pi
    slm_tail_phase_sigma_rad = math.radians(35.0)
    slm_mu_log = math.log(slm_typical_phase_sigma_rad)
    slm_sigma_log = (math.log(slm_tail_phase_sigma_rad) - slm_mu_log) / 1.6448536269514722

    # Metasurface fabrication pushforward from size error to phase / wavelength:
    # 10 nm diameter error -> ~pi/4 dephasing, ~25 nm wavelength shift at 750 nm
    metasurface_pitch_nm = 420.0
    metasurface_phase_sigma_rad = math.pi / 4.0
    metasurface_wavelength_sigma_fraction = 25.0 / 750.0
    metasurface_mild_shift_sigma_px = 50.0 / metasurface_pitch_nm
    metasurface_stress_shift_px = {
        "100nm": 100.0 / metasurface_pitch_nm,
        "250nm": 250.0 / metasurface_pitch_nm,
    }

    return {
        "profiles": [
            {
                "profile_name": "slm_lcos_visible_reflective",
                "device_class": "single-plane reflective LCoS SLM",
                "simulation_binding_status": {
                    "phase_noise_sigma_rad": "bound",
                    "shift_sigma_px": "not_fabrication_native_for_single_plane_device",
                    "rotation_sigma_deg": "not_fabrication_native_for_single_plane_device",
                    "wavelength_drift_fraction": "external_source_or_recalibration_dependent",
                },
                "device_geometry": {
                    "example_panel_pitch_um": 8.0,
                    "alternate_wss_pitch_um": 3.74,
                    "fill_factor_percent": 87.0,
                },
                "phase_noise_prior": {
                    "family": "lognormal",
                    "median_sigma_rad": slm_typical_phase_sigma_rad,
                    "p95_sigma_rad": slm_tail_phase_sigma_rad,
                    "mu_log": slm_mu_log,
                    "sigma_log": slm_sigma_log,
                    "derivation": "Median from 3.1% average phase stability times 2pi; 95th anchor from 35 degree maximum flicker.",
                },
                "wavelength_prior": {
                    "family": "qualitative_close_wavelength_recalibration_regime",
                    "status": "not numerically fixed from panel fabrication alone",
                    "note": "Panel calibration must be wavelength-specific; close calibrated wavelengths can remain similar, but the relevant quantitative prior belongs to the source and calibration stack rather than the fabricated panel itself.",
                },
                "source_refs": [asdict(src) for src in slm_sources()],
            },
            {
                "profile_name": "bilayer_tio2_metasurface_visible",
                "device_class": "stacked dielectric metasurface",
                "simulation_binding_status": {
                    "phase_noise_sigma_rad": "bound",
                    "shift_sigma_px": "bound",
                    "rotation_sigma_deg": "partially_bound_via_stacked_layer_alignment_class",
                    "wavelength_drift_fraction": "bound",
                },
                "device_geometry": {
                    "unit_cell_pitch_nm": metasurface_pitch_nm,
                    "visible_device_reference_wavelength_nm": 560.0,
                    "alternate_beam_deflector_reference_wavelength_nm": 750.0,
                },
                "phase_noise_prior": {
                    "family": "gaussian_pushforward",
                    "sigma_rad": metasurface_phase_sigma_rad,
                    "physical_origin": "10 nm diameter variation mapped to about pi/4 dephasing.",
                },
                "lateral_misalignment_prior": {
                    "family": "gaussian_pushforward",
                    "sigma_nm": 50.0,
                    "sigma_pitch_fraction": metasurface_mild_shift_sigma_px,
                    "stress_anchors_pitch_fraction": metasurface_stress_shift_px,
                    "physical_origin": "50 nm bilayer misalignment tolerance; 100 nm and 250 nm explicitly studied as stronger displacement cases.",
                },
                "rotation_prior": {
                    "family": "surrogate_from_lateral_registration_class",
                    "status": "requires device-specific overlay metrology for exact degree-scale calibration",
                    "note": "Current simulation rotation term should be interpreted as a companion variable to bilayer overlay error rather than as an independently measured literature distribution.",
                },
                "wavelength_prior": {
                    "family": "gaussian_pushforward",
                    "sigma_fraction": metasurface_wavelength_sigma_fraction,
                    "sigma_nm_at_750nm": 25.0,
                    "physical_origin": "10 nm geometry error induces about 25 nm shift of the wavelength of maximum diffraction efficiency at 750 nm.",
                },
                "source_refs": [asdict(src) for src in metasurface_sources()],
            },
        ]
    }


def build_summary_rows(payload: dict[str, object]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for profile in payload["profiles"]:
        rows.extend(
            [
                {
                    "profile_name": profile["profile_name"],
                    "device_class": profile["device_class"],
                    "simulation_variable": "phase_noise_sigma_rad",
                    "binding_status": profile["simulation_binding_status"]["phase_noise_sigma_rad"],
                    "prior_family": profile["phase_noise_prior"]["family"],
                    "value_summary": json.dumps(profile["phase_noise_prior"], ensure_ascii=True),
                },
                {
                    "profile_name": profile["profile_name"],
                    "device_class": profile["device_class"],
                    "simulation_variable": "shift_sigma_px",
                    "binding_status": profile["simulation_binding_status"]["shift_sigma_px"],
                    "prior_family": profile.get("lateral_misalignment_prior", {}).get("family", "none"),
                    "value_summary": json.dumps(profile.get("lateral_misalignment_prior", {}), ensure_ascii=True),
                },
                {
                    "profile_name": profile["profile_name"],
                    "device_class": profile["device_class"],
                    "simulation_variable": "rotation_sigma_deg",
                    "binding_status": profile["simulation_binding_status"]["rotation_sigma_deg"],
                    "prior_family": profile.get("rotation_prior", {}).get("family", "none"),
                    "value_summary": json.dumps(profile.get("rotation_prior", {}), ensure_ascii=True),
                },
                {
                    "profile_name": profile["profile_name"],
                    "device_class": profile["device_class"],
                    "simulation_variable": "wavelength_drift_fraction",
                    "binding_status": profile["simulation_binding_status"]["wavelength_drift_fraction"],
                    "prior_family": profile["wavelength_prior"]["family"],
                    "value_summary": json.dumps(profile["wavelength_prior"], ensure_ascii=True),
                },
            ]
        )
    return rows


def build_markdown(payload: dict[str, object]) -> str:
    lines = [
        "# Literature-Bound Device Tolerance Priors",
        "",
        "This package binds the current simulation variables to actual device classes where the literature supports a defensible mapping.",
        "",
        "## Core rule",
        "",
        "- `phase_noise_sigma_rad` can be device-native for both LCoS-SLM and metasurface platforms.",
        "- `shift_sigma_px` and `rotation_sigma_deg` are device-native for stacked metasurfaces but not for a single-plane SLM panel.",
        "- `wavelength_drift_fraction` is device-native for metasurface resonance shift, but SLM wavelength behavior is primarily a calibration and source issue rather than a fabricated-panel tolerance by itself.",
        "",
    ]
    for profile in payload["profiles"]:
        lines.append(f"## {profile['profile_name']}")
        lines.append("")
        lines.append(f"- Device class: `{profile['device_class']}`")
        lines.append("- Binding status:")
        for key, value in profile["simulation_binding_status"].items():
            lines.append(f"  - `{key}`: `{value}`")
        lines.append("- Prior anchors:")
        lines.append(f"  - `phase_noise_sigma_rad`: {json.dumps(profile['phase_noise_prior'], ensure_ascii=True)}")
        if "lateral_misalignment_prior" in profile:
            lines.append(f"  - `shift_sigma_px`: {json.dumps(profile['lateral_misalignment_prior'], ensure_ascii=True)}")
        if "rotation_prior" in profile:
            lines.append(f"  - `rotation_sigma_deg`: {json.dumps(profile['rotation_prior'], ensure_ascii=True)}")
        lines.append(f"  - `wavelength_drift_fraction`: {json.dumps(profile['wavelength_prior'], ensure_ascii=True)}")
        lines.append("- Sources:")
        for src in profile["source_refs"]:
            lines.append(f"  - `{src['short_name']}`: {src['title']} | {src['url']}")
            lines.append(f"    - {src['note']}")
        lines.append("")
    lines.append("## Interpretation boundary")
    lines.append("")
    lines.append("- The metasurface profile is the cleaner match to the current linked phase-noise plus misalignment plus wavelength-drift simulation.")
    lines.append("- The SLM profile is still useful, but only the phase-noise term maps directly to fabricated-panel behavior. The current misalignment variable should not be overinterpreted as an SLM fabrication prior.")
    return "\n".join(lines) + "\n"


def main() -> int:
    out_dir = output_root()
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = build_profiles()
    summary = pd.DataFrame(build_summary_rows(payload))
    json_path = out_dir / "device_tolerance_prior_profiles.json"
    csv_path = out_dir / "device_tolerance_prior_summary.csv"
    md_path = out_dir / "device_tolerance_prior_summary.md"
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    summary.to_csv(csv_path, index=False)
    md_path.write_text(build_markdown(payload), encoding="utf-8")
    print(
        json.dumps(
            {
                "status": "completed",
                "json": str(json_path),
                "csv": str(csv_path),
                "md": str(md_path),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
