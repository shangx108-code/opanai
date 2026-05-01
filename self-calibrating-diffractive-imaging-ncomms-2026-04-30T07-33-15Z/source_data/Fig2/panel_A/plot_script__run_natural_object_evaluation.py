#!/usr/bin/env python3
"""Natural-object evaluation entrypoint for the active project root."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

from run_baseline_phase_only_megadiverse_train_dual_heldout_thickstats import (
    PhaseOnlyConfig,
    build_split_samples,
    make_aberration_cases,
)
from run_real_pipeline import (
    PipelineRunConfig,
    compute_psnr,
    fit_pipeline,
    forward_diffractive,
    load_dataset,
    model,
)


@dataclass
class DatasetSpec:
    dataset_name: str
    dataset_version: str
    subset_role: str
    planned_subset_size: int
    selection_rule: str
    eligibility_rule: str
    preprocessing: str
    shared_across_methods: str
    raw_data_redistributed: str
    license_note: str
    local_status: str


SUPPORTED_IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".webp")


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def natural_root() -> Path:
    return project_root() / "results" / "natural_objects"


def staging_root() -> Path:
    return project_root() / "data" / "natural_objects"


def load_subset_index() -> list[DatasetSpec]:
    index_path = natural_root() / "natural_object_subset_index.csv"
    rows: list[DatasetSpec] = []
    with index_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(
                DatasetSpec(
                    dataset_name=row["dataset_name"],
                    dataset_version=row["dataset_version"],
                    subset_role=row["subset_role"],
                    planned_subset_size=int(row["planned_subset_size"]),
                    selection_rule=row["selection_rule"],
                    eligibility_rule=row["eligibility_rule"],
                    preprocessing=row["preprocessing"],
                    shared_across_methods=row["shared_across_methods"],
                    raw_data_redistributed=row["raw_data_redistributed"],
                    license_note=row["license_note"],
                    local_status=row["local_status"],
                )
            )
    return rows


def dataset_dir_name(spec: DatasetSpec) -> str:
    stem = f"{spec.dataset_name}-{spec.dataset_version}"
    sanitized = stem.lower().replace(" ", "-").replace("/", "-")
    sanitized = sanitized.replace(".", "").replace("_", "-")
    return sanitized


def inspect_local_staging(specs: list[DatasetSpec]) -> dict[str, object]:
    rows = []
    missing = []
    for spec in specs:
        expected_dir = staging_root() / dataset_dir_name(spec)
        image_paths = list_image_files(expected_dir)
        image_count = len(image_paths)
        present = image_count > 0
        row = {
            "dataset_name": spec.dataset_name,
            "dataset_version": spec.dataset_version,
            "expected_dir": str(expected_dir),
            "image_count": image_count,
            "detected_extensions": sorted({path.suffix.lower() for path in image_paths}),
            "exists": present,
            "status": "ready" if present else "missing",
        }
        rows.append(row)
        if not present:
            missing.append(row)
    return {"rows": rows, "missing": missing}


def list_image_files(directory: Path) -> list[Path]:
    if not directory.exists():
        return []
    files = [path for path in sorted(directory.iterdir()) if path.is_file() and path.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS]
    return files


def load_grayscale_objects(directory: Path) -> list[tuple[str, np.ndarray]]:
    rows: list[tuple[str, np.ndarray]] = []
    for path in list_image_files(directory):
        image = Image.open(path).convert("L").resize((128, 128), Image.Resampling.BICUBIC)
        rows.append((path.stem, np.asarray(image, dtype=np.float64) / 255.0))
    return rows


def run_metrics(specs: list[DatasetSpec]) -> dict[str, object]:
    phase_config = PhaseOnlyConfig(seed=0, train_case_count=24, heldout_case_count=6)
    dataset = load_dataset(PipelineRunConfig(seed=0, train_case_count=24, eval_case_count=6))
    state = fit_pipeline(dataset["train"], PipelineRunConfig(seed=0, train_case_count=24, eval_case_count=6))
    eval_cases = make_aberration_cases(phase_config.heldout_case_count, phase_config.seed + 500)

    all_rows: list[pd.DataFrame] = []
    summary_rows: list[dict[str, object]] = []
    for spec in specs:
        directory = staging_root() / dataset_dir_name(spec)
        objects_with_names = load_grayscale_objects(directory)
        object_arrays = [arr for _, arr in objects_with_names]
        eval_samples = build_split_samples(object_arrays, "natural_object_eval", eval_cases, phase_config)
        for index, (name, _) in enumerate(objects_with_names):
            for case_id in range(phase_config.heldout_case_count):
                sample_index = case_id * len(objects_with_names) + index
                eval_samples[sample_index]["object_id"] = f"{spec.dataset_name}:{name}"
        optical_output = forward_diffractive(eval_samples, state)
        recon = model(optical_output, state)
        metrics_df, summary = compute_psnr(eval_samples, recon, state)
        metrics_df["dataset_name"] = spec.dataset_name
        metrics_df["dataset_version"] = spec.dataset_version
        all_rows.append(metrics_df)
        summary_rows.append(
            {
                "dataset_name": spec.dataset_name,
                "dataset_version": spec.dataset_version,
                "image_count": len(objects_with_names),
                **summary,
            }
        )

    metrics = pd.concat(all_rows, ignore_index=True)
    out_dir = natural_root()
    metrics_path = out_dir / "natural_object_metrics.csv"
    summary_path = out_dir / "natural_object_summary.json"
    metrics.to_csv(metrics_path, index=False)
    payload = {
        "status": "completed_with_staged_public_open_images",
        "summary_rows": summary_rows,
        "metrics_csv": str(metrics_path),
        "summary_json": str(summary_path),
    }
    summary_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    out_dir = natural_root()
    out_dir.mkdir(parents=True, exist_ok=True)
    specs = load_subset_index()
    inspection = inspect_local_staging(specs)

    inspection_path = out_dir / "natural_object_input_audit.json"
    blocker_path = out_dir / "natural_object_blocker_report.md"

    inspection_path.write_text(
        json.dumps(
            {
                "project_root": str(project_root()),
                "staging_root": str(staging_root()),
                "datasets": inspection["rows"],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    if inspection["missing"]:
        blocker_lines = [
            "# Natural-Object Evaluation Blocker Report",
            "",
            "## Status",
            "",
            "- Execution attempted: `yes`",
            "- Evaluation completed: `no`",
            "- Reason: required raw natural-image datasets are missing from the project-space staging root.",
            "",
            "## Missing inputs",
            "",
        ]
        for row in inspection["missing"]:
            blocker_lines.extend(
                [
                    f"- `{row['dataset_name']} / {row['dataset_version']}`",
                    f"  - expected path: `{row['expected_dir']}`",
                ]
            )
        blocker_lines.extend(
            [
                "",
                "## Rule",
                "",
                "Strict 1->2->3 execution forbids moving to step 3 before step 2 has real inputs and produces metrics.",
            ]
        )
        blocker_path.write_text("\n".join(blocker_lines) + "\n", encoding="utf-8")
        print(
            json.dumps(
                {
                    "status": "blocked",
                    "inspection_json": str(inspection_path),
                    "blocker_report": str(blocker_path),
                    "missing_dataset_count": len(inspection["missing"]),
                },
                indent=2,
            )
        )
        return 2

    payload = run_metrics(specs)
    print(
        json.dumps({**payload, "inspection_json": str(inspection_path)}, indent=2)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
