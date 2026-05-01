from __future__ import annotations

import numpy as np

from round6_numpy_passive_d2nn import GOOD_REFERENCE, WRONG_REFERENCE
from round7_parameter_scan import phase_from_coeffs


def mixed_coeffs(coeffs: np.ndarray, pattern: str) -> np.ndarray:
    if pattern == "bandstop_shuffle":
        return np.array([coeffs[2], -coeffs[0], coeffs[3], -coeffs[1]])
    if pattern == "orthogonal_swap":
        return np.array([coeffs[1], -coeffs[0], -coeffs[3], coeffs[2]])
    if pattern == "chirped_reflection":
        return np.array([-coeffs[0], 1.4 * coeffs[3], -1.2 * coeffs[2], coeffs[1]])
    if pattern == "task_decoy":
        return np.array([1.2 * coeffs[0], -1.1 * coeffs[2], coeffs[1], -1.3 * coeffs[3]])
    raise ValueError(pattern)


def wrong_reference_v2(sample, mode: str) -> tuple[np.ndarray, np.ndarray]:
    object_phase = phase_from_coeffs(sample.coeffs)

    if mode == "decoy_bandstop":
        ref_amp = GOOD_REFERENCE
        ref_phase = phase_from_coeffs(1.45 * mixed_coeffs(sample.coeffs, "bandstop_shuffle"))
        return ref_amp, ref_phase

    if mode == "orthogonal_decoy":
        ref_amp = GOOD_REFERENCE
        ref_phase = phase_from_coeffs(1.30 * mixed_coeffs(sample.coeffs, "orthogonal_swap"))
        return ref_amp, ref_phase

    if mode == "chirped_opposition":
        ref_amp = WRONG_REFERENCE
        ref_phase = phase_from_coeffs(1.55 * mixed_coeffs(sample.coeffs, "chirped_reflection"))
        return ref_amp, ref_phase

    if mode == "task_matched_decoy":
        ref_amp = 0.6 * GOOD_REFERENCE + 0.4 * WRONG_REFERENCE
        ref_phase = phase_from_coeffs(1.35 * mixed_coeffs(sample.coeffs, "task_decoy"))
        return np.clip(ref_amp, 0.0, 1.0), ref_phase

    if mode == "anti_phase_plus_decoy":
        ref_amp = WRONG_REFERENCE
        ref_phase = -1.10 * object_phase + 0.65 * phase_from_coeffs(mixed_coeffs(sample.coeffs, "orthogonal_swap"))
        return ref_amp, ref_phase

    raise ValueError(mode)


WRONG_REFERENCE_V2_MODES = [
    "decoy_bandstop",
    "orthogonal_decoy",
    "chirped_opposition",
    "task_matched_decoy",
    "anti_phase_plus_decoy",
]
