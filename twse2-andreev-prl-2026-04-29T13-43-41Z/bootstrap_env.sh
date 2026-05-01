#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ACTIVE_ROOT="/workspace/memory/twse2-andreev-prl"
LOG_DIR="${PROJECT_ROOT}/logs"
mkdir -p "${LOG_DIR}" "${PROJECT_ROOT}/results" "${PROJECT_ROOT}/manuscript" "${PROJECT_ROOT}/supplementary"

python3 - <<'PY' > "${LOG_DIR}/environment-check-latest.txt"
from __future__ import annotations

import json
import platform
import sys
from datetime import datetime, UTC
from pathlib import Path

required = ["numpy", "pandas", "PIL"]
status = {}
for name in required:
    try:
        __import__(name)
        status[name] = "ok"
    except Exception as exc:  # pragma: no cover
        status[name] = f"missing: {exc}"

report = {
    "timestamp_utc": datetime.now(UTC).isoformat(),
    "python": sys.version,
    "platform": platform.platform(),
    "required_modules": status,
    "project_root_exists": Path("/workspace/memory/twse2-andreev-prl-2026-04-29T13-43-41Z").exists(),
    "active_compute_root_exists": Path("/workspace/memory/twse2-andreev-prl").exists(),
}
print(json.dumps(report, indent=2))
PY

echo "Environment bootstrap complete."
echo "Project root: ${PROJECT_ROOT}"
echo "Active compute root: ${ACTIVE_ROOT}"
echo "Log: ${LOG_DIR}/environment-check-latest.txt"