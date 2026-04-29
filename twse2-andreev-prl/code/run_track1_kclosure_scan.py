from __future__ import annotations

from itertools import permutations
from pathlib import Path

import numpy as np

from twse2_persistent_pipeline import (
    DATA_ROOT,
    B1,
    B2,
    build_hamiltonian,
    build_hops,
    load_tb_source,
    reduced_kvec,
    save_csv,
    save_json,
)


def main() -> None:
    out_dir = DATA_ROOT / "track1-kclosure-2026-04-29"
    out_dir.mkdir(parents=True, exist_ok=True)

    source = load_tb_source().to_numpy()
    hops = build_hops()

    k_candidates = {
        "K1": (2.0 * B1 + B2) / 3.0,
        "K2": (B1 + 2.0 * B2) / 3.0,
        "K3": (B1 - B2) / 3.0,
        "K4": -(2.0 * B1 + B2) / 3.0,
        "K5": -(B1 + 2.0 * B2) / 3.0,
        "K6": -(B1 - B2) / 3.0,
    }
    m_candidates = {
        "M1": (B1 + B2) / 2.0,
        "M2": B1 / 2.0,
        "M3": B2 / 2.0,
    }

    rows: list[list[object]] = []
    best = None
    for (name_kb, k_b), (name_kt, k_t) in permutations(k_candidates.items(), 2):
        for name_m, m_point in m_candidates.items():
            bands = {
                "K_B": np.linalg.eigvalsh(build_hamiltonian(k_b, hops))[::-1],
                "M": np.linalg.eigvalsh(build_hamiltonian(m_point, hops))[::-1],
                "K_T": np.linalg.eigvalsh(build_hamiltonian(k_t, hops))[::-1],
            }
            src = {
                "K_B": source[150],
                "M": source[300],
                "K_T": source[450],
            }
            deltas = {label: bands[label] - src[label] for label in bands}
            rmse = float(np.sqrt(np.mean(np.concatenate([deltas["K_B"], deltas["M"], deltas["K_T"]]) ** 2)))
            row = [
                name_kb,
                name_m,
                name_kt,
                rmse,
                *deltas["K_B"],
                *deltas["M"],
                *deltas["K_T"],
            ]
            rows.append(row)
            if best is None or rmse < best[0]:
                best = (rmse, name_kb, name_m, name_kt, deltas)

    rows.sort(key=lambda item: item[3])
    save_csv(
        out_dir / "kclosure_convention_scan.csv",
        [
            "K_B_choice",
            "M_choice",
            "K_T_choice",
            "rmse_meV",
            "delta_KB_1",
            "delta_KB_2",
            "delta_KB_3",
            "delta_M_1",
            "delta_M_2",
            "delta_M_3",
            "delta_KT_1",
            "delta_KT_2",
            "delta_KT_3",
        ],
        rows,
    )

    top_rows = rows[:10]
    lines = [
        "# Track 1 K-Closure Convention Scan",
        "",
        "This scan treats the current reconstructed hopping table as fixed and only tests whether alternative",
        "high-symmetry-point conventions can reduce the `K^B / K^T` mismatch.",
        "",
        f"- Best high-symmetry RMSE found in this scan: {best[0]:.3f} meV",
        f"- Best convention triple: `K_B={best[1]}`, `M={best[2]}`, `K_T={best[3]}`",
        "- Status: no convention-only candidate in this scan closes the residual exactly; Track 1 remains open.",
        "",
        "Top 10 candidates:",
    ]
    for row in top_rows:
        lines.append(
            f"- K_B={row[0]}, M={row[1]}, K_T={row[2]} | RMSE={row[3]:.3f} meV | "
            f"KB delta=({row[4]:.3f}, {row[5]:.3f}, {row[6]:.3f}) | "
            f"KT delta=({row[10]:.3f}, {row[11]:.3f}, {row[12]:.3f})"
        )
    (out_dir / "summary.md").write_text("\n".join(lines), encoding="utf-8")

    save_json(
        out_dir / "best_candidate.json",
        {
            "best_rmse_meV": best[0],
            "best_K_B_choice": best[1],
            "best_M_choice": best[2],
            "best_K_T_choice": best[3],
            "baseline_path_choice": {
                "K_B": "K1",
                "M": "M1",
                "K_T": "K2",
            },
        },
    )


if __name__ == "__main__":
    main()
