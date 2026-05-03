from __future__ import annotations

import json
import platform
from datetime import datetime, UTC
from pathlib import Path

import numpy as np
from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = PROJECT_ROOT / "results" / "environment_smoke_test_2026-05-03"
LOGS_DIR = PROJECT_ROOT / "logs"


def build_probe_image() -> dict[str, float]:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    grid = np.linspace(0.0, 1.0, 64, dtype=np.float32)
    xx, yy = np.meshgrid(grid, grid, indexing="xy")
    field = 0.55 + 0.25 * np.sin(2 * np.pi * xx) + 0.20 * np.cos(2 * np.pi * yy)
    image_array = np.clip(field * 255.0, 0, 255).astype(np.uint8)
    image = Image.fromarray(image_array, mode="L")
    image.save(RESULTS_DIR / "probe.png")
    return {
        "min": float(field.min()),
        "max": float(field.max()),
        "mean": float(field.mean()),
    }


def main() -> None:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    field_stats = build_probe_image()
    report = {
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "pillow": Image.__version__,
        "project_root": str(PROJECT_ROOT),
        "result_dir": str(RESULTS_DIR),
        "field_stats": field_stats,
        "status": "ok",
    }
    report_path = RESULTS_DIR / "environment_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    (LOGS_DIR / "environment-smoke-test.log").write_text(
        json.dumps(report, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
