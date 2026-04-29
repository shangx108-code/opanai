from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from reconstruct_tuo_tb import evaluate_candidate, load_source, write_candidate_package


DEFAULT_KPATH_LEDGER = Path(
    "/workspace/memory/twse2-andreev-prl/data/track1-2026-04-28-kpath-scan/k_path_mapping_scan.csv"
)
DEFAULT_C7_LEDGER = Path(
    "/workspace/memory/twse2-andreev-prl/data/track1-2026-04-29-asymmetric-c7/asymmetric_c7_scan.csv"
)
DEFAULT_OUTPUT_DIR = Path("/workspace/output/twse2_coupled_path_c7_scan")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Jointly scan top k-path mappings against exact-Gamma asymmetric sqrt(7) candidates "
            "to test the next coupled path-plus-hopping layer."
        )
    )
    parser.add_argument("--kpath-ledger", type=Path, default=DEFAULT_KPATH_LEDGER)
    parser.add_argument("--c7-ledger", type=Path, default=DEFAULT_C7_LEDGER)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--top-kpaths", type=int, default=20)
    parser.add_argument("--gamma-threshold-meV", type=float, default=0.05)
    return parser.parse_args()


def load_top_kpaths(path: Path, top_n: int) -> pd.DataFrame:
    ledger = pd.read_csv(path)
    ranked = ledger.sort_values(
        ["overall_rmse_meV", "gamma_end_max_abs_delta_meV", "k_b_window_rmse_meV", "k_t_window_rmse_meV"]
    )
    return ranked.head(top_n).reset_index(drop=True)


def load_exact_gamma_c7(path: Path, threshold: float) -> pd.DataFrame:
    ledger = pd.read_csv(path)
    filtered = ledger[ledger["gamma_end_max_abs_delta_meV"] <= threshold].copy()
    ranked = filtered.sort_values(
        ["overall_rmse_meV", "gamma_end_max_abs_delta_meV", "k_b_window_rmse_meV", "k_t_window_rmse_meV"]
    )
    return ranked.reset_index(drop=True)


def row_to_mixed_star_config(row: pd.Series) -> dict[str, object]:
    return {
        "ac1_pattern": "cyc",
        "bc1_pattern": "cyc",
        "ac2_pattern": "anti",
        "bc2_pattern": "anti",
        "ac7_first_pattern": str(row["ac7_first_pattern"]),
        "bc7_first_pattern": str(row["bc7_first_pattern"]),
        "ac7_second_pattern": str(row["ac7_second_pattern"]),
        "bc7_second_pattern": str(row["bc7_second_pattern"]),
        "ac7_second_conjugated": bool(row["ac7_second_conjugated"]),
        "bc7_second_conjugated": bool(row["bc7_second_conjugated"]),
    }


def main() -> None:
    args = parse_args()
    out_dir = args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    top_kpaths = load_top_kpaths(args.kpath_ledger, args.top_kpaths)
    exact_gamma_c7 = load_exact_gamma_c7(args.c7_ledger, args.gamma_threshold_meV)
    if top_kpaths.empty:
        raise RuntimeError("No k-path candidates were loaded.")
    if exact_gamma_c7.empty:
        raise RuntimeError("No exact-Gamma asymmetric sqrt(7) candidates are available for the coupled scan.")

    source, source_origin = load_source()
    rows = []
    best_overall_result = None
    best_exact_gamma_result = None
    best_exact_gamma_metric = None

    for path_rank, kpath_row in top_kpaths.iterrows():
        for c7_rank, c7_row in exact_gamma_c7.iterrows():
            mixed_star_config = row_to_mixed_star_config(c7_row)
            result = evaluate_candidate(
                str(kpath_row["path_mode"]),
                str(kpath_row["k_b_label"]),
                str(kpath_row["m_label"]),
                str(kpath_row["k_t_label"]),
                source=source,
                mixed_star_config=mixed_star_config,
            )
            result["source_origin"] = source_origin
            row = {
                "path_rank": int(path_rank + 1),
                "c7_rank": int(c7_rank + 1),
                "path_mode": str(kpath_row["path_mode"]),
                "k_b_label": str(kpath_row["k_b_label"]),
                "m_label": str(kpath_row["m_label"]),
                "k_t_label": str(kpath_row["k_t_label"]),
                "ac7_first_pattern": str(c7_row["ac7_first_pattern"]),
                "bc7_first_pattern": str(c7_row["bc7_first_pattern"]),
                "ac7_second_pattern": str(c7_row["ac7_second_pattern"]),
                "bc7_second_pattern": str(c7_row["bc7_second_pattern"]),
                "ac7_second_conjugated": bool(c7_row["ac7_second_conjugated"]),
                "bc7_second_conjugated": bool(c7_row["bc7_second_conjugated"]),
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

            if row["gamma_end_max_abs_delta_meV"] <= args.gamma_threshold_meV:
                if best_exact_gamma_result is None or row["overall_rmse_meV"] < best_exact_gamma_metric:
                    best_exact_gamma_result = result
                    best_exact_gamma_metric = row["overall_rmse_meV"]

    ledger = pd.DataFrame(rows).sort_values(
        ["overall_rmse_meV", "gamma_end_max_abs_delta_meV", "k_b_window_rmse_meV", "k_t_window_rmse_meV"]
    )
    ledger.to_csv(out_dir / "coupled_path_c7_scan.csv", index=False)
    ledger.head(20).to_csv(out_dir / "coupled_path_c7_scan_top20.csv", index=False)

    if best_overall_result is None:
        raise RuntimeError("The coupled scan produced no candidates.")

    if best_exact_gamma_result is not None:
        best_dir = out_dir / "best_exact_gamma_candidate"
        write_candidate_package(best_exact_gamma_result, best_dir)

    summary_lines = [
        "# Coupled Path + Asymmetric sqrt(7) Exact-Gamma Scan Summary",
        "",
        f"- Source origin: {source_origin}",
        f"- K-path ledger: {args.kpath_ledger}",
        f"- Asymmetric sqrt(7) ledger: {args.c7_ledger}",
        f"- Top k-path candidates included: {len(top_kpaths)}",
        f"- Exact-Gamma asymmetric sqrt(7) candidates included: {len(exact_gamma_c7)}",
        f"- Total coupled candidates scanned: {len(ledger)}",
        f"- Gamma acceptance threshold: {args.gamma_threshold_meV:.3f} meV",
        "",
        "## Best overall candidate",
        f"- Path mode: {best_overall_result['path_mode']}",
        f"- K_B label: {best_overall_result['k_b_label']}",
        f"- M label: {best_overall_result['m_label']}",
        f"- K_T label: {best_overall_result['k_t_label']}",
        f"- Mixed-star config: {best_overall_result['mixed_star_config']}",
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
                f"- Path mode: {best_exact_gamma_result['path_mode']}",
                f"- K_B label: {best_exact_gamma_result['k_b_label']}",
                f"- M label: {best_exact_gamma_result['m_label']}",
                f"- K_T label: {best_exact_gamma_result['k_t_label']}",
                f"- Mixed-star config: {best_exact_gamma_result['mixed_star_config']}",
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
            "- coupled_path_c7_scan.csv",
            "- coupled_path_c7_scan_top20.csv",
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
