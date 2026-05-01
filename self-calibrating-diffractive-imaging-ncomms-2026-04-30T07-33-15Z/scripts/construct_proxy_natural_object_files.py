#!/usr/bin/env python3
"""Construct project-local proxy natural-object files when external datasets are unavailable."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = PROJECT_ROOT / "data" / "natural_objects"
RESULT_ROOT = PROJECT_ROOT / "results" / "natural_objects"
IMAGE_SIZE = 128
IMAGES_PER_DATASET = 12


def normalize_to_uint8(arr: np.ndarray) -> np.ndarray:
    clipped = np.clip(arr, 0.0, 1.0)
    return np.uint8(np.round(clipped * 255.0))


def smooth_noise(rng: np.random.Generator, scale: float) -> np.ndarray:
    coarse = rng.normal(0.0, 1.0, size=(16, 16))
    image = Image.fromarray(normalize_to_uint8((coarse - coarse.min()) / (np.ptp(coarse) + 1.0e-8)), mode="L")
    image = image.resize((IMAGE_SIZE, IMAGE_SIZE), Image.Resampling.BICUBIC)
    image = image.filter(ImageFilter.GaussianBlur(radius=scale))
    return np.asarray(image, dtype=np.float64) / 255.0


def make_proxy_image(dataset_tag: str, image_index: int) -> tuple[np.ndarray, str]:
    rng = np.random.default_rng(1000 + image_index + (0 if dataset_tag == "imagenet" else 100))
    xx, yy = np.meshgrid(
        np.linspace(-1.0, 1.0, IMAGE_SIZE, endpoint=False),
        np.linspace(-1.0, 1.0, IMAGE_SIZE, endpoint=False),
    )
    base = 0.35 * smooth_noise(rng, scale=1.2) + 0.25 * smooth_noise(rng, scale=2.4)

    if dataset_tag == "imagenet":
        orientation = rng.uniform(0.0, np.pi)
        freq = rng.uniform(1.5, 4.0)
        stripe = 0.5 + 0.5 * np.sin(freq * (np.cos(orientation) * xx + np.sin(orientation) * yy) * np.pi)
        blobs = np.zeros_like(base)
        recipe = "layered texture + oriented structure"
        for _ in range(3):
            cx, cy = rng.uniform(-0.4, 0.4, size=2)
            radius = rng.uniform(0.12, 0.32)
            blobs += np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * radius**2))
        arr = 0.35 * base + 0.35 * stripe + 0.30 * blobs / (blobs.max() + 1.0e-8)
    else:
        horizon = 0.5 + 0.3 * np.tanh((yy + rng.uniform(-0.2, 0.2)) * rng.uniform(2.5, 4.0))
        canopy = np.zeros_like(base)
        recipe = "smooth scene gradient + clustered blobs"
        for _ in range(5):
            cx, cy = rng.uniform(-0.8, 0.8), rng.uniform(-0.6, 0.2)
            radius_x = rng.uniform(0.08, 0.24)
            radius_y = rng.uniform(0.05, 0.18)
            canopy += np.exp(-(((xx - cx) / radius_x) ** 2 + ((yy - cy) / radius_y) ** 2) / 2.0)
        arr = 0.30 * base + 0.35 * horizon + 0.35 * canopy / (canopy.max() + 1.0e-8)

    arr = (arr - arr.min()) / (np.ptp(arr) + 1.0e-8)
    image = Image.fromarray(normalize_to_uint8(arr), mode="L").filter(ImageFilter.GaussianBlur(radius=1.0))
    return np.asarray(image, dtype=np.float64) / 255.0, recipe


def main() -> int:
    RESULT_ROOT.mkdir(parents=True, exist_ok=True)
    manifests: list[dict[str, object]] = []
    datasets = {
        "imagenet": DATA_ROOT / "imagenet-1k-ilsvrc2012-validation",
        "coco": DATA_ROOT / "coco-2017-validation",
    }
    for dataset_tag, dataset_dir in datasets.items():
        dataset_dir.mkdir(parents=True, exist_ok=True)
        for image_index in range(IMAGES_PER_DATASET):
            arr, recipe = make_proxy_image(dataset_tag, image_index)
            filename = f"{dataset_tag}_proxy_{image_index:03d}.png"
            path = dataset_dir / filename
            Image.fromarray(normalize_to_uint8(arr), mode="L").save(path)
            manifests.append(
                {
                    "dataset": dataset_tag,
                    "filename": filename,
                    "path": str(path),
                    "image_size": IMAGE_SIZE,
                    "source_type": "project_local_proxy",
                    "generation_recipe": recipe,
                }
            )

    manifest_csv = RESULT_ROOT / "constructed_natural_object_manifest.csv"
    with manifest_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(manifests[0].keys()))
        writer.writeheader()
        writer.writerows(manifests)

    manifest_json = RESULT_ROOT / "constructed_natural_object_manifest.json"
    manifest_json.write_text(
        json.dumps(
            {
                "status": "proxy_dataset_constructed",
                "image_count": len(manifests),
                "datasets": list(datasets.keys()),
                "files": manifests,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "status": "proxy_dataset_constructed",
                "image_count": len(manifests),
                "manifest_csv": str(manifest_csv),
                "manifest_json": str(manifest_json),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
