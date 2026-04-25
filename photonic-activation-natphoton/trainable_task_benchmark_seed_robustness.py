#!/usr/bin/env python3
"""Seed-robustness analysis for the trainable task-level benchmark.

This script reuses the existing trainable benchmark model and asks whether the
main systems-level conclusions survive across multiple independently seeded data
splits and training initializations.
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

import trainable_task_benchmark as base


ROOT = Path("/workspace/memory/photonic-activation-natphoton")
OUTDIR = ROOT / "trainable_task_benchmark_seed_robustness"
ROBUSTNESS_REPEATS = 3
MARGIN_THRESHOLD = 0.02


def evaluate_repeat(repeat_index: int) -> tuple[list[dict[str, float | str | bool | int]], dict[str, float], dict[tuple[str, float, float], dict[str, float | str | bool | int]]]:
    rows: list[dict[str, float | str | bool | int]] = []
    baselines: dict[str, float] = {}
    best_implementable: dict[tuple[str, float, float], dict[str, float | str | bool | int]] = {}

    for task_name in base.TASKS:
        split_seed = base.stable_seed(task_name, "split", "robustness", repeat_index)
        split = base.build_split(task_name, split_seed)
        linear_seed = base.stable_seed(task_name, "linear", "robustness", repeat_index)
        linear_row = base.eval_linear_baseline(split, base.train_linear_baseline(split, linear_seed))
        linear_test = float(linear_row["mean_test_accuracy"])
        baselines[task_name] = linear_test

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
                                task_name,
                                route,
                                eta,
                                total_budget,
                                width,
                                trial,
                                "trainable",
                                "robustness",
                                repeat_index,
                            )
                            params, _ = base.train_hidden_layer(split, width, epsilon, train_seed)
                            val_mean, _ = base.evaluate_with_physical_activation(
                                params,
                                split.x_val,
                                split.y_val,
                                epsilon,
                                base.stable_seed(
                                    task_name,
                                    route,
                                    eta,
                                    total_budget,
                                    width,
                                    trial,
                                    "val",
                                    "robustness",
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
                                    task_name,
                                    route,
                                    eta,
                                    total_budget,
                                    width,
                                    trial,
                                    "test",
                                    "robustness",
                                    repeat_index,
                                ),
                                base.EVAL_TRIALS,
                            )
                            val_scores.append(val_mean)
                            test_scores.append((test_mean, test_std))

                        route_rows.append(
                            {
                                "repeat": repeat_index,
                                "task": task_name,
                                "eta": eta,
                                "total_budget": total_budget,
                                "route": route,
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
                best_implementable[(task_name, eta, total_budget)] = best_row

    return rows, baselines, best_implementable


def write_csv(path: Path, rows: list[dict[str, float | str | bool | int]]) -> None:
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="ascii") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)

    all_rows: list[dict[str, float | str | bool | int]] = []
    per_condition: dict[tuple[str, float, float], list[dict[str, float | str | bool | int]]] = defaultdict(list)
    repeat_counts: list[dict[str, int]] = []

    for repeat_index in range(ROBUSTNESS_REPEATS):
        rows, baselines, best_implementable = evaluate_repeat(repeat_index)
        all_rows.extend(rows)

        activation_beats = 0
        onoff_beats = 0
        for key, row in sorted(best_implementable.items()):
            per_condition[key].append(row)
            if float(row["margin_vs_linear"]) > MARGIN_THRESHOLD:
                activation_beats += 1

        for task_name in base.TASKS:
            for eta in base.ETAS:
                for total_budget in base.TOTAL_BUDGETS:
                    homodyne = next(
                        row
                        for row in rows
                        if row["repeat"] == repeat_index
                        and row["task"] == task_name
                        and row["eta"] == eta
                        and row["total_budget"] == total_budget
                        and row["route"] == "homodyne"
                        and row["selected"]
                    )
                    on_off = next(
                        row
                        for row in rows
                        if row["repeat"] == repeat_index
                        and row["task"] == task_name
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
                "not_worth_count": len(best_implementable) - activation_beats,
                "on_off_beats_homodyne_count": onoff_beats,
            }
        )

    summary_rows = []
    robust_positive = []
    fragile_rows = []
    for key, rows in sorted(per_condition.items()):
        task_name, eta, total_budget = key
        margins = np.array([float(row["margin_vs_linear"]) for row in rows], dtype=float)
        test_accs = np.array([float(row["mean_test_accuracy"]) for row in rows], dtype=float)
        routes = [str(row["route"]) for row in rows]
        width_values = [int(row["width"]) for row in rows]
        linear_accs = np.array([float(row["linear_test_accuracy"]) for row in rows], dtype=float)
        onoff_wins = sum(route == "on_off" for route in routes)
        homodyne_wins = sum(route == "homodyne" for route in routes)

        summary_row = {
            "task": task_name,
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
            "on_off_wins": onoff_wins,
            "homodyne_wins": homodyne_wins,
            "most_common_width": int(np.bincount(np.array(width_values, dtype=int)).argmax()),
        }
        summary_rows.append(summary_row)
        if summary_row["positive_margin_repeats"] == ROBUSTNESS_REPEATS:
            robust_positive.append(summary_row)
        else:
            fragile_rows.append(summary_row)

    write_csv(OUTDIR / "seed_robustness_detail.csv", all_rows)
    write_csv(OUTDIR / "seed_robustness_summary.csv", summary_rows)
    write_csv(OUTDIR / "seed_repeat_counts.csv", repeat_counts)

    payload = {
        "repeats": ROBUSTNESS_REPEATS,
        "margin_threshold": MARGIN_THRESHOLD,
        "repeat_counts": repeat_counts,
        "summary_rows": summary_rows,
        "robust_positive_count": len(robust_positive),
        "fragile_count": len(fragile_rows),
        "all_positive_repeats_count_distribution": sorted(
            [int(row["positive_margin_repeats"]) for row in summary_rows], reverse=True
        ),
    }
    with (OUTDIR / "seed_robustness_summary.json").open("w", encoding="ascii") as handle:
        json.dump(payload, handle, indent=2)

    mean_activation_beats = float(np.mean([row["activation_beats_count"] for row in repeat_counts]))
    min_activation_beats = int(min(row["activation_beats_count"] for row in repeat_counts))
    max_activation_beats = int(max(row["activation_beats_count"] for row in repeat_counts))
    mean_onoff_beats = float(np.mean([row["on_off_beats_homodyne_count"] for row in repeat_counts]))

    lines = [
        "# Trainable Task Benchmark Seed Robustness Summary",
        "",
        "## Purpose",
        "- Test whether the trainable-benchmark systems claim remains stable across independently reseeded data splits and training initializations.",
        f"- Repeats run: {ROBUSTNESS_REPEATS}",
        f"- Positive-margin threshold: margin versus trainable linear baseline > {MARGIN_THRESHOLD:.2f}",
        "",
        "## Headline findings",
        f"- Activation beats the trainable linear baseline in {mean_activation_beats:.1f} of 30 scanned conditions on average across repeats, with a range of {min_activation_beats} to {max_activation_beats}.",
        f"- On-off beats homodyne in {mean_onoff_beats:.1f} of 30 matched task/eta/budget comparisons on average across repeats.",
        f"- {len(robust_positive)} of 30 scanned conditions stay above the +{MARGIN_THRESHOLD:.2f} margin threshold in all {ROBUSTNESS_REPEATS} repeats.",
        f"- {len(fragile_rows)} of 30 scanned conditions change sign or fall below the +{MARGIN_THRESHOLD:.2f} threshold in at least one repeat.",
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
            "## Conditions robustly above the positive-margin threshold in every repeat",
        ]
    )
    if robust_positive:
        for row in robust_positive:
            lines.append(
                f"- {row['task']}, eta={row['eta']:.2f}, budget={row['total_budget']:.1f}: "
                f"mean margin {row['mean_margin_vs_linear']:.3f} +/- {row['std_margin_vs_linear']:.3f}, "
                f"route wins on_off/homodyne = {row['on_off_wins']}/{row['homodyne_wins']}."
            )
    else:
        lines.append("- None.")

    lines.extend(
        [
            "",
            "## Conditions that remain fragile under reseeding",
        ]
    )
    if fragile_rows:
        for row in fragile_rows:
            lines.append(
                f"- {row['task']}, eta={row['eta']:.2f}, budget={row['total_budget']:.1f}: "
                f"mean margin {row['mean_margin_vs_linear']:.3f} +/- {row['std_margin_vs_linear']:.3f}, "
                f"range [{row['min_margin_vs_linear']:.3f}, {row['max_margin_vs_linear']:.3f}], "
                f"positive in {row['positive_margin_repeats']}/{ROBUSTNESS_REPEATS} repeats."
            )
    else:
        lines.append("- None.")

    lines.extend(
        [
            "",
            "## Interpretation bounds",
            "- This is a real seed-robustness check of the existing small trainable benchmark, not a new large-scale learning study.",
            "- It strengthens confidence only if the positive/negative regime split survives reseeding; it does not establish dataset generality, hardware feasibility, or full control-overhead accounting.",
        ]
    )
    (OUTDIR / "seed_robustness_summary.md").write_text("\n".join(lines) + "\n", encoding="ascii")


if __name__ == "__main__":
    main()
