#!/usr/bin/env python3

from __future__ import annotations

import importlib
import json
import os
import platform
import shutil
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOG_PATH = PROJECT_ROOT / "logs" / "env_check.json"

REQUIRED_MODULES = [
    "numpy",
    "pandas",
    "scipy",
    "matplotlib",
    "seaborn",
]

EXPECTED_DIRS = [
    PROJECT_ROOT / "code",
    PROJECT_ROOT / "data" / "raw",
    PROJECT_ROOT / "data" / "processed",
    PROJECT_ROOT / "figures",
    PROJECT_ROOT / "derivations",
    PROJECT_ROOT / "manuscript",
    PROJECT_ROOT / "logs",
]


def check_module(name: str) -> dict[str, str]:
    try:
        module = importlib.import_module(name)
        return {
            "status": "available",
            "version": getattr(module, "__version__", "unknown"),
        }
    except Exception as exc:
        return {
            "status": "missing",
            "error": str(exc),
        }


def main() -> int:
    report = {
        "project_root": str(PROJECT_ROOT),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "executable": sys.executable,
        "cwd": os.getcwd(),
        "venv": os.environ.get("VIRTUAL_ENV", ""),
        "commands": {cmd: shutil.which(cmd) or "" for cmd in ["python", "python3", "git", "node", "rg"]},
        "modules": {name: check_module(name) for name in REQUIRED_MODULES},
        "directories": {str(path): path.exists() for path in EXPECTED_DIRS},
    }

    LOG_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))

    missing = [name for name, info in report["modules"].items() if info["status"] != "available"]
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
