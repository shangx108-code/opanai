from __future__ import annotations

import argparse
from itertools import product
from pathlib import Path

import pandas as pd

from reconstruct_tuo_tb import evaluate_candidate, load_source, write_candidate_package


DEFAULT_PATH_MODE = "exclusive_150"
DEFAULT_K_B_LABEL = "K_-2b1-b2"
DEFAULT_M_LABEL = "M_b2"
DEFAULT_K_T_LABEL = "K_2b1+b2"
PHASE_PATTERNS = ["const", "cyc", "anti"]
FIXED_SHORT_RANGE = {
    "ac1_pattern": "cyc",
    "bc1_pattern": "cyc",
    "ac2_pattern": "anti",
    "bc2_pattern": "anti",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan asymmetric sqrt(7) A-C / B-C phase rules on top of the best exact-Gamma mixed-star baseline."
    )
    parser.add_argument("--output-dir", type=Path, default=Path("/workspace/output/twse2_asymmetric_c7_scan"))
    parser.add_argument("--gamma-threshold-meV", type=float, default=0.05)
    parser.add_argument("--path-mode", default=DEFAULT_PATH_MODE)
    parser.add_argument("--k-b-label", default=DEFAULT_K_B_LABEL)
    parser.add_argument("--m-label", default=DEFAULT_M_LABEL)
    parser.add_argument("--k-t-label", default=DEFAULT_K_T_LABEL)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    out_dir = args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    source, source_origin = load_source()
    rows = []
    best_overall_result = None
    best_exact_gamma_result = None
    best_exact_gamma_metric = None

    for ac7_first_pattern, bc7_first_pattern, ac7_second_pattern, bc7_second_pattern, ac7_second_conjugated, bc7_second_conjugated in product(
        PHASE_PATTERNS, PHASE_PATTERNS, PHASE_PATTERNS, PHASE_PATTERNS, [False, True], [False, True]
    ):
        mixed_star_config = {
            **FIXED_SHORT_RANGE,
            "ac7_first_pattern": ac7_first_pattern,
            "bc7_first_pattern": bc7_first_pattern,
            "ac7_second_pattern": ac7_second_pattern,
            "bc7_second_pattern": bc7_second_pattern,
            "ac7_second_conjugated": ac7_second_conjugated,
            "bc7_second_conjugated": bc7_second_conjugated,
        }
        result = evaluate_candidate(
            args.path_mode,
            args.k_b_label,
            args.m_label,
            args.k_t_label,
            source=source,
            mixed_star_config=mixed_star_config,
        )
        result["source_origin"] = source_origin
        row = {
            "ac7_first_pattern": ac7_first_pattern,
            "bc7_first_pattern": bc7_first_pattern,
            "ac7_second_pattern": ac7_second_pattern,
            "bc7_second_pattern": bc7_second_pattern,
            "ac7_second_conjugated": ac7_second_conjugated,
            "bc7_second_conjugated": bc7_second_conjugated,
            "overall_rmse_meV": float(result["overall_rmse"]),
            "gamma_end_max_abs_delta_meV": float(result["gamma_end_max_abs_delta"]),
            "k_b_window_rmse_meV": float(result["k_b_rmse_window"]),
            "m_window_rmse_meV": float(result["m_rmse_window"]),
            "k_t_window_rmse_meV": float(result["k_t_rmse_window"]),
            "rowwise_sum_rmse_meV": float(result["rowwise_sum_rmse"]),
            "valley_window_gap_meV": abs(float(result["k_b_rmse_window"]) - float(result["k_t_rmse_window"])),
        }
        rows.append(row)

        if best_overall_result is None or row["overall_rmse_meV"] < float(best_overall_result["overall_rmse"]):
            best_overall_result = result

        gamma_ok = row["gamma_end_max_abs_delta_meV"] <= args.gamma_threshold_meV
        if gamma_ok:
            metric = row["overall_rmse_meV"]
            if best_exact_gamma_result is None or metric < best_exact_gamma_metric:
                best_exact_gamma_result = result
                best_exact_gamma_metric = metric

    ledger = pd.DataFrame(rows).sort_values(
        ["overall_rmse_meV", "gamma_end_max_abs_delta_meV", "k_b_window_rmse_meV", "k_t_window_rmse_meV"]
    )
    ledger.to_csv(out_dir / "asymmetric_c7_scan.csv", index=False)
    ledger.head(20).to_csv(out_dir / "asymmetric_c7_scan_top20.csv", index=False)

    if best_overall_result is None:
        raise RuntimeError("Scan did not produce any candidate.")

    if best_exact_gamma_result is not None:
        best_dir = out_dir / "best_exact_gamma_candidate"
        write_candidate_package(best_exact_gamma_result, best_dir)

    summary_lines = [
        "# Asymmetric sqrt(7) Scan Summary",
        "",
        f"- Source origin: {source_origin}",
        f"- Fixed path mode: {args.path_mode}",
        f"- Fixed K_B label: {args.k_b_label}",
        f"- Fixed M label: {args.m_label}",
        f"- Fixed K_T label: {args.k_t_label}",
        f"- Fixed short-range setting: {FIXED_SHORT_RANGE}",
        f"- Total candidates scanned: {len(ledger)}",
        f"- Gamma acceptance threshold: {args.gamma_threshold_meV:.3f} meV",
        "",
        "## Best overall candidate",
        f"- ac7 first pattern: {best_overall_result['mixed_star_config']['ac7_first_pattern']}",
        f"- bc7 first pattern: {best_overall_result['mixed_star_config']['bc7_first_pattern']}",
        f"- ac7 second pattern: {best_overall_result['mixed_star_config']['ac7_second_pattern']}",
        f"- bc7 second pattern: {best_overall_result['mixed_star_config']['bc7_second_pattern']}",
        f"- ac7 second conjugated: {best_overall_result['mixed_star_config']['ac7_second_conjugated']}",
        f"- bc7 second conjugated: {best_overall_result['mixed_star_config']['bc7_second_conjugated']}",
        f"- Overall RMSE: {float(best_overall_result['overall_rmse']):.3f} meV",
        f"- Gamma-end max abs delta: {float(best_overall_result['gamma_end_max_abs_delta']):.6f} meV",
        f"- K_B window RMSE: {float(best_overall_result['k_b_rmse_window']):.3f} meV",
        f"- M window RMSE: {float(best_overall_result['m_rmse_window']):.3f} meV",
        f"- K_T window RMSE: {float(best_overall_result['k_t_rmse_window']):.3f} meV",
        "",
    ]

    if best_exact_gamma_result is None:
        summary_lines.extend(["## Best exact-Gamma candidate", "- none within the current acceptance threshold", ""])
    else:
        summary_lines.extend(
            [
                "## Best exact-Gamma candidate",
                f"- ac7 first pattern: {best_exact_gamma_result['mixed_star_config']['ac7_first_pattern']}",
                f"- bc7 first pattern: {best_exact_gamma_result['mixed_star_config']['bc7_first_pattern']}",
                f"- ac7 second pattern: {best_exact_gamma_result['mixed_star_config']['ac7_second_pattern']}",
                f"- bc7 second pattern: {best_exact_gamma_result['mixed_star_config']['bc7_second_pattern']}",
                f"- ac7 second conjugated: {best_exact_gamma_result['mixed_star_config']['ac7_second_conjugated']}",
                f"- bc7 second conjugated: {best_exact_gamma_result['mixed_star_config']['bc7_second_conjugated']}",
                f"- Overall RMSE: {float(best_exact_gamma_result['overall_rmse']):.3f} meV",
                f"- Gamma-end max abs delta: {float(best_exact_gamma_result['gamma_end_max_abs_delta']):.6f} meV",
                f"- K_B window RMSE: {float(best_exact_gamma_result['k_b_rmse_window']):.3f} meV",
                f"- M window RMSE: {float(best_exact_gamma_result['m_rmse_window']):.3f} meV",
                f"- K_T window RMSE: {float(best_exact_gamma_result['k_t_rmse_window']):.3f} meV",
                "",
            ]
        )

    summary_lines.extend(
        [
            "Generated files:",
            "- asymmetric_c7_scan.csv",
            "- asymmetric_c7_scan_top20.csv",
        ]
    )
    if best_exact_gamma_result is not None:
        summary_lines.extend(
            [
                "- best_exact_gamma_candidate/reconstructed_hopping_table.csv",
                "- best_exact_gamma_candidate/band_comparison.csv",
                "- best_exact_gamma_candidate/high_symmetry_residuals.csv",
                "- best_exact_gamma_candidate/band_reconstruction_check.png",
                "- best_exact_gamma_candidate/summary.md",
            ]
        )

    (out_dir / "summary.md").write_text("\n".join(summary_lines), encoding="utf-8")


if __name__ == "__main__":
    main()
