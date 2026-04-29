from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

from twse2_persistent_pipeline import (
    B1,
    B2,
    DATA_ROOT,
    ensure_dir,
    save_csv,
    save_heatmap_png,
    save_json,
)

sys.path.insert(0, str(DATA_ROOT.parent / "code" / "track1-2026-04-29-asymmetry"))
from reconstruct_tuo_tb import build_hamiltonian, build_hops, build_path


MODEL_PATH = DATA_ROOT / "track1-2026-04-29-v3-kspace-sparse-model" / "kspace_sparse_model.json"
OUTPUT_DIR = DATA_ROOT / "sgf-kspace-sparse-v3-trial-2026-04-29"


def reduced_kvec(k1_red: float, k2_red: float) -> np.ndarray:
    return k1_red * B1 + k2_red * B2


def load_model(model_path: Path) -> dict[str, object]:
    return json.loads(model_path.read_text(encoding="utf-8"))


def evaluate_term_at_k(k_vec: np.ndarray, path: np.ndarray, term: dict[str, object]) -> float:
    width = float(term["width"])
    amplitude = float(term["amplitude_meV"])

    def gaussian(center_index: int) -> float:
        center = path[int(center_index)]
        distance = float(np.linalg.norm(k_vec - center))
        return float(np.exp(-0.5 * (distance / width) ** 2))

    kind = term["kind"]
    if kind in {"gamma", "central"}:
        return amplitude * gaussian(int(term["center_index"]))
    if kind == "even_pair":
        return amplitude * (
            gaussian(int(term["center_left_index"])) + gaussian(int(term["center_right_index"]))
        )
    if kind == "odd_pair":
        return amplitude * (
            gaussian(int(term["center_left_index"])) - gaussian(int(term["center_right_index"]))
        )
    raise ValueError(f"Unsupported term kind: {kind}")


def evaluate_correction(k_vec: np.ndarray, path: np.ndarray, model: dict[str, object]) -> np.ndarray:
    common = sum(evaluate_term_at_k(k_vec, path, term) for term in model["common_terms"])
    orbital = sum(evaluate_term_at_k(k_vec, path, term) for term in model["orbital_terms"])
    c_term = sum(evaluate_term_at_k(k_vec, path, term) for term in model["c_terms"])
    return np.array([common + orbital, common - orbital, c_term], dtype=float)


def fourier_chain_blocks_with_correction(
    k2_red: float,
    path: np.ndarray,
    model: dict[str, object],
    nk1: int = 192,
    m_max: int = 2,
) -> dict[int, np.ndarray]:
    hops = build_hops()
    k1_values = np.arange(nk1) / nk1
    h_of_k = []
    for k1_red in k1_values:
        k_vec = reduced_kvec(k1_red, k2_red)
        correction = evaluate_correction(k_vec, path, model)
        h_of_k.append(build_hamiltonian(k_vec, hops) + np.diag(correction))
    h_of_k = np.asarray(h_of_k)

    blocks: dict[int, np.ndarray] = {}
    for m in range(-m_max, m_max + 1):
        phase = np.exp(-1j * 2.0 * np.pi * k1_values * m)
        blocks[m] = np.tensordot(phase, h_of_k, axes=(0, 0)) / nk1
    return blocks


def finite_ribbon_hamiltonian_with_correction(
    k2_red: float,
    path: np.ndarray,
    model: dict[str, object],
    num_cells: int = 48,
    m_max: int = 2,
) -> np.ndarray:
    blocks = fourier_chain_blocks_with_correction(k2_red=k2_red, path=path, model=model, m_max=m_max)
    dim = 3 * num_cells
    h_ribbon = np.zeros((dim, dim), dtype=complex)
    for i in range(num_cells):
        for m, block in blocks.items():
            j = i + m
            if 0 <= j < num_cells:
                h_ribbon[3 * i : 3 * (i + 1), 3 * j : 3 * (j + 1)] += block
    return h_ribbon


def edge_spectral_weight_from_ribbon(
    h_ribbon: np.ndarray,
    energies: np.ndarray,
    eta: float = 0.8,
    edge_cells: int = 2,
) -> np.ndarray:
    dim_edge = 3 * edge_cells
    identity = np.eye(h_ribbon.shape[0], dtype=complex)
    weights = np.zeros_like(energies, dtype=float)
    for idx, energy in enumerate(energies):
        green = np.linalg.inv((energy + 1j * eta) * identity - h_ribbon)
        edge_green = green[:dim_edge, :dim_edge]
        weights[idx] = float(-np.imag(np.trace(edge_green)) / np.pi)
    return weights


def main() -> None:
    out_dir = ensure_dir(OUTPUT_DIR)
    model = load_model(MODEL_PATH)
    path, _, _, _ = build_path("exclusive_150", "K_2b1+b2", "M_b2", "K_-2b1-b2")

    k2_grid = np.linspace(0.0, 1.0, 41, endpoint=False)
    energy_grid = np.linspace(-80.0, 20.0, 121)
    eta = 0.8
    num_cells = 48
    edge_cells = 2

    from twse2_persistent_pipeline import edge_spectral_weight

    baseline_map = np.zeros((len(k2_grid), len(energy_grid)))
    corrected_map = np.zeros((len(k2_grid), len(energy_grid)))

    for i, k2_red in enumerate(k2_grid):
        baseline_map[i] = edge_spectral_weight(
            k2_red=k2_red,
            energies=energy_grid,
            eta=eta,
            num_cells=num_cells,
            edge_cells=edge_cells,
        )
        corrected_ribbon = finite_ribbon_hamiltonian_with_correction(
            k2_red=k2_red,
            path=path,
            model=model,
            num_cells=num_cells,
        )
        corrected_map[i] = edge_spectral_weight_from_ribbon(
            h_ribbon=corrected_ribbon,
            energies=energy_grid,
            eta=eta,
            edge_cells=edge_cells,
        )

    delta_map = corrected_map - baseline_map
    zero_idx = int(np.argmin(np.abs(energy_grid)))

    rows = []
    for i, k2_red in enumerate(k2_grid):
        for j, energy in enumerate(energy_grid):
            rows.append(
                [
                    float(k2_red),
                    float(energy),
                    float(baseline_map[i, j]),
                    float(corrected_map[i, j]),
                    float(delta_map[i, j]),
                ]
            )
    save_csv(
        out_dir / "edge_spectral_map_comparison.csv",
        ["k2_reduced", "energy_meV", "baseline_weight", "corrected_weight", "delta_weight"],
        rows,
    )

    zero_rows = []
    for i, k2_red in enumerate(k2_grid):
        zero_rows.append(
            [
                float(k2_red),
                float(baseline_map[i, zero_idx]),
                float(corrected_map[i, zero_idx]),
                float(delta_map[i, zero_idx]),
            ]
        )
    save_csv(
        out_dir / "zero_bias_edge_profile_comparison.csv",
        ["k2_reduced", "baseline_E0", "corrected_E0", "delta_E0"],
        zero_rows,
    )

    save_heatmap_png(out_dir / "baseline_edge_spectral_map.png", baseline_map)
    save_heatmap_png(out_dir / "corrected_edge_spectral_map.png", corrected_map)
    save_heatmap_png(out_dir / "delta_edge_spectral_map.png", delta_map)

    stability = {
        "package_type": "finite_ribbon_edge_greens_proxy_with_kspace_sparse_v3",
        "model_path": str(MODEL_PATH),
        "k2_grid_size": len(k2_grid),
        "energy_grid_size": len(energy_grid),
        "eta_meV": eta,
        "num_cells_open_direction": num_cells,
        "edge_cells_measured": edge_cells,
        "baseline_all_finite": bool(np.isfinite(baseline_map).all()),
        "corrected_all_finite": bool(np.isfinite(corrected_map).all()),
        "baseline_min_weight": float(np.min(baseline_map)),
        "corrected_min_weight": float(np.min(corrected_map)),
        "baseline_max_weight": float(np.max(baseline_map)),
        "corrected_max_weight": float(np.max(corrected_map)),
        "zero_bias_delta_l2": float(np.linalg.norm(delta_map[:, zero_idx])),
        "full_map_delta_l2": float(np.linalg.norm(delta_map)),
        "zero_bias_baseline_mean": float(np.mean(baseline_map[:, zero_idx])),
        "zero_bias_corrected_mean": float(np.mean(corrected_map[:, zero_idx])),
        "zero_bias_baseline_max": float(np.max(baseline_map[:, zero_idx])),
        "zero_bias_corrected_max": float(np.max(corrected_map[:, zero_idx])),
        "note": (
            "This is a downstream SGF stability trial using the k-space sparse compressed-V3 model "
            "inside the same finite-ribbon proxy framework. It is a stability check, not yet a final "
            "semi-infinite manuscript-grade SGF benchmark."
        ),
    }
    save_json(out_dir / "stability_metrics.json", stability)

    summary = [
        "# SGF Trial With K-Space Sparse V3",
        "",
        "- Data status: generated",
        "- Method status: finite-ribbon SGF proxy with baseline-vs-kspace-sparse-V3 comparison",
        f"- k2 grid size: {len(k2_grid)}",
        f"- energy grid size: {len(energy_grid)}",
        f"- Broadening eta: {eta:.2f} meV",
        f"- Baseline all finite: {stability['baseline_all_finite']}",
        f"- Corrected all finite: {stability['corrected_all_finite']}",
        f"- Full-map delta L2: {stability['full_map_delta_l2']:.6f}",
        f"- Zero-bias delta L2: {stability['zero_bias_delta_l2']:.6f}",
        f"- Baseline zero-bias max: {stability['zero_bias_baseline_max']:.6f}",
        f"- Corrected zero-bias max: {stability['zero_bias_corrected_max']:.6f}",
        "- Caution: this is a downstream stability trial for compressed-V3, not yet a final semi-infinite SGF result.",
    ]
    (out_dir / "summary.md").write_text("\n".join(summary), encoding="utf-8")


if __name__ == "__main__":
    main()
