from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path


PROJECT_ROOT = Path("/workspace/memory/twse2-andreev-prl-2026-04-29T13-43-41Z")
ACTIVE_ROOT = Path("/workspace/memory/twse2-andreev-prl")
CONFIG_PATH = PROJECT_ROOT / "project-config.json"
LOG_DIR = PROJECT_ROOT / "logs"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def build_status() -> dict:
    config = read_json(CONFIG_PATH)
    required_paths = {
        "project_root": PROJECT_ROOT,
        "active_compute_root": ACTIVE_ROOT,
        "active_pipeline": ACTIVE_ROOT / "code" / "twse2_persistent_pipeline.py",
        "semi_infinite_btk_summary": ACTIVE_ROOT / "data" / "btk-generalized-valley-resolved-semi-infinite-2026-04-29" / "summary.md",
        "project_state": PROJECT_ROOT / "project-state.md",
        "journal_criteria": PROJECT_ROOT / "journal-criteria.md",
    }
    path_status = {name: path.exists() for name, path in required_paths.items()}
    return {
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "project_slug": config["project_slug"],
        "target_journal": config["target_journal"],
        "iteration_cadence": config["iteration"]["cadence"],
        "stop_criterion": config["stop_criterion"],
        "path_status": path_status,
        "ready_for_hourly_iteration": all(path_status.values()),
    }


def main() -> None:
    ensure_dir(LOG_DIR)
    status = build_status()
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    out_path = LOG_DIR / f"hourly-driver-status-{stamp}.json"
    out_path.write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()