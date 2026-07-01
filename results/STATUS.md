# Replication Artifact Status

**Last updated:** 2026-07-01  
**Package scope:** BCEL + CLI only ([`docs/package-scope.md`](../docs/package-scope.md))

## Legend

| Status | Meaning |
|--------|---------|
| `done` | Tests archived, metrics in `results/raw/`, CSVs generated |
| `out_of_scope` | In the paper but not shipped |

## Included projects

| Project | Developer | Opus 4.5 | Sonnet 4.5 | GPT-5.1 Codex Max |
|---------|-----------|----------|------------|-------------------|
| Commons BCEL | done | done | done | done |
| Commons CLI | done | done | done | done |

## Generated outputs

| Output | Location | Rows |
|--------|----------|------|
| Per-class metrics | `results/processed/classes/` | 8 CSV files |
| Table 2 (line coverage) | `results/processed/table2_line_coverage.csv` | 8 |
| Table 3 (high complexity) | `results/processed/table3_high_complexity.csv` | 8 |
| Table 4 (LLM ranking) | `results/processed/table4_llm_ranking.csv` | 6 |
| Figures 2 & 4 (subset) | `results/processed/figures/` | PNG |

Regenerate:

```powershell
.\scripts\archive_metrics_from_target.ps1
python scripts\04_parse_results.py --all
python scripts\05_aggregate_tables.py --figures
```

## Validation vs. paper (Table 2 line coverage, subset)

| Project | Origin | Paper mean | Artifact mean |
|---------|--------|------------|---------------|
| CLI | Developer | 98.47 | 98.35 |
| CLI | Opus 4.5 | 94.69 | 94.69 |
| BCEL | Developer | 75.27 | 73.48 |
| BCEL | Opus 4.5 | 80.11 | 80.24 |

Small differences may arise from JaCoCo re-run on BCEL developer (`-Dmaven.test.failure.ignore=true`) and class-level aggregation.

## Out of scope

Collections, Compress, Lang — manuscript only.

## Notes

- PIT metrics parsed from HTML reports (no `mutations.xml`).
- BCEL PIT uses multi-module reports; mutation aggregates may differ slightly from paper tooling.
- `target/` folders remain gitignored; canonical archived copy is under `results/raw/`.

## Before Anonymous GitHub (manual)

- [ ] Review `docs/ANONYMIZATION_CHECKLIST.md`
- [ ] Push to private GitHub repo
- [ ] Configure https://anonymous.4open.science/
- [ ] Insert link using `docs/manuscript-artifact-text.md`
