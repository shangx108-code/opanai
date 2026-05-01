#!/usr/bin/env python3
"""Stage a public, traceable natural-image subset into the active project root."""

from __future__ import annotations

import csv
import hashlib
import json
import urllib.request
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = PROJECT_ROOT / "data" / "natural_objects"
RESULT_ROOT = PROJECT_ROOT / "results" / "natural_objects"


PUBLIC_DATASETS = [
    {
        "dataset_name": "Kodak-PCD0992",
        "dataset_version": "unrestricted public release",
        "subset_role": "natural-object primary ledger",
        "planned_subset_size": 12,
        "selection_rule": "Freeze kodim01.png through kodim12.png from the public Kodak-PCD0992 release mirrored in girfa/ColorImageDatasets.",
        "eligibility_rule": "Use the frozen unrestricted Kodak images exactly as mirrored; no manual filtering beyond file integrity checks.",
        "preprocessing": "center-crop to square, resize to 128x128, convert to grayscale, normalize to [0,1], then downsample to the active 12x12 frontend for all methods.",
        "shared_across_methods": "yes",
        "raw_data_redistributed": "yes",
        "license_note": "The Kodak-PCD0992 dataset is described in the mirrored repository README as an unrestricted Kodak release.",
        "local_status": "public_open_data_staged",
        "source_repository": "https://github.com/girfa/ColorImageDatasets",
        "source_subdir": "Kodak-PCD0992",
        "filenames": [f"kodim{i:02d}.png" for i in range(1, 13)],
    },
    {
        "dataset_name": "UCID",
        "dataset_version": "1338 public citation subset",
        "subset_role": "natural-object diversity stress test",
        "planned_subset_size": 12,
        "selection_rule": "Freeze numeric files 1.tif through 12.tif from the public UCID mirror in girfa/ColorImageDatasets.",
        "eligibility_rule": "Use the frozen UCID images exactly as mirrored; no manual filtering beyond file integrity checks.",
        "preprocessing": "center-crop to square, resize to 128x128, convert to grayscale, normalize to [0,1], then downsample to the active 12x12 frontend for all methods.",
        "shared_across_methods": "yes",
        "raw_data_redistributed": "yes",
        "license_note": "Use the mirrored UCID subset with citation back to Schaefer and Stich, Proc. SPIE 5307 (2003), as documented in the repository README.",
        "local_status": "public_open_data_staged",
        "source_repository": "https://github.com/girfa/ColorImageDatasets",
        "source_subdir": "UCID-1338",
        "filenames": [f"{i}.tif" for i in range(1, 13)],
    },
]


def dataset_dir_name(dataset_name: str, dataset_version: str) -> str:
    stem = f"{dataset_name}-{dataset_version}"
    sanitized = stem.lower().replace(" ", "-").replace("/", "-")
    sanitized = sanitized.replace(".", "").replace("_", "-")
    return sanitized


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, destination)


def write_subset_index() -> Path:
    path = RESULT_ROOT / "natural_object_subset_index.csv"
    fieldnames = [
        "dataset_name",
        "dataset_version",
        "subset_role",
        "planned_subset_size",
        "selection_rule",
        "eligibility_rule",
        "preprocessing",
        "shared_across_methods",
        "raw_data_redistributed",
        "license_note",
        "local_status",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for dataset in PUBLIC_DATASETS:
            writer.writerow({key: dataset[key] for key in fieldnames})
    return path


def write_protocol_files(rows: list[dict[str, object]]) -> tuple[Path, Path, Path]:
    manifest_csv = RESULT_ROOT / "public_dataset_download_manifest.csv"
    manifest_json = RESULT_ROOT / "public_dataset_download_manifest.json"
    protocol_md = RESULT_ROOT / "public_dataset_protocol.md"

    with manifest_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    manifest_json.write_text(
        json.dumps(
            {
                "status": "completed",
                "dataset_count": len(PUBLIC_DATASETS),
                "file_count": len(rows),
                "files": rows,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    lines = [
        "# Public Natural-Object Protocol",
        "",
        "This protocol replaces the unavailable benchmark-root ImageNet/COCO branch with a directly staged public subset that can be re-downloaded from stable GitHub raw URLs.",
        "",
        "## Datasets",
        "",
    ]
    for dataset in PUBLIC_DATASETS:
        lines.extend(
            [
                f"- `{dataset['dataset_name']} / {dataset['dataset_version']}`",
                f"  - subset size: `{dataset['planned_subset_size']}`",
                f"  - source repository: `{dataset['source_repository']}`",
                f"  - source subdirectory: `{dataset['source_subdir']}`",
                f"  - selection rule: {dataset['selection_rule']}",
                f"  - preprocessing: {dataset['preprocessing']}",
                f"  - license note: {dataset['license_note']}",
            ]
        )
    lines.extend(
        [
            "",
            "## Traceability",
            "",
            "- Every staged file is listed with source URL, local path, byte size, and SHA-256 digest in `public_dataset_download_manifest.csv`.",
            "- The frozen subset definition is recorded in `natural_object_subset_index.csv`.",
            "- These files are public-open-data subsets, not ImageNet/COCO replacements.",
        ]
    )
    protocol_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return manifest_csv, manifest_json, protocol_md


def write_package_note() -> Path:
    package_path = RESULT_ROOT / "natural_object_package.md"
    lines = [
        "# Natural-Object Package",
        "",
        "## Status",
        "",
        "- Package type: `public-open-data execution package`",
        "- Execution status: `ready for rerun on staged public Kodak and UCID subsets`",
        "- Reason: benchmark-root ImageNet/COCO files were unavailable, so this branch now uses directly staged public datasets with frozen manifests.",
        "",
        "## Frozen protocol",
        "",
        "- Datasets selected for the auditable natural-object pass:",
        "  - `Kodak-PCD0992 / unrestricted public release`",
        "  - `UCID / 1338 public citation subset`",
        "- Proposed subset size: `12 + 12` images.",
        "- Shared preprocessing for all methods: center-crop to square, resize to `128 x 128`, convert to grayscale, normalize to `[0, 1]`, then downsample to the active `12 x 12` frontend.",
        "- Shared fairness rule: every method must use the exact same frozen subset and preprocessing chain.",
        "",
        "## Included files",
        "",
        "- `natural_object_subset_index.csv` freezes dataset version, selection rule, preprocessing, and provenance handling.",
        "- `public_dataset_download_manifest.csv` lists the exact downloaded raw files and digests.",
        "- `public_dataset_protocol.md` records the public-data substitution boundary and traceability notes.",
        "",
        "## Interpretation boundary",
        "",
        "This package upgrades the natural-image branch from proxy-only placeholders to real public-open-data evaluation. It still does not justify claims about benchmark-root ImageNet/COCO performance, and the manuscript should name the Kodak/UCID protocol explicitly.",
        "",
        "## Previous blocker status",
        "",
        "- The old ImageNet/COCO benchmark-root blocker remains historically true but is no longer the active natural-image execution path in this project root.",
    ]
    package_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return package_path


def main() -> int:
    RESULT_ROOT.mkdir(parents=True, exist_ok=True)
    subset_index = write_subset_index()
    rows: list[dict[str, object]] = []
    for dataset in PUBLIC_DATASETS:
        local_dir = DATA_ROOT / dataset_dir_name(dataset["dataset_name"], dataset["dataset_version"])
        for filename in dataset["filenames"]:
            url = f"https://raw.githubusercontent.com/girfa/ColorImageDatasets/main/{dataset['source_subdir']}/{filename}"
            destination = local_dir / filename
            if not destination.exists():
                download(url, destination)
            rows.append(
                {
                    "dataset_name": dataset["dataset_name"],
                    "dataset_version": dataset["dataset_version"],
                    "filename": filename,
                    "source_url": url,
                    "local_path": str(destination.relative_to(PROJECT_ROOT)),
                    "size_bytes": destination.stat().st_size,
                    "sha256": sha256(destination),
                }
            )

    manifest_csv, manifest_json, protocol_md = write_protocol_files(rows)
    package_md = write_package_note()
    payload = {
        "status": "completed",
        "subset_index": str(subset_index),
        "manifest_csv": str(manifest_csv),
        "manifest_json": str(manifest_json),
        "protocol_md": str(protocol_md),
        "package_md": str(package_md),
        "file_count": len(rows),
    }
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
