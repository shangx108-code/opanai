from __future__ import annotations

from pathlib import Path

import numpy as np

from twse2_persistent_pipeline import DATA_ROOT, edge_spectral_weight, save_csv, save_heatmap_png, save_json


def main() -> None:
    out_dir = DATA_ROOT / "sgf-minimal-2026-04-29"
    out_dir.mkdir(parents=True, exist_ok=True)

    k2_grid = np.linspace(0.0, 1.0, 81, endpoint=False)
    energy_grid = np.linspace(-80.0, 20.0, 201)
    eta = 0.8
    num_cells = 72
    edge_cells = 2

    spectral_map = np.zeros((len(k2_grid), len(energy_grid)))
    for i, k2_red in enumerate(k2_grid):
        spectral_map[i] = edge_spectral_weight(
            k2_red=k2_red,
            energies=energy_grid,
            eta=eta,
            num_cells=num_cells,
            edge_cells=edge_cells,
        )

    rows: list[list[object]] = []
    for i, k2_red in enumerate(k2_grid):
        for j, energy in enumerate(energy_grid):
            rows.append([float(k2_red), float(energy), float(spectral_map[i, j])])
    save_csv(out_dir / "edge_spectral_map.csv", ["k2_reduced", "energy_meV", "edge_spectral_weight"], rows)
    save_heatmap_png(out_dir / "edge_spectral_map.png", spectral_map)

    zero_idx = int(np.argmin(np.abs(energy_grid)))
    zero_bias_rows = [[float(k2), float(spectral_map[i, zero_idx])] for i, k2 in enumerate(k2_grid)]
    save_csv(out_dir / "zero_bias_edge_profile.csv", ["k2_reduced", "edge_spectral_weight_E0"], zero_bias_rows)

    save_json(
        out_dir / "parameters.json",
        {
            "package_type": "finite_ribbon_edge_greens_proxy",
            "k2_grid_size": len(k2_grid),
            "energy_grid_size": len(energy_grid),
            "eta_meV": eta,
            "num_cells_open_direction": num_cells,
            "edge_cells_measured": edge_cells,
            "note": "This is a minimal edge Green's proxy extracted from the current Track-1 tight-binding candidate; it is not yet a final semi-infinite SGF benchmark.",
        },
    )

    summary = [
        "# SGF Minimal Data Package",
        "",
        "- Data status: generated",
        "- Method status: finite-ribbon edge Green's proxy from the current Track-1 TB candidate",
        f"- k2 grid size: {len(k2_grid)}",
        f"- energy grid size: {len(energy_grid)}",
        f"- Broadening eta: {eta:.2f} meV",
        f"- Maximum zero-bias edge spectral weight: {float(np.max(spectral_map[:, zero_idx])):.4f}",
        f"- Mean zero-bias edge spectral weight: {float(np.mean(spectral_map[:, zero_idx])):.4f}",
        "- Caution: this package is suitable as a persistent minimal edge-spectrum baseline, not yet a final manuscript-grade semi-infinite SGF result.",
    ]
    (out_dir / "summary.md").write_text("\n".join(summary), encoding="utf-8")


if __name__ == "__main__":
    main()
