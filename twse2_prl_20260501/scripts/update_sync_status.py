#!/usr/bin/env python3

from __future__ import annotations

import subprocess
from datetime import datetime, timezone
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
REPO_DIR = PROJECT_DIR.parent
PROJECT_NAME = PROJECT_DIR.name
REMOTE_REF = "github-user/open-ai"
OUTPUT_FILE = PROJECT_DIR / "sync-status.md"
IGNORED_PROJECT_PATHS = {f"{PROJECT_NAME}/sync-status.md"}


def run_git(*args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", "-C", str(REPO_DIR), *args],
        check=check,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


def list_project_files() -> list[str]:
    entries = []
    for path in sorted(PROJECT_DIR.rglob("*")):
        if path.is_file():
            entries.append(path.relative_to(PROJECT_DIR).as_posix())
    return entries


def format_lines(lines: list[str]) -> str:
    if not lines:
        return "- none"
    return "\n".join(f"- `{line}`" for line in lines)


def filter_project_lines(lines: list[str]) -> list[str]:
    filtered = []
    for line in lines:
        if not line:
            continue
        path = line.split(maxsplit=1)[-1]
        if path in IGNORED_PROJECT_PATHS:
            continue
        filtered.append(line)
    return filtered


def main() -> None:
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    project_status = filter_project_lines(
        run_git("status", "--short", "--", PROJECT_NAME).splitlines()
    )
    remote_ref_exists = subprocess.run(
        ["git", "-C", str(REPO_DIR), "rev-parse", "--verify", REMOTE_REF],
        text=True,
        capture_output=True,
    ).returncode == 0

    diff_to_remote = filter_project_lines(
        run_git("diff", "--name-status", f"HEAD..{REMOTE_REF}", "--", PROJECT_NAME).splitlines()
        if remote_ref_exists
        else []
    )
    diff_from_remote = filter_project_lines(
        run_git("diff", "--name-status", f"{REMOTE_REF}..HEAD", "--", PROJECT_NAME).splitlines()
        if remote_ref_exists
        else []
    )

    project_in_sync = (
        remote_ref_exists
        and not project_status
        and not diff_to_remote
        and not diff_from_remote
    )

    repo_status = run_git("status", "--short")
    repo_untracked_outside_project = []
    for line in repo_status.splitlines():
        if not line.startswith("?? "):
            continue
        path = line[3:]
        if not path.startswith(f"{PROJECT_NAME}/"):
            repo_untracked_outside_project.append(path)

    lines = [
        "# Sync Status",
        "",
        f"Generated: `{generated_at}`",
        f"Project: `{PROJECT_NAME}`",
        f"Canonical path: `{PROJECT_DIR}`",
        "",
        "## Summary",
        "",
        f"- Project subtree synced to `{REMOTE_REF}`: `{'yes' if project_in_sync else 'no'}`",
        f"- Local project subtree clean: `{'yes' if not project_status else 'no'}`",
        f"- Remote tracking ref available: `{'yes' if remote_ref_exists else 'no'}`",
        f"- Audit file excluded from sync check: `yes`",
        "",
        "## Local Project Changes",
        "",
        format_lines(project_status),
        "",
        "## Remote Changes Missing Locally In Project Subtree",
        "",
        format_lines(diff_to_remote),
        "",
        "## Local Project Changes Not Yet In Remote Tracking Ref",
        "",
        format_lines(diff_from_remote),
        "",
        "## Untracked Files Outside This Project",
        "",
        format_lines(repo_untracked_outside_project),
        "",
        "## Project File Inventory",
        "",
        format_lines(list_project_files()),
        "",
        "## Update Rule",
        "",
        "- Refresh this file after each substantive turn that changes project data, scripts, results, notes, or manuscript assets.",
        "- Treat this file as the quick audit entry for whether `twse2_prl_20260501` is ready for later inspection from GitHub.",
    ]

    OUTPUT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
