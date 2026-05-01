from __future__ import annotations

import numpy as np

from round6_numpy_passive_d2nn import GOOD_REFERENCE, WRONG_REFERENCE, normalize
from round7_parameter_scan import phase_from_coeffs
from wrong_reference_designs_v2 import mixed_coeffs


def edge_map(pattern: np.ndarray) -> np.ndarray:
    gx = np.zeros_like(pattern)
    gy = np.zeros_like(pattern)
    gx[:, 1:-1] = pattern[:, 2:] - pattern[:, :-2]
    gy[1:-1, :] = pattern[2:, :] - pattern[:-2, :]
    return normalize(np.sqrt(gx**2 + gy**2))


def sparse_map(pattern: np.ndarray) -> np.ndarray:
    return normalize(np.clip(pattern, 0.0, 1.0) ** 1.7)


def wrong_reference_v3(sample, mode: str) -> tuple[np.ndarray, np.ndarray]:
    object_phase = phase_from_coeffs(sample.coeffs)
    edges = edge_map(sample.object_pattern)
    sparse = sparse_map(sample.object_pattern)

    if mode == "edge_echo_decoy":
        ref_amp = normalize(0.55 * WRONG_REFERENCE + 0.45 * edges)
        ref_phase = -0.95 * object_phase + 0.80 * phase_from_coeffs(mixed_coeffs(sample.coeffs, "orthogonal_swap"))
        return ref_amp, ref_phase

    if mode == "sparse_tracker_decoy":
        ref_amp = normalize(0.35 * GOOD_REFERENCE + 0.65 * sparse)
        ref_phase = 0.60 * object_phase + 0.85 * phase_from_coeffs(mixed_coeffs(sample.coeffs, "task_decoy"))
        return ref_amp, ref_phase

    if mode == "hybrid_risk_decoy":
        ref_amp = normalize(0.30 * WRONG_REFERENCE + 0.35 * edges + 0.35 * sparse)
        ref_phase = (
            -0.85 * object_phase
            + 0.55 * phase_from_coeffs(mixed_coeffs(sample.coeffs, "orthogonal_swap"))
            + 0.35 * phase_from_coeffs(mixed_coeffs(sample.coeffs, "task_decoy"))
        )
        return ref_amp, ref_phase

    raise ValueError(mode)


WRONG_REFERENCE_V3_MODES = [
    "edge_echo_decoy",
    "sparse_tracker_decoy",
    "hybrid_risk_decoy",
]
