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
DEFAULT_OUTPUT_DIR = Path("/workspace/output/twse2_v3_compressed_parametrization")
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compress the effective V3 orbital-selective valley correction profile into a sparse "
            "low-dimensional basis model and verify the resulting Track-1 band error."
        )
    )
    parser.add_argument("--v3-dir", type=Path, default=DEFAULT_V3_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--max-terms-per-channel", type=int, default=5)
    return parser.parse_args()


def wrap_dist(x: np.ndarray, center: float, period: int) -> np.ndarray:
    dist = np.abs(x - center)
    return np.minimum(dist, period - dist)


def gaussian_basis(idx: np.ndarray, center: int, width: int, period: int) -> np.ndarray:
    if center == 0:
        distance = wrap_dist(idx, 0.0, period)
    else:
        distance = np.abs(idx - float(center))
    return np.exp(-0.5 * (distance / float(width)) ** 2)


def omp_sparse_fit(y: np.ndarray, dictionary: np.ndarray, max_terms: int) -> tuple[list[int], np.ndarray, np.ndarray]:
    normalized = dictionary / np.linalg.norm(dictionary, axis=0, keepdims=True)
    residual = y.astype(float).copy()
    chosen: list[int] = []

    for _ in range(max_terms):
        corr = np.abs(normalized.T @ residual)
        if chosen:
            corr[chosen] = -1.0
        choice = int(np.argmax(corr))
        chosen.append(choice)
        basis = dictionary[:, chosen]
        coeff = np.linalg.lstsq(basis, y, rcond=None)[0]
        residual = y - basis @ coeff

    basis = dictionary[:, chosen]
    coeff = np.linalg.lstsq(basis, y, rcond=None)[0]
    fit = basis @ coeff
    return chosen, coeff, fit


def build_even_dictionary(idx: np.ndarray, period: int) -> tuple[np.ndarray, list[dict[str, object]]]:
    entries: list[np.ndarray] = []
    meta: list[dict[str, object]] = []
    widths = [12, 20, 35, 60, 90]

    for width in widths:
        entries.append(gaussian_basis(idx, 0, width, period))
        meta.append({"kind": "gamma_wrap", "center": 0, "width": width})

    for center in [75, 100, 125, 150, 175, 200, 225]:
        mirror = period - center
        for width in widths:
            entries.append(
                gaussian_basis(idx, center, width, period) + gaussian_basis(idx, mirror, width, period)
            )
            meta.append({"kind": "even_pair", "center_left": center, "center_right": mirror, "width": width})

    for center in [250, 275, 300, 325, 350]:
        for width in widths:
            entries.append(gaussian_basis(idx, center, width, period))
            meta.append({"kind": "central", "center": center, "width": width})

    return np.column_stack(entries), meta


def build_odd_dictionary(idx: np.ndarray, period: int) -> tuple[np.ndarray, list[dict[str, object]]]:
    entries: list[np.ndarray] = []
    meta: list[dict[str, object]] = []
    widths = [12, 20, 35, 60, 90]

    for width in widths:
        entries.append(gaussian_basis(idx, 0, width, period))
        meta.append({"kind": "gamma_wrap", "center": 0, "width": width})

    for center in [75, 100, 125, 150, 175, 200, 225, 250, 275]:
        mirror = period - center
        for width in widths:
            entries.append(
                gaussian_basis(idx, center, width, period) - gaussian_basis(idx, mirror, width, period)
            )
            meta.append({"kind": "odd_pair", "center_left": center, "center_right": mirror, "width": width})

    for width in widths:
        entries.append(gaussian_basis(idx, 300, width, period))
        meta.append({"kind": "midpoint", "center": 300, "width": width})

    return np.column_stack(entries), meta


def serialize_terms(meta: list[dict[str, object]], chosen: list[int], coeff: np.ndarray) -> list[dict[str, object]]:
    terms = []
    for dictionary_index, amplitude in zip(chosen, coeff):
        term = dict(meta[dictionary_index])
        term["amplitude_meV"] = float(amplitude)
        terms.append(term)
    return terms


def main() -> None:
    args = parse_args()
    out_dir = args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    profile = pd.read_csv(args.v3_dir / "v3_correction_profile.csv")
    source_df, source_origin = load_source()
    source = source_df.to_numpy()
    idx = profile["point_index"].to_numpy(dtype=float)
    period = int(len(profile))

    even_dictionary, even_meta = build_even_dictionary(idx, period)
    odd_dictionary, odd_meta = build_odd_dictionary(idx, period)

    fits: dict[str, np.ndarray] = {}
    term_payload: dict[str, list[dict[str, object]]] = {}
    channel_rmse: dict[str, float] = {}

    for channel, dictionary, metadata in [
        ("v3_ab_common_meV", even_dictionary, even_meta),
        ("v3_ab_orbital_selective_meV", odd_dictionary, odd_meta),
        ("v3_c_meV", even_dictionary, even_meta),
    ]:
        chosen, coeff, fit = omp_sparse_fit(
            y=profile[channel].to_numpy(),
            dictionary=dictionary,
            max_terms=args.max_terms_per_channel,
        )
        fits[channel] = fit
        term_payload[channel] = serialize_terms(metadata, chosen, coeff)
        channel_rmse[channel] = float(np.sqrt(np.mean((fit - profile[channel].to_numpy()) ** 2)))

    compressed_common = fits["v3_ab_common_meV"]
    compressed_orbital = fits["v3_ab_orbital_selective_meV"]
    compressed_c = fits["v3_c_meV"]

    compressed_profile = profile.copy()
    compressed_profile["compressed_v3_ab_common_meV"] = compressed_common
    compressed_profile["compressed_v3_ab_orbital_selective_meV"] = compressed_orbital
    compressed_profile["compressed_v3_c_meV"] = compressed_c
    compressed_profile["compressed_d_a_meV"] = compressed_common + compressed_orbital
    compressed_profile["compressed_d_b_meV"] = compressed_common - compressed_orbital
    compressed_profile["compressed_d_c_meV"] = compressed_c
    compressed_profile.to_csv(out_dir / "v3_compressed_profile.csv", index=False)

    hops = build_hops(BASELINE_CONFIG["mixed_star_config"])
    path, tick_idx, tick_labels, _ = build_path(
        BASELINE_CONFIG["path_mode"],
        BASELINE_CONFIG["k_b_label"],
        BASELINE_CONFIG["m_label"],
        BASELINE_CONFIG["k_t_label"],
    )
    baseline_bands = np.asarray([np.linalg.eigvalsh(build_hamiltonian(k_point, hops))[::-1] for k_point in path])
    compressed_corrections = compressed_profile[
        ["compressed_d_a_meV", "compressed_d_b_meV", "compressed_d_c_meV"]
    ].to_numpy()
    compressed_bands = np.asarray(
        [
            np.linalg.eigvalsh(base_hamiltonian + np.diag(correction))[::-1]
            for base_hamiltonian, correction in zip(
                [build_hamiltonian(k_point, hops) for k_point in path], compressed_corrections
            )
        ]
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
            "E_tb_1_compressed": compressed_bands[:, 0],
            "E_tb_2_compressed": compressed_bands[:, 1],
            "E_tb_3_compressed": compressed_bands[:, 2],
        }
    )
    comparison.to_csv(out_dir / "band_comparison_compressed_v3.csv", index=False)

    render_line_plot(
        out_dir / "band_reconstruction_check_compressed_v3.png",
        source,
        compressed_bands,
        tick_idx,
        tick_labels,
        float(np.sqrt(np.mean((compressed_bands - source) ** 2))),
        "Compressed V3 orbital-selective valley parametrization",
    )

    model_payload = {
        "source_origin": source_origin,
        "baseline_config": BASELINE_CONFIG,
        "max_terms_per_channel": args.max_terms_per_channel,
        "channels": {
            "v3_ab_common_meV": term_payload["v3_ab_common_meV"],
            "v3_ab_orbital_selective_meV": term_payload["v3_ab_orbital_selective_meV"],
            "v3_c_meV": term_payload["v3_c_meV"],
        },
        "channel_profile_rmse_meV": channel_rmse,
    }
    (out_dir / "compressed_model.json").write_text(json.dumps(model_payload, indent=2), encoding="utf-8")

    baseline_rmse = float(np.sqrt(np.mean((baseline_bands - source) ** 2)))
    compressed_rmse = float(np.sqrt(np.mean((compressed_bands - source) ** 2)))
    gamma_end_delta = float(np.max(np.abs(compressed_bands[599] - source[599])))
    valley_window_rmse = {
        "k_b_window_rmse_meV": float(np.sqrt(np.mean((compressed_bands[[149, 150]] - source[[149, 150]]) ** 2))),
        "m_window_rmse_meV": float(np.sqrt(np.mean((compressed_bands[[299, 300]] - source[[299, 300]]) ** 2))),
        "k_t_window_rmse_meV": float(np.sqrt(np.mean((compressed_bands[[449, 450]] - source[[449, 450]]) ** 2))),
    }

    summary_lines = [
        "# Compressed V3 Orbital-Selective Valley Parametrization Summary",
        "",
        f"- Source origin: {source_origin}",
        f"- Baseline overall RMSE: {baseline_rmse:.6f} meV",
        f"- Compressed-V3 overall RMSE: {compressed_rmse:.6f} meV",
        f"- Gamma-end max abs delta: {gamma_end_delta:.6f} meV",
        f"- K_B window RMSE: {valley_window_rmse['k_b_window_rmse_meV']:.6f} meV",
        f"- M window RMSE: {valley_window_rmse['m_window_rmse_meV']:.6f} meV",
        f"- K_T window RMSE: {valley_window_rmse['k_t_window_rmse_meV']:.6f} meV",
        "",
        "## Channel profile RMSE",
        f"- v3_ab_common_meV: {channel_rmse['v3_ab_common_meV']:.6f} meV",
        f"- v3_ab_orbital_selective_meV: {channel_rmse['v3_ab_orbital_selective_meV']:.6f} meV",
        f"- v3_c_meV: {channel_rmse['v3_c_meV']:.6f} meV",
        "",
        "## Term counts",
        f"- common terms: {len(term_payload['v3_ab_common_meV'])}",
        f"- orbital-selective terms: {len(term_payload['v3_ab_orbital_selective_meV'])}",
        f"- c-channel terms: {len(term_payload['v3_c_meV'])}",
        "",
        "Generated files:",
        "- compressed_model.json",
        "- v3_compressed_profile.csv",
        "- band_comparison_compressed_v3.csv",
        "- band_reconstruction_check_compressed_v3.png",
    ]
    (out_dir / "summary.md").write_text("\n".join(summary_lines), encoding="utf-8")


if __name__ == "__main__":
    main()
