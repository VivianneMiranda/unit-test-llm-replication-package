#!/usr/bin/env python3
"""
Optional: parse locally collected JaCoCo/PIT reports into per-class CSV files.

Use this only after re-running metrics with scripts/03_collect_metrics.* on a local
checkout under projects/. Published study results are already in results/per-class/.

Usage:
    python scripts/optional/04_parse_results.py --project collections --origin developer
    python scripts/optional/04_parse_results.py --all
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH = ROOT / "config" / "projects.json"


def load_config() -> dict:
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


def parse_jacoco_csv(jacoco_dir: Path) -> dict[str, dict]:
    csv_path = jacoco_dir / "jacoco.csv"
    if not csv_path.exists():
        return {}

    metrics: dict[str, dict] = {}
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("CLASS", "").endswith(".package"):
                continue
            class_name = row["CLASS"]
            line_missed = int(row.get("LINE_MISSED", 0))
            line_covered = int(row.get("LINE_COVERED", 0))
            branch_missed = int(row.get("BRANCH_MISSED", 0))
            branch_covered = int(row.get("BRANCH_COVERED", 0))
            complexity = int(row.get("COMPLEXITY_MISSED", 0)) + int(
                row.get("COMPLEXITY_COVERED", 0)
            )

            line_total = line_missed + line_covered
            branch_total = branch_missed + branch_covered

            metrics[class_name] = {
                "line_coverage_pct": (
                    100.0 * line_covered / line_total if line_total else 0.0
                ),
                "branch_coverage_pct": (
                    100.0 * branch_covered / branch_total if branch_total else 0.0
                ),
                "cyclomatic_complexity": complexity,
            }
    return metrics


def parse_pit_html(pit_dir: Path) -> dict[str, dict]:
    metrics: dict[str, dict] = {}
    if not pit_dir.exists():
        return metrics

    row_pattern = re.compile(
        r'<td><a href="\./([^"]+\.java)\.html">\1</a></td>\s*'
        r"<td>.*?coverage_percentage\">(\d+)%\s*.*?"
        r'coverage_legend">(\d+)/(\d+)</div>.*?</td>\s*'
        r"<td>.*?coverage_percentage\">(\d+)%\s*.*?"
        r'coverage_legend">(\d+)/(\d+)</div>.*?</td>\s*'
        r"<td>.*?coverage_percentage\">(\d+)%\s*.*?"
        r'coverage_legend">(\d+)/(\d+)</div>',
        re.DOTALL,
    )

    for html_file in pit_dir.rglob("*.html"):
        if ".java.html" in html_file.name:
            continue
        content = html_file.read_text(encoding="utf-8", errors="replace")
        if "Breakdown by Class" not in content:
            continue
        section = content.split("Breakdown by Class", 1)[1]
        package_name = html_file.parent.name
        for match in row_pattern.finditer(section):
            java_file, line_pct, _line_cov, _line_tot, mut_pct, mut_killed, mut_tot, ts_pct, _ts_num, _ts_den = (
                match.groups()
            )
            short_name = java_file.replace(".java", "")
            class_name = (
                f"{package_name}.{short_name}"
                if package_name.startswith("org.")
                else short_name
            )
            mut_killed_i = int(mut_killed)
            mut_tot_i = int(mut_tot)

            entry = {
                "pit_line_coverage_pct": float(line_pct),
                "mutation_coverage_pct": (
                    100.0 * mut_killed_i / mut_tot_i if mut_tot_i else float(mut_pct)
                ),
                "test_strength_pct": float(ts_pct),
                "mutants_total": mut_tot_i,
                "mutants_killed": mut_killed_i,
                "mutants_survived": max(mut_tot_i - mut_killed_i, 0),
                "mutants_no_coverage": 0,
            }
            if class_name in metrics:
                if mut_tot_i <= metrics[class_name]["mutants_total"]:
                    continue
            metrics[class_name] = entry
    return metrics


def parse_pit_mutations(pit_dir: Path) -> dict[str, dict]:
    mutations_path = pit_dir / "mutations.xml"
    if mutations_path.exists():
        tree = ET.parse(mutations_path)
        root = tree.getroot()

        by_class: dict[str, list[str]] = {}
        for mutation in root.findall("mutation"):
            status = mutation.get("status", "")
            desc = mutation.findtext("description", "")
            match = re.search(r"in\s+([\w.$]+)", desc)
            if not match:
                mutated_class = mutation.findtext("mutatedClass", "")
                class_name = mutated_class.split(".")[-1] if mutated_class else "unknown"
            else:
                class_name = match.group(1).split(".")[-1]

            by_class.setdefault(class_name, []).append(status)

        metrics: dict[str, dict] = {}
        for class_name, statuses in by_class.items():
            total = len(statuses)
            killed = sum(1 for s in statuses if s == "KILLED")
            survived = sum(1 for s in statuses if s == "SURVIVED")
            no_cov = sum(1 for s in statuses if s in ("NO_COVERAGE", "TIMED_OUT"))

            covered = total - no_cov
            metrics[class_name] = {
                "mutation_coverage_pct": 100.0 * killed / total if total else 0.0,
                "test_strength_pct": 100.0 * killed / covered if covered else 0.0,
                "pit_line_coverage_pct": 100.0 * covered / total if total else 0.0,
                "mutants_total": total,
                "mutants_killed": killed,
                "mutants_survived": survived,
                "mutants_no_coverage": no_cov,
            }
        return metrics

    return parse_pit_html(pit_dir)


def merge_and_write(project_id: str, origin: str) -> Path | None:
    raw_dir = ROOT / "results" / "raw" / project_id / origin
    jacoco_dir = raw_dir / "jacoco"
    pit_dir = raw_dir / "pit"

    if not raw_dir.exists():
        print(f"[skip] No raw data: {raw_dir}")
        return None

    jacoco = parse_jacoco_csv(jacoco_dir)
    pit = parse_pit_mutations(pit_dir)

    def jacoco_key(short_or_full: str) -> str:
        return short_or_full.split(".")[-1]

    pit_by_short: dict[str, dict] = {}
    for key, data in pit.items():
        pit_by_short[jacoco_key(key)] = data

    all_classes = set(jacoco.keys()) | set(pit_by_short.keys())
    if not all_classes:
        print(f"[warn] No class metrics found for {project_id}/{origin}")
        return None

    out_dir = ROOT / "results" / "processed" / "classes" / project_id
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{origin}.csv"

    fieldnames = [
        "class_name",
        "line_coverage_pct",
        "branch_coverage_pct",
        "cyclomatic_complexity",
        "pit_line_coverage_pct",
        "mutation_coverage_pct",
        "test_strength_pct",
        "mutants_total",
        "mutants_killed",
        "mutants_survived",
        "mutants_no_coverage",
    ]

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for class_name in sorted(all_classes):
            j = jacoco.get(class_name, {})
            p = pit_by_short.get(class_name, {})
            writer.writerow(
                {
                    "class_name": class_name,
                    "line_coverage_pct": round(j.get("line_coverage_pct", 0.0), 2),
                    "branch_coverage_pct": round(j.get("branch_coverage_pct", 0.0), 2),
                    "cyclomatic_complexity": j.get("cyclomatic_complexity", 0),
                    "pit_line_coverage_pct": round(
                        p.get("pit_line_coverage_pct", 0.0), 2
                    ),
                    "mutation_coverage_pct": round(
                        p.get("mutation_coverage_pct", 0.0), 2
                    ),
                    "test_strength_pct": round(p.get("test_strength_pct", 0.0), 2),
                    "mutants_total": p.get("mutants_total", 0),
                    "mutants_killed": p.get("mutants_killed", 0),
                    "mutants_survived": p.get("mutants_survived", 0),
                    "mutants_no_coverage": p.get("mutants_no_coverage", 0),
                }
            )

    print(f"[parse] Wrote {out_path} ({len(all_classes)} classes)")
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse JaCoCo/PIT into per-class CSV")
    parser.add_argument("--project", help="Project id (e.g., collections)")
    parser.add_argument("--origin", help="Test suite origin (e.g., developer)")
    parser.add_argument(
        "--all", action="store_true", help="Parse all available raw results"
    )
    args = parser.parse_args()

    if args.all:
        raw_root = ROOT / "results" / "raw"
        if not raw_root.exists():
            print("No results/raw directory.")
            return
        for project_dir in sorted(raw_root.iterdir()):
            if not project_dir.is_dir() or project_dir.name.endswith(".md"):
                continue
            for origin_dir in sorted(project_dir.iterdir()):
                if origin_dir.is_dir():
                    merge_and_write(project_dir.name, origin_dir.name)
        return

    if not args.project or not args.origin:
        parser.error("Specify --project and --origin, or use --all")
    merge_and_write(args.project, args.origin)


if __name__ == "__main__":
    main()
