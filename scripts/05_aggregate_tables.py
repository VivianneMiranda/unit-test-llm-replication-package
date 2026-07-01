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
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config" / "projects.json"
SCOPE_PATH = ROOT / "config" / "package-scope.json"
CLASSES_DIR = ROOT / "results" / "processed" / "classes"
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


def load_config() -> dict:
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


def load_included_project_ids() -> list[str]:
    if SCOPE_PATH.exists():
        with open(SCOPE_PATH, encoding="utf-8") as f:
            scope = json.load(f)
        return scope.get("included_project_ids", [])
    return [p["id"] for p in load_config()["projects"]]


def included_projects(config: dict) -> list[dict]:
    ids = set(load_included_project_ids())
    return [p for p in config["projects"] if p["id"] in ids]


def read_class_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def stats(values: list[float]) -> tuple[float, float, float]:
    if not values:
        return 0.0, 0.0, 0.0
    mean = statistics.mean(values)
    median = statistics.median(values)
    stdev = statistics.stdev(values) if len(values) > 1 else 0.0
    return round(mean, 2), round(median, 2), round(stdev, 2)


def aggregate_table2() -> Path:
    """Table 2: JaCoCo line coverage descriptive statistics."""
    rows = []
    config = load_config()

    for proj in included_projects(config):
        pid = proj["id"]
        project_dir = CLASSES_DIR / pid
        if not project_dir.exists():
            continue
        for origin_file in sorted(project_dir.glob("*.csv")):
            origin = origin_file.stem
            data = read_class_csv(origin_file)
            values = [float(r["line_coverage_pct"]) for r in data if r.get("line_coverage_pct")]
            mean, median, stdev = stats(values)
            rows.append(
                {
                    "project": PROJECT_LABELS.get(pid, pid),
                    "test_suite_origin": ORIGIN_LABELS.get(origin, origin),
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
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[aggregate] Table 2 -> {out_path} ({len(rows)} rows)")
    return out_path


def aggregate_table4() -> Path:
    """Table 4: LLM ranking by project (line, mutation, test strength)."""
    rows = []
    config = load_config()
    llm_origins = [m["id"] for m in config["llm_models"]]

    for proj in included_projects(config):
        pid = proj["id"]
        for origin in llm_origins:
            csv_path = CLASSES_DIR / pid / f"{origin}.csv"
            data = read_class_csv(csv_path)
            if not data:
                continue
            line_vals = [float(r["line_coverage_pct"]) for r in data]
            mut_vals = [float(r["mutation_coverage_pct"]) for r in data]
            ts_vals = [float(r["test_strength_pct"]) for r in data]
            total_mut = sum(int(r.get("mutants_total") or 0) for r in data)
            killed_mut = sum(int(r.get("mutants_killed") or 0) for r in data)
            rows.append(
                {
                    "project": PROJECT_LABELS.get(pid, pid),
                    "llm": ORIGIN_LABELS.get(origin, origin),
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
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[aggregate] Table 4 -> {out_path} ({len(rows)} rows)")
    return out_path


def aggregate_table3(high_complexity_percentile: float = 75.0) -> Path:
    """Table 3: High-complexity class metrics (top percentile by complexity)."""
    rows = []
    config = load_config()
    threshold_doc = OUT_DIR / "high-complexity-threshold.md"

    for proj in included_projects(config):
        pid = proj["id"]
        project_dir = CLASSES_DIR / pid
        if not project_dir.exists():
            continue

        # Compute complexity threshold across all origins for this project
        all_complexity: list[float] = []
        for origin_file in project_dir.glob("*.csv"):
            for r in read_class_csv(origin_file):
                all_complexity.append(float(r.get("cyclomatic_complexity", 0)))

        if not all_complexity:
            continue

        sorted_cx = sorted(all_complexity)
        idx = int(len(sorted_cx) * high_complexity_percentile / 100.0)
        idx = min(idx, len(sorted_cx) - 1)
        threshold = sorted_cx[idx]

        for origin_file in sorted(project_dir.glob("*.csv")):
            origin = origin_file.stem
            data = read_class_csv(origin_file)
            high = [
                r
                for r in data
                if float(r.get("cyclomatic_complexity", 0)) >= threshold
            ]
            if not high:
                continue

            line_vals = [float(r["line_coverage_pct"]) for r in high]
            mut_vals = [float(r["mutation_coverage_pct"]) for r in high]
            ts_vals = [float(r["test_strength_pct"]) for r in high]
            rows.append(
                {
                    "project": PROJECT_LABELS.get(pid, pid),
                    "origin": ORIGIN_LABELS.get(origin, origin),
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
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[aggregate] Table 3 -> {out_path} ({len(rows)} rows)")
    return out_path


def generate_figures() -> None:
    """Generate Figures 2-5 when matplotlib is available and data exists."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("[figures] matplotlib not installed; skip with: pip install matplotlib")
        return

    fig_dir = OUT_DIR / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    config = load_config()
    projects = included_projects(config)

    # Figure 2: line coverage boxplot by project and origin
    for fig_name, metric, ylabel in [
        ("fig2_line_coverage", "line_coverage_pct", "JaCoCo Line Coverage (%)"),
        ("fig4_test_strength", "test_strength_pct", "PIT Test Strength (%)"),
    ]:
        if not projects:
            continue
        fig, axes = plt.subplots(1, len(projects), figsize=(8 * len(projects), 4), sharey=True)
        if len(projects) == 1:
            axes = [axes]
        for ax, proj in zip(axes, projects):
            pid = proj["id"]
            project_dir = CLASSES_DIR / pid
            if not project_dir.exists():
                continue
            data_by_origin = []
            labels = []
            for origin_file in sorted(project_dir.glob("*.csv")):
                origin = origin_file.stem
                vals = [
                    float(r[metric])
                    for r in read_class_csv(origin_file)
                    if r.get(metric)
                ]
                if vals:
                    data_by_origin.append(vals)
                    labels.append(ORIGIN_LABELS.get(origin, origin))
            if data_by_origin:
                ax.boxplot(data_by_origin, tick_labels=labels)
                ax.set_title(PROJECT_LABELS.get(pid, pid))
                ax.tick_params(axis="x", rotation=45)
        fig.supylabel(ylabel)
        fig.tight_layout()
        out = fig_dir / f"{fig_name}.png"
        fig.savefig(out, dpi=150)
        plt.close(fig)
        print(f"[figures] Wrote {out}")

    print("[figures] Figure 3 and 5 require scatter plots; run after all class CSVs exist.")


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

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    aggregate_table2()
    aggregate_table3(args.high_complexity_percentile)
    aggregate_table4()

    if args.figures:
        generate_figures()


if __name__ == "__main__":
    main()
