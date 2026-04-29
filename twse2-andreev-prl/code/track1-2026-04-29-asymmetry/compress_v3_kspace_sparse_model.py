from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from reconstruct_tuo_tb import build_hamiltonian, build_hops, build_path, load_source, render_line_plot


DEFAULT_V3_DIR = Path(
    "/workspace/memory/twse2-andreev-prl/data/track1-2026-04-29-v3-orbital-selective-valley-correction"
)
DEFAULT_OUTPUT_DIR = Path("/workspace/output/twse2_v3_kspace_sparse_model")
BASELINE_CONFIG = {
    "path_mode": "exclusive_150",
    "k_b_label": "K_2b1+b2",
    "m_label": "M_b2",
    "k_t_label": "K_-2b1-b2",
    "mixed_star_config": {
        "ac1_pattern": "cyc",
        "bc1_pattern": "cyc",
        "ac2_pattern": "anti",
        "bc2_pattern": "anti",
        "ac7_first_pattern": "cyc",
        "bc7_first_pattern": "cyc",
        "ac7_second_pattern": "anti",
        "bc7_second_pattern": "anti",
        "ac7_second_conjugated": False,
        "bc7_second_conjugated": False,
    },
}
WIDTHS = [0.08, 0.12, 0.18, 0.25, 0.35, 0.5]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compress the full V3 profile into a sparse k-space envelope model that remains "
            "usable away from the high-symmetry path."
        )
    )
    parser.add_argument("--v3-dir", type=Path, default=DEFAULT_V3_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--common-terms", type=int, default=28)
    parser.add_argument("--orbital-terms", type=int, default=48)
    parser.add_argument("--c-terms", type=int, default=28)
    return parser.parse_args()


def gaussian_on_path(path: np.ndarray, center_index: int, width: float) -> np.ndarray:
    distances = np.linalg.norm(path - path[center_index], axis=1)
    return np.exp(-0.5 * (distances / width) ** 2)


def build_even_dictionary(path: np.ndarray) -> tuple[np.ndarray, list[dict[str, object]]]:
    columns: list[np.ndarray] = []
    meta: list[dict[str, object]] = []

    for width in WIDTHS:
        columns.append(gaussian_on_path(path, 0, width))
        meta.append({"kind": "gamma", "center_index": 0, "width": width})

    for center in [50, 75, 100, 125, 150, 175, 200, 225, 250]:
        partner = (600 - center) % 600
        for width in WIDTHS:
            columns.append(gaussian_on_path(path, center, width) + gaussian_on_path(path, partner, width))
            meta.append(
                {
                    "kind": "even_pair",
                    "center_left_index": center,
                    "center_right_index": partner,
                    "width": width,
                }
            )

    for center in [275, 300, 325]:
        for width in WIDTHS:
            columns.append(gaussian_on_path(path, center, width))
            meta.append({"kind": "central", "center_index": center, "width": width})

    return np.column_stack(columns), meta


def build_odd_dictionary(path: np.ndarray) -> tuple[np.ndarray, list[dict[str, object]]]:
    columns: list[np.ndarray] = []
    meta: list[dict[str, object]] = []

    for center in [50, 75, 100, 125, 150, 175, 200, 225, 250, 275]:
        partner = (600 - center) % 600
        for width in WIDTHS:
            columns.append(gaussian_on_path(path, center, width) - gaussian_on_path(path, partner, width))
            meta.append(
                {
                    "kind": "odd_pair",
                    "center_left_index": center,
                    "center_right_index": partner,
                    "width": width,
                }
            )

    return np.column_stack(columns), meta


def omp_sparse_fit(y: np.ndarray, dictionary: np.ndarray, max_terms: int) -> tuple[list[int], np.ndarray, np.ndarray]:
    norms = np.linalg.norm(dictionary, axis=0)
    valid = norms > 1e-12
    filtered = dictionary[:, valid]
    map_indices = np.where(valid)[0]
    normalized = filtered / norms[valid]

    residual = y.astype(float).copy()
    chosen_local: list[int] = []

    for _ in range(max_terms):
        corr = np.abs(normalized.T @ residual)
        if chosen_local:
            corr[chosen_local] = -1.0
        choice = int(np.argmax(corr))
        chosen_local.append(choice)
        basis = filtered[:, chosen_local]
        coeff = np.linalg.lstsq(basis, y, rcond=None)[0]
        residual = y - basis @ coeff

    basis = filtered[:, chosen_local]
    coeff = np.linalg.lstsq(basis, y, rcond=None)[0]
    fit = basis @ coeff
    chosen = [int(map_indices[j]) for j in chosen_local]
    return chosen, coeff, fit


def serialize_terms(meta: list[dict[str, object]], chosen: list[int], coeff: np.ndarray) -> list[dict[str, object]]:
    payload = []
    for dictionary_index, amplitude in zip(chosen, coeff):
        row = dict(meta[dictionary_index])
        row["amplitude_meV"] = float(amplitude)
        payload.append(row)
    return payload


def evaluate_term_at_k(k_vec: np.ndarray, path: np.ndarray, term: dict[str, object]) -> float:
    width = float(term["width"])
    amplitude = float(term["amplitude_meV"])

    if term["kind"] == "gamma":
        center = path[int(term["center_index"])]
        distance = float(np.linalg.norm(k_vec - center))
        return amplitude * float(np.exp(-0.5 * (distance / width) ** 2))

    if term["kind"] == "central":
        center = path[int(term["center_index"])]
        distance = float(np.linalg.norm(k_vec - center))
        return amplitude * float(np.exp(-0.5 * (distance / width) ** 2))

    left = path[int(term["center_left_index"])]
    right = path[int(term["center_right_index"])]
    left_weight = float(np.exp(-0.5 * (np.linalg.norm(k_vec - left) / width) ** 2))
    right_weight = float(np.exp(-0.5 * (np.linalg.norm(k_vec - right) / width) ** 2))

    if term["kind"] == "even_pair":
        return amplitude * (left_weight + right_weight)
    if term["kind"] == "odd_pair":
        return amplitude * (left_weight - right_weight)

    raise ValueError(f"Unsupported term kind: {term['kind']}")


def evaluate_model_on_path(path: np.ndarray, channels: dict[str, list[dict[str, object]]]) -> dict[str, np.ndarray]:
    outputs: dict[str, np.ndarray] = {}
    for channel_name, terms in channels.items():
        values = np.zeros(len(path), dtype=float)
        for index, k_vec in enumerate(path):
            values[index] = sum(evaluate_term_at_k(k_vec, path, term) for term in terms)
        outputs[channel_name] = values
    return outputs


def main() -> None:
    args = parse_args()
    out_dir = args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    profile = pd.read_csv(args.v3_dir / "v3_correction_profile.csv")
    source_df, source_origin = load_source()
    source = source_df.to_numpy()

    path, tick_idx, tick_labels, _ = build_path(
        BASELINE_CONFIG["path_mode"],
        BASELINE_CONFIG["k_b_label"],
        BASELINE_CONFIG["m_label"],
        BASELINE_CONFIG["k_t_label"],
    )
    even_dict, even_meta = build_even_dictionary(path)
    odd_dict, odd_meta = build_odd_dictionary(path)

    channel_settings = [
        ("v3_ab_common_meV", even_dict, even_meta, args.common_terms),
        ("v3_ab_orbital_selective_meV", odd_dict, odd_meta, args.orbital_terms),
        ("v3_c_meV", even_dict, even_meta, args.c_terms),
    ]

    serialized_channels: dict[str, list[dict[str, object]]] = {}
    profile_rmse: dict[str, float] = {}
    fitted_channels: dict[str, np.ndarray] = {}
    for channel_name, dictionary, metadata, max_terms in channel_settings:
        chosen, coeff, fit = omp_sparse_fit(profile[channel_name].to_numpy(), dictionary, max_terms)
        serialized_channels[channel_name] = serialize_terms(metadata, chosen, coeff)
        profile_rmse[channel_name] = float(np.sqrt(np.mean((fit - profile[channel_name].to_numpy()) ** 2)))
        fitted_channels[channel_name] = fit

    reevaluated = evaluate_model_on_path(path, serialized_channels)
    compressed_profile = profile.copy()
    compressed_profile["kspace_v3_ab_common_meV"] = reevaluated["v3_ab_common_meV"]
    compressed_profile["kspace_v3_ab_orbital_selective_meV"] = reevaluated["v3_ab_orbital_selective_meV"]
    compressed_profile["kspace_v3_c_meV"] = reevaluated["v3_c_meV"]
    compressed_profile["kspace_d_a_meV"] = (
        compressed_profile["kspace_v3_ab_common_meV"] + compressed_profile["kspace_v3_ab_orbital_selective_meV"]
    )
    compressed_profile["kspace_d_b_meV"] = (
        compressed_profile["kspace_v3_ab_common_meV"] - compressed_profile["kspace_v3_ab_orbital_selective_meV"]
    )
    compressed_profile["kspace_d_c_meV"] = compressed_profile["kspace_v3_c_meV"]
    compressed_profile.to_csv(out_dir / "v3_kspace_sparse_profile.csv", index=False)

    hops = build_hops(BASELINE_CONFIG["mixed_star_config"])
    base_hamiltonians = [build_hamiltonian(k_point, hops) for k_point in path]
    baseline_bands = np.asarray([np.linalg.eigvalsh(matrix)[::-1] for matrix in base_hamiltonians])
    compressed_corrections = compressed_profile[["kspace_d_a_meV", "kspace_d_b_meV", "kspace_d_c_meV"]].to_numpy()
    compressed_bands = np.asarray(
        [np.linalg.eigvalsh(matrix + np.diag(correction))[::-1] for matrix, correction in zip(base_hamiltonians, compressed_corrections)]
    )

    comparison = pd.DataFrame(
        {
            "point_index": np.arange(len(path)),
            "E_tb_1_source": source[:, 0],
            "E_tb_2_source": source[:, 1],
            "E_tb_3_source": source[:, 2],
            "E_tb_1_baseline": baseline_bands[:, 0],
            "E_tb_2_baseline": baseline_bands[:, 1],
            "E_tb_3_baseline": baseline_bands[:, 2],
            "E_tb_1_kspace_sparse": compressed_bands[:, 0],
            "E_tb_2_kspace_sparse": compressed_bands[:, 1],
            "E_tb_3_kspace_sparse": compressed_bands[:, 2],
        }
    )
    comparison.to_csv(out_dir / "band_comparison_kspace_sparse_v3.csv", index=False)

    render_line_plot(
        out_dir / "band_reconstruction_check_kspace_sparse_v3.png",
        source,
        compressed_bands,
        tick_idx,
        tick_labels,
        float(np.sqrt(np.mean((compressed_bands - source) ** 2))),
        "k-space sparse compressed V3 model",
    )

    model_payload = {
        "source_origin": source_origin,
        "baseline_config": BASELINE_CONFIG,
        "common_terms": serialized_channels["v3_ab_common_meV"],
        "orbital_terms": serialized_channels["v3_ab_orbital_selective_meV"],
        "c_terms": serialized_channels["v3_c_meV"],
        "channel_profile_rmse_meV": profile_rmse,
    }
    (out_dir / "kspace_sparse_model.json").write_text(json.dumps(model_payload, indent=2), encoding="utf-8")

    baseline_rmse = float(np.sqrt(np.mean((baseline_bands - source) ** 2)))
    compressed_rmse = float(np.sqrt(np.mean((compressed_bands - source) ** 2)))
    gamma_end_delta = float(np.max(np.abs(compressed_bands[599] - source[599])))
    valley_window_rmse = {
        "k_b_window_rmse_meV": float(np.sqrt(np.mean((compressed_bands[[149, 150]] - source[[149, 150]]) ** 2))),
        "m_window_rmse_meV": float(np.sqrt(np.mean((compressed_bands[[299, 300]] - source[[299, 300]]) ** 2))),
        "k_t_window_rmse_meV": float(np.sqrt(np.mean((compressed_bands[[449, 450]] - source[[449, 450]]) ** 2))),
    }

    summary_lines = [
        "# K-Space Sparse Compressed V3 Summary",
        "",
        f"- Source origin: {source_origin}",
        f"- Baseline overall RMSE: {baseline_rmse:.6f} meV",
        f"- K-space sparse V3 overall RMSE: {compressed_rmse:.6f} meV",
        f"- Gamma-end max abs delta: {gamma_end_delta:.6f} meV",
        f"- K_B window RMSE: {valley_window_rmse['k_b_window_rmse_meV']:.6f} meV",
        f"- M window RMSE: {valley_window_rmse['m_window_rmse_meV']:.6f} meV",
        f"- K_T window RMSE: {valley_window_rmse['k_t_window_rmse_meV']:.6f} meV",
        "",
        "## Channel profile RMSE",
        f"- v3_ab_common_meV: {profile_rmse['v3_ab_common_meV']:.6f} meV",
        f"- v3_ab_orbital_selective_meV: {profile_rmse['v3_ab_orbital_selective_meV']:.6f} meV",
        f"- v3_c_meV: {profile_rmse['v3_c_meV']:.6f} meV",
        "",
        "Generated files:",
        "- kspace_sparse_model.json",
        "- v3_kspace_sparse_profile.csv",
        "- band_comparison_kspace_sparse_v3.csv",
        "- band_reconstruction_check_kspace_sparse_v3.png",
    ]
    (out_dir / "summary.md").write_text("\n".join(summary_lines), encoding="utf-8")


if __name__ == "__main__":
    main()
