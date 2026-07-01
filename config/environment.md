# Execution Environment

Documented environment for the SAST 2026 empirical study (Paper Section 4.5).

## Required software

| Component | Version | Notes |
|-----------|---------|-------|
| Java JDK | 21 | Required for compilation and test execution |
| Apache Maven | 3.8+ | Build, JaCoCo, PIT integration |
| Cursor | Pro 2.1.39 | LLM test generation with project context |
| Python | 3.9+ | For `scripts/organize_published_metrics.py` and `scripts/05_aggregate_tables.py` |

## LLM models (via Cursor)

| Model ID | Paper name |
|----------|------------|
| opus-4.5 | Claude Opus 4.5 |
| gpt-5.1-codex-max | GPT-5.1 Codex Max |
| sonnet-4.5 | Claude Sonnet 4.5 |

## Evaluation tools

| Tool | Purpose | Maven command |
|------|---------|---------------|
| JaCoCo | Line coverage, branch coverage, cyclomatic complexity | `mvn clean test jacoco:report` |
| PIT | Mutation coverage, test strength, PIT line coverage | `mvn test org.pitest:pitest-maven:mutationCoverage` |

**Note:** The paper does not pin JaCoCo/PIT plugin versions. After checkout, record the versions from each project's `pom.xml`:

```bash
mvn help:evaluate -Dexpression=jacoco.version -q -DforceStdout
mvn help:evaluate -Dexpression=pitest.version -q -DforceStdout
```

Store recorded versions in `logs/environment-versions.txt` when running experiments.

## Hardware recommendations

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| RAM | 8 GB | 16 GB+ |
| Disk | 5 GB free | 10 GB+ (PIT reports are large) |
| CPU | 4 cores | 8+ cores |

## Estimated runtime (per project)

| Step | Approximate time |
|------|------------------|
| Maven test + JaCoCo | 5–30 min |
| PIT mutation testing | 30 min – 4+ hours |
| LLM test generation | 30 min – 2 hours (manual, via Cursor) |

PIT on Commons BCEL and Lang is the slowest due to project size.

## Replication without Cursor

LLM-generated suites cannot be fully reproduced without access to the same models and IDE integration. The package includes:

- The exact prompt (`prompts/test-generation-prompt.md`)
- Published per-class metrics in `results/per-class/`
- Scripts to clone projects and re-run metrics locally (`scripts/00_setup.*`, `scripts/03_collect_metrics.*`)

Baseline (developer-written) suites and metric collection are fully reproducible via Maven after checkout.
