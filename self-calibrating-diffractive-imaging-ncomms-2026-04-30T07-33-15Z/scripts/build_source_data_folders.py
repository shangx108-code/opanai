#!/usr/bin/env python3
"""Build figure-level source-data folders from the authoritative index."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
from collections import defaultdict
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_INDEX = PROJECT_ROOT / "source_data" / "source_data_index.csv"
OUT_ROOT = PROJECT_ROOT / "source_data"
TARGET_FIGURES = {"Fig1", "Fig2", "Fig3", "Fig4", "FigS1"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_name(text: str) -> str:
    return text.replace("/", "_").replace(" ", "_")


def resolve_project_path(value: str) -> Path | None:
    if not value or value in {"not_applicable", "pending/configs/unified_comparison.yaml", "pending/configs/natural_object_eval.yaml", "pending/configs/mixed_train_natural_thickstats.yaml", "pending/configs/mixed_train_tolerance.yaml", "pending/configs/robust_mask_tolerance_compare.yaml"}:
        return None
    return PROJECT_ROOT / value


def copy_if_exists(src: Path | None, dst: Path) -> bool:
    if src is None or not src.exists():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return True


def default_forbidden_overclaim(row: dict[str, str]) -> str:
    evidence = row["evidence_status"]
    if evidence == "proxy-only":
        return "Do not claim benchmark-root ImageNet/COCO performance or remove the proxy qualifier."
    if evidence == "simulation-only":
        return "Do not translate this simulation-only tolerance result into a fabricated-device robustness claim."
    return "Do not generalize this panel beyond the datasets, ledgers, and perturbation families it directly measures."


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    with SOURCE_INDEX.open("r", encoding="utf-8", newline="") as handle:
        rows = [row for row in csv.DictReader(handle) if row["figure"] in TARGET_FIGURES]

    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["figure"]].append(row)

    for figure, figure_rows in grouped.items():
        fig_dir = OUT_ROOT / figure
        fig_dir.mkdir(parents=True, exist_ok=True)
        manifest_rows: list[tuple[str, str, str]] = []
        readme_lines = [
            f"# {figure} Source Data",
            "",
            "This folder packages the final panel-level source data, scripts, config snapshots, and claim-boundary notes for one manuscript figure.",
            "",
            "## Panels",
        ]
        notes_lines = [f"# {figure} Claim Boundary Notes", ""]

        for row in figure_rows:
            panel = row["panel"]
            panel_prefix = f"panel_{safe_name(panel)}"
            panel_dir = fig_dir / panel_prefix
            panel_dir.mkdir(parents=True, exist_ok=True)

            copied_any = False
            summary_src = resolve_project_path(row["summary_file"])
            raw_src = resolve_project_path(row["raw_file"])
            plot_src = resolve_project_path(row["plot_script"])
            analysis_src = resolve_project_path(row["analysis_script"])
            config_src = resolve_project_path(row["config_file"])

            for label, src in [
                ("summary", summary_src),
                ("raw", raw_src),
                ("plot_script", plot_src),
                ("analysis_script", analysis_src),
            ]:
                if src is not None and src.exists():
                    dst = panel_dir / f"{label}__{src.name}"
                    copy_if_exists(src, dst)
                    manifest_rows.append((str(dst.relative_to(fig_dir)), sha256(dst), label))
                    copied_any = True

            config_snapshot = {
                "figure": row["figure"],
                "panel": row["panel"],
                "config_reference": row["config_file"],
                "resolved_config_exists": bool(config_src and config_src.exists()),
                "evidence_status": row["evidence_status"],
                "last_verified_utc": row["last_verified_utc"],
            }
            if config_src and config_src.exists():
                dst = panel_dir / f"config_snapshot__{config_src.name}"
                copy_if_exists(config_src, dst)
                config_snapshot["copied_config_file"] = str(dst.relative_to(fig_dir))
                manifest_rows.append((str(dst.relative_to(fig_dir)), sha256(dst), "config_snapshot_file"))
            snapshot_path = panel_dir / "config_snapshot.json"
            write_text(snapshot_path, json.dumps(config_snapshot, indent=2) + "\n")
            manifest_rows.append((str(snapshot_path.relative_to(fig_dir)), sha256(snapshot_path), "config_snapshot_json"))

            panel_readme = [
                f"# {figure} Panel {panel}",
                "",
                f"Supported claim: {row['claim_supported']}",
                f"Evidence status: {row['evidence_status']}",
                f"Section: {row['section']}",
                f"Notes: {row['notes']}",
                "",
                "The copied files in this panel folder are the final artifacts referenced by `source_data_index.csv` for this panel.",
            ]
            readme_path = panel_dir / "README.md"
            write_text(readme_path, "\n".join(panel_readme) + "\n")
            manifest_rows.append((str(readme_path.relative_to(fig_dir)), sha256(readme_path), "panel_readme"))

            readme_lines.append(f"- `{panel}`: {row['claim_supported']} [{row['evidence_status']}]")
            notes_lines.extend(
                [
                    f"## Panel {panel}",
                    "",
                    f"- Approved claim: {row['claim_supported']}",
                    f"- Forbidden overclaim: {default_forbidden_overclaim(row)}",
                    f"- Evidence status: {row['evidence_status']}",
                    f"- Source-data panel folder: `{panel_prefix}`",
                    "",
                ]
            )
            if not copied_any:
                readme_lines.append(f"  - Warning: no source artifact could be copied for panel `{panel}`.")

        folder_readme = fig_dir / "README.md"
        write_text(folder_readme, "\n".join(readme_lines) + "\n")
        manifest_rows.append((folder_readme.name, sha256(folder_readme), "figure_readme"))

        notes_path = fig_dir / "claim_boundary_notes.md"
        write_text(notes_path, "\n".join(notes_lines) + "\n")
        manifest_rows.append((notes_path.name, sha256(notes_path), "claim_boundary_notes"))

        manifest_path = fig_dir / "checksum_manifest.csv"
        with manifest_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["relative_path", "sha256", "role"])
            for rel, digest, role in sorted(manifest_rows):
                writer.writerow([rel, digest, role])

    print(json.dumps({"status": "completed", "figures": sorted(grouped), "output_root": str(OUT_ROOT)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
