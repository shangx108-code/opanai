from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont


SQRT3 = float(np.sqrt(3.0))
SQRT7 = float(np.sqrt(7.0))
OMEGA = np.exp(1j * 2.0 * np.pi / 3.0)
DEFAULT_SOURCE_FILE = Path("/workspace/tmp/ws2/41467_2025_64519_MOESM3_ESM.xlsx")
DEFAULT_FALLBACK_FILE = Path("/workspace/memory/twse2-andreev-prl/data/track1-2026-04-29/band_comparison.csv")


def apply_phase_pattern(amplitude: complex, step: int, pattern: str) -> complex:
    if pattern == "const":
        return amplitude
    if pattern == "cyc":
        return amplitude * (OMEGA**step)
    if pattern == "anti":
        return amplitude * (np.conj(OMEGA) ** step)
    raise ValueError(f"Unsupported phase pattern: {pattern}")


def default_mixed_star_config() -> dict[str, object]:
    return {
        "ac1_pattern": "cyc",
        "bc1_pattern": "cyc",
        "ac2_pattern": "cyc",
        "bc2_pattern": "cyc",
        "ac7_first_pattern": "cyc",
        "ac7_second_pattern": "cyc",
        "ac7_second_conjugated": True,
        "bc7_first_pattern": "cyc",
        "bc7_second_pattern": "cyc",
        "bc7_second_conjugated": True,
    }


def build_hops(mixed_star_config: dict[str, object] | None = None) -> dict[tuple[str, str, tuple[float, float]], complex]:
    mixed_star_config = {**default_mixed_star_config(), **(mixed_star_config or {})}
    params = {
        ("A", "A", 0.0): complex(-15.26, 0.0),
        ("B", "B", 0.0): complex(-15.26, 0.0),
        ("C", "C", 0.0): complex(-42.89, 0.0),
        ("B", "B", SQRT3): 5.16 * np.exp(1j * 0.618 * np.pi),
        ("C", "C", SQRT3): complex(2.76, 0.0),
        ("B", "B", 3.0): complex(-0.31, 0.0),
        ("C", "C", 3.0): complex(0.43, 0.0),
        ("A", "B", 1.0): complex(-4.99, 0.0),
        ("B", "C", 1.0): complex(7.12, 0.0),
        ("A", "B", 2.0): complex(0.70, 0.0),
        ("A", "C", 2.0): complex(1.15, 0.0),
        ("A", "B", SQRT7): complex(0.78, 0.0),
        ("A", "C", SQRT7): 3.01 * np.exp(1j * 0.965 * np.pi),
    }

    stars = {
        ("A", "A", SQRT3): [
            np.array([0.0, -SQRT3]),
            np.array([1.5, SQRT3 / 2.0]),
            np.array([-1.5, SQRT3 / 2.0]),
            np.array([0.0, SQRT3]),
            np.array([-1.5, -SQRT3 / 2.0]),
            np.array([1.5, -SQRT3 / 2.0]),
        ],
        ("B", "B", SQRT3): [
            np.array([0.0, -SQRT3]),
            np.array([1.5, SQRT3 / 2.0]),
            np.array([-1.5, SQRT3 / 2.0]),
            np.array([0.0, SQRT3]),
            np.array([-1.5, -SQRT3 / 2.0]),
            np.array([1.5, -SQRT3 / 2.0]),
        ],
        ("C", "C", SQRT3): [
            np.array([0.0, -SQRT3]),
            np.array([1.5, SQRT3 / 2.0]),
            np.array([-1.5, SQRT3 / 2.0]),
            np.array([0.0, SQRT3]),
            np.array([-1.5, -SQRT3 / 2.0]),
            np.array([1.5, -SQRT3 / 2.0]),
        ],
        ("A", "A", 3.0): [
            np.array([-3.0, 0.0]),
            np.array([1.5, -1.5 * SQRT3]),
            np.array([1.5, 1.5 * SQRT3]),
            np.array([3.0, 0.0]),
            np.array([-1.5, 1.5 * SQRT3]),
            np.array([-1.5, -1.5 * SQRT3]),
        ],
        ("B", "B", 3.0): [
            np.array([-3.0, 0.0]),
            np.array([1.5, -1.5 * SQRT3]),
            np.array([1.5, 1.5 * SQRT3]),
            np.array([3.0, 0.0]),
            np.array([-1.5, 1.5 * SQRT3]),
            np.array([-1.5, -1.5 * SQRT3]),
        ],
        ("C", "C", 3.0): [
            np.array([-3.0, 0.0]),
            np.array([1.5, -1.5 * SQRT3]),
            np.array([1.5, 1.5 * SQRT3]),
            np.array([3.0, 0.0]),
            np.array([-1.5, 1.5 * SQRT3]),
            np.array([-1.5, -1.5 * SQRT3]),
        ],
        ("A", "B", 1.0): [
            np.array([-1.0, 0.0]),
            np.array([0.5, -SQRT3 / 2.0]),
            np.array([0.5, SQRT3 / 2.0]),
        ],
        ("A", "B", 2.0): [
            np.array([2.0, 0.0]),
            np.array([-1.0, SQRT3]),
            np.array([-1.0, -SQRT3]),
        ],
        ("A", "B", SQRT7): [
            np.array([-2.5, -SQRT3 / 2.0]),
            np.array([2.0, -SQRT3]),
            np.array([0.5, 1.5 * SQRT3]),
            np.array([2.5, SQRT3 / 2.0]),
            np.array([-2.0, SQRT3]),
            np.array([-0.5, -1.5 * SQRT3]),
        ],
        ("A", "C", 1.0): [
            np.array([1.0, 0.0]),
            np.array([-0.5, SQRT3 / 2.0]),
            np.array([-0.5, -SQRT3 / 2.0]),
        ],
        ("B", "C", 1.0): [
            np.array([-1.0, 0.0]),
            np.array([0.5, -SQRT3 / 2.0]),
            np.array([0.5, SQRT3 / 2.0]),
        ],
        ("A", "C", 2.0): [
            np.array([1.0, -SQRT3]),
            np.array([1.0, SQRT3]),
            np.array([-2.0, 0.0]),
        ],
        ("B", "C", 2.0): [
            np.array([2.0, 0.0]),
            np.array([-1.0, SQRT3]),
            np.array([-1.0, -SQRT3]),
        ],
        ("A", "C", SQRT7): [
            np.array([-0.5, -1.5 * SQRT3]),
            np.array([2.5, -SQRT3 / 2.0]),
            np.array([-2.0, SQRT3]),
            np.array([0.5, 1.5 * SQRT3]),
            np.array([-2.5, SQRT3 / 2.0]),
            np.array([2.0, -SQRT3]),
        ],
        ("B", "C", SQRT7): [
            np.array([2.0, -SQRT3]),
            np.array([-2.5, -SQRT3 / 2.0]),
            np.array([0.5, 1.5 * SQRT3]),
            np.array([-2.0, SQRT3]),
            np.array([2.5, SQRT3 / 2.0]),
            np.array([-0.5, -1.5 * SQRT3]),
        ],
    }

    hops: dict[tuple[str, str, tuple[float, float]], complex] = {}

    for key in [("A", "A", 0.0), ("B", "B", 0.0), ("C", "C", 0.0)]:
        alpha, beta, _ = key
        hops[(alpha, beta, (0.0, 0.0))] = params[key]

    for key in [("C", "C", SQRT3), ("C", "C", 3.0), ("B", "B", SQRT3), ("B", "B", 3.0)]:
        alpha, beta, _ = key
        for vec in stars[key]:
            hops[(alpha, beta, tuple(np.round(vec, 6)))] = params[key]

    for distance in [SQRT3, 3.0]:
        amplitude = np.conj(params[("B", "B", distance)])
        for vec in stars[("A", "A", distance)]:
            hops[("A", "A", tuple(np.round(vec, 6)))] = amplitude

    for key in [("A", "B", 1.0), ("A", "B", 2.0), ("A", "B", SQRT7)]:
        amplitude = params[key]
        for vec in stars[key]:
            hops[("A", "B", tuple(np.round(vec, 6)))] = amplitude
            hops[("B", "A", tuple(np.round(-vec, 6)))] = np.conj(amplitude)

    def add_mixed_star(
        key: tuple[str, str, float],
        amplitude: complex,
        first_pattern: str = "cyc",
        second_pattern: str = "cyc",
        second_orbit_conjugated: bool = False,
    ) -> None:
        alpha, beta, _ = key
        vecs = stars[key]
        first_orbit = vecs if len(vecs) == 3 else vecs[:3]
        for step, vec in enumerate(first_orbit):
            current = apply_phase_pattern(amplitude, step, first_pattern)
            hops[(alpha, beta, tuple(np.round(vec, 6)))] = current
            hops[(beta, alpha, tuple(np.round(-vec, 6)))] = np.conj(current)
        if len(vecs) == 6:
            second_base = np.conj(amplitude) if second_orbit_conjugated else amplitude
            for step, vec in enumerate(vecs[3:]):
                current = apply_phase_pattern(second_base, step, second_pattern)
                hops[(alpha, beta, tuple(np.round(vec, 6)))] = current
                hops[(beta, alpha, tuple(np.round(-vec, 6)))] = np.conj(current)

    add_mixed_star(("A", "C", 1.0), params[("B", "C", 1.0)], first_pattern=str(mixed_star_config["ac1_pattern"]))
    add_mixed_star(("B", "C", 1.0), params[("B", "C", 1.0)], first_pattern=str(mixed_star_config["bc1_pattern"]))
    add_mixed_star(("A", "C", 2.0), params[("A", "C", 2.0)], first_pattern=str(mixed_star_config["ac2_pattern"]))
    add_mixed_star(("B", "C", 2.0), params[("A", "C", 2.0)], first_pattern=str(mixed_star_config["bc2_pattern"]))
    add_mixed_star(
        ("A", "C", SQRT7),
        params[("A", "C", SQRT7)],
        first_pattern=str(mixed_star_config["ac7_first_pattern"]),
        second_pattern=str(mixed_star_config["ac7_second_pattern"]),
        second_orbit_conjugated=bool(mixed_star_config["ac7_second_conjugated"]),
    )
    add_mixed_star(
        ("B", "C", SQRT7),
        params[("A", "C", SQRT7)],
        first_pattern=str(mixed_star_config["bc7_first_pattern"]),
        second_pattern=str(mixed_star_config["bc7_second_pattern"]),
        second_orbit_conjugated=bool(mixed_star_config["bc7_second_conjugated"]),
    )
    return hops


def build_hamiltonian(k: np.ndarray, hops: dict[tuple[str, str, tuple[float, float]], complex]) -> np.ndarray:
    idx = {"A": 0, "B": 1, "C": 2}
    matrix = np.zeros((3, 3), dtype=complex)
    for (alpha, beta, vec), amplitude in hops.items():
        matrix[idx[alpha], idx[beta]] += amplitude * np.exp(1j * np.dot(k, np.array(vec)))
    return matrix


def reciprocal_points() -> dict[str, np.ndarray]:
    a1 = np.array([1.5, SQRT3 / 2.0])
    a2 = np.array([0.0, SQRT3])
    basis = np.column_stack([a1, a2])
    reciprocal = 2.0 * np.pi * np.linalg.inv(basis).T
    b1, b2 = reciprocal[:, 0], reciprocal[:, 1]
    return {
        "Gamma": np.array([0.0, 0.0]),
        "K_2b1+b2": (2.0 * b1 + b2) / 3.0,
        "K_b1+2b2": (b1 + 2.0 * b2) / 3.0,
        "K_-b1+b2": (-b1 + b2) / 3.0,
        "K_-2b1-b2": (-2.0 * b1 - b2) / 3.0,
        "K_-b1-2b2": (-b1 - 2.0 * b2) / 3.0,
        "K_b1-b2": (b1 - b2) / 3.0,
        "M_b1": b1 / 2.0,
        "M_b2": b2 / 2.0,
        "M_b1+b2": (b1 + b2) / 2.0,
    }


def build_path(
    mode: str = "exclusive_150",
    k_b_label: str = "K_2b1+b2",
    m_label: str = "M_b1+b2",
    k_t_label: str = "K_b1+2b2",
) -> tuple[np.ndarray, list[int], list[str], dict[str, int]]:
    points = reciprocal_points()
    gamma = points["Gamma"]
    k_b = points[k_b_label]
    m = points[m_label]
    k_t = points[k_t_label]

    path = []
    if mode == "exclusive_150":
        for start, end in [(gamma, k_b), (k_b, m), (m, k_t), (k_t, gamma)]:
            for t in np.linspace(0.0, 1.0, 150, endpoint=False):
                path.append((1.0 - t) * start + t * end)
        tick_idx = [0, 150, 300, 450, 599]
        labels = [r"$\Gamma$", r"$K^B$", r"$M$", r"$K^T$", r"$\Gamma$"]
        high_symmetry_idx = {"Gamma_start": 0, "K_B": 150, "M": 300, "K_T": 450, "Gamma_end": 599}
    elif mode == "duplicated_150":
        for start, end in [(gamma, k_b), (k_b, m), (m, k_t), (k_t, gamma)]:
            for t in np.linspace(0.0, 1.0, 150, endpoint=True):
                path.append((1.0 - t) * start + t * end)
        tick_idx = [0, 149, 299, 449, 599]
        labels = [r"$\Gamma$", r"$K^B$", r"$M$", r"$K^T$", r"$\Gamma$"]
        high_symmetry_idx = {
            "Gamma_start": 0,
            "K_B_entry": 149,
            "K_B_exit": 150,
            "M_entry": 299,
            "M_exit": 300,
            "K_T_entry": 449,
            "K_T_exit": 450,
            "Gamma_end": 599,
        }
    else:
        raise ValueError(f"Unsupported path mode: {mode}")
    return np.asarray(path), tick_idx, labels, high_symmetry_idx


def load_source(source_file: Path = DEFAULT_SOURCE_FILE, fallback_file: Path = DEFAULT_FALLBACK_FILE) -> tuple[pd.DataFrame, str]:
    if source_file.exists():
        df = pd.read_excel(source_file, sheet_name="Fig1c_EnergyBand")[["E_tb_1", "E_tb_2", "E_tb_3"]].copy()
        return df, f"workbook:{source_file}"
    if fallback_file.exists():
        df = pd.read_csv(fallback_file)[["E_tb_1_source", "E_tb_2_source", "E_tb_3_source"]].copy()
        df.columns = ["E_tb_1", "E_tb_2", "E_tb_3"]
        return df, f"fallback_csv:{fallback_file}"
    raise FileNotFoundError(
        "Neither the original workbook nor the mirrored fallback source table is available. "
        f"Missing: {source_file} and {fallback_file}"
    )


def evaluate_candidate(
    path_mode: str,
    k_b_label: str,
    m_label: str,
    k_t_label: str,
    source: pd.DataFrame | None = None,
    hops: dict[tuple[str, str, tuple[float, float]], complex] | None = None,
    mixed_star_config: dict[str, object] | None = None,
) -> dict[str, object]:
    if source is None:
        source, source_origin = load_source()
    else:
        source_origin = "caller_provided"
    if hops is None:
        hops = build_hops(mixed_star_config=mixed_star_config)

    path, tick_idx, tick_labels, high_symmetry_idx = build_path(path_mode, k_b_label, m_label, k_t_label)
    bands = np.asarray([np.linalg.eigvalsh(build_hamiltonian(k, hops))[::-1] for k in path])
    source_values = source.to_numpy()
    rmse_per_band = np.sqrt(np.mean((bands - source_values) ** 2, axis=0))
    overall_rmse = float(np.sqrt(np.mean((bands - source_values) ** 2)))
    rowwise_sum_rmse = float(np.sqrt(np.mean(np.sum((bands - source_values) ** 2, axis=1))))

    high_symmetry_rows = []
    for label, point_index in high_symmetry_idx.items():
        src_row = source_values[point_index]
        rec_row = bands[point_index]
        high_symmetry_rows.append(
            {
                "label": label,
                "point_index": point_index,
                "source_1": src_row[0],
                "source_2": src_row[1],
                "source_3": src_row[2],
                "reconstructed_1": rec_row[0],
                "reconstructed_2": rec_row[1],
                "reconstructed_3": rec_row[2],
                "delta_1": rec_row[0] - src_row[0],
                "delta_2": rec_row[1] - src_row[1],
                "delta_3": rec_row[2] - src_row[2],
            }
        )
    residuals = pd.DataFrame(high_symmetry_rows)

    def slice_rmse(indices: list[int]) -> float:
        return float(np.sqrt(np.mean((bands[indices] - source_values[indices]) ** 2)))

    return {
        "path_mode": path_mode,
        "k_b_label": k_b_label,
        "m_label": m_label,
        "k_t_label": k_t_label,
        "source_origin": source_origin,
        "mixed_star_config": {**default_mixed_star_config(), **(mixed_star_config or {})},
        "path": path,
        "tick_idx": tick_idx,
        "tick_labels": tick_labels,
        "high_symmetry_idx": high_symmetry_idx,
        "bands": bands,
        "hops": hops,
        "source": source,
        "rmse_per_band": rmse_per_band,
        "overall_rmse": overall_rmse,
        "rowwise_sum_rmse": rowwise_sum_rmse,
        "high_symmetry_residuals": residuals,
        "gamma_end_max_abs_delta": float(np.max(np.abs(bands[599] - source_values[599]))),
        "k_b_rmse_window": slice_rmse([149, 150]),
        "m_rmse_window": slice_rmse([299, 300]),
        "k_t_rmse_window": slice_rmse([449, 450]),
    }


def render_line_plot(
    output_path: Path,
    source: np.ndarray,
    reconstructed: np.ndarray,
    tick_idx: list[int],
    tick_labels: list[str],
    overall_rmse: float,
    title_suffix: str,
) -> None:
    width, height = 1400, 900
    margin_left, margin_right = 110, 50
    margin_top, margin_bottom = 80, 90
    plot_w = width - margin_left - margin_right
    plot_h = height - margin_top - margin_bottom
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    all_vals = np.concatenate([source.reshape(-1), reconstructed.reshape(-1)])
    y_min = float(np.min(all_vals)) - 3.0
    y_max = float(np.max(all_vals)) + 3.0
    x_max = source.shape[0] - 1

    def xpix(i: int) -> float:
        return margin_left + plot_w * i / x_max

    def ypix(v: float) -> float:
        return margin_top + plot_h * (y_max - v) / (y_max - y_min)

    draw.rectangle([margin_left, margin_top, margin_left + plot_w, margin_top + plot_h], outline="#444444", width=2)
    for tick in tick_idx:
        x = xpix(min(tick, x_max))
        draw.line([(x, margin_top), (x, margin_top + plot_h)], fill="#cccccc", width=1)
    for frac in np.linspace(0.0, 1.0, 6):
        value = y_min + frac * (y_max - y_min)
        y = ypix(value)
        draw.line([(margin_left, y), (margin_left + plot_w, y)], fill="#efefef", width=1)
        draw.text((15, y - 6), f"{value:6.1f}", fill="black", font=font)

    colors = [(214, 39, 40), (44, 160, 44), (31, 119, 180)]
    for band in range(3):
        source_pts = [(xpix(i), ypix(v)) for i, v in enumerate(source[:, band])]
        rec_pts = [(xpix(i), ypix(v)) for i, v in enumerate(reconstructed[:, band])]
        draw.line(source_pts, fill=colors[band], width=3)
        draw.line(rec_pts, fill=tuple(max(0, c - 90) for c in colors[band]), width=2)

    title = f"Tuo TB reconstruction check  |  overall RMSE = {overall_rmse:.2f} meV"
    draw.text((margin_left, 20), title, fill="black", font=font)
    draw.text((margin_left, 40), title_suffix, fill="black", font=font)
    for tick, label in zip(tick_idx, tick_labels):
        x = xpix(min(tick, x_max))
        draw.text((x - 12, margin_top + plot_h + 18), label, fill="black", font=font)
    draw.text((width // 2 - 30, height - 30), "k-path", fill="black", font=font)
    draw.text((10, 20), "E (meV)", fill="black", font=font)
    draw.text((margin_left + 20, margin_top + 60), "bright = source, dark = reconstructed", fill="black", font=font)
    img.save(output_path)


def write_candidate_package(result: dict[str, object], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    hops = result.get("hops") or build_hops()

    with (out_dir / "reconstructed_hopping_table.csv").open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["alpha", "beta", "dx", "dy", "real_meV", "imag_meV"])
        for (alpha, beta, vec), amplitude in sorted(hops.items()):
            writer.writerow([alpha, beta, vec[0], vec[1], amplitude.real, amplitude.imag])

    source = result["source"]
    bands = result["bands"]
    comparison = pd.DataFrame(
        {
            "point_index": np.arange(len(bands)),
            "E_tb_1_source": source["E_tb_1"].to_numpy(),
            "E_tb_2_source": source["E_tb_2"].to_numpy(),
            "E_tb_3_source": source["E_tb_3"].to_numpy(),
            "E_tb_1_reconstructed": bands[:, 0],
            "E_tb_2_reconstructed": bands[:, 1],
            "E_tb_3_reconstructed": bands[:, 2],
        }
    )
    comparison.to_csv(out_dir / "band_comparison.csv", index=False)
    result["high_symmetry_residuals"].to_csv(out_dir / "high_symmetry_residuals.csv", index=False)

    title_suffix = (
        f"mode={result['path_mode']} | K_B={result['k_b_label']} | M={result['m_label']} | "
        f"K_T={result['k_t_label']}"
    )
    render_line_plot(
        out_dir / "band_reconstruction_check.png",
        source.to_numpy(),
        bands,
        result["tick_idx"],
        result["tick_labels"],
        float(result["overall_rmse"]),
        title_suffix,
    )

    rmse_per_band = result["rmse_per_band"]
    summary = [
        "# Tuo TB Reconstruction Summary",
        "",
        f"- Source origin: {result['source_origin']}",
        f"- Path mode: {result['path_mode']}",
        f"- K_B label: {result['k_b_label']}",
        f"- M label: {result['m_label']}",
        f"- K_T label: {result['k_t_label']}",
        f"- Overall RMSE against source Fig. 1c arrays: {float(result['overall_rmse']):.3f} meV",
        f"- Row-wise summed RMSE against source Fig. 1c arrays: {float(result['rowwise_sum_rmse']):.3f} meV",
        f"- Per-band RMSE: [{rmse_per_band[0]:.3f}, {rmse_per_band[1]:.3f}, {rmse_per_band[2]:.3f}] meV",
        f"- Gamma-end max abs delta: {float(result['gamma_end_max_abs_delta']):.6f} meV",
        f"- K_B window RMSE over source indices [149, 150]: {float(result['k_b_rmse_window']):.3f} meV",
        f"- M window RMSE over source indices [299, 300]: {float(result['m_rmse_window']):.3f} meV",
        f"- K_T window RMSE over source indices [449, 450]: {float(result['k_t_rmse_window']):.3f} meV",
        f"- Mixed-star configuration: {result['mixed_star_config']}",
        "",
        "Generated files:",
        "- reconstructed_hopping_table.csv",
        "- band_comparison.csv",
        "- high_symmetry_residuals.csv",
        "- band_reconstruction_check.png",
    ]
    (out_dir / "summary.md").write_text("\n".join(summary), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reconstruct the Tuo TB candidate with configurable k-path conventions.")
    parser.add_argument("--output-dir", type=Path, default=Path("/workspace/output/twse2_tb_reconstruction"))
    parser.add_argument("--path-mode", choices=["exclusive_150", "duplicated_150"], default="exclusive_150")
    parser.add_argument("--k-b-label", default="K_-2b1-b2")
    parser.add_argument("--m-label", default="M_b2")
    parser.add_argument("--k-t-label", default="K_2b1+b2")
    parser.add_argument("--ac1-pattern", choices=["const", "cyc", "anti"], default="cyc")
    parser.add_argument("--bc1-pattern", choices=["const", "cyc", "anti"], default="cyc")
    parser.add_argument("--ac2-pattern", choices=["const", "cyc", "anti"], default="anti")
    parser.add_argument("--bc2-pattern", choices=["const", "cyc", "anti"], default="anti")
    parser.add_argument("--ac7-first-pattern", choices=["const", "cyc", "anti"], default="cyc")
    parser.add_argument("--bc7-first-pattern", choices=["const", "cyc", "anti"], default="cyc")
    parser.add_argument("--ac7-second-pattern", choices=["const", "cyc", "anti"], default="anti")
    parser.add_argument("--bc7-second-pattern", choices=["const", "cyc", "anti"], default="anti")
    parser.add_argument("--ac7-second-conjugated", action="store_true")
    parser.add_argument("--bc7-second-conjugated", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = evaluate_candidate(
        args.path_mode,
        args.k_b_label,
        args.m_label,
        args.k_t_label,
        mixed_star_config={
            "ac1_pattern": args.ac1_pattern,
            "bc1_pattern": args.bc1_pattern,
            "ac2_pattern": args.ac2_pattern,
            "bc2_pattern": args.bc2_pattern,
            "ac7_first_pattern": args.ac7_first_pattern,
            "bc7_first_pattern": args.bc7_first_pattern,
            "ac7_second_pattern": args.ac7_second_pattern,
            "bc7_second_pattern": args.bc7_second_pattern,
            "ac7_second_conjugated": args.ac7_second_conjugated,
            "bc7_second_conjugated": args.bc7_second_conjugated,
        },
    )
    write_candidate_package(result, args.output_dir)


if __name__ == "__main__":
    main()
