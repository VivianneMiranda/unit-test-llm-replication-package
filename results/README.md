# Published Study Results

Per-class JaCoCo and PIT metrics for all five Apache Commons projects in the paper.
Source files were normalized from `metricas_commons-*.csv` using
`scripts/organize_published_metrics.py`.

## Per-class CSVs (`per-class/`)

| File | Project | Classes (rows) | Origins |
|------|---------|----------------|---------|
| `commons-bcel.csv` | commons-bcel | 1633 | developer, gpt-5.1-codex-max, opus-4.5, sonnet-4.5 |
| `commons-cli.csv` | commons-cli | 173 | developer, gpt-5.1-codex-max, opus-4.5, sonnet-4.5 |
| `commons-collections.csv` | commons-collections | 924 | developer, gpt-5.1-codex-max, opus-4.5, sonnet-4.5 |
| `commons-compress.csv` | commons-compress | 544 | developer, gpt-5.1-codex-max, opus-4.5, sonnet-4.5 |
| `commons-lang.csv` | commons-lang | 464 | developer, gpt-5.1-codex-max, opus-4.5, sonnet-4.5 |

## Aggregated tables (`processed/`)

| Paper item | File |
|------------|------|
| Table 2 (line coverage) | `processed/table2_line_coverage.csv` |
| Table 3 (high complexity) | `processed/table3_high_complexity.csv` |
| Table 4 (LLM ranking) | `processed/table4_llm_ranking.csv` |

Regenerate aggregated tables:

```powershell
python scripts\05_aggregate_tables.py
```

## Column schema (`per-class/*.csv`)

| Column | Description |
|--------|-------------|
| `project_id` | Short project id (`bcel`, `cli`, ...) |
| `origin_id` | Test suite origin (`developer`, `opus-4.5`, ...) |
| `class_name` | Fully qualified Java class name |
| `line_coverage_pct` | JaCoCo line coverage (%) |
| `branch_coverage_pct` | JaCoCo branch coverage (%) |
| `cyclomatic_complexity` | JaCoCo cyclomatic complexity (total) |
| `mutation_coverage_pct` | PIT mutation coverage (%) |
| `test_strength_pct` | PIT test strength (%) |
| `mutants_killed` | PIT mutants killed |
| `mutants_total` | PIT mutants generated |
