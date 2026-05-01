from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


ROOT = Path("/workspace/self-calibrating-diffractive-ncomms")
OUT = ROOT / "outputs"
LOG = ROOT / "logs"
SIZE = 24
NUM_LAYERS = 2
TRAIN_STEPS = 18
REFERENCE_WEIGHT = 0.65
RNG = np.random.default_rng(7)


@dataclass
class Sample:
    name: str
    object_pattern: np.ndarray
    coeffs: np.ndarray


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    LOG.mkdir(parents=True, exist_ok=True)


def make_coords(size: int) -> tuple[np.ndarray, np.ndarray]:
    x = np.linspace(-1.0, 1.0, size)
    return np.meshgrid(x, x, indexing="xy")


XX, YY = make_coords(SIZE)
RADIUS = np.sqrt(XX**2 + YY**2)


def basis_stack() -> list[np.ndarray]:
    return [
        2.0 * RADIUS**2 - 1.0,
        XX**2 - YY**2,
        XX,
        YY,
    ]


BASIS = basis_stack()


def make_reference(kind: str = "good") -> np.ndarray:
    if kind == "good":
        ref = 0.55 + 0.20 * np.cos(2.5 * np.pi * XX) + 0.15 * np.sin(2.0 * np.pi * YY)
    else:
        ref = 0.50 + 0.22 * np.sin(3.0 * np.pi * XX + 0.4) - 0.18 * np.cos(2.2 * np.pi * YY)
    ref = np.clip(ref, 0.0, 1.0)
    return ref


GOOD_REFERENCE = make_reference("good")
WRONG_REFERENCE = make_reference("wrong")


def make_shape(name: str) -> np.ndarray:
    img = np.zeros((SIZE, SIZE), dtype=np.float64)
    c = SIZE // 2
    if name == "cross":
        img[c - 1 : c + 1, 4:-4] = 1.0
        img[4:-4, c - 1 : c + 1] = 1.0
    elif name == "diag":
        idx = np.arange(4, SIZE - 4)
        img[idx, idx] = 1.0
        img[idx, np.clip(idx + 1, 0, SIZE - 1)] = 0.7
    elif name == "box":
        img[6:18, 6:8] = 1.0
        img[6:18, 16:18] = 1.0
        img[6:8, 6:18] = 1.0
        img[16:18, 6:18] = 1.0
    elif name == "bars":
        img[5:19, 6:8] = 1.0
        img[5:19, 11:13] = 0.9
        img[5:19, 16:18] = 0.8
    elif name == "ring":
        img[(RADIUS > 0.34) & (RADIUS < 0.52)] = 1.0
    elif name == "chevron":
        for i in range(5, 17):
            img[i, abs(i - 11) + 6] = 1.0
            img[i, SIZE - abs(i - 11) - 7] = 1.0
    elif name == "disk":
        img[RADIUS < 0.42] = 1.0
    elif name == "two_spots":
        img[(XX + 0.35) ** 2 + (YY + 0.12) ** 2 < 0.06] = 1.0
        img[(XX - 0.28) ** 2 + (YY - 0.18) ** 2 < 0.05] = 0.9
    elif name == "frame":
        img[4:20, 4:5] = 1.0
        img[4:20, 19:20] = 1.0
        img[4:5, 4:20] = 1.0
        img[19:20, 4:20] = 1.0
        img[9:15, 9:15] = 0.7
    img = np.clip(img, 0.0, 1.0)
    return img


def normalize(img: np.ndarray) -> np.ndarray:
    vmax = float(np.max(img))
    if vmax <= 0.0:
        return img.copy()
    return img / vmax


def phase_from_coeffs(coeffs: np.ndarray) -> np.ndarray:
    phase = np.zeros((SIZE, SIZE), dtype=np.float64)
    for c, b in zip(coeffs, BASIS):
        phase += c * b
    return phase


def build_samples(names: list[str], coeff_scale: float, seed_offset: int) -> list[Sample]:
    local = np.random.default_rng(100 + seed_offset)
    samples: list[Sample] = []
    for name in names:
        coeffs = local.uniform(-coeff_scale, coeff_scale, size=len(BASIS))
        samples.append(Sample(name=name, object_pattern=normalize(make_shape(name)), coeffs=coeffs))
    return samples


TRAIN_SAMPLES = build_samples(["cross", "diag", "box", "bars", "ring", "chevron"], 0.65, 0)
TEST_SAMPLES = build_samples(["disk", "two_spots", "frame"], 1.15, 1)


def fresnel_kernel(size: int) -> np.ndarray:
    fx = np.fft.fftfreq(size)
    fy = np.fft.fftfreq(size)
    fxx, fyy = np.meshgrid(fx, fy, indexing="xy")
    return np.exp(-1j * 3.8 * np.pi * (fxx**2 + fyy**2))


KERNEL = fresnel_kernel(SIZE)


def propagate(field: np.ndarray) -> np.ndarray:
    return np.fft.ifft2(np.fft.fft2(field) * KERNEL)


def processor_forward(input_amp: np.ndarray, input_phase: np.ndarray, masks: np.ndarray) -> np.ndarray:
    field = np.sqrt(np.clip(input_amp, 0.0, None)) * np.exp(1j * input_phase)
    for idx in range(masks.shape[0]):
        field = propagate(field)
        field = field * np.exp(1j * masks[idx])
    field = propagate(field)
    intensity = np.abs(field) ** 2
    return normalize(intensity)


def make_input(sample: Sample, condition: str) -> tuple[np.ndarray, np.ndarray]:
    object_amp = sample.object_pattern
    object_phase = phase_from_coeffs(sample.coeffs)
    if condition == "ordinary":
        ref_amp = np.zeros_like(object_amp)
        ref_phase = np.zeros_like(object_phase)
    elif condition == "common_path":
        ref_amp = GOOD_REFERENCE
        ref_phase = object_phase
    elif condition == "noncommon_path":
        ref_amp = GOOD_REFERENCE
        ref_phase = phase_from_coeffs(sample.coeffs[::-1] * np.array([1.1, -0.9, 1.0, -1.0]))
    elif condition == "wrong_reference":
        ref_amp = WRONG_REFERENCE
        ref_phase = object_phase
    else:
        raise ValueError(condition)
    amp = np.clip(object_amp + REFERENCE_WEIGHT * ref_amp, 0.0, 1.7)
    phase = object_phase + 0.35 * ref_phase
    return amp, phase


def mse(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.mean((a - b) ** 2))


def psnr(a: np.ndarray, b: np.ndarray) -> float:
    err = max(mse(a, b), 1e-12)
    return float(10.0 * np.log10(1.0 / err))


def objective(masks: np.ndarray, samples: list[Sample], condition: str) -> float:
    losses = []
    for sample in samples:
        amp, phase = make_input(sample, condition)
        pred = processor_forward(amp, phase, masks)
        losses.append(mse(pred, sample.object_pattern))
    return float(np.mean(losses))


def train_condition(condition: str) -> tuple[np.ndarray, list[dict[str, float]]]:
    masks = RNG.uniform(-0.15, 0.15, size=(NUM_LAYERS, SIZE, SIZE))
    history: list[dict[str, float]] = []
    best_masks = masks.copy()
    best_loss = objective(best_masks, TRAIN_SAMPLES, condition)
    for step in range(TRAIN_STEPS):
        delta = RNG.choice([-1.0, 1.0], size=masks.shape)
        ck = 0.35 / ((step + 1) ** 0.22)
        ak = 0.55 / ((step + 2) ** 0.55)
        plus_loss = objective(masks + ck * delta, TRAIN_SAMPLES, condition)
        minus_loss = objective(masks - ck * delta, TRAIN_SAMPLES, condition)
        grad = (plus_loss - minus_loss) / (2.0 * ck) * delta
        masks = np.mod(masks - ak * grad + np.pi, 2.0 * np.pi) - np.pi
        train_loss = objective(masks, TRAIN_SAMPLES, condition)
        if train_loss < best_loss:
            best_loss = train_loss
            best_masks = masks.copy()
        history.append({"step": step + 1, "train_mse": train_loss})
    return best_masks, history


def to_uint8(img: np.ndarray) -> np.ndarray:
    arr = normalize(img)
    return np.clip(np.round(255.0 * arr), 0, 255).astype(np.uint8)


def tile_images(rows: list[list[np.ndarray]], labels: list[str], target: Path) -> None:
    h, w = rows[0][0].shape
    canvas = Image.new("RGB", (w * len(rows[0]), h * len(rows) + 20), (245, 245, 245))
    draw = ImageDraw.Draw(canvas)
    for idx, label in enumerate(labels):
        draw.text((idx * w + 4, 2), label, fill=(20, 20, 20))
    for r, row in enumerate(rows):
        for c, img in enumerate(row):
            tile = Image.fromarray(to_uint8(img), mode="L").convert("RGB")
            canvas.paste(tile, (c * w, 20 + r * h))
    canvas.save(target)


def write_csv(rows: list[dict[str, object]], target: Path) -> None:
    fieldnames = list(rows[0].keys())
    with target.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    ensure_dirs()
    conditions = ["ordinary", "common_path", "noncommon_path", "wrong_reference"]
    trained: dict[str, np.ndarray] = {}
    train_histories: dict[str, list[dict[str, float]]] = {}
    for condition in conditions:
        masks, history = train_condition(condition)
        trained[condition] = masks
        train_histories[condition] = history

    metrics_rows: list[dict[str, object]] = []
    preview_rows: list[list[np.ndarray]] = []
    labels = ["target", "ordinary", "common", "noncommon", "wrongref"]
    condition_to_column = {
        "ordinary": 1,
        "common_path": 2,
        "noncommon_path": 3,
        "wrong_reference": 4,
    }

    aggregate: dict[str, list[float]] = {c: [] for c in conditions}
    preview_targets = TEST_SAMPLES[:3]
    for sample in preview_targets:
        row = [sample.object_pattern] + [np.zeros_like(sample.object_pattern) for _ in range(4)]
        for condition in conditions:
            amp, phase = make_input(sample, condition)
            pred = processor_forward(amp, phase, trained[condition])
            row[condition_to_column[condition]] = pred
        preview_rows.append(row)

    for split_name, samples in [("train", TRAIN_SAMPLES), ("ood", TEST_SAMPLES)]:
        for sample in samples:
            for condition in conditions:
                amp, phase = make_input(sample, condition)
                pred = processor_forward(amp, phase, trained[condition])
                err = mse(pred, sample.object_pattern)
                score = psnr(pred, sample.object_pattern)
                aggregate[condition].append(score if split_name == "ood" else np.nan)
                metrics_rows.append(
                    {
                        "split": split_name,
                        "sample": sample.name,
                        "condition": condition,
                        "psnr_db": round(score, 6),
                        "mse": round(err, 8),
                    }
                )

    summary_rows: list[dict[str, object]] = []
    for condition in conditions:
        ood_scores = [row["psnr_db"] for row in metrics_rows if row["condition"] == condition and row["split"] == "ood"]
        ood_mses = [row["mse"] for row in metrics_rows if row["condition"] == condition and row["split"] == "ood"]
        summary_rows.append(
            {
                "condition": condition,
                "ood_mean_psnr_db": round(float(np.mean(ood_scores)), 6),
                "ood_mean_mse": round(float(np.mean(ood_mses)), 8),
                "train_final_mse": round(train_histories[condition][-1]["train_mse"], 8),
            }
        )

    summary_by_condition = {row["condition"]: row for row in summary_rows}
    deltas = {
        "common_minus_ordinary_db": round(
            summary_by_condition["common_path"]["ood_mean_psnr_db"] - summary_by_condition["ordinary"]["ood_mean_psnr_db"], 6
        ),
        "common_minus_noncommon_db": round(
            summary_by_condition["common_path"]["ood_mean_psnr_db"] - summary_by_condition["noncommon_path"]["ood_mean_psnr_db"], 6
        ),
        "common_minus_wrongref_db": round(
            summary_by_condition["common_path"]["ood_mean_psnr_db"] - summary_by_condition["wrong_reference"]["ood_mean_psnr_db"], 6
        ),
    }

    metrics_path = OUT / "round6_numpy_passive_d2nn_metrics.csv"
    summary_json_path = OUT / "round6_numpy_passive_d2nn_summary.json"
    summary_md_path = OUT / "round6_numpy_passive_d2nn_summary.md"
    panel_path = OUT / "round6_numpy_passive_d2nn_panel.png"
    history_json_path = OUT / "round6_numpy_passive_d2nn_training_history.json"

    write_csv(metrics_rows, metrics_path)
    tile_images(preview_rows, labels, panel_path)

    payload = {
        "status": "ok",
        "environment": {
            "numpy": np.__version__,
            "uses_pillow": True,
            "num_layers": NUM_LAYERS,
            "train_steps": TRAIN_STEPS,
            "grid_size": SIZE,
        },
        "summary_rows": summary_rows,
        "deltas_db": deltas,
        "artifacts": {
            "metrics_csv": str(metrics_path),
            "summary_md": str(summary_md_path),
            "summary_json": str(summary_json_path),
            "panel_png": str(panel_path),
            "training_history_json": str(history_json_path),
        },
        "note": "This is a minimal numpy-based passive D2NN rebuild intended to restore a reproducible data pipeline, not a submission-grade final result.",
    }
    summary_json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    history_json_path.write_text(json.dumps(train_histories, indent=2), encoding="utf-8")

    lines = [
        "# Round 6 NumPy Passive D2NN",
        "",
        "- status: ok",
        f"- ordinary OOD mean PSNR: {summary_by_condition['ordinary']['ood_mean_psnr_db']:.3f} dB",
        f"- common-path OOD mean PSNR: {summary_by_condition['common_path']['ood_mean_psnr_db']:.3f} dB",
        f"- non-common-path OOD mean PSNR: {summary_by_condition['noncommon_path']['ood_mean_psnr_db']:.3f} dB",
        f"- wrong-reference OOD mean PSNR: {summary_by_condition['wrong_reference']['ood_mean_psnr_db']:.3f} dB",
        f"- common minus ordinary: {deltas['common_minus_ordinary_db']:+.3f} dB",
        f"- common minus noncommon: {deltas['common_minus_noncommon_db']:+.3f} dB",
        f"- common minus wrongref: {deltas['common_minus_wrongref_db']:+.3f} dB",
        "- interpretation: minimal rebuild for reproducible data completion under current numpy-only environment",
    ]
    summary_md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
