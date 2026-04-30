#!/usr/bin/env python3
"""Validate the minimal local environment for this project."""

from __future__ import annotations

import importlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path


REQUIRED_MODULES = [
    "numpy",
    "pandas",
    "PIL",
    "reportlab",
    "pypdf",
]


def check_modules() -> dict[str, bool]:
    status: dict[str, bool] = {}
    for module_name in REQUIRED_MODULES:
        try:
            importlib.import_module(module_name)
        except Exception:
            status[module_name] = False
        else:
            status[module_name] = True
    return status


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    output_dir = project_root / "results" / "environment"
    output_dir.mkdir(parents=True, exist_ok=True)

    report = {
        "checked_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
        "project_root": str(project_root),
        "required_modules": check_modules(),
    }
    report["all_required_modules_available"] = all(report["required_modules"].values())

    report_path = output_dir / "environment/environment_check.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(json.dumps(report, indent=2))
    return 0 if report["all_required_modules_available"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
