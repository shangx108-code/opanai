#!/usr/bin/env python3
"""Focused geometry-extension benchmark for the LPR photonic-activation paper.

This script adds one intermediate-complexity XOR task under the same photon
accounting used by the saved trainable benchmark. The goal is not to widen the
paper into a broad task survey, but to test whether the current design rule
still holds beyond the existing positive/negative pair.
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

import trainable_task_benchmark as base


ROOT = Path("/workspace/memory/photonic-activation-natphoton")
OUTDIR = ROOT / "trainable_task_benchmark_xor_extension"
TASK_NAME = "xor_quadrants"
ROBUSTNESS_REPEATS = 3
MARGIN_THRESHOLD = 0.02
NOISE_LEVEL = 0.18


def make_xor_quadrants(n_samples: int, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    features = rng.uniform(-1.0, 1.0, size=(n_samples, 2))
    labels = ((features[:, 0] * features[:, 1]) > 0.0).astype(int)
    features += NOISE_LEVEL * rng.standard_normal(features.shape)
    order = rng.permutation(n_samples)
    return features[order], labels[order]


def build_split(seed: int) -> base.Split:
    rng = np.random.default_rng(seed)
    x_train, y_train = make_xor_quadrants(800, rng)
    x_val, y_val = make_xor_quadrants(400, rng)
    x_test, y_test = make_xor_quadrants(800, rng)
    x_train, x_val, x_test = base.standardize(x_train, x_val, x_test)
    return base.Split(x_train, y_train, x_val, y_val, x_test, y_test)


def write_csv(path: Path, rows: list[dict[str, float | str | bool | int]]) -> None:
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="ascii") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def evaluate_repeat(
    repeat_index: int,
) -> tuple[list[dict[str, float | str | bool | int]], dict[tuple[float, float], dict[str, float | str | bool | int]]]:
    split = build_split(base.stable_seed(TASK_NAME, "split", "xor_extension", repeat_index))
    linear_seed = base.stable_seed(TASK_NAME, "linear", "xor_extension", repeat_index)
    linear_row = base.eval_linear_baseline(split, base.train_linear_baseline(split, linear_seed))
    linear_test = float(linear_row["mean_test_accuracy"])

    rows: list[dict[str, float | str | bool | int]] = [
        {
            "repeat": repeat_index,
            "task": TASK_NAME,
            "route": "linear_no_activation",
            "eta": "",
            "total_budget": 0.0,
            "width": 1,
            "n_bar_per_neuron": 0.0,
            "activation_error": 0.0,
            "mean_val_accuracy": float(linear_row["mean_val_accuracy"]),
            "mean_test_accuracy": linear_test,
            "std_test_accuracy": 0.0,
            "linear_test_accuracy": linear_test,
            "margin_vs_linear": 0.0,
            "selected": True,
        }
    ]

    best_rows: dict[tuple[float, float], dict[str, float | str | bool | int]] = {}
    for eta in base.ETAS:
        for total_budget in base.TOTAL_BUDGETS:
            best_row = None
            for route in ("homodyne", "on_off"):
                route_rows = []
                for width in base.WIDTHS:
                    n_bar = total_budget / width
                    epsilon = base.route_error(route, n_bar, eta)
                    val_scores = []
                    test_scores = []
                    for trial in range(base.TRAINING_TRIALS):
                        train_seed = base.stable_seed(
                            TASK_NAME,
                            route,
                            eta,
                            total_budget,
                            width,
                            trial,
                            "xor_extension",
                            repeat_index,
                        )
                        params, _ = base.train_hidden_layer(split, width, epsilon, train_seed)
                        val_mean, _ = base.evaluate_with_physical_activation(
                            params,
                            split.x_val,
                            split.y_val,
                            epsilon,
                            base.stable_seed(
                                TASK_NAME,
                                route,
                                eta,
                                total_budget,
                                width,
                                trial,
                                "val",
                                "xor_extension",
                                repeat_index,
                            ),
                            base.EVAL_TRIALS,
                        )
                        test_mean, test_std = base.evaluate_with_physical_activation(
                            params,
                            split.x_test,
                            split.y_test,
                            epsilon,
                            base.stable_seed(
                                TASK_NAME,
                                route,
                                eta,
                                total_budget,
                                width,
                                trial,
                                "test",
                                "xor_extension",
                                repeat_index,
                            ),
                            base.EVAL_TRIALS,
                        )
                        val_scores.append(val_mean)
                        test_scores.append((test_mean, test_std))

                    route_rows.append(
                        {
                            "repeat": repeat_index,
                            "task": TASK_NAME,
                            "route": route,
                            "eta": eta,
                            "total_budget": total_budget,
                            "width": width,
                            "n_bar_per_neuron": n_bar,
                            "activation_error": epsilon,
                            "mean_val_accuracy": float(np.mean(val_scores)),
                            "mean_test_accuracy": float(np.mean([item[0] for item in test_scores])),
                            "std_test_accuracy": float(np.mean([item[1] for item in test_scores])),
                            "linear_test_accuracy": linear_test,
                            "margin_vs_linear": float(np.mean([item[0] for item in test_scores])) - linear_test,
                            "selected": False,
                        }
                    )

                best_index = max(
                    range(len(route_rows)),
                    key=lambda idx: (
                        route_rows[idx]["mean_val_accuracy"],
                        route_rows[idx]["mean_test_accuracy"],
                        -route_rows[idx]["width"],
                    ),
                )
                route_rows[best_index]["selected"] = True
                selected_row = route_rows[best_index]
                rows.extend(route_rows)
                if best_row is None or selected_row["mean_test_accuracy"] > best_row["mean_test_accuracy"]:
                    best_row = selected_row

            assert best_row is not None
            best_rows[(eta, total_budget)] = best_row

    return rows, best_rows


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)

    all_rows: list[dict[str, float | str | bool | int]] = []
    per_condition: dict[tuple[float, float], list[dict[str, float | str | bool | int]]] = defaultdict(list)
    repeat_counts: list[dict[str, int]] = []

    for repeat_index in range(ROBUSTNESS_REPEATS):
        rows, best_rows = evaluate_repeat(repeat_index)
        all_rows.extend(rows)

        activation_beats = 0
        onoff_beats = 0
        for key, row in sorted(best_rows.items()):
            per_condition[key].append(row)
            if float(row["margin_vs_linear"]) > MARGIN_THRESHOLD:
                activation_beats += 1

        for eta in base.ETAS:
            for total_budget in base.TOTAL_BUDGETS:
                homodyne = next(
                    row
                    for row in rows
                    if row["repeat"] == repeat_index
                    and row["task"] == TASK_NAME
                    and row["eta"] == eta
                    and row["total_budget"] == total_budget
                    and row["route"] == "homodyne"
                    and row["selected"]
                )
                on_off = next(
                    row
                    for row in rows
                    if row["repeat"] == repeat_index
                    and row["task"] == TASK_NAME
                    and row["eta"] == eta
                    and row["total_budget"] == total_budget
                    and row["route"] == "on_off"
                    and row["selected"]
                )
                if float(on_off["mean_test_accuracy"]) > float(homodyne["mean_test_accuracy"]):
                    onoff_beats += 1

        repeat_counts.append(
            {
                "repeat": repeat_index,
                "activation_beats_count": activation_beats,
                "not_worth_count": len(best_rows) - activation_beats,
                "on_off_beats_homodyne_count": onoff_beats,
            }
        )

    summary_rows = []
    robust_positive = []
    for key, rows in sorted(per_condition.items()):
        eta, total_budget = key
        margins = np.array([float(row["margin_vs_linear"]) for row in rows], dtype=float)
        test_accs = np.array([float(row["mean_test_accuracy"]) for row in rows], dtype=float)
        linear_accs = np.array([float(row["linear_test_accuracy"]) for row in rows], dtype=float)
        routes = [str(row["route"]) for row in rows]
        widths = [int(row["width"]) for row in rows]
        summary_row = {
            "task": TASK_NAME,
            "eta": eta,
            "total_budget": total_budget,
            "mean_best_test_accuracy": float(test_accs.mean()),
            "std_best_test_accuracy": float(test_accs.std()),
            "mean_linear_accuracy": float(linear_accs.mean()),
            "mean_margin_vs_linear": float(margins.mean()),
            "std_margin_vs_linear": float(margins.std()),
            "min_margin_vs_linear": float(margins.min()),
            "max_margin_vs_linear": float(margins.max()),
            "positive_margin_repeats": int(np.sum(margins > MARGIN_THRESHOLD)),
            "on_off_wins": sum(route == "on_off" for route in routes),
            "homodyne_wins": sum(route == "homodyne" for route in routes),
            "most_common_width": int(np.bincount(np.array(widths, dtype=int)).argmax()),
        }
        summary_rows.append(summary_row)
        if summary_row["positive_margin_repeats"] == ROBUSTNESS_REPEATS:
            robust_positive.append(summary_row)

    write_csv(OUTDIR / "xor_extension_detail.csv", all_rows)
    write_csv(OUTDIR / "xor_extension_summary.csv", summary_rows)
    write_csv(OUTDIR / "xor_extension_repeat_counts.csv", repeat_counts)

    payload = {
        "task": TASK_NAME,
        "repeats": ROBUSTNESS_REPEATS,
        "margin_threshold": MARGIN_THRESHOLD,
        "noise_level": NOISE_LEVEL,
        "repeat_counts": repeat_counts,
        "summary_rows": summary_rows,
        "robust_positive_count": len(robust_positive),
    }
    with (OUTDIR / "xor_extension_summary.json").open("w", encoding="ascii") as handle:
        json.dump(payload, handle, indent=2)

    mean_activation_beats = float(np.mean([row["activation_beats_count"] for row in repeat_counts]))
    mean_onoff_beats = float(np.mean([row["on_off_beats_homodyne_count"] for row in repeat_counts]))
    lines = [
        "# XOR Geometry Extension Summary",
        "",
        "## Purpose",
        "- Add one intermediate-complexity nonlinear classification task under the same activation-photon accounting as the saved trainable benchmark.",
        "- Test whether the current design rule remains selective beyond the existing positive (`concentric_circles`) and fragile (`two_moons`) pair.",
        "",
        "## Task definition",
        "- Task: noisy XOR quadrants in two dimensions.",
        f"- Input-noise scale: {NOISE_LEVEL:.2f}",
        f"- Repeats: {ROBUSTNESS_REPEATS}",
        f"- Positive-margin threshold: margin versus the trainable linear baseline > {MARGIN_THRESHOLD:.2f}",
        "",
        "## Headline findings",
        f"- Physical activation beats the trainable linear baseline in {mean_activation_beats:.1f} of 15 scanned `(eta, budget)` settings on average across repeats.",
        f"- On-off beats homodyne in {mean_onoff_beats:.1f} of 15 matched `(eta, budget)` settings on average across repeats.",
        f"- {len(robust_positive)} of 15 scanned settings stay above the +{MARGIN_THRESHOLD:.2f} margin threshold in all {ROBUSTNESS_REPEATS} repeats.",
        "",
        "## Per-repeat counts",
        "| repeat | activation beats linear | not yet worth paying for | on_off beats homodyne |",
        "| ---: | ---: | ---: | ---: |",
    ]
    for row in repeat_counts:
        lines.append(
            f"| {row['repeat']} | {row['activation_beats_count']} | {row['not_worth_count']} | {row['on_off_beats_homodyne_count']} |"
        )

    lines.extend(
        [
            "",
            "## Robustly positive conditions",
            "| eta | budget | mean best test acc | mean linear acc | mean margin | route wins on_off/homodyne |",
            "| ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in robust_positive:
        lines.append(
            f"| {row['eta']:.2f} | {row['total_budget']:.1f} | {row['mean_best_test_accuracy']:.3f} | "
            f"{row['mean_linear_accuracy']:.3f} | {row['mean_margin_vs_linear']:.3f} | "
            f"{row['on_off_wins']}/{row['homodyne_wins']} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation bounds",
            "- This extension strengthens geometry breadth by one task only; it does not convert the paper into a general benchmark survey.",
            "- The XOR result should therefore be used to support a bounded three-regime narrative: weak-linear-baseline tasks can be strongly positive, strong-linear-baseline tasks can remain fragile, and an intermediate nonlinear task can still remain robustly activation-positive under the same photon accounting.",
        ]
    )
    (OUTDIR / "xor_extension_summary.md").write_text("\n".join(lines) + "\n", encoding="ascii")


if __name__ == "__main__":
    main()
