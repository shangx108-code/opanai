from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image


PROJECT_ROOT = Path("/workspace/memory/twse2-andreev-prl")
CODE_ROOT = PROJECT_ROOT / "code"
DATA_ROOT = PROJECT_ROOT / "data"
SOURCE_XLSX = Path("/workspace/tmp/ws2/41467_2025_64519_MOESM3_ESM.xlsx")

SQRT3 = float(np.sqrt(3.0))
SQRT7 = float(np.sqrt(7.0))
OMEGA = np.exp(1j * 2.0 * np.pi / 3.0)

A1 = np.array([1.5, SQRT3 / 2.0])
A2 = np.array([0.0, SQRT3])
RECIPROCAL = 2.0 * np.pi * np.linalg.inv(np.column_stack([A1, A2])).T
B1, B2 = RECIPROCAL[:, 0], RECIPROCAL[:, 1]


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def build_hops() -> dict[tuple[str, str, tuple[float, float]], complex]:
    params = {
        ("A", "A", 0.0): complex(-15.26, 0.0),
        ("B", "B", 0.0): complex(-15.26, 0.0),
        ("C", "C", 0.0): complex(-42.89, 0.0),
        ("B", "B", SQRT3): 5.16 * np.exp(1j * 0.618 * np.pi),
        ("C", "C", SQRT3): complex(2.76, 0.0),
        ("B", "B", 3.0): complex(-0.31, 0.0),
        ("C", "C", 3.0): complex(0.43, 0.0),
        ("A", "B", 1.0): complex(-4.99, 0.0),
        ("B", "C", 1.0): complex(7.12, 0.0),
        ("A", "B", 2.0): complex(0.70, 0.0),
        ("A", "C", 2.0): complex(1.15, 0.0),
        ("A", "B", SQRT7): complex(0.78, 0.0),
        ("A", "C", SQRT7): 3.01 * np.exp(1j * 0.965 * np.pi),
    }

    stars = {
        ("A", "A", SQRT3): [
            np.array([0.0, -SQRT3]),
            np.array([1.5, SQRT3 / 2.0]),
            np.array([-1.5, SQRT3 / 2.0]),
            np.array([0.0, SQRT3]),
            np.array([-1.5, -SQRT3 / 2.0]),
            np.array([1.5, -SQRT3 / 2.0]),
        ],
        ("B", "B", SQRT3): [
            np.array([0.0, -SQRT3]),
            np.array([1.5, SQRT3 / 2.0]),
            np.array([-1.5, SQRT3 / 2.0]),
            np.array([0.0, SQRT3]),
            np.array([-1.5, -SQRT3 / 2.0]),
            np.array([1.5, -SQRT3 / 2.0]),
        ],
        ("C", "C", SQRT3): [
            np.array([0.0, -SQRT3]),
            np.array([1.5, SQRT3 / 2.0]),
            np.array([-1.5, SQRT3 / 2.0]),
            np.array([0.0, SQRT3]),
            np.array([-1.5, -SQRT3 / 2.0]),
            np.array([1.5, -SQRT3 / 2.0]),
        ],
        ("A", "A", 3.0): [
            np.array([-3.0, 0.0]),
            np.array([1.5, -1.5 * SQRT3]),
            np.array([1.5, 1.5 * SQRT3]),
            np.array([3.0, 0.0]),
            np.array([-1.5, 1.5 * SQRT3]),
            np.array([-1.5, -1.5 * SQRT3]),
        ],
        ("B", "B", 3.0): [
            np.array([-3.0, 0.0]),
            np.array([1.5, -1.5 * SQRT3]),
            np.array([1.5, 1.5 * SQRT3]),
            np.array([3.0, 0.0]),
            np.array([-1.5, 1.5 * SQRT3]),
            np.array([-1.5, -1.5 * SQRT3]),
        ],
        ("C", "C", 3.0): [
            np.array([-3.0, 0.0]),
            np.array([1.5, -1.5 * SQRT3]),
            np.array([1.5, 1.5 * SQRT3]),
            np.array([3.0, 0.0]),
            np.array([-1.5, 1.5 * SQRT3]),
            np.array([-1.5, -1.5 * SQRT3]),
        ],
        ("A", "B", 1.0): [
            np.array([-1.0, 0.0]),
            np.array([0.5, -SQRT3 / 2.0]),
            np.array([0.5, SQRT3 / 2.0]),
        ],
        ("A", "B", 2.0): [
            np.array([2.0, 0.0]),
            np.array([-1.0, SQRT3]),
            np.array([-1.0, -SQRT3]),
        ],
        ("A", "B", SQRT7): [
            np.array([-2.5, -SQRT3 / 2.0]),
            np.array([2.0, -SQRT3]),
            np.array([0.5, 1.5 * SQRT3]),
            np.array([2.5, SQRT3 / 2.0]),
            np.array([-2.0, SQRT3]),
            np.array([-0.5, -1.5 * SQRT3]),
        ],
        ("A", "C", 1.0): [
            np.array([1.0, 0.0]),
            np.array([-0.5, SQRT3 / 2.0]),
            np.array([-0.5, -SQRT3 / 2.0]),
        ],
        ("B", "C", 1.0): [
            np.array([-1.0, 0.0]),
            np.array([0.5, -SQRT3 / 2.0]),
            np.array([0.5, SQRT3 / 2.0]),
        ],
        ("A", "C", 2.0): [
            np.array([1.0, -SQRT3]),
            np.array([1.0, SQRT3]),
            np.array([-2.0, 0.0]),
        ],
        ("B", "C", 2.0): [
            np.array([2.0, 0.0]),
            np.array([-1.0, SQRT3]),
            np.array([-1.0, -SQRT3]),
        ],
        ("A", "C", SQRT7): [
            np.array([-0.5, -1.5 * SQRT3]),
            np.array([2.5, -SQRT3 / 2.0]),
            np.array([-2.0, SQRT3]),
            np.array([0.5, 1.5 * SQRT3]),
            np.array([-2.5, SQRT3 / 2.0]),
            np.array([2.0, -SQRT3]),
        ],
        ("B", "C", SQRT7): [
            np.array([2.0, -SQRT3]),
            np.array([-2.5, -SQRT3 / 2.0]),
            np.array([0.5, 1.5 * SQRT3]),
            np.array([-2.0, SQRT3]),
            np.array([2.5, SQRT3 / 2.0]),
            np.array([-0.5, -1.5 * SQRT3]),
        ],
    }

    hops: dict[tuple[str, str, tuple[float, float]], complex] = {}

    for key in [("A", "A", 0.0), ("B", "B", 0.0), ("C", "C", 0.0)]:
        alpha, beta, _ = key
        hops[(alpha, beta, (0.0, 0.0))] = params[key]

    for key in [("C", "C", SQRT3), ("C", "C", 3.0), ("B", "B", SQRT3), ("B", "B", 3.0)]:
        alpha, beta, _ = key
        for vec in stars[key]:
            hops[(alpha, beta, tuple(np.round(vec, 6)))] = params[key]

    for distance in [SQRT3, 3.0]:
        amplitude = np.conj(params[("B", "B", distance)])
        for vec in stars[("A", "A", distance)]:
            hops[("A", "A", tuple(np.round(vec, 6)))] = amplitude

    for key in [("A", "B", 1.0), ("A", "B", 2.0), ("A", "B", SQRT7)]:
        amplitude = params[key]
        for vec in stars[key]:
            hops[("A", "B", tuple(np.round(vec, 6)))] = amplitude
            hops[("B", "A", tuple(np.round(-vec, 6)))] = np.conj(amplitude)

    def add_mixed_star(key: tuple[str, str, float], amplitude: complex, second_orbit_conjugated: bool = False) -> None:
        alpha, beta, _ = key
        vecs = stars[key]
        amp = amplitude
        first_orbit = vecs if len(vecs) == 3 else vecs[:3]
        for vec in first_orbit:
            hops[(alpha, beta, tuple(np.round(vec, 6)))] = amp
            hops[(beta, alpha, tuple(np.round(-vec, 6)))] = np.conj(amp)
            amp *= OMEGA
        if len(vecs) == 6:
            amp = np.conj(amplitude) if second_orbit_conjugated else amplitude
            for vec in vecs[3:]:
                hops[(alpha, beta, tuple(np.round(vec, 6)))] = amp
                hops[(beta, alpha, tuple(np.round(-vec, 6)))] = np.conj(amp)
                amp *= OMEGA

    add_mixed_star(("A", "C", 1.0), params[("B", "C", 1.0)])
    add_mixed_star(("B", "C", 1.0), params[("B", "C", 1.0)])
    add_mixed_star(("A", "C", 2.0), params[("A", "C", 2.0)])
    add_mixed_star(("B", "C", 2.0), params[("A", "C", 2.0)])
    add_mixed_star(("A", "C", SQRT7), params[("A", "C", SQRT7)], second_orbit_conjugated=True)
    add_mixed_star(("B", "C", SQRT7), params[("A", "C", SQRT7)], second_orbit_conjugated=True)
    return hops


def build_hamiltonian(k: np.ndarray, hops: dict[tuple[str, str, tuple[float, float]], complex] | None = None) -> np.ndarray:
    if hops is None:
        hops = build_hops()
    idx = {"A": 0, "B": 1, "C": 2}
    matrix = np.zeros((3, 3), dtype=complex)
    for (alpha, beta, vec), amplitude in hops.items():
        matrix[idx[alpha], idx[beta]] += amplitude * np.exp(1j * np.dot(k, np.array(vec)))
    return matrix


def build_path(num_per_segment: int = 150) -> tuple[np.ndarray, list[int], list[str]]:
    gamma = np.array([0.0, 0.0])
    k_b = (2.0 * B1 + B2) / 3.0
    m = (B1 + B2) / 2.0
    k_t = (B1 + 2.0 * B2) / 3.0
    path = []
    tick_idx = [0]
    for start, end in [(gamma, k_b), (k_b, m), (m, k_t), (k_t, gamma)]:
        for t in np.linspace(0.0, 1.0, num_per_segment, endpoint=False):
            path.append((1.0 - t) * start + t * end)
        tick_idx.append(len(path))
    labels = [r"$\Gamma$", r"$K^B$", r"$M$", r"$K^T$", r"$\Gamma$"]
    return np.asarray(path), tick_idx, labels


def reduced_kvec(k1_red: float, k2_red: float) -> np.ndarray:
    return k1_red * B1 + k2_red * B2


def load_tb_source() -> pd.DataFrame:
    return pd.read_excel(SOURCE_XLSX, sheet_name="Fig1c_EnergyBand")[["E_tb_1", "E_tb_2", "E_tb_3"]]


def load_continuous_source() -> pd.DataFrame:
    return pd.read_excel(SOURCE_XLSX, sheet_name="Fig1c_EnergyBand")[["E_continuous_1", "E_continuous_2", "E_continuous_3"]]


def compute_baseline_bands(hops: dict[tuple[str, str, tuple[float, float]], complex] | None = None) -> tuple[np.ndarray, np.ndarray]:
    if hops is None:
        hops = build_hops()
    path, _, _ = build_path()
    bands = np.asarray([np.linalg.eigvalsh(build_hamiltonian(k, hops))[::-1] for k in path])
    return path, bands


def fourier_chain_blocks(k2_red: float, nk1: int = 256, m_max: int = 2) -> dict[int, np.ndarray]:
    hops = build_hops()
    k1_values = np.arange(nk1) / nk1
    h_of_k = np.asarray([build_hamiltonian(reduced_kvec(k1_red, k2_red), hops) for k1_red in k1_values])
    blocks: dict[int, np.ndarray] = {}
    for m in range(-m_max, m_max + 1):
        phase = np.exp(-1j * 2.0 * np.pi * k1_values * m)
        blocks[m] = np.tensordot(phase, h_of_k, axes=(0, 0)) / nk1
    return blocks


def finite_ribbon_hamiltonian(k2_red: float, num_cells: int = 64, m_max: int = 2) -> np.ndarray:
    blocks = fourier_chain_blocks(k2_red=k2_red, m_max=m_max)
    dim = 3 * num_cells
    h_ribbon = np.zeros((dim, dim), dtype=complex)
    for i in range(num_cells):
        for m, block in blocks.items():
            j = i + m
            if 0 <= j < num_cells:
                h_ribbon[3 * i : 3 * (i + 1), 3 * j : 3 * (j + 1)] += block
    return h_ribbon


def edge_spectral_weight(k2_red: float, energies: np.ndarray, eta: float = 0.6, num_cells: int = 64, edge_cells: int = 2) -> np.ndarray:
    h_ribbon = finite_ribbon_hamiltonian(k2_red=k2_red, num_cells=num_cells)
    dim_edge = 3 * edge_cells
    identity = np.eye(h_ribbon.shape[0], dtype=complex)
    weights = np.zeros_like(energies, dtype=float)
    for idx, energy in enumerate(energies):
        green = np.linalg.inv((energy + 1j * eta) * identity - h_ribbon)
        edge_green = green[:dim_edge, :dim_edge]
        weights[idx] = float(-np.imag(np.trace(edge_green)) / np.pi)
    return weights


def save_csv(path: Path, columns: list[str], rows: list[list[object]]) -> None:
    ensure_dir(path.parent)
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(rows)


def save_json(path: Path, payload: dict[str, object]) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def save_heatmap_png(path: Path, matrix: np.ndarray) -> None:
    ensure_dir(path.parent)
    data = matrix.astype(float)
    data = data - np.min(data)
    scale = np.max(data)
    if scale > 0:
        data = data / scale
    red = np.clip(255.0 * data, 0, 255).astype(np.uint8)
    blue = np.clip(255.0 * (1.0 - data), 0, 255).astype(np.uint8)
    green = np.clip(255.0 * (0.5 - np.abs(data - 0.5)), 0, 255).astype(np.uint8)
    rgb = np.stack([red, green, blue], axis=-1)
    Image.fromarray(rgb[::-1], mode="RGB").save(path)
