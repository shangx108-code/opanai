from __future__ import annotations

import argparse
import json
from itertools import product
from pathlib import Path

import pandas as pd

from reconstruct_tuo_tb import evaluate_candidate, load_source, write_candidate_package


DEFAULT_KPATH_LEDGER = Path(
    "/workspace/memory/twse2-andreev-prl/data/track1-2026-04-28-kpath-scan/k_path_mapping_scan.csv"
)
DEFAULT_OUTPUT_DIR = Path("/workspace/output/twse2_joint_valley_layer_scan")
PHASE_PATTERNS = ["const", "cyc", "anti"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Broader coupled valley-specific scan: around the top path mappings, jointly release "
            "short-range and sqrt(7) A-C / B-C phase rules."
        )
    )
    parser.add_argument("--kpath-ledger", type=Path, default=DEFAULT_KPATH_LEDGER)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--top-kpaths", type=int, default=2)
    parser.add_argument("--path-rank-start", type=int, default=1)
    parser.add_argument("--path-rank-stop", type=int, default=None)
    parser.add_argument("--chunk-size", type=int, default=1000)
    parser.add_argument("--config-limit", type=int, default=None)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--gamma-threshold-meV", type=float, default=0.05)
    return parser.parse_args()


def load_top_kpaths(path: Path, top_n: int) -> pd.DataFrame:
    ledger = pd.read_csv(path)
    ranked = ledger.sort_values(
        ["overall_rmse_meV", "gamma_end_max_abs_delta_meV", "k_b_window_rmse_meV", "k_t_window_rmse_meV"]
    )
    return ranked.head(top_n).reset_index(drop=True)


def iter_joint_configs():
    for ac1_pattern, bc1_pattern, ac2_pattern, bc2_pattern in product(PHASE_PATTERNS, repeat=4):
        for ac7_first_pattern, bc7_first_pattern, ac7_second_pattern, bc7_second_pattern in product(
            PHASE_PATTERNS, repeat=4
        ):
            for ac7_second_conjugated, bc7_second_conjugated in product([False, True], repeat=2):
                yield {
                    "ac1_pattern": ac1_pattern,
                    "bc1_pattern": bc1_pattern,
                    "ac2_pattern": ac2_pattern,
                    "bc2_pattern": bc2_pattern,
                    "ac7_first_pattern": ac7_first_pattern,
                    "bc7_first_pattern": bc7_first_pattern,
                    "ac7_second_pattern": ac7_second_pattern,
                    "bc7_second_pattern": bc7_second_pattern,
                    "ac7_second_conjugated": ac7_second_conjugated,
                    "bc7_second_conjugated": bc7_second_conjugated,
                }


def finalize_outputs(
    out_dir: Path,
    source_origin: str,
    gamma_threshold_meV: float,
) -> None:
    chunk_files = sorted(out_dir.glob("path*_chunk*.csv"))
    if not chunk_files:
        raise RuntimeError("No chunk files were produced.")

    ledger = pd.concat((pd.read_csv(path) for path in chunk_files), ignore_index=True).sort_values(
        ["overall_rmse_meV", "gamma_end_max_abs_delta_meV", "k_b_window_rmse_meV", "k_t_window_rmse_meV"]
    )
    ledger.to_csv(out_dir / "joint_valley_layer_scan.csv", index=False)
    ledger.head(20).to_csv(out_dir / "joint_valley_layer_scan_top20.csv", index=False)

    exact_gamma = ledger[ledger["gamma_end_max_abs_delta_meV"] <= gamma_threshold_meV].copy()
    exact_gamma.to_csv(out_dir / "joint_valley_layer_scan_exact_gamma.csv", index=False)
    exact_gamma.head(20).to_csv(out_dir / "joint_valley_layer_scan_exact_gamma_top20.csv", index=False)

    best_overall_row = ledger.iloc[0]
    best_exact_gamma_row = exact_gamma.iloc[0] if not exact_gamma.empty else None

    summary_lines = [
        "# Joint Valley-Layer Scan Summary",
        "",
        f"- Source origin: {source_origin}",
        f"- Total coupled candidates scanned: {len(ledger)}",
        f"- Gamma acceptance threshold: {gamma_threshold_meV:.3f} meV",
        f"- Exact-Gamma coupled candidates: {len(exact_gamma)}",
        f"- Chunk files: {len(chunk_files)}",
        "",
        "## Best overall candidate",
        f"- Path rank: {int(best_overall_row['path_rank'])}",
        f"- Config rank: {int(best_overall_row['config_rank'])}",
        f"- Path mode: {best_overall_row['path_mode']}",
        f"- K_B label: {best_overall_row['k_b_label']}",
        f"- M label: {best_overall_row['m_label']}",
        f"- K_T label: {best_overall_row['k_t_label']}",
        f"- Overall RMSE: {float(best_overall_row['overall_rmse_meV']):.3f} meV",
        f"- Gamma-end max abs delta: {float(best_overall_row['gamma_end_max_abs_delta_meV']):.6f} meV",
        f"- K_B window RMSE: {float(best_overall_row['k_b_window_rmse_meV']):.3f} meV",
        f"- M window RMSE: {float(best_overall_row['m_window_rmse_meV']):.3f} meV",
        f"- K_T window RMSE: {float(best_overall_row['k_t_window_rmse_meV']):.3f} meV",
        "",
    ]

    if best_exact_gamma_row is None:
        summary_lines.extend(["## Best exact-Gamma candidate", "- none within the current acceptance threshold", ""])
    else:
        summary_lines.extend(
            [
                "## Best exact-Gamma candidate",
                f"- Path rank: {int(best_exact_gamma_row['path_rank'])}",
                f"- Config rank: {int(best_exact_gamma_row['config_rank'])}",
                f"- Path mode: {best_exact_gamma_row['path_mode']}",
                f"- K_B label: {best_exact_gamma_row['k_b_label']}",
                f"- M label: {best_exact_gamma_row['m_label']}",
                f"- K_T label: {best_exact_gamma_row['k_t_label']}",
                f"- Overall RMSE: {float(best_exact_gamma_row['overall_rmse_meV']):.3f} meV",
                f"- Gamma-end max abs delta: {float(best_exact_gamma_row['gamma_end_max_abs_delta_meV']):.6f} meV",
                f"- K_B window RMSE: {float(best_exact_gamma_row['k_b_window_rmse_meV']):.3f} meV",
                f"- M window RMSE: {float(best_exact_gamma_row['m_window_rmse_meV']):.3f} meV",
                f"- K_T window RMSE: {float(best_exact_gamma_row['k_t_window_rmse_meV']):.3f} meV",
                "",
            ]
        )

    summary_lines.extend(
        [
            "Generated files:",
            "- joint_valley_layer_scan.csv",
            "- joint_valley_layer_scan_top20.csv",
            "- joint_valley_layer_scan_exact_gamma.csv",
            "- joint_valley_layer_scan_exact_gamma_top20.csv",
            "- progress.json",
            "- path*_chunk*.csv",
        ]
    )
    (out_dir / "summary.md").write_text("\n".join(summary_lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    out_dir = args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    top_kpaths = load_top_kpaths(args.kpath_ledger, args.top_kpaths)
    if top_kpaths.empty:
        raise RuntimeError("No k-path candidates were loaded.")
    path_rank_stop = args.path_rank_stop if args.path_rank_stop is not None else len(top_kpaths)
    selected_kpaths = top_kpaths.iloc[args.path_rank_start - 1 : path_rank_stop].reset_index(drop=True)
    if selected_kpaths.empty:
        raise RuntimeError("Selected path-rank window is empty.")

    source, source_origin = load_source()
    all_configs = list(iter_joint_configs())
    total_configs = len(all_configs) if args.config_limit is None else min(len(all_configs), args.config_limit)
    progress_path = out_dir / "progress.json"

    for local_path_index, kpath_row in selected_kpaths.iterrows():
        original_path_rank = args.path_rank_start + local_path_index
        start_config_rank = 1
        chunk_id = 1
        if args.resume and progress_path.exists():
            progress_payload = json.loads(progress_path.read_text(encoding="utf-8"))
            same_window = (
                int(progress_payload.get("path_rank_start", -1)) == int(args.path_rank_start)
                and int(progress_payload.get("path_rank_stop", -1)) == int(path_rank_stop)
                and int(progress_payload.get("top_kpaths", -1)) == int(args.top_kpaths)
            )
            if same_window and int(progress_payload.get("current_path_rank", -1)) == int(original_path_rank):
                start_config_rank = int(progress_payload.get("last_completed_config_rank", 0)) + 1
                chunk_id = len(sorted(out_dir.glob(f"path{original_path_rank:02d}_chunk*.csv"))) + 1
            elif same_window and int(progress_payload.get("current_path_rank", -1)) > int(original_path_rank):
                start_config_rank = total_configs + 1
                chunk_id = len(sorted(out_dir.glob(f"path{original_path_rank:02d}_chunk*.csv"))) + 1

        if start_config_rank > total_configs:
            continue

        chunk_rows = []
        for config_rank, mixed_star_config in enumerate(all_configs[start_config_rank - 1 : total_configs], start=start_config_rank):
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
                "path_rank": int(original_path_rank),
                "config_rank": int(config_rank),
                "path_mode": str(kpath_row["path_mode"]),
                "k_b_label": str(kpath_row["k_b_label"]),
                "m_label": str(kpath_row["m_label"]),
                "k_t_label": str(kpath_row["k_t_label"]),
                **mixed_star_config,
                "overall_rmse_meV": float(result["overall_rmse"]),
                "gamma_end_max_abs_delta_meV": float(result["gamma_end_max_abs_delta"]),
                "k_b_window_rmse_meV": float(result["k_b_rmse_window"]),
                "m_window_rmse_meV": float(result["m_rmse_window"]),
                "k_t_window_rmse_meV": float(result["k_t_rmse_window"]),
                "rowwise_sum_rmse_meV": float(result["rowwise_sum_rmse"]),
                "valley_window_gap_meV": abs(float(result["k_b_rmse_window"]) - float(result["k_t_rmse_window"])),
            }
            chunk_rows.append(row)

            if len(chunk_rows) >= args.chunk_size or config_rank == total_configs:
                chunk_df = pd.DataFrame(chunk_rows).sort_values(
                    ["overall_rmse_meV", "gamma_end_max_abs_delta_meV", "k_b_window_rmse_meV", "k_t_window_rmse_meV"]
                )
                chunk_df.to_csv(out_dir / f"path{original_path_rank:02d}_chunk{chunk_id:03d}.csv", index=False)
                chunk_rows = []
                chunk_id += 1

                progress_payload = {
                    "source_origin": source_origin,
                    "kpath_ledger": str(args.kpath_ledger),
                    "top_kpaths": int(args.top_kpaths),
                    "path_rank_start": int(args.path_rank_start),
                    "path_rank_stop": int(path_rank_stop),
                    "current_path_rank": int(original_path_rank),
                    "last_completed_config_rank": int(config_rank),
                    "total_configs_per_path": int(total_configs),
                    "chunk_size": int(args.chunk_size),
                    "gamma_threshold_meV": float(args.gamma_threshold_meV),
                }
                progress_path.write_text(json.dumps(progress_payload, indent=2), encoding="utf-8")

    finalize_outputs(out_dir=out_dir, source_origin=source_origin, gamma_threshold_meV=args.gamma_threshold_meV)

    exact_gamma_path = out_dir / "joint_valley_layer_scan_exact_gamma.csv"
    exact_gamma = pd.read_csv(exact_gamma_path)
    if not exact_gamma.empty:
        best_exact_gamma_row = exact_gamma.sort_values(
            ["overall_rmse_meV", "gamma_end_max_abs_delta_meV", "k_b_window_rmse_meV", "k_t_window_rmse_meV"]
        ).iloc[0]
        best_exact_gamma_result = evaluate_candidate(
            str(best_exact_gamma_row["path_mode"]),
            str(best_exact_gamma_row["k_b_label"]),
            str(best_exact_gamma_row["m_label"]),
            str(best_exact_gamma_row["k_t_label"]),
            source=source,
            mixed_star_config={
                "ac1_pattern": str(best_exact_gamma_row["ac1_pattern"]),
                "bc1_pattern": str(best_exact_gamma_row["bc1_pattern"]),
                "ac2_pattern": str(best_exact_gamma_row["ac2_pattern"]),
                "bc2_pattern": str(best_exact_gamma_row["bc2_pattern"]),
                "ac7_first_pattern": str(best_exact_gamma_row["ac7_first_pattern"]),
                "bc7_first_pattern": str(best_exact_gamma_row["bc7_first_pattern"]),
                "ac7_second_pattern": str(best_exact_gamma_row["ac7_second_pattern"]),
                "bc7_second_pattern": str(best_exact_gamma_row["bc7_second_pattern"]),
                "ac7_second_conjugated": bool(best_exact_gamma_row["ac7_second_conjugated"]),
                "bc7_second_conjugated": bool(best_exact_gamma_row["bc7_second_conjugated"]),
            },
        )
        write_candidate_package(best_exact_gamma_result, out_dir / "best_exact_gamma_candidate")


if __name__ == "__main__":
    main()
