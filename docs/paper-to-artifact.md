# Paper-to-Artifact Mapping

Maps paper figures and tables to files in this replication package.

**Important:** This artifact includes **BCEL and CLI only**. Tables and figures below are reproduced as a **subset** (2 of 5 paper projects). Paper-wide aggregates that pool all five projects are in the manuscript, not in `results/processed/`.

Scope: [`docs/package-scope.md`](package-scope.md)

## Tables

| Paper item | Full paper | This artifact |
|------------|------------|---------------|
| **Table 1** | All 5 projects | `config/projects.json` (metadata for all 5; artifacts for 2) |
| **Table 2** | 5 projects × 4 origins | `results/processed/table2_line_coverage.csv` — **BCEL + CLI rows only** |
| **Table 3** | High-complexity classes | `results/processed/table3_high_complexity.csv` — subset |
| **Table 4** | LLM ranking | `results/processed/table4_llm_ranking.csv` — subset |

Reproduce subset tables:

```powershell
.\scripts\archive_metrics_from_target.ps1
python scripts\04_parse_results.py --all
python scripts\05_aggregate_tables.py
```

## Figures

| Paper item | This artifact |
|------------|---------------|
| **Figure 1** | `docs/experimental-protocol.md` |
| **Figures 2–5** | `results/processed/figures/` — BCEL + CLI only (`05_aggregate_tables.py --figures`) |

## Sections

| Paper section | Artifact |
|---------------|----------|
| 4.1–4.5 | `docs/experimental-protocol.md`, `prompts/`, `scripts/` |
| Appendix A | `prompts/test-generation-prompt.md` |
| Section 6 | `docs/threats-to-validity.md` |

## Included project snapshots

| Paper project | In package | Folder |
|---------------|------------|--------|
| Commons BCEL | Yes | `commons-bcel/` |
| Commons CLI | Yes | `commons-cli/` |
| Commons Collections | No (paper only) | — |
| Commons Compress | No (paper only) | — |
| Commons Lang | No (paper only) | — |

## Raw data layout (`results/raw/`)

```
results/raw/
├── bcel/
│   ├── developer/
│   ├── opus-4.5/
│   ├── sonnet-4.5/
│   └── gpt-5.1-codex-max/
└── cli/
    ├── developer/
    ├── opus-4.5/
    ├── sonnet-4.5/
    └── gpt-5.1-codex-max/
```

Per-class CSVs: `results/processed/classes/<project>/<origin>.csv`

## Validation values (paper Table 2 — included projects only)

| Project | Origin | Mean | Median | Std. Dev. |
|---------|--------|------|--------|-----------|
| BCEL | Developer | 75.27 | 87.00 | 30.58 |
| BCEL | Opus 4.5 | 80.11 | 95.00 | 28.05 |
| CLI | Developer | 98.47 | 100.00 | 3.68 |

Compare after aggregation. Full five-project values: `paper/paper.pdf`.
