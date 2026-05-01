#!/usr/bin/env python3
"""Audit whether staged natural-object roots are genuine benchmark data or only proxy placeholders."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class DatasetAudit:
    dataset_name: str
    dataset_version: str
    expected_dir: str
    file_count: int
    png_count: int
    jpg_count: int
    jpeg_count: int
    proxy_named_count: int
    first_files: list[str]
    inferred_status: str
    benchmark_root_ready: bool
    blocker_reason: str


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def natural_results_root() -> Path:
    return project_root() / "results" / "natural_objects"


def staging_root() -> Path:
    return project_root() / "data" / "natural_objects"


def load_subset_index() -> list[dict[str, str]]:
    path = natural_results_root() / "natural_object_subset_index.csv"
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def dataset_dir_name(row: dict[str, str]) -> str:
    stem = f"{row['dataset_name']}-{row['dataset_version']}"
    sanitized = stem.lower().replace(" ", "-").replace("/", "-")
    sanitized = sanitized.replace(".", "").replace("_", "-")
    return sanitized


def audit_dataset(row: dict[str, str]) -> DatasetAudit:
    directory = staging_root() / dataset_dir_name(row)
    files = sorted([p for p in directory.iterdir() if p.is_file()]) if directory.exists() else []
    names = [p.name for p in files]
    png_count = sum(p.suffix.lower() == ".png" for p in files)
    jpg_count = sum(p.suffix.lower() == ".jpg" for p in files)
    jpeg_count = sum(p.suffix.lower() == ".jpeg" for p in files)
    proxy_named_count = sum(("proxy" in p.stem.lower()) for p in files)

    if not directory.exists() or not files:
        inferred_status = "missing"
        benchmark_root_ready = False
        blocker_reason = "no staged files present"
    elif proxy_named_count == len(files):
        inferred_status = "proxy_only"
        benchmark_root_ready = False
        blocker_reason = "all staged files are proxy-named placeholders rather than benchmark-root images"
    elif jpg_count + jpeg_count == 0 and png_count > 0:
        inferred_status = "unverified_png_only"
        benchmark_root_ready = False
        blocker_reason = "staged files are PNG-only and do not yet verify licensed benchmark-root provenance"
    else:
        inferred_status = "candidate_benchmark_root"
        benchmark_root_ready = True
        blocker_reason = ""

    return DatasetAudit(
        dataset_name=row["dataset_name"],
        dataset_version=row["dataset_version"],
        expected_dir=str(directory),
        file_count=len(files),
        png_count=png_count,
        jpg_count=jpg_count,
        jpeg_count=jpeg_count,
        proxy_named_count=proxy_named_count,
        first_files=names[:5],
        inferred_status=inferred_status,
        benchmark_root_ready=benchmark_root_ready,
        blocker_reason=blocker_reason,
    )


def main() -> int:
    rows = load_subset_index()
    audits = [audit_dataset(row) for row in rows]
    results_root = natural_results_root()
    results_root.mkdir(parents=True, exist_ok=True)

    manifest_rows = []
    for audit in audits:
        manifest_rows.append(
            {
                "dataset_name": audit.dataset_name,
                "dataset_version": audit.dataset_version,
                "expected_dir": audit.expected_dir,
                "file_count": audit.file_count,
                "proxy_named_count": audit.proxy_named_count,
                "inferred_status": audit.inferred_status,
                "benchmark_root_ready": audit.benchmark_root_ready,
                "blocker_reason": audit.blocker_reason,
            }
        )

    manifest_path = results_root / "benchmark_root_subset_manifest.csv"
    with manifest_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(manifest_rows[0].keys()))
        writer.writeheader()
        writer.writerows(manifest_rows)

    summary_path = results_root / "benchmark_root_summary.csv"
    with summary_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["dataset_name", "dataset_version", "benchmark_root_ready", "inferred_status", "file_count"],
        )
        writer.writeheader()
        for audit in audits:
            writer.writerow(
                {
                    "dataset_name": audit.dataset_name,
                    "dataset_version": audit.dataset_version,
                    "benchmark_root_ready": audit.benchmark_root_ready,
                    "inferred_status": audit.inferred_status,
                    "file_count": audit.file_count,
                }
            )

    readme_lines = [
        "# Benchmark-Root Natural-Object Audit",
        "",
        "This file records whether the active staging directories contain genuine benchmark-root natural images or only proxy placeholders.",
        "",
        "## Status",
        "",
    ]
    for audit in audits:
        readme_lines.append(
            f"- `{audit.dataset_name} / {audit.dataset_version}`: `{audit.inferred_status}` with `{audit.file_count}` files in `{audit.expected_dir}`"
        )
        if audit.blocker_reason:
            readme_lines.append(f"  blocker: {audit.blocker_reason}")
    readme_lines.extend(
        [
            "",
            "## Rule",
            "",
            "Natural-image evidence may be promoted from `proxy-only` only when both dataset roots are benchmark-root ready and the staged subset can be traced to licensed ImageNet/COCO files rather than project-local placeholders.",
        ]
    )
    readme_path = results_root / "benchmark_root_readme.md"
    readme_path.write_text("\n".join(readme_lines) + "\n", encoding="utf-8")

    audit_json_path = results_root / "benchmark_root_audit.json"
    audit_json_path.write_text(
        json.dumps(
            {
                "project_root": str(project_root()),
                "staging_root": str(staging_root()),
                "datasets": [asdict(audit) for audit in audits],
                "all_benchmark_root_ready": all(audit.benchmark_root_ready for audit in audits),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "benchmark_root_manifest": str(manifest_path),
                "benchmark_root_summary": str(summary_path),
                "benchmark_root_readme": str(readme_path),
                "all_benchmark_root_ready": all(audit.benchmark_root_ready for audit in audits),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
