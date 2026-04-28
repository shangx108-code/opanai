from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from reconstruct_tuo_tb import evaluate_candidate, load_source, write_candidate_package


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan k-path mapping conventions for the current Tuo TB candidate.")
    parser.add_argument("--output-dir", type=Path, default=Path("/workspace/output/twse2_k_path_scan"))
    parser.add_argument("--gamma-threshold-meV", type=float, default=0.05)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    out_dir = args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    source, source_origin = load_source()
    k_labels = [
        "K_2b1+b2",
        "K_b1+2b2",
        "K_-b1+b2",
        "K_-2b1-b2",
        "K_-b1-2b2",
        "K_b1-b2",
    ]
    m_labels = ["M_b1", "M_b2", "M_b1+b2"]
    path_modes = ["exclusive_150", "duplicated_150"]

    rows = []
    best_exact_gamma_result = None
    best_exact_gamma_metric = None
    best_overall_result = None

    for path_mode in path_modes:
        for k_b_label in k_labels:
            for k_t_label in k_labels:
                if k_t_label == k_b_label:
                    continue
                for m_label in m_labels:
                    result = evaluate_candidate(path_mode, k_b_label, m_label, k_t_label, source=source)
                    result["source_origin"] = source_origin
                    row = {
                        "path_mode": path_mode,
                        "k_b_label": k_b_label,
                        "m_label": m_label,
                        "k_t_label": k_t_label,
                        "overall_rmse_meV": float(result["overall_rmse"]),
                        "gamma_end_max_abs_delta_meV": float(result["gamma_end_max_abs_delta"]),
                        "k_b_window_rmse_meV": float(result["k_b_rmse_window"]),
                        "m_window_rmse_meV": float(result["m_rmse_window"]),
                        "k_t_window_rmse_meV": float(result["k_t_rmse_window"]),
                        "rowwise_sum_rmse_meV": float(result["rowwise_sum_rmse"]),
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
    ledger.to_csv(out_dir / "k_path_mapping_scan.csv", index=False)
    ledger.head(20).to_csv(out_dir / "k_path_mapping_scan_top20.csv", index=False)

    if best_exact_gamma_result is None or best_overall_result is None:
        raise RuntimeError("Scan did not produce a valid candidate set.")

    best_dir = out_dir / "best_exact_gamma_candidate"
    write_candidate_package(best_exact_gamma_result, best_dir)

    summary_lines = [
        "# K-Path Mapping Scan Summary",
        "",
        f"- Source origin: {source_origin}",
        f"- Total candidates scanned: {len(ledger)}",
        f"- Gamma acceptance threshold: {args.gamma_threshold_meV:.3f} meV",
        "",
        "## Best overall candidate",
        f"- Path mode: {best_overall_result['path_mode']}",
        f"- K_B label: {best_overall_result['k_b_label']}",
        f"- M label: {best_overall_result['m_label']}",
        f"- K_T label: {best_overall_result['k_t_label']}",
        f"- Overall RMSE: {float(best_overall_result['overall_rmse']):.3f} meV",
        f"- Gamma-end max abs delta: {float(best_overall_result['gamma_end_max_abs_delta']):.6f} meV",
        "",
        "## Best exact-Gamma candidate",
        f"- Path mode: {best_exact_gamma_result['path_mode']}",
        f"- K_B label: {best_exact_gamma_result['k_b_label']}",
        f"- M label: {best_exact_gamma_result['m_label']}",
        f"- K_T label: {best_exact_gamma_result['k_t_label']}",
        f"- Overall RMSE: {float(best_exact_gamma_result['overall_rmse']):.3f} meV",
        f"- Gamma-end max abs delta: {float(best_exact_gamma_result['gamma_end_max_abs_delta']):.6f} meV",
        f"- K_B window RMSE: {float(best_exact_gamma_result['k_b_rmse_window']):.3f} meV",
        f"- M window RMSE: {float(best_exact_gamma_result['m_rmse_window']):.3f} meV",
        f"- K_T window RMSE: {float(best_exact_gamma_result['k_t_rmse_window']):.3f} meV",
        "",
        "Generated files:",
        "- k_path_mapping_scan.csv",
        "- k_path_mapping_scan_top20.csv",
        "- best_exact_gamma_candidate/reconstructed_hopping_table.csv",
        "- best_exact_gamma_candidate/band_comparison.csv",
        "- best_exact_gamma_candidate/high_symmetry_residuals.csv",
        "- best_exact_gamma_candidate/band_reconstruction_check.png",
        "- best_exact_gamma_candidate/summary.md",
    ]
    (out_dir / "summary.md").write_text("\n".join(summary_lines), encoding="utf-8")


if __name__ == "__main__":
    main()
