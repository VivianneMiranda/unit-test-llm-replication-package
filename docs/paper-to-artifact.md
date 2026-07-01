# Paper-to-Artifact Mapping

Maps paper figures and tables to files in this replication package.

Scope: [`docs/package-scope.md`](package-scope.md)

## Tables

| Paper item | Full paper | This artifact |
|------------|------------|---------------|
| **Table 1** | All 5 projects | `config/projects.json` |
| **Table 2** | 5 projects × 4 origins | `results/processed/table2_line_coverage.csv` (20 rows) |
| **Table 3** | High-complexity classes | `results/processed/table3_high_complexity.csv` |
| **Table 4** | LLM ranking | `results/processed/table4_llm_ranking.csv` |

Regenerate aggregated tables:

```powershell
python scripts\05_aggregate_tables.py
```

## Figures

| Paper item | This artifact |
|------------|---------------|
| **Figure 1** | `docs/experimental-protocol.md` |
| **Figures 2–5** | `results/processed/figures/` (`05_aggregate_tables.py --figures`) |

## Sections

| Paper section | Artifact |
|---------------|----------|
| 4.1–4.5 | `docs/experimental-protocol.md`, `prompts/`, `scripts/` |
| Appendix A | `prompts/test-generation-prompt.md` |
| Section 6 | `docs/threats-to-validity.md` |

## Published metrics layout

```
results/
├── per-class/
│   ├── commons-bcel.csv
│   ├── commons-cli.csv
│   ├── commons-collections.csv
│   ├── commons-compress.csv
│   └── commons-lang.csv
└── processed/
    ├── table2_line_coverage.csv
    ├── table3_high_complexity.csv
    └── table4_llm_ranking.csv
```

Optional local reproduction output: `results/raw/<project>/<origin>/` after running `scripts/03_collect_metrics.*`.

## Validation values (paper Table 2)

| Project | Origin | Mean | Median | Std. Dev. |
|---------|--------|------|--------|-----------|
| BCEL | Developer | 75.27 | 87.00 | 30.58 |
| BCEL | Opus 4.5 | 80.11 | 95.00 | 28.05 |
| CLI | Developer | 98.47 | 100.00 | 3.68 |

Compare against `results/processed/table2_line_coverage.csv`. Full values: `paper/paper.pdf`.
