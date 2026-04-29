from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from reconstruct_tuo_tb import (
    build_hamiltonian,
    build_hops,
    build_path,
    load_source,
    render_line_plot,
)


DEFAULT_OUTPUT_DIR = Path("/workspace/output/twse2_v3_orbital_selective_valley_correction")
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
            "Build V3: an effective orbital-selective valley correction layer on top of the current "
            "best coupled Track-1 baseline, and verify whether it closes the source-band path."
        )
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--max-iter", type=int, default=12)
    parser.add_argument("--tol", type=float, default=1e-10)
    parser.add_argument("--fd-eps", type=float, default=1e-5)
    return parser.parse_args()


def solve_diagonal_correction(
    base_hamiltonian: np.ndarray,
    target_eigs_desc: np.ndarray,
    initial_guess: np.ndarray | None,
    max_iter: int,
    tol: float,
    fd_eps: float,
) -> tuple[np.ndarray, np.ndarray, int, float]:
    def residual(diagonal_shift: np.ndarray) -> np.ndarray:
        corrected = base_hamiltonian + np.diag(diagonal_shift)
        return np.linalg.eigvalsh(corrected)[::-1] - target_eigs_desc

    base_eigs, base_vecs = np.linalg.eigh(base_hamiltonian)
    order = np.argsort(base_eigs)[::-1]
    base_eigs = base_eigs[order]
    base_vecs = base_vecs[:, order]
    orbital_weights = np.abs(base_vecs) ** 2

    seed_guesses = [
        np.zeros(3, dtype=float),
        np.linalg.lstsq(orbital_weights.T, target_eigs_desc - base_eigs, rcond=None)[0],
        target_eigs_desc - base_eigs,
    ]
    if initial_guess is not None:
        seed_guesses.insert(0, initial_guess.astype(float).copy())

    best_guess = None
    best_corrected = None
    best_iteration = None
    best_norm = None

    for seed in seed_guesses:
        guess = np.array(seed, dtype=float)
        current = residual(guess)
        final_iteration = 0

        for iteration in range(max_iter):
            norm = float(np.linalg.norm(current))
            final_iteration = iteration
            if norm <= tol:
                break

            jacobian = np.zeros((3, 3), dtype=float)
            for axis in range(3):
                shifted = guess.copy()
                shifted[axis] += fd_eps
                jacobian[:, axis] = (residual(shifted) - current) / fd_eps

            step = np.linalg.lstsq(jacobian, -current, rcond=None)[0]

            accepted = False
            step_scale = 1.0
            while step_scale >= 2.0 ** -12:
                candidate = guess + step_scale * step
                candidate_residual = residual(candidate)
                if float(np.linalg.norm(candidate_residual)) < norm:
                    guess = candidate
                    current = candidate_residual
                    accepted = True
                    break
                step_scale *= 0.5

            if not accepted:
                break

        corrected = np.linalg.eigvalsh(base_hamiltonian + np.diag(guess))[::-1]
        norm = float(np.linalg.norm(corrected - target_eigs_desc))

        if best_norm is None or norm < best_norm:
            best_guess = guess
            best_corrected = corrected
            best_iteration = final_iteration
            best_norm = norm

    assert best_guess is not None
    assert best_corrected is not None
    assert best_iteration is not None
    assert best_norm is not None
    return best_guess, best_corrected, best_iteration, best_norm


def build_high_symmetry_table(source: np.ndarray, corrected: np.ndarray) -> pd.DataFrame:
    high_symmetry_idx = {
        "Gamma_start": 0,
        "K_B": 150,
        "M": 300,
        "K_T": 450,
        "Gamma_end": 599,
    }
    rows = []
    for label, point_index in high_symmetry_idx.items():
        src_row = source[point_index]
        cor_row = corrected[point_index]
        rows.append(
            {
                "label": label,
                "point_index": point_index,
                "source_1": src_row[0],
                "source_2": src_row[1],
                "source_3": src_row[2],
                "corrected_1": cor_row[0],
                "corrected_2": cor_row[1],
                "corrected_3": cor_row[2],
                "delta_1": cor_row[0] - src_row[0],
                "delta_2": cor_row[1] - src_row[1],
                "delta_3": cor_row[2] - src_row[2],
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    args = parse_args()
    out_dir = args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    source_df, source_origin = load_source()
    source = source_df.to_numpy()
    hops = build_hops(BASELINE_CONFIG["mixed_star_config"])
    path, tick_idx, tick_labels, _ = build_path(
        BASELINE_CONFIG["path_mode"],
        BASELINE_CONFIG["k_b_label"],
        BASELINE_CONFIG["m_label"],
        BASELINE_CONFIG["k_t_label"],
    )

    baseline_bands = []
    corrected_bands = []
    profile_rows = []
    guess = None

    for point_index, k_point in enumerate(path):
        base_hamiltonian = build_hamiltonian(k_point, hops)
        baseline_eigs = np.linalg.eigvalsh(base_hamiltonian)[::-1]
        baseline_bands.append(baseline_eigs)

        correction, corrected_eigs, iterations, residual_norm = solve_diagonal_correction(
            base_hamiltonian=base_hamiltonian,
            target_eigs_desc=source[point_index],
            initial_guess=guess,
            max_iter=args.max_iter,
            tol=args.tol,
            fd_eps=args.fd_eps,
        )
        guess = correction
        corrected_bands.append(corrected_eigs)

        d_a, d_b, d_c = correction
        profile_rows.append(
            {
                "point_index": point_index,
                "d_a_meV": d_a,
                "d_b_meV": d_b,
                "d_c_meV": d_c,
                "v3_ab_common_meV": 0.5 * (d_a + d_b),
                "v3_ab_orbital_selective_meV": 0.5 * (d_a - d_b),
                "v3_c_meV": d_c,
                "solver_iterations": iterations,
                "solver_residual_norm_meV": residual_norm,
            }
        )

    baseline_bands = np.asarray(baseline_bands)
    corrected_bands = np.asarray(corrected_bands)
    profile = pd.DataFrame(profile_rows)

    comparison = pd.DataFrame(
        {
            "point_index": np.arange(len(path)),
            "E_tb_1_source": source[:, 0],
            "E_tb_2_source": source[:, 1],
            "E_tb_3_source": source[:, 2],
            "E_tb_1_baseline": baseline_bands[:, 0],
            "E_tb_2_baseline": baseline_bands[:, 1],
            "E_tb_3_baseline": baseline_bands[:, 2],
            "E_tb_1_corrected": corrected_bands[:, 0],
            "E_tb_2_corrected": corrected_bands[:, 1],
            "E_tb_3_corrected": corrected_bands[:, 2],
        }
    )
    comparison.to_csv(out_dir / "band_comparison_v3.csv", index=False)
    profile.to_csv(out_dir / "v3_correction_profile.csv", index=False)

    high_symmetry = build_high_symmetry_table(source, corrected_bands)
    high_symmetry.to_csv(out_dir / "high_symmetry_residuals_v3.csv", index=False)

    render_line_plot(
        out_dir / "band_reconstruction_check_v3.png",
        source,
        corrected_bands,
        tick_idx,
        tick_labels,
        float(np.sqrt(np.mean((corrected_bands - source) ** 2))),
        "V3 orbital-selective valley correction on top of coupled baseline",
    )

    baseline_rmse = float(np.sqrt(np.mean((baseline_bands - source) ** 2)))
    corrected_rmse = float(np.sqrt(np.mean((corrected_bands - source) ** 2)))
    gamma_end_delta = float(np.max(np.abs(corrected_bands[599] - source[599])))
    valley_slice = profile.iloc[140:161].copy()
    valley_slice_2 = profile.iloc[440:461].copy()
    combined_valley = pd.concat([valley_slice, valley_slice_2], ignore_index=True)

    summary_lines = [
        "# V3 Orbital-Selective Valley Correction Summary",
        "",
        "## Baseline",
        f"- Source origin: {source_origin}",
        f"- Path mode: {BASELINE_CONFIG['path_mode']}",
        f"- K_B label: {BASELINE_CONFIG['k_b_label']}",
        f"- M label: {BASELINE_CONFIG['m_label']}",
        f"- K_T label: {BASELINE_CONFIG['k_t_label']}",
        f"- Mixed-star config: {BASELINE_CONFIG['mixed_star_config']}",
        f"- Baseline overall RMSE: {baseline_rmse:.6f} meV",
        "",
        "## V3 closure result",
        "- Definition: solve a diagonal orbital correction layer `diag(d_A(k), d_B(k), d_C(k))` point-by-point on the coupled baseline.",
        "- Decomposition:",
        "  - `v3_ab_common = (d_A + d_B) / 2`",
        "  - `v3_ab_orbital_selective = (d_A - d_B) / 2`",
        "  - `v3_c = d_C`",
        f"- Corrected overall RMSE: {corrected_rmse:.12f} meV",
        f"- Gamma-end max abs delta after V3: {gamma_end_delta:.12e} meV",
        f"- Max solver residual norm: {profile['solver_residual_norm_meV'].max():.12e} meV",
        "",
        "## Valley localization check",
        f"- Max |v3_ab_orbital_selective| over points 140-160 and 440-460: {combined_valley['v3_ab_orbital_selective_meV'].abs().max():.6f} meV",
        f"- Max |v3_ab_common| over points 140-160 and 440-460: {combined_valley['v3_ab_common_meV'].abs().max():.6f} meV",
        f"- Max |v3_c| over points 140-160 and 440-460: {combined_valley['v3_c_meV'].abs().max():.6f} meV",
        f"- Global max |v3_ab_orbital_selective|: {profile['v3_ab_orbital_selective_meV'].abs().max():.6f} meV",
        f"- Global max |v3_ab_common|: {profile['v3_ab_common_meV'].abs().max():.6f} meV",
        f"- Global max |v3_c|: {profile['v3_c_meV'].abs().max():.6f} meV",
        "",
        "Generated files:",
        "- band_comparison_v3.csv",
        "- v3_correction_profile.csv",
        "- high_symmetry_residuals_v3.csv",
        "- band_reconstruction_check_v3.png",
    ]

    (out_dir / "summary.md").write_text("\n".join(summary_lines), encoding="utf-8")


if __name__ == "__main__":
    main()
