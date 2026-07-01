#!/usr/bin/env python3
"""
Organize author-published per-class metrics into results/per-class/.

Reads metricas_commons-*.csv from the repo root (or an explicit input directory),
normalizes origin labels and locale-specific percentages, and writes one CSV per
project under results/per-class/. Also generates results/README.md.
"""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = ROOT
OUT_DIR = ROOT / "results" / "per-class"
README_PATH = ROOT / "results" / "README.md"

EXPECTED_FILES = [
    "metricas_commons-bcel.csv",
    "metricas_commons-cli.csv",
    "metricas_commons-collections.csv",
    "metricas_commons-compress.csv",
    "metricas_commons-lang.csv",
]

ORIGIN_MAP = {
    "desenvolvedor": "developer",
    "desenvolvedores": "developer",
    "opus 4.5": "opus-4.5",
    "sonnet 4.5": "sonnet-4.5",
    "gpt-5.1 codex max": "gpt-5.1-codex-max",
}

PROJECT_ID_MAP = {
    "commons-bcel": "bcel",
    "commons-cli": "cli",
    "commons-collections": "collections",
    "commons-compress": "compress",
    "commons-lang": "lang",
}

OUTPUT_FIELDS = [
    "project_id",
    "origin_id",
    "class_name",
    "line_coverage_pct",
    "branch_coverage_pct",
    "cyclomatic_complexity",
    "mutation_coverage_pct",
    "test_strength_pct",
    "mutants_killed",
    "mutants_total",
]


def normalize_origin(raw: str) -> str:
    key = raw.strip().lower()
    if key not in ORIGIN_MAP:
        raise ValueError(f"Unknown origin label: {raw!r}")
    return ORIGIN_MAP[key]


def parse_pct(value: str | None) -> float | None:
    if value is None:
        return None
    text = str(value).strip().strip('"')
    if not text or text.lower() == "n/a":
        return None
    text = text.replace("%", "").replace(",", ".")
    try:
        return float(text)
    except ValueError:
        return None


def parse_ratio(value: str | None) -> tuple[int, int] | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.lower() == "n/a":
        return None
    match = re.match(r"^(\d+)\s*/\s*(\d+)$", text)
    if not match:
        return None
    return int(match.group(1)), int(match.group(2))


def parse_complexity(value: str | None) -> int:
    ratio = parse_ratio(value)
    if ratio is None:
        return 0
    missed, total = ratio
    return max(total, missed)


def parse_mutants(value: str | None) -> tuple[int, int]:
    ratio = parse_ratio(value)
    if ratio is None:
        return 0, 0
    killed, total = ratio
    return killed, total


def project_slug_from_input(path: Path) -> str:
    name = path.name
    if not name.startswith("metricas_") or not name.endswith(".csv"):
        raise ValueError(f"Unexpected metrics filename: {name}")
    return name.removeprefix("metricas_").removesuffix(".csv")


def normalize_row(row: dict[str, str], project_id: str) -> dict[str, str | float | int]:
    origin_id = normalize_origin(row["Origem"])
    line_cov = parse_pct(row.get("JaCoCo Line Cov."))
    branch_cov = parse_pct(row.get("JaCoCo Branch Cov."))
    mutation_cov = parse_pct(row.get("PIT Mutation Cov."))
    test_strength = parse_pct(row.get("PIT Test Strength"))
    mut_killed, mut_total = parse_mutants(row.get("PIT Mutantes Mortos/Total"))

    if mutation_cov is None and mut_total:
        mutation_cov = round(100.0 * mut_killed / mut_total, 2)

    return {
        "project_id": project_id,
        "origin_id": origin_id,
        "class_name": row["Classe"].strip(),
        "line_coverage_pct": round(line_cov, 2) if line_cov is not None else 0.0,
        "branch_coverage_pct": round(branch_cov, 2) if branch_cov is not None else 0.0,
        "cyclomatic_complexity": parse_complexity(row.get("JaCoCo Cxty Missed/Total")),
        "mutation_coverage_pct": round(mutation_cov, 2) if mutation_cov is not None else 0.0,
        "test_strength_pct": round(test_strength, 2) if test_strength is not None else 0.0,
        "mutants_killed": mut_killed,
        "mutants_total": mut_total,
    }


def read_source_csv(path: Path) -> list[dict[str, str | float | int]]:
    project_slug = project_slug_from_input(path)
    project_id = PROJECT_ID_MAP.get(project_slug, project_slug.replace("commons-", ""))

    rows: list[dict[str, str | float | int]] = []
    with open(path, encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(normalize_row(row, project_id))
    return rows


def write_project_csv(project_slug: str, rows: list[dict[str, str | float | int]]) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"{project_slug}.csv"
    with open(out_path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    return out_path


def write_readme(summary: dict[str, dict[str, int]]) -> None:
    lines = [
        "# Published Study Results",
        "",
        "Per-class JaCoCo and PIT metrics for all five Apache Commons projects in the paper.",
        "Source files were normalized from `metricas_commons-*.csv` using",
        "`scripts/organize_published_metrics.py`.",
        "",
        "## Per-class CSVs (`per-class/`)",
        "",
        "| File | Project | Classes (rows) | Origins |",
        "|------|---------|----------------|---------|",
    ]

    for slug in sorted(summary):
        info = summary[slug]
        origins = ", ".join(sorted(info["origins"]))
        lines.append(
            f"| `{slug}.csv` | {slug} | {info['rows']} | {origins} |"
        )

    lines.extend(
        [
            "",
            "## Aggregated tables (`processed/`)",
            "",
            "| Paper item | File |",
            "|------------|------|",
            "| Table 2 (line coverage) | `processed/table2_line_coverage.csv` |",
            "| Table 3 (high complexity) | `processed/table3_high_complexity.csv` |",
            "| Table 4 (LLM ranking) | `processed/table4_llm_ranking.csv` |",
            "",
            "Regenerate aggregated tables:",
            "",
            "```powershell",
            "python scripts\\organize_published_metrics.py",
            "python scripts\\05_aggregate_tables.py",
            "```",
            "",
            "## Column schema (`per-class/*.csv`)",
            "",
            "| Column | Description |",
            "|--------|-------------|",
            "| `project_id` | Short project id (`bcel`, `cli`, ...) |",
            "| `origin_id` | Test suite origin (`developer`, `opus-4.5`, ...) |",
            "| `class_name` | Fully qualified Java class name |",
            "| `line_coverage_pct` | JaCoCo line coverage (%) |",
            "| `branch_coverage_pct` | JaCoCo branch coverage (%) |",
            "| `cyclomatic_complexity` | JaCoCo cyclomatic complexity (total) |",
            "| `mutation_coverage_pct` | PIT mutation coverage (%) |",
            "| `test_strength_pct` | PIT test strength (%) |",
            "| `mutants_killed` | PIT mutants killed |",
            "| `mutants_total` | PIT mutants generated |",
            "",
        ]
    )

    README_PATH.parent.mkdir(parents=True, exist_ok=True)
    README_PATH.write_text("\n".join(lines), encoding="utf-8")


def organize(input_dir: Path, keep_source: bool = False) -> list[Path]:
    missing = [name for name in EXPECTED_FILES if not (input_dir / name).exists()]
    if missing:
        raise SystemExit(f"Missing metrics files in {input_dir}: {', '.join(missing)}")

    written: list[Path] = []
    summary: dict[str, dict[str, int | set[str]]] = {}

    for filename in EXPECTED_FILES:
        source = input_dir / filename
        project_slug = project_slug_from_input(source)
        rows = read_source_csv(source)
        out_path = write_project_csv(project_slug, rows)
        written.append(out_path)

        origin_counts: Counter[str] = Counter(str(r["origin_id"]) for r in rows)
        summary[project_slug] = {
            "rows": len(rows),
            "origins": set(origin_counts),
        }
        print(f"[organize] {source.name} -> {out_path} ({len(rows)} rows)")

        if not keep_source and source.parent == ROOT and source.exists():
            source.unlink()
            print(f"[organize] removed source {source.name}")

    readme_summary = {
        slug: {"rows": info["rows"], "origins": info["origins"]}
        for slug, info in summary.items()
    }
    write_readme(readme_summary)
    print(f"[organize] wrote {README_PATH}")
    return written


def main() -> None:
    parser = argparse.ArgumentParser(description="Organize published metrics CSVs")
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=DEFAULT_INPUT,
        help="Directory containing metricas_commons-*.csv (default: repo root)",
    )
    parser.add_argument(
        "--keep-source",
        action="store_true",
        help="Do not delete metricas_commons-*.csv from the input directory",
    )
    args = parser.parse_args()
    organize(args.input_dir.resolve(), keep_source=args.keep_source)


if __name__ == "__main__":
    main()
