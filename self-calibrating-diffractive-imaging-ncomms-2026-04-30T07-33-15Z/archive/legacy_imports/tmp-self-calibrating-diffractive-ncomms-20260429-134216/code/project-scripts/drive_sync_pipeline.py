from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CONFIG_PATH = Path("/workspace/self-calibrating-diffractive-ncomms/scripts/drive_sync_config.json")
AUTO_SYNC_START = "<!-- auto-drive-sync:start -->"
AUTO_SYNC_END = "<!-- auto-drive-sync:end -->"


def load_config() -> dict[str, Any]:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_utc(ts: float) -> str:
    return datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def artifact_group_for(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".py":
        return "code"
    if suffix in {".csv", ".json"}:
        return "data"
    if suffix in {".png", ".jpg", ".jpeg", ".pdf"}:
        return "figure"
    if suffix == ".md":
        if "protocol" in path.name:
            return "protocol"
        if "review" in path.name:
            return "review"
        if "manuscript" in path.name:
            return "manuscript"
        return "report"
    return "artifact"


def section_for(path: Path) -> str:
    name = path.name
    suffix = path.suffix.lower()
    if name.startswith("round") and suffix == ".py":
        return "07-code"
    if "protocol" in name:
        return "03-theory"
    if suffix == ".py":
        return "07-code"
    if suffix in {".csv", ".json"}:
        return "04-data"
    if suffix in {".png", ".jpg", ".jpeg", ".pdf"}:
        return "05-figures"
    if "manuscript" in name:
        return "06-manuscript"
    if "review" in name or "supervision" in name:
        return "08-review-and-supervision"
    if "reference-ledger" in name:
        return "02-literature"
    return "09-archive"


def subpath_for(section: str, path: Path, stamp: str) -> str:
    stem = path.stem
    if path.parent.name == "outputs":
        round_hint = stem.split("_")[0]
        return f"{section}/{stamp}/{round_hint}"
    if path.parent.name == "scripts":
        return f"{section}/{stamp}/scripts"
    return f"{section}/{stamp}/memory"


def note_for(path: Path, status: str) -> str:
    if status != "local-ready":
        return "referenced in project memory but not present in current active workspace"
    if path.parent.name == "outputs":
        return "generated output ready for cloud archive"
    if path.parent.name == "scripts":
        return "runtime script or protocol needed for reproduction"
    return "memory-side project state document"


def build_row(project: str, stage: str, path: Path, status: str, stamp: str) -> dict[str, object]:
    group = artifact_group_for(path)
    section = section_for(path)
    row = {
        "project": project,
        "stage": stage,
        "artifact_group": group,
        "status": status,
        "local_path": str(path),
        "recommended_drive_section": section,
        "recommended_subpath": subpath_for(section, path, stamp),
        "notes": note_for(path, status),
        "exists": path.exists(),
        "file_size_bytes": path.stat().st_size if path.exists() else "",
        "modified_utc": iso_utc(path.stat().st_mtime) if path.exists() else "",
    }
    return row


def collect_rows(config: dict[str, Any], stamp: str) -> list[dict[str, object]]:
    project_root = Path(config["project_root"])
    memory_root = Path(config["memory_root"])
    project_name = config["project_name"]

    rows: list[dict[str, object]] = []
    seen: set[Path] = set()

    for pattern in config["local_ready_globs"]:
        for path in sorted(project_root.glob(pattern)):
            if path in seen:
                continue
            seen.add(path)
            rows.append(build_row(project_name, "active-workspace", path, "local-ready", stamp))

    for rel in config["memory_docs"]:
        path = memory_root / rel
        if path in seen:
            continue
        seen.add(path)
        rows.append(build_row(project_name, "memory-state", path, "local-ready", stamp))

    for raw in config["missing_expected"]:
        path = Path(raw)
        if path in seen:
            continue
        seen.add(path)
        rows.append(build_row(project_name, "history-gap", path, "missing-from-active-workspace", stamp))

    rows.sort(key=lambda item: (str(item["status"]), str(item["local_path"])))
    return rows


def write_csv(rows: list[dict[str, object]], target: Path) -> None:
    ensure_dir(target.parent)
    fieldnames = list(rows[0].keys())
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def replace_or_append_block(text: str, block: str) -> str:
    if AUTO_SYNC_START in text and AUTO_SYNC_END in text:
        start = text.index(AUTO_SYNC_START)
        end = text.index(AUTO_SYNC_END) + len(AUTO_SYNC_END)
        return text[:start].rstrip() + "\n\n" + block + "\n"
    text = text.rstrip() + "\n\n" if text.strip() else ""
    return text + block + "\n"


def update_managed_block(path: Path, body: str) -> None:
    current = path.read_text(encoding="utf-8") if path.exists() else ""
    block = f"{AUTO_SYNC_START}\n{body.rstrip()}\n{AUTO_SYNC_END}"
    path.write_text(replace_or_append_block(current, block), encoding="utf-8")


def summarise_rows(rows: list[dict[str, object]]) -> dict[str, Any]:
    ready = [row for row in rows if row["status"] == "local-ready"]
    missing = [row for row in rows if row["status"] != "local-ready"]
    return {
        "local_ready_count": len(ready),
        "missing_count": len(missing),
        "code_count": sum(1 for row in ready if row["artifact_group"] == "code"),
        "data_count": sum(1 for row in ready if row["artifact_group"] == "data"),
        "figure_count": sum(1 for row in ready if row["artifact_group"] == "figure"),
        "memory_doc_count": sum(1 for row in ready if row["stage"] == "memory-state"),
        "missing_paths": [row["local_path"] for row in missing],
    }


def render_drive_index_block(config: dict[str, Any], summary: dict[str, Any], manifest_latest: Path, status_json: Path, stamp: str) -> str:
    lines = [
        "## 自动同步状态",
        f"- 最近刷新时间（UTC）：`{stamp}`",
        f"- 本地已就绪待同步资产：`{summary['local_ready_count']}`",
        f"- 当前缺失历史资产：`{summary['missing_count']}`",
        f"- 最新 manifest：`{manifest_latest}`",
        f"- 最新状态 JSON：`{status_json}`",
        f"- 默认目标文件夹：`{config['target_drive_folder']['title']}` -> `{config['target_drive_folder']['url']}`",
        "- 当前云端写入状态：受限。现有工作流已能自动整理同步包和长期索引，但仍需可写 Drive 入口才能完成真正上云。",
        "- 已发现的 Drive 台账：",
    ]
    for ledger in config["drive_ledgers"]:
        lines.append(f"  - `{ledger['title']}`: `{ledger['url']}`")
    return "\n".join(lines)


def render_archive_block(config: dict[str, Any], summary: dict[str, Any], manifest_latest: Path, stamp: str) -> str:
    return "\n".join(
        [
            "## 自动同步监视",
            f"- 最近刷新时间（UTC）：`{stamp}`",
            f"- 本地已就绪待同步资产：`{summary['local_ready_count']}`",
            f"- 当前缺失历史资产：`{summary['missing_count']}`",
            f"- 最新同步清单：`{manifest_latest}`",
            f"- 默认目标文件夹：`{config['target_drive_folder']['title']}`",
            "- 当前状态：已打通“迭代后自动整理长期归档包”的本地流程；Google Drive 实际写入仍待可写入口。",
        ]
    )


def render_iteration_block(config: dict[str, Any], summary: dict[str, Any], manifest_latest: Path, stamp: str) -> str:
    missing_preview = summary["missing_paths"][:3]
    lines = [
        "## 自动云端同步监视",
        f"- 最近刷新时间（UTC）：`{stamp}`",
        f"- 本轮本地待同步资产数：`{summary['local_ready_count']}`",
        f"- 当前仍缺失的历史资产数：`{summary['missing_count']}`",
        f"- 最新同步清单：`{manifest_latest}`",
        f"- 默认目标文件夹：`{config['target_drive_folder']['title']}`",
        "- 当前判断：每轮迭代后的长期保存数据已经能自动汇总到统一同步包，但还不能直接写入 Google Drive。",
    ]
    if missing_preview:
        lines.append("- 仍需恢复的代表性历史文件：")
        for item in missing_preview:
            lines.append(f"  - `{item}`")
    return "\n".join(lines)


def main() -> None:
    config = load_config()
    stamp = utc_now().strftime("%Y-%m-%dT%H-%M-%SZ")
    date_stamp = utc_now().strftime("%Y-%m-%d")
    output_root = Path(config["output_root"])
    ensure_dir(output_root)

    rows = collect_rows(config, date_stamp)
    if not rows:
        raise RuntimeError("No archive rows were collected.")

    manifest_latest = output_root / "sc-don-drive-sync-manifest-latest.csv"
    manifest_dated = output_root / f"sc-don-drive-sync-manifest-{date_stamp}.csv"
    status_json = output_root / "sc-don-drive-sync-status.json"
    summary_md = output_root / "sc-don-drive-sync-summary.md"

    write_csv(rows, manifest_latest)
    write_csv(rows, manifest_dated)

    summary = summarise_rows(rows)
    payload = {
        "project": config["project_name"],
        "updated_at_utc": stamp,
        "manifest_latest": str(manifest_latest),
        "manifest_dated": str(manifest_dated),
        "target_drive_folder": config["target_drive_folder"],
        "drive_ledgers": config["drive_ledgers"],
        "summary": summary,
        "cloud_write_status": "blocked-no-write-endpoint",
    }
    status_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    summary_md.write_text(
        "\n".join(
            [
                "# Drive Sync Summary",
                "",
                f"- updated_at_utc: `{stamp}`",
                f"- local_ready_count: `{summary['local_ready_count']}`",
                f"- missing_count: `{summary['missing_count']}`",
                f"- manifest_latest: `{manifest_latest}`",
                f"- status_json: `{status_json}`",
                f"- target_drive_folder: `{config['target_drive_folder']['title']}`",
                "- cloud_write_status: blocked-no-write-endpoint",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    memory_root = Path(config["memory_root"])
    update_managed_block(
        memory_root / "drive-index.md",
        render_drive_index_block(config, summary, manifest_latest, status_json, stamp),
    )
    update_managed_block(
        memory_root / "archive-checklist.md",
        render_archive_block(config, summary, manifest_latest, stamp),
    )
    update_managed_block(
        memory_root / "iteration-log.md",
        render_iteration_block(config, summary, manifest_latest, stamp),
    )


if __name__ == "__main__":
    main()
