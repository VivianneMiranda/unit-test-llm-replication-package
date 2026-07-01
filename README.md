# Replication Package — Human-Written vs. LLM-Generated Unit Test Suites

Replication package for the SAST 2026 paper *Studying the Effectiveness of Human-Written versus LLM-Generated Unit Test Suites*.

**Anonymized artifact:** https://anonymous.4open.science/r/SAST26-UnitTest-LLM/

## What this package contains

This artifact provides the **published per-class JaCoCo and PIT metrics for all five Apache Commons projects** studied in the paper (Collections, Compress, Lang, CLI, and BCEL), together with the experimental protocol and Appendix A prompt. **Project source code and LLM-generated test suites are not bundled**; they can be reproduced locally using the provided scripts (`scripts/00_setup.*`, `scripts/03_collect_metrics.*`).

| Included | Not bundled |
|----------|-------------|
| Full methodology and Appendix A prompt | Apache Commons source trees |
| Per-class JaCoCo/PIT metrics (5 projects × 4 origins) | LLM-generated test suites |
| Aggregated Tables 2–4 | Raw JaCoCo/PIT HTML reports |
| Reproduction scripts (`00_setup`, metrics collection) | |

See [`docs/package-scope.md`](docs/package-scope.md) for the full scope statement.

## Quick start

### Prerequisites

Java 21, Maven 3.8+, Python 3.9+. Details: [`config/environment.md`](config/environment.md).

### 1. Inspect published results

- Per-class metrics: [`results/per-class/`](results/README.md)
- Aggregated tables: [`results/processed/table2_line_coverage.csv`](results/processed/table2_line_coverage.csv) (20 rows)

Regenerate aggregated tables:

```powershell
python scripts\05_aggregate_tables.py
```

### 2. Reproduce the study locally (optional)

```powershell
.\scripts\00_setup.ps1
# Generate tests with Cursor using prompts/test-generation-prompt.md
.\scripts\03_collect_metrics.ps1 -Project bcel -Origin developer
```

Clone checkouts live under `projects/` (gitignored). See [`projects/README.md`](projects/README.md).

## Directory structure

```
├── config/                # projects.json, package-scope.json
├── docs/                  # protocol, scope, Anonymous GitHub guide
├── prompts/               # Appendix A prompt
├── scripts/               # setup, metrics, aggregation
├── projects/              # populated locally by 00_setup (not in git)
├── results/
│   ├── per-class/         # published per-class metrics (5 CSVs)
│   ├── processed/         # Tables 2–4
│   └── README.md
└── paper/paper.pdf
```

## Paper mapping

| Paper item | In this package |
|------------|-----------------|
| Table 1 | `config/projects.json` |
| Tables 2–4 | `results/processed/table*.csv` |
| Figures 2–5 | `results/processed/figures/` (optional: `--figures`) |
| Appendix A, Section 4.5 | Full documentation + scripts |

Details: [`docs/paper-to-artifact.md`](docs/paper-to-artifact.md).

## Known limitations

- Project code and test suites must be reproduced locally; only metrics are published.
- Re-running Maven/PIT locally may differ slightly from the published CSVs.
- One LLM generation per model–project pair; failing tests removed before PIT.

## Citation and license

See [`LICENSE`](LICENSE) and the paper PDF in [`paper/`](paper/).
