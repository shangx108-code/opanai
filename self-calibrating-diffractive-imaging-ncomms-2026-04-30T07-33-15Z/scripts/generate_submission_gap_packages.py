#!/usr/bin/env python3
"""Generate minimal auditable packages for remaining submission-gap evidence."""

from __future__ import annotations

import csv
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
NATURAL_DIR = PROJECT_ROOT / "results" / "natural_objects"
TOLERANCE_DIR = PROJECT_ROOT / "results" / "tolerance"


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_natural_object_package() -> dict[str, object]:
    rows = [
        {
            "dataset_name": "ImageNet-1k",
            "dataset_version": "ILSVRC2012 validation",
            "subset_role": "natural-object primary ledger",
            "planned_subset_size": 64,
            "selection_rule": "Freeze the first 64 images after sorting eligible validation IDs by filename and removing extreme aspect-ratio outliers.",
            "eligibility_rule": "RGB natural-object images only; exclude unreadable files and images with min side < 160 px.",
            "preprocessing": "center-crop to square, resize to 128x128, convert to grayscale, normalize to [0,1], then downsample to the active 12x12 frontend for all methods.",
            "shared_across_methods": "yes",
            "raw_data_redistributed": "no",
            "license_note": "Raw images remain under the original ImageNet terms and are referenced by index only.",
            "local_status": "not_present_in_active_root",
        },
        {
            "dataset_name": "COCO",
            "dataset_version": "2017 validation",
            "subset_role": "natural-object diversity stress test",
            "planned_subset_size": 64,
            "selection_rule": "Freeze the first 64 eligible images after sorting by COCO image id and removing crowd-heavy or extreme aspect-ratio cases.",
            "eligibility_rule": "Natural-scene RGB images only; exclude images with min side < 160 px and annotation crowd fraction > 0.5.",
            "preprocessing": "center-crop to square, resize to 128x128, convert to grayscale, normalize to [0,1], then downsample to the active 12x12 frontend for all methods.",
            "shared_across_methods": "yes",
            "raw_data_redistributed": "no",
            "license_note": "Raw images remain under the original COCO terms and are referenced by index only.",
            "local_status": "not_present_in_active_root",
        },
    ]
    fieldnames = list(rows[0].keys())
    write_csv(NATURAL_DIR / "natural_object_subset_index.csv", rows, fieldnames)

    package = {
        "package_name": "natural_object_package",
        "status": "protocol_frozen_but_not_executed",
        "active_root_has_raw_images": False,
        "deliverables": [
            "results/natural_objects/natural_object_subset_index.csv",
            "results/natural_objects/natural_object_package.md",
            "results/natural_objects/natural_object_package.json",
        ],
        "frozen_protocol": {
            "shared_preprocessing": "All methods will see the same resized grayscale inputs and the same held-out image list.",
            "primary_datasets": [
                "ImageNet-1k ILSVRC2012 validation",
                "COCO 2017 validation",
            ],
            "frontend_resolution": "12x12 low-resolution target grid",
        },
        "true_blocker": "The active project root does not contain the licensed raw natural-image files, so no reproducible natural-object metrics can be generated in this round.",
    }
    (NATURAL_DIR / "natural_object_package.json").write_text(
        json.dumps(package, indent=2) + "\n",
        encoding="utf-8",
    )
    (NATURAL_DIR / "natural_object_package.md").write_text(
        "\n".join(
            [
                "# Natural-Object Package",
                "",
                "## Status",
                "",
                "- Package type: `protocol and audit scaffold`",
                "- Execution status: `not yet run`",
                "- Reason: the active root does not contain licensed raw natural-image files.",
                "",
                "## Frozen protocol",
                "",
                "- Datasets selected for the first auditable natural-object pass:",
                "  - `ImageNet-1k / ILSVRC2012 validation`",
                "  - `COCO 2017 validation`",
                "- Proposed subset size: `64 + 64` images.",
                "- Shared preprocessing for all methods: center-crop to square, resize to `128 x 128`, convert to grayscale, normalize to `[0, 1]`, then downsample to the active `12 x 12` frontend.",
                "- Shared fairness rule: every method must use the exact same frozen subset and preprocessing chain.",
                "",
                "## Included file",
                "",
                "- `natural_object_subset_index.csv` freezes dataset version, selection rule, preprocessing, and license handling.",
                "",
                "## Interpretation boundary",
                "",
                "This package closes the audit gap around source specification, subset-selection rules, preprocessing, and license handling. It does not claim that natural-object evaluation has already been executed.",
                "",
                "## True blocker",
                "",
                "- Missing licensed raw datasets in the active root.",
                "- Therefore no natural-object metric table or source-data bundle can be truthfully produced in this round.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return package


def build_tolerance_package() -> dict[str, object]:
    rows = [
        {
            "perturbation_family": "reference_channel_misregistration",
            "physical_unit": "low-resolution pixels",
            "applied_location": "reference input channel before reconstruction",
            "method_scope": "all four methods",
            "fairness_class": "cross-method common perturbation",
            "levels": "0.0, 0.5, 1.0 px",
            "status": "protocol_frozen_not_yet_run",
            "comment": "Preserves identical distorted-image inputs while testing reference-channel alignment sensitivity for every method.",
        },
        {
            "perturbation_family": "reference_channel_intensity_noise",
            "physical_unit": "relative sigma",
            "applied_location": "reference input channel before reconstruction",
            "method_scope": "all four methods",
            "fairness_class": "cross-method common perturbation",
            "levels": "0.00, 0.01, 0.02",
            "status": "protocol_frozen_not_yet_run",
            "comment": "Common calibration-noise analogue that does not privilege the phase-only stack.",
        },
        {
            "perturbation_family": "propagation_distance_error",
            "physical_unit": "fractional error in z",
            "applied_location": "forward-model or PSF generation stage",
            "method_scope": "phase_only_stack, reference_psf_deconvolution, spectral_frontend",
            "fairness_class": "physics-grounded shared perturbation",
            "levels": "-5%, 0%, +5%",
            "status": "protocol_frozen_not_yet_run",
            "comment": "Applies only to methods whose forward model explicitly depends on propagation geometry.",
        },
        {
            "perturbation_family": "phase_mask_quantization",
            "physical_unit": "bits",
            "applied_location": "phase-only diffractive masks",
            "method_scope": "phase_only_stack only",
            "fairness_class": "method-specific engineering perturbation",
            "levels": "3, 4, 6, inf bits",
            "status": "protocol_frozen_not_yet_run",
            "comment": "Report separately from headline method ranking because no equivalent optical mask exists for the digital-only baselines.",
        },
        {
            "perturbation_family": "phase_mask_lateral_shift",
            "physical_unit": "native-grid pixels",
            "applied_location": "phase-only diffractive masks",
            "method_scope": "phase_only_stack only",
            "fairness_class": "method-specific engineering perturbation",
            "levels": "0, 1, 2 px",
            "status": "protocol_frozen_not_yet_run",
            "comment": "Engineering robustness test for fabricated-mask alignment, not a cross-method fairness metric.",
        },
    ]
    fieldnames = list(rows[0].keys())
    write_csv(TOLERANCE_DIR / "method_fair_tolerance_matrix.csv", rows, fieldnames)

    package = {
        "package_name": "method_fair_hardware_tolerance_package",
        "status": "protocol_frozen_but_not_executed",
        "deliverables": [
            "results/tolerance/method_fair_tolerance_matrix.csv",
            "results/tolerance/hardware_tolerance_package.md",
            "results/tolerance/hardware_tolerance_package.json",
        ],
        "fairness_rule": "Only cross-method common perturbations should be used for headline ranking. Phase-mask-specific perturbations must be reported as engineering robustness diagnostics.",
        "true_blocker": "No executed tolerance result tables exist yet in the active root, so this round can freeze the protocol but not claim quantitative tolerance outcomes.",
    }
    (TOLERANCE_DIR / "hardware_tolerance_package.json").write_text(
        json.dumps(package, indent=2) + "\n",
        encoding="utf-8",
    )
    (TOLERANCE_DIR / "hardware_tolerance_package.md").write_text(
        "\n".join(
            [
                "# Method-Fair Hardware-Tolerance Package",
                "",
                "## Status",
                "",
                "- Package type: `fairness protocol scaffold`",
                "- Execution status: `not yet run`",
                "",
                "## Fairness rule",
                "",
                "- Use common perturbations for headline cross-method comparison.",
                "- Report phase-mask-specific perturbations separately as engineering diagnostics for the phase-only stack.",
                "",
                "## Frozen perturbation matrix",
                "",
                "- `method_fair_tolerance_matrix.csv` records perturbation family, units, applied location, method scope, and fairness class.",
                "",
                "## Interpretation boundary",
                "",
                "This package does not claim that tolerance curves or source-data tables already exist. It only freezes a reviewer-safe protocol so later runs cannot quietly mix common-input perturbations with phase-mask-only perturbations.",
                "",
                "## True blocker",
                "",
                "- No executed tolerance result files are present in the active root.",
                "- Therefore the remaining quantitative task is to run the frozen perturbation matrix and export seed-level result tables.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return package


def main() -> None:
    natural = build_natural_object_package()
    tolerance = build_tolerance_package()
    summary = {
        "natural_object_package": natural["status"],
        "hardware_tolerance_package": tolerance["status"],
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
