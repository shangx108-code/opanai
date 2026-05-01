#!/usr/bin/env python3
"""Build a project-wide reproducibility manifest."""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = PROJECT_ROOT / "archive" / "reproducibility_manifest.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def inventory_files(relative_root: str) -> list[dict[str, object]]:
    root = PROJECT_ROOT / relative_root
    if not root.exists():
        return []
    rows: list[dict[str, object]] = []
    for path in sorted(p for p in root.rglob("*") if p.is_file() and "__pycache__" not in p.parts):
        rows.append(
            {
                "path": str(path.relative_to(PROJECT_ROOT)),
                "sha256": sha256(path),
                "size_bytes": path.stat().st_size,
            }
        )
    return rows


def installed_packages() -> list[dict[str, str]]:
    code = (
        "import importlib.metadata as m, json; "
        "print(json.dumps(sorted([{'name':d.metadata['Name'] or d.metadata['Summary'] or '', 'version':d.version} "
        "for d in m.distributions() if d.metadata.get('Name')], key=lambda x: x['name'].lower())))"
    )
    output = subprocess.check_output([sys.executable, "-c", code], text=True)
    return json.loads(output)


def main() -> int:
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "project_id": PROJECT_ROOT.name,
        "generated_at_utc": subprocess.check_output(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"], text=True).strip(),
        "environment": {
            "python_executable": sys.executable,
            "python_version": sys.version,
            "platform": platform.platform(),
        },
        "package_versions": installed_packages(),
        "script_inventory": inventory_files("scripts"),
        "config_inventory": inventory_files("config"),
        "result_inventory": inventory_files("results"),
        "manuscript_inventory": inventory_files("manuscript"),
        "source_data_inventory": inventory_files("source_data"),
        "archive_inventory": inventory_files("archive"),
        "hash_inventory_policy": "All file hashes use SHA-256 over file bytes; __pycache__ files are excluded.",
    }
    OUT_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "completed", "manifest": str(OUT_PATH)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
