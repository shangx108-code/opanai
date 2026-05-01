#!/usr/bin/env python3
"""Bootstrap the Majorana three-terminal recovery workspace.

This script rebuilds the recovery folder for the missing three-terminal
benchmark bundle, records the currently available Python stack, and emits an
auditable missing-asset list for the next real rerun.
"""

from __future__ import annotations

import json
import platform
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path("/workspace")
OUTPUT_DIR = ROOT / "output" / "three-terminal-benchmark"
EXPECTED_FILES = [
    "selected_operating_points.csv",
    "positive_three_terminal_scan.csv",
    "positive_three_terminal_bias.csv",
    "dot_three_terminal_bias.csv",
    "impurity_three_terminal_bias.csv",
    "disorder_three_terminal_bias.csv",
    "positive_three_terminal_robustness.csv",
    "figure3_failure_local_peaks.png",
    "figure4_nonlocal_rescue.png",
]
OPTIONAL_ENTRYPOINTS = [
    ROOT / "output" / "three-terminal-benchmark" / "three_terminal_benchmark.py",
    ROOT / "three_terminal_benchmark.py",
    ROOT / "scripts" / "three_terminal_benchmark.py",
    ROOT / "memory" / "majorana-diagnostic-natphys" / "code" / "three_terminal_benchmark.py",
]
DEPENDENCIES = ["numpy", "scipy", "matplotlib", "pandas"]


@dataclass
class DependencyStatus:
    name: str
    available: bool
    version: str | None
    detail: str


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def ensure_dirs() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def iter_missing_assets() -> Iterable[str]:
    for filename in EXPECTED_FILES:
        if not (OUTPUT_DIR / filename).exists():
            yield filename


def dependency_status() -> list[DependencyStatus]:
    results: list[DependencyStatus] = []
    for name in DEPENDENCIES:
        try:
            module = __import__(name)
            results.append(
                DependencyStatus(
                    name=name,
                    available=True,
                    version=getattr(module, "__version__", None),
                    detail="import ok",
                )
            )
        except Exception as exc:  # pragma: no cover - direct environment audit
            results.append(
                DependencyStatus(
                    name=name,
                    available=False,
                    version=None,
                    detail=str(exc),
                )
            )
    return results


def script_candidates() -> list[dict[str, object]]:
    return [{"path": str(path), "exists": path.exists()} for path in OPTIONAL_ENTRYPOINTS]


def build_manifest_payload() -> dict[str, object]:
    deps = dependency_status()
    missing_assets = list(iter_missing_assets())
    return {
        "project": "majorana-diagnostic-natphys",
        "generated_at_utc": utc_now(),
        "workspace_root": str(ROOT),
        "output_dir": str(OUTPUT_DIR),
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "dependency_status": [asdict(item) for item in deps],
        "script_candidates": script_candidates(),
        "expected_files": EXPECTED_FILES,
        "present_files": sorted(path.name for path in OUTPUT_DIR.glob("*") if path.is_file()),
        "missing_files": missing_assets,
        "ready_for_topology_rerun": not missing_assets
        and any(item["exists"] for item in script_candidates()),
    }


def write_json(payload: dict[str, object]) -> None:
    (OUTPUT_DIR / "provenance_manifest.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (OUTPUT_DIR / "environment_audit.json").write_text(
        json.dumps(
            {
                "generated_at_utc": payload["generated_at_utc"],
                "python_version": payload["python_version"],
                "platform": payload["platform"],
                "dependency_status": payload["dependency_status"],
                "script_candidates": payload["script_candidates"],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    (OUTPUT_DIR / "missing_assets.json").write_text(
        json.dumps(
            {
                "generated_at_utc": payload["generated_at_utc"],
                "output_dir": payload["output_dir"],
                "missing_files": payload["missing_files"],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def write_recovery_manifest(payload: dict[str, object]) -> None:
    dep_lines = []
    for item in payload["dependency_status"]:
        status = "OK" if item["available"] else "MISSING"
        version = item["version"] or "-"
        dep_lines.append(f"- `{item['name']}`: {status} ({version}) - {item['detail']}")

    script_lines = []
    for item in payload["script_candidates"]:
        status = "present" if item["exists"] else "missing"
        script_lines.append(f"- `{item['path']}`: {status}")

    missing_lines = [f"- `{name}`" for name in payload["missing_files"]]
    if not missing_lines:
        missing_lines = ["- none"]

    text = "\n".join(
        [
            "# Recovery Manifest",
            "",
            f"- Generated at: `{payload['generated_at_utc']}`",
            f"- Workspace root: `{payload['workspace_root']}`",
            f"- Recovery output directory: `{payload['output_dir']}`",
            f"- Python version: `{payload['python_version']}`",
            "",
            "## Dependency audit",
            *dep_lines,
            "",
            "## Script entry-point search",
            *script_lines,
            "",
            "## Expected benchmark bundle",
            *[f"- `{name}`" for name in payload["expected_files"]],
            "",
            "## Missing assets in current workspace",
            *missing_lines,
            "",
            "## Recovery status",
            (
                "- The workspace is ready for a topology rerun."
                if payload["ready_for_topology_rerun"]
                else "- The workspace is not ready for a topology rerun."
            ),
            "- This manifest records recovery state only and does not certify regenerated benchmark data.",
        ]
    )
    (OUTPUT_DIR / "RECOVERY_MANIFEST.md").write_text(text + "\n", encoding="utf-8")


def main() -> int:
    ensure_dirs()
    payload = build_manifest_payload()
    write_json(payload)
    write_recovery_manifest(payload)
    print(f"Recovery folder: {OUTPUT_DIR}")
    print(f"Missing assets: {len(payload['missing_files'])}")
    print(f"Ready for topology rerun: {payload['ready_for_topology_rerun']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
