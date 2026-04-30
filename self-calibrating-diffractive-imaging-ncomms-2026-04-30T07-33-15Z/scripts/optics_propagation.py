#!/usr/bin/env python3
"""Fourier-optics propagation helpers with explicit physical coordinates."""

from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np


@dataclass(frozen=True)
class PropagationConfig:
    grid_size: int
    sample_spacing: float
    wavelength: float
    propagation_distance: float

    def to_dict(self) -> dict[str, float]:
        return asdict(self)


def spatial_coordinates(config: PropagationConfig) -> tuple[np.ndarray, np.ndarray]:
    axis = (np.arange(config.grid_size) - config.grid_size // 2) * config.sample_spacing
    xx, yy = np.meshgrid(axis, axis)
    return xx, yy


def frequency_coordinates(config: PropagationConfig) -> tuple[np.ndarray, np.ndarray]:
    freq_axis = np.fft.fftfreq(config.grid_size, d=config.sample_spacing)
    fx, fy = np.meshgrid(freq_axis, freq_axis)
    return fx, fy


def angular_spectrum_kernel(config: PropagationConfig) -> np.ndarray:
    fx, fy = frequency_coordinates(config)
    lambda_fx = config.wavelength * fx
    lambda_fy = config.wavelength * fy
    argument = 1.0 - lambda_fx**2 - lambda_fy**2
    propagating = argument >= 0.0
    kz = np.zeros_like(argument, dtype=np.complex128)
    kz[propagating] = np.sqrt(argument[propagating])
    kz[~propagating] = 1j * np.sqrt(-argument[~propagating])
    phase = 2.0 * np.pi * config.propagation_distance / config.wavelength * kz
    return np.exp(1j * phase)


def fresnel_kernel(config: PropagationConfig) -> np.ndarray:
    fx, fy = frequency_coordinates(config)
    phase = -np.pi * config.wavelength * config.propagation_distance * (fx**2 + fy**2)
    carrier = 2.0 * np.pi * config.propagation_distance / config.wavelength
    return np.exp(1j * carrier) * np.exp(1j * phase)


def propagate_angular_spectrum(field: np.ndarray, config: PropagationConfig) -> np.ndarray:
    kernel = angular_spectrum_kernel(config)
    spectrum = np.fft.fft2(field)
    return np.fft.ifft2(spectrum * kernel)
