from __future__ import annotations

import importlib
import platform
from pathlib import Path


MODULES = ["numpy", "pandas", "scipy", "matplotlib", "kwant", "tinyarray", "yaml"]


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    log_path = project_root / "logs" / "environment-check.md"
    lines = [
        "# Environment Check",
        "",
        f"- Python: `{platform.python_version()}`",
        f"- Platform: `{platform.platform()}`",
        "",
        "| Module | Status | Version or Error |",
        "|---|---|---|",
    ]

    for module_name in MODULES:
        try:
            module = importlib.import_module(module_name)
            version = getattr(module, "__version__", "n/a")
            lines.append(f"| `{module_name}` | available | `{version}` |")
        except Exception as exc:  # pragma: no cover - reporting only
            lines.append(f"| `{module_name}` | missing | `{type(exc).__name__}: {exc}` |")

    log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"environment report written to {log_path}")


if __name__ == "__main__":
    main()
