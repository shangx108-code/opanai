from __future__ import annotations

import importlib
import platform
from datetime import UTC, datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOG_PATH = PROJECT_ROOT / "logs" / "runtime-check-latest.md"
OPTIONAL_MODULES = ["numpy", "scipy", "matplotlib", "pandas", "kwant", "sympy"]


def module_status(name: str) -> tuple[str, str]:
    try:
        module = importlib.import_module(name)
    except Exception as exc:  # pragma: no cover - diagnostic only
        return "missing", str(exc)

    version = getattr(module, "__version__", "version-unknown")
    return "ok", version


def main() -> None:
    now = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    lines = [
        "# Runtime Check",
        "",
        f"- Timestamp: `{now}`",
        f"- Python: `{platform.python_version()}`",
        f"- Platform: `{platform.platform()}`",
        f"- Project root: `{PROJECT_ROOT}`",
        "",
        "## Module status",
        "",
        "| Module | Status | Detail |",
        "| --- | --- | --- |",
    ]

    for name in OPTIONAL_MODULES:
        status, detail = module_status(name)
        lines.append(f"| `{name}` | `{status}` | `{detail}` |")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `numpy/scipy/matplotlib/pandas` should be present for the first clean-limit calculation path.",
            "- `kwant` is optional at setup time but may be needed later for transport-oriented workflows.",
            "- Any missing package should be treated as an environment blocker only when the next concrete script requires it.",
            "",
        ]
    )

    LOG_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(LOG_PATH)


if __name__ == "__main__":
    main()
