#!/usr/bin/env python3
"""Reproducible same-axis comparison for photonic activation boundary costs."""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Row:
    epsilon: float
    n_lower_bound: float
    n_homodyne: float
    n_kennedy: float


def lower_bound_error(n_bar: float) -> float:
    return 0.5 * (1.0 - math.sqrt(1.0 - math.exp(-4.0 * n_bar)))


def lower_bound_inverse(epsilon: float) -> float:
    return 0.25 * math.log(1.0 / (4.0 * epsilon * (1.0 - epsilon)))


def homodyne_error(n_bar: float, eta: float) -> float:
    return 0.5 * math.erfc(math.sqrt(2.0 * eta * n_bar))


def invert_homodyne_error(epsilon: float, eta: float) -> float:
    lo, hi = 0.0, 20.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if homodyne_error(mid, eta) > epsilon:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def kennedy_error(n_bar: float, eta: float, dark_count: float = 0.0) -> float:
    return 0.5 * (dark_count + (1.0 - dark_count) * math.exp(-4.0 * eta * n_bar))


def invert_kennedy_error(epsilon: float, eta: float, dark_count: float = 0.0) -> float:
    if 2.0 * epsilon <= dark_count:
        raise ValueError(
            "Target error is below the dark-count floor for this Kennedy/on-off model."
        )
    return math.log((1.0 - dark_count) / (2.0 * epsilon - dark_count)) / (4.0 * eta)


def build_rows(eta: float, dark_count: float) -> list[Row]:
    rows = []
    for epsilon in (0.10, 0.05, 0.02, 0.01):
        rows.append(
            Row(
                epsilon=epsilon,
                n_lower_bound=lower_bound_inverse(epsilon),
                n_homodyne=invert_homodyne_error(epsilon, eta),
                n_kennedy=invert_kennedy_error(epsilon, eta, dark_count),
            )
        )
    return rows


def print_table(eta: float, dark_count: float) -> None:
    print(f"# Same-axis comparison for eta={eta:.2f}, dark_count={dark_count:g}")
    print(
        "| epsilon | n_lb | n_homodyne | hom/lb | n_kennedy | ken/lb | hom/ken |"
    )
    print("| --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for row in build_rows(eta, dark_count):
        print(
            "| "
            f"{row.epsilon:.2f} | "
            f"{row.n_lower_bound:.6f} | "
            f"{row.n_homodyne:.6f} | "
            f"{row.n_homodyne / row.n_lower_bound:.3f} | "
            f"{row.n_kennedy:.6f} | "
            f"{row.n_kennedy / row.n_lower_bound:.3f} | "
            f"{row.n_homodyne / row.n_kennedy:.3f} |"
        )


def print_fixed_budget(n_bar: float, dark_count: float) -> None:
    print(f"\n# Fixed photon budget n_bar={n_bar:.2f}, dark_count={dark_count:g}")
    print("| eta | epsilon_lb | epsilon_homodyne | epsilon_kennedy |")
    print("| --- | ---: | ---: | ---: |")
    for eta in (0.99, 0.95, 0.85, 0.70, 0.50):
        print(
            "| "
            f"{eta:.2f} | "
            f"{lower_bound_error(n_bar):.6f} | "
            f"{homodyne_error(n_bar, eta):.6f} | "
            f"{kennedy_error(n_bar, eta, dark_count):.6f} |"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eta", type=float, default=0.85)
    parser.add_argument("--dark-count", type=float, default=0.0)
    parser.add_argument("--n-bar", type=float, default=0.25)
    args = parser.parse_args()

    print_table(args.eta, args.dark_count)
    print_fixed_budget(args.n_bar, args.dark_count)


if __name__ == "__main__":
    main()
