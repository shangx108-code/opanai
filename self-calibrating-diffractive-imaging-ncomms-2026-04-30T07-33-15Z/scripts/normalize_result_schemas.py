from __future__ import annotations

import csv
import re
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path("/workspace/memory/self-calibrating-diffractive-imaging-ncomms-2026-04-30T07-33-15Z")
OUT_DIR = PROJECT_ROOT / "source_data" / "normalized_results_v1"


def ensure_out_dir() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)


def parse_ci_interval(value: str) -> tuple[float | None, float | None]:
    if not isinstance(value, str):
        return None, None
    match = re.match(r"\[\s*([-+0-9.eE]+)\s*,\s*([-+0-9.eE]+)\s*\]", value)
    if not match:
        return None, None
    return float(match.group(1)), float(match.group(2))


def add_condition_columns(df: pd.DataFrame, family_col: str = "condition_family", level_col: str = "condition_level") -> pd.DataFrame:
    if family_col in df.columns and level_col in df.columns:
        df["condition"] = df[family_col].astype(str) + ":" + df[level_col].astype(str)
    return df


def normalize_unified_detail() -> Path:
    src = PROJECT_ROOT / "results/unified_comparison/unified_comparison_detail.csv"
    df = pd.read_csv(src)
    df = df.rename(
        columns={
            "object_id": "sample_id",
            "case_id": "aberration_id",
            "fixed_psnr_lowres": "psnr_fixed",
            "method_psnr_lowres": "psnr_method",
            "psnr_gain_over_fixed_lowres": "psnr_gain",
        }
    )
    df["dataset_name"] = "synthetic_dual_ledger"
    df["dataset_version"] = "registered_dual_ledger_v1"
    df["object_family"] = pd.NA
    out = OUT_DIR / "unified_comparison_detail_canonical.csv"
    df.to_csv(out, index=False)
    return out


def normalize_unified_per_seed() -> Path:
    src = PROJECT_ROOT / "results/unified_comparison/unified_comparison_per_seed.csv"
    df = pd.read_csv(src)
    df["aggregation_scope"] = "dual_ledger_pooled"
    df["n_samples"] = pd.NA
    out = OUT_DIR / "unified_comparison_per_seed_canonical.csv"
    df.to_csv(out, index=False)
    return out


def normalize_unified_summary() -> Path:
    src = PROJECT_ROOT / "results/unified_comparison_ci.csv"
    df = pd.read_csv(src)
    ci = df["95% CI"].apply(parse_ci_interval)
    df["ci_low"] = [x[0] for x in ci]
    df["ci_high"] = [x[1] for x in ci]
    df = df.rename(columns={"std": "std_psnr_gain"})
    df["n_seeds"] = 10
    df["n_samples"] = pd.NA
    df["aggregation_scope"] = "dual_ledger_pooled"
    df = df.drop(columns=["95% CI"])
    out = OUT_DIR / "unified_comparison_summary_canonical.csv"
    df.to_csv(out, index=False)
    return out


def normalize_by_ledger() -> Path:
    src = PROJECT_ROOT / "results/tables/unified_comparison_by_ledger.csv"
    df = pd.read_csv(src)
    if "std_psnr_gain" not in df.columns and "std" in df.columns:
        df = df.rename(columns={"std": "std_psnr_gain"})
    if "ci95_half_width" not in df.columns and "ci_half_width" in df.columns:
        df = df.rename(columns={"ci_half_width": "ci95_half_width"})
    if "n_seeds" not in df.columns:
        df["n_seeds"] = 10
    if "n_samples" not in df.columns:
        df["n_samples"] = pd.NA
    out = OUT_DIR / "unified_comparison_by_ledger_canonical.csv"
    df.to_csv(out, index=False)
    return out


def normalize_natural_metrics(src_rel: str, out_name: str, include_seed: bool) -> Path:
    src = PROJECT_ROOT / src_rel
    df = pd.read_csv(src)
    df = df.rename(
        columns={
            "object_id": "sample_id",
            "case_id": "aberration_id",
            "fixed_psnr_lowres": "psnr_fixed",
            "guided_psnr_lowres": "psnr_guided",
            "pipeline_psnr_lowres": "psnr_method",
            "psnr_gain_over_fixed_lowres": "psnr_gain",
            "psnr_gap_to_guided_lowres": "psnr_gap_to_guided",
        }
    )
    if not include_seed:
        df["seed"] = pd.NA
    df["method"] = "phase_only_stack"
    df["object_family"] = pd.NA
    df["better_than_fixed"] = df["psnr_gain"] > 0
    out = OUT_DIR / out_name
    df.to_csv(out, index=False)
    return out


def normalize_tolerance_metrics() -> Path:
    src = PROJECT_ROOT / "results/tolerance/mixed_train_tolerance_metrics.csv"
    df = pd.read_csv(src)
    df = df.rename(
        columns={
            "object_id": "sample_id",
            "fixed_psnr_lowres": "psnr_fixed",
            "guided_psnr_lowres": "psnr_guided",
            "method_psnr_lowres": "psnr_method",
            "psnr_gain_over_fixed_lowres": "psnr_gain",
            "perturbation_family": "condition_family",
            "level": "condition_level",
        }
    )
    df["object_family"] = pd.NA
    df["aberration_id"] = pd.NA
    df["better_than_fixed"] = df["psnr_gain"] > 0
    df = add_condition_columns(df)
    out = OUT_DIR / "mixed_train_tolerance_metrics_canonical.csv"
    df.to_csv(out, index=False)
    return out


def normalize_robust_tolerance_metrics() -> Path:
    src = PROJECT_ROOT / "results/tolerance/robust_mask_tolerance_metrics.csv"
    df = pd.read_csv(src)
    df = df.rename(
        columns={
            "object_id": "sample_id",
            "fixed_psnr_lowres": "psnr_fixed",
            "robust_method_psnr_lowres": "psnr_method",
            "psnr_gain_over_fixed_lowres": "psnr_gain",
            "perturbation_family": "condition_family",
            "level": "condition_level",
        }
    )
    df["method"] = "robust_phase_only_stack"
    df["object_family"] = pd.NA
    df["aberration_id"] = pd.NA
    df["psnr_guided"] = pd.NA
    df["better_than_fixed"] = df["psnr_gain"] > 0
    df = add_condition_columns(df)
    out = OUT_DIR / "robust_mask_tolerance_metrics_canonical.csv"
    df.to_csv(out, index=False)
    return out


def normalize_robust_tolerance_compare() -> Path:
    src = PROJECT_ROOT / "results/tolerance/robust_mask_tolerance_compare.csv"
    df = pd.read_csv(src)
    df = df.rename(columns={"perturbation_family": "condition_family", "level": "condition_level"})
    df = add_condition_columns(df)
    out = OUT_DIR / "robust_mask_tolerance_compare_canonical.csv"
    df.to_csv(out, index=False)
    return out


def normalize_failure_cases() -> Path:
    src = PROJECT_ROOT / "results/failure_cases/object_shift_failure_cases.csv"
    df = pd.read_csv(src)
    df = df.rename(
        columns={
            "object_id": "sample_id",
            "case_id": "aberration_id",
            "object_label": "object_family",
            "fixed_psnr_lowres": "psnr_fixed",
            "phase_psnr_lowres": "psnr_method",
            "psnr_gain_over_fixed_lowres": "psnr_gain",
        }
    )
    df["method"] = "phase_only_stack"
    df["dataset_name"] = "synthetic_dual_ledger"
    df["dataset_version"] = "registered_dual_ledger_v1"
    df["better_than_fixed"] = df["psnr_gain"] > 0
    out = OUT_DIR / "object_shift_failure_cases_canonical.csv"
    df.to_csv(out, index=False)
    return out


def normalize_fairness_table() -> Path:
    src = PROJECT_ROOT / "results/tables/method_fairness_table.csv"
    df = pd.read_csv(src)
    df = df.rename(columns={"training_samples": "train_data_count"})
    df["total_trainable_parameters"] = df["optical_trainable_parameters"] + df["digital_trainable_parameters"]
    df["uses_reference_channel_at_test_time"] = "yes"
    role_map = {
        "phase_only_stack": "proposed hybrid",
        "reference_psf_deconvolution": "reference-guided classical comparator",
        "parameter_matched_digital_surrogate": "parameter-matched digital comparator",
        "spectral_frontend": "learned spectral comparator",
        "trainable_surrogate_ridge": "digital comparator",
    }
    note_map = {
        "phase_only_stack": "Optical and digital capacity should be interpreted jointly.",
        "reference_psf_deconvolution": "Uses explicit test-time reference PSF information.",
        "parameter_matched_digital_surrogate": "Digital-only comparator with the same trainable parameter count as the phase_only_stack ridge stage.",
        "spectral_frontend": "Digital learned comparator with Fourier-cropped inputs.",
        "trainable_surrogate_ridge": "Digital learned comparator without optical trainable parameters.",
    }
    df["comparator_role"] = df["method"].map(role_map).fillna("unspecified")
    df["notes"] = df["method"].map(note_map).fillna("")
    out = OUT_DIR / "method_fairness_table_canonical.csv"
    df.to_csv(out, index=False)
    return out


def write_readme(outputs: list[Path]) -> Path:
    readme = OUT_DIR / "README.md"
    with readme.open("w", newline="") as f:
        f.write("# Normalized Results v1\n\n")
        f.write("These files are canonicalized exports derived from the current executed result tables.\n")
        f.write("They do not overwrite the original result files. Missing values indicate fields not present in the current raw exports.\n\n")
        f.write("## Files\n")
        for path in outputs:
            f.write(f"- `{path.name}`\n")
    return readme


def write_manifest(outputs: list[Path]) -> Path:
    manifest = OUT_DIR / "manifest.csv"
    with manifest.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["file"])
        for path in outputs:
            writer.writerow([path.name])
    return manifest


def main() -> None:
    ensure_out_dir()
    outputs = [
        normalize_unified_detail(),
        normalize_unified_per_seed(),
        normalize_unified_summary(),
        normalize_by_ledger(),
        normalize_natural_metrics(
            "results/natural_objects/natural_object_metrics.csv",
            "natural_object_metrics_canonical.csv",
            include_seed=False,
        ),
        normalize_natural_metrics(
            "results/natural_objects/mixed_train_natural_object_metrics.csv",
            "mixed_train_natural_object_metrics_canonical.csv",
            include_seed=False,
        ),
        normalize_natural_metrics(
            "results/natural_objects/mixed_train_natural_object_thickstats_metrics.csv",
            "mixed_train_natural_object_thickstats_metrics_canonical.csv",
            include_seed=True,
        ),
        normalize_tolerance_metrics(),
        normalize_robust_tolerance_metrics(),
        normalize_robust_tolerance_compare(),
        normalize_failure_cases(),
        normalize_fairness_table(),
    ]
    outputs.append(write_readme(outputs))
    outputs.append(write_manifest(outputs))
    print(f"Wrote {len(outputs)} files to {OUT_DIR}")


if __name__ == "__main__":
    main()
