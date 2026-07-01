#!/usr/bin/env python3
"""
Aggregate per-class CSVs into paper-style tables (Tables 2-4).

Usage:
    python 05_aggregate_tables.py
    python 05_aggregate_tables.py --figures
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config" / "projects.json"
PER_CLASS_DIR = ROOT / "results" / "per-class"
OUT_DIR = ROOT / "results" / "processed"

ORIGIN_LABELS = {
    "developer": "Developer",
    "opus-4.5": "Opus 4.5",
    "sonnet-4.5": "Sonnet 4.5",
    "gpt-5.1-codex-max": "GPT-5.1 Codex Max",
}

PROJECT_LABELS = {
    "bcel": "Commons BCEL",
    "cli": "Commons CLI",
    "collections": "Commons Collections",
    "compress": "Commons Compress",
    "lang": "Commons Lang",
}

PROJECT_ORDER = ["collections", "compress", "lang", "cli", "bcel"]
ORIGIN_ORDER = ["developer", "opus-4.5", "gpt-5.1-codex-max", "sonnet-4.5"]


def load_config() -> dict:
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


def project_ids_from_config(config: dict) -> list[str]:
    return [p["id"] for p in config["projects"]]


def read_published_metrics() -> dict[str, dict[str, list[dict]]]:
    """Return {project_id: {origin_id: [rows]}} from results/per-class/*.csv."""
    grouped: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))

    if not PER_CLASS_DIR.exists():
        raise SystemExit(
            f"No published metrics in {PER_CLASS_DIR}. "
            "Run scripts/organize_published_metrics.py first."
        )

    for csv_path in sorted(PER_CLASS_DIR.glob("*.csv")):
        with open(csv_path, newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                project_id = row["project_id"]
                origin_id = row["origin_id"]
                grouped[project_id][origin_id].append(row)

    return grouped


def stats(values: list[float]) -> tuple[float, float, float]:
    if not values:
        return 0.0, 0.0, 0.0
    mean = statistics.mean(values)
    median = statistics.median(values)
    stdev = statistics.stdev(values) if len(values) > 1 else 0.0
    return round(mean, 2), round(median, 2), round(stdev, 2)


def float_field(row: dict, key: str) -> float:
    value = row.get(key, "")
    if value in ("", None):
        return 0.0
    return float(value)


def int_field(row: dict, key: str) -> int:
    value = row.get(key, "")
    if value in ("", None):
        return 0
    return int(float(value))


def aggregate_table2(grouped: dict[str, dict[str, list[dict]]]) -> Path:
    rows = []
    for project_id in PROJECT_ORDER:
        origins = grouped.get(project_id, {})
        for origin_id in ORIGIN_ORDER:
            data = origins.get(origin_id, [])
            if not data:
                continue
            values = [float_field(r, "line_coverage_pct") for r in data]
            mean, median, stdev = stats(values)
            rows.append(
                {
                    "project": PROJECT_LABELS.get(project_id, project_id),
                    "test_suite_origin": ORIGIN_LABELS.get(origin_id, origin_id),
                    "mean_pct": mean,
                    "median_pct": median,
                    "std_dev_pct": stdev,
                    "n_classes": len(values),
                }
            )

    out_path = OUT_DIR / "table2_line_coverage.csv"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "project",
        "test_suite_origin",
        "mean_pct",
        "median_pct",
        "std_dev_pct",
        "n_classes",
    ]
    with open(out_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[aggregate] Table 2 -> {out_path} ({len(rows)} rows)")
    return out_path


def aggregate_table4(grouped: dict[str, dict[str, list[dict]]], config: dict) -> Path:
    rows = []
    llm_origins = [m["id"] for m in config["llm_models"]]

    for project_id in PROJECT_ORDER:
        origins = grouped.get(project_id, {})
        for origin_id in llm_origins:
            data = origins.get(origin_id, [])
            if not data:
                continue
            line_vals = [float_field(r, "line_coverage_pct") for r in data]
            mut_vals = [float_field(r, "mutation_coverage_pct") for r in data]
            ts_vals = [float_field(r, "test_strength_pct") for r in data]
            total_mut = sum(int_field(r, "mutants_total") for r in data)
            killed_mut = sum(int_field(r, "mutants_killed") for r in data)
            rows.append(
                {
                    "project": PROJECT_LABELS.get(project_id, project_id),
                    "llm": ORIGIN_LABELS.get(origin_id, origin_id),
                    "line_coverage_mean_pct": stats(line_vals)[0],
                    "mutation_coverage_mean_pct": (
                        round(100.0 * killed_mut / total_mut, 2) if total_mut else stats(mut_vals)[0]
                    ),
                    "test_strength_mean_pct": stats(ts_vals)[0],
                }
            )

    out_path = OUT_DIR / "table4_llm_ranking.csv"
    fieldnames = [
        "project",
        "llm",
        "line_coverage_mean_pct",
        "mutation_coverage_mean_pct",
        "test_strength_mean_pct",
    ]
    with open(out_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[aggregate] Table 4 -> {out_path} ({len(rows)} rows)")
    return out_path


def aggregate_table3(
    grouped: dict[str, dict[str, list[dict]]],
    high_complexity_percentile: float = 75.0,
) -> Path:
    rows = []
    threshold_doc = OUT_DIR / "high-complexity-threshold.md"

    for project_id in PROJECT_ORDER:
        origins = grouped.get(project_id, {})
        if not origins:
            continue

        all_complexity: list[float] = []
        for origin_rows in origins.values():
            for row in origin_rows:
                all_complexity.append(float_field(row, "cyclomatic_complexity"))

        if not all_complexity:
            continue

        sorted_cx = sorted(all_complexity)
        idx = int(len(sorted_cx) * high_complexity_percentile / 100.0)
        idx = min(idx, len(sorted_cx) - 1)
        threshold = sorted_cx[idx]

        for origin_id in ORIGIN_ORDER:
            data = origins.get(origin_id, [])
            if not data:
                continue
            high = [
                row
                for row in data
                if float_field(row, "cyclomatic_complexity") >= threshold
            ]
            if not high:
                continue

            line_vals = [float_field(r, "line_coverage_pct") for r in high]
            mut_vals = [float_field(r, "mutation_coverage_pct") for r in high]
            ts_vals = [float_field(r, "test_strength_pct") for r in high]
            rows.append(
                {
                    "project": PROJECT_LABELS.get(project_id, project_id),
                    "origin": ORIGIN_LABELS.get(origin_id, origin_id),
                    "high_cxty_line_cov_pct": stats(line_vals)[0],
                    "high_cxty_mutation_cov_pct": stats(mut_vals)[0],
                    "high_cxty_test_strength_pct": stats(ts_vals)[0],
                    "n_high_cxty_classes": len(high),
                    "complexity_threshold": threshold,
                }
            )

    threshold_doc.write_text(
        f"# High-Complexity Threshold\n\n"
        f"Classes at or above the **{high_complexity_percentile}th percentile** "
        f"of cyclomatic complexity per project (computed across all available origins).\n",
        encoding="utf-8",
    )

    out_path = OUT_DIR / "table3_high_complexity.csv"
    fieldnames = [
        "project",
        "origin",
        "high_cxty_line_cov_pct",
        "high_cxty_mutation_cov_pct",
        "high_cxty_test_strength_pct",
        "n_high_cxty_classes",
        "complexity_threshold",
    ]
    with open(out_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[aggregate] Table 3 -> {out_path} ({len(rows)} rows)")
    return out_path


def generate_figures(grouped: dict[str, dict[str, list[dict]]]) -> None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("[figures] matplotlib not installed; skip with: pip install matplotlib")
        return

    fig_dir = OUT_DIR / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    project_ids = [pid for pid in PROJECT_ORDER if pid in grouped]

    for fig_name, metric, ylabel in [
        ("fig2_line_coverage", "line_coverage_pct", "JaCoCo Line Coverage (%)"),
        ("fig4_test_strength", "test_strength_pct", "PIT Test Strength (%)"),
    ]:
        if not project_ids:
            continue
        fig, axes = plt.subplots(1, len(project_ids), figsize=(4 * len(project_ids), 4), sharey=True)
        if len(project_ids) == 1:
            axes = [axes]
        for ax, project_id in zip(axes, project_ids):
            origins = grouped[project_id]
            data_by_origin = []
            labels = []
            for origin_id in ORIGIN_ORDER:
                rows = origins.get(origin_id, [])
                vals = [float_field(r, metric) for r in rows if float_field(r, metric) or metric == "line_coverage_pct"]
                if vals:
                    data_by_origin.append(vals)
                    labels.append(ORIGIN_LABELS.get(origin_id, origin_id))
            if data_by_origin:
                ax.boxplot(data_by_origin, tick_labels=labels)
                ax.set_title(PROJECT_LABELS.get(project_id, project_id))
                ax.tick_params(axis="x", rotation=45)
        fig.supylabel(ylabel)
        fig.tight_layout()
        out = fig_dir / f"{fig_name}.png"
        fig.savefig(out, dpi=150)
        plt.close(fig)
        print(f"[figures] Wrote {out}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate class metrics into tables")
    parser.add_argument("--figures", action="store_true", help="Generate figure PNGs")
    parser.add_argument(
        "--high-complexity-percentile",
        type=float,
        default=75.0,
        help="Percentile for Table 3 high-complexity threshold",
    )
    args = parser.parse_args()

    config = load_config()
    grouped = read_published_metrics()
    missing = [pid for pid in project_ids_from_config(config) if pid not in grouped]
    if missing:
        print(f"[warn] Missing published metrics for: {', '.join(missing)}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    aggregate_table2(grouped)
    aggregate_table3(grouped, args.high_complexity_percentile)
    aggregate_table4(grouped, config)

    if args.figures:
        generate_figures(grouped)


if __name__ == "__main__":
    main()
