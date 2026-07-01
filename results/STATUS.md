# Replication Artifact Status

**Last updated:** 2026-07-01  
**Package scope:** Light artifact — published metrics for all five projects ([`docs/package-scope.md`](../docs/package-scope.md))

## Published results

| Output | Location | Expected rows |
|--------|----------|---------------|
| Per-class metrics | `results/per-class/*.csv` | 5 files |
| Table 2 (line coverage) | `results/processed/table2_line_coverage.csv` | 20 |
| Table 3 (high complexity) | `results/processed/table3_high_complexity.csv` | 20 |
| Table 4 (LLM ranking) | `results/processed/table4_llm_ranking.csv` | 15 |
| Figures 2 & 4 (optional) | `results/processed/figures/` | PNG |

Regenerate:

```powershell
python scripts\organize_published_metrics.py --keep-source
python scripts\05_aggregate_tables.py --figures
```

## Projects and origins

| Project | Developer | Opus 4.5 | Sonnet 4.5 | GPT-5.1 Codex Max |
|---------|-----------|----------|------------|-------------------|
| Commons Collections | published | published | published | published |
| Commons Compress | published | published | published | published |
| Commons Lang | published | published | published | published |
| Commons CLI | published | published | published | published |
| Commons BCEL | published | published | published | published |

Metrics source: author CSVs normalized into `results/per-class/`.

## Before Anonymous GitHub (manual)

- [ ] Review `docs/ANONYMIZATION_CHECKLIST.md`
- [ ] Push to private GitHub repo
- [ ] Configure https://anonymous.4open.science/
- [ ] Insert link using `docs/manuscript-artifact-text.md`
