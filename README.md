# Replication Package — Human-Written vs. LLM-Generated Unit Test Suites

Replication package for the SAST 2026 paper *Studying the Effectiveness of Human-Written versus LLM-Generated Unit Test Suites*.

**Anonymous review link (fill after setup):** `https://anonymous.4open.science/r/SAST26-UnitTest-LLM/`

## What this package contains

This artifact is intentionally scoped to **two of the five paper projects** — **Commons BCEL** and **Commons CLI** — for which complete test suites and executed metrics are available.

| Included | Not required / not shipped |
|----------|----------------------------|
| Full methodology and Appendix A prompt | Collections, Compress, Lang project trees |
| BCEL + CLI (developer + 3 LLMs each) | Paper-wide Tables 2–4 across all 5 projects |
| Scripts to parse metrics and build subset tables | Re-running LLMs for missing projects |

See [`docs/package-scope.md`](docs/package-scope.md) for the full scope statement.

## Quick start

### Prerequisites

Java 21, Maven 3.8+, Python 3.9+. Details: [`config/environment.md`](config/environment.md).

### 1. Inspect included projects

- [`commons-bcel/`](commons-bcel/README.md) — 4 variants (developer, Opus, Sonnet, GPT)
- [`commons-cli/`](commons-cli/README.md) — 4 variants

Metrics from the original study are under each variant's `target/site/jacoco/` and `target/pit-reports/` (local Maven output).

### 2. Archive and parse metrics

```powershell
.\scripts\archive_metrics_from_target.ps1
python scripts\04_parse_results.py --all
python scripts\05_aggregate_tables.py --figures
```

See [`results/STATUS.md`](results/STATUS.md) for generated tables and validation.

### 3. Re-run metrics on one variant (optional)

```powershell
.\scripts\03_collect_metrics.ps1 -Project bcel -Origin developer
.\scripts\03_collect_metrics.ps1 -Project cli -Origin opus-4.5
```

## Directory structure

```
├── commons-bcel/          # BCEL: code + tests + metrics (target/)
├── commons-cli/           # CLI: code + tests + metrics (target/)
├── config/                # projects.json, package-scope.json, artifact paths
├── docs/                  # protocol, scope, Anonymous GitHub guide
├── prompts/               # Appendix A prompt
├── scripts/               # metrics, parsing, aggregation
├── results/
│   ├── raw/               # archived JaCoCo/PIT (bcel + cli only)
│   ├── processed/         # CSVs and subset tables
│   └── STATUS.md
└── paper/paper.pdf
```

## Paper mapping (subset)

| Paper item | In this package |
|------------|-----------------|
| Table 1 (all 5 projects) | `config/projects.json` (metadata only) |
| Tables 2–4 | **Subset** for BCEL + CLI → `results/processed/table*.csv` |
| Figures 2–5 | **Subset** for BCEL + CLI (after parsing) |
| Appendix A, Section 4.5 | Full documentation + scripts |

Details: [`docs/paper-to-artifact.md`](docs/paper-to-artifact.md).

## Known limitations

- Artifact covers **2/5** paper projects; three projects are reported in the manuscript only.
- Subset tables are **not** identical to paper aggregates that pool all five projects.
- One LLM generation per model–project pair; failing tests removed before PIT.

See [`docs/threats-to-validity.md`](docs/threats-to-validity.md) and [`results/STATUS.md`](results/STATUS.md).

## Anonymous GitHub

[`docs/anonymous-github-guide.md`](docs/anonymous-github-guide.md)

## License

Apache License 2.0 — [LICENSE](LICENSE).
