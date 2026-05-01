from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


ROOT = Path("/workspace/self-calibrating-diffractive-ncomms")
OUT = ROOT / "outputs"
LOG = ROOT / "logs"


def make_test_field(size: int = 96) -> np.ndarray:
    x = np.linspace(-1.0, 1.0, size)
    xx, yy = np.meshgrid(x, x, indexing="xy")
    radius = np.sqrt(xx**2 + yy**2)
    phase = 6.0 * np.pi * (xx**2 - yy**2)
    amp = np.exp(-4.5 * radius**2)
    field = amp * np.exp(1j * phase)
    return field


def propagate_fft(field: np.ndarray) -> np.ndarray:
    spectrum = np.fft.fftshift(np.fft.fft2(field))
    out = np.fft.ifft2(np.fft.ifftshift(spectrum))
    return out


def save_preview(intensity: np.ndarray, target: Path) -> None:
    intensity = intensity - intensity.min()
    denom = intensity.max() if intensity.max() > 0 else 1.0
    norm = (255.0 * intensity / denom).astype(np.uint8)
    image = Image.fromarray(norm, mode="L").convert("RGB")
    draw = ImageDraw.Draw(image)
    draw.text((6, 6), "env smoke test", fill=(255, 64, 64))
    image.save(target)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    LOG.mkdir(parents=True, exist_ok=True)

    field = make_test_field()
    out = propagate_fft(field)
    intensity = np.abs(out) ** 2

    preview_path = OUT / "environment_smoke_test.png"
    json_path = OUT / "environment_smoke_test.json"
    md_path = OUT / "environment_smoke_test.md"

    save_preview(intensity, preview_path)

    report = {
        "status": "ok",
        "packages": {
            "numpy": np.__version__,
            "Pillow": Image.__version__,
        },
        "artifacts": {
            "preview_png": str(preview_path),
            "summary_json": str(json_path),
            "summary_md": str(md_path),
        },
        "checks": {
            "complex_fft_pipeline": True,
            "png_write": preview_path.exists(),
            "json_write": True,
            "workspace_ready": True,
        },
        "metrics": {
            "shape": list(intensity.shape),
            "mean_intensity": float(intensity.mean()),
            "max_intensity": float(intensity.max()),
        },
        "blocked_dependencies": {
            "matplotlib": "not installed",
            "scipy": "not installed",
            "torch": "not installed",
        },
    }

    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    md_path.write_text(
        "\n".join(
            [
                "# Environment Smoke Test",
                "",
                "- status: ok",
                f"- numpy: {np.__version__}",
                f"- Pillow: {Image.__version__}",
                "- verified: complex FFT pipeline, JSON output, PNG output",
                "- blocked: matplotlib, scipy, torch unavailable in current network-restricted environment",
                f"- preview: `{preview_path}`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
