# Threats to Validity and Limitations

**Paper reference:** Section 6

This replication package documents known threats so reviewers can interpret results within the study's constraints.

## Internal validity

### Prompt dependency

All LLM-generated suites depend on the standardized prompt (Appendix A). Different prompts, example ordering, or wording could yield different coverage and mutation results.

**Mitigation in package:** Exact prompt in `prompts/test-generation-prompt.md`.

### LLM non-determinism

LLMs may produce different outputs across runs even with the same prompt. The study performed **one generation per model–project pair**.

**Mitigation in package:** `results/STATUS.md` records which runs exist; future work may add multiple seeds.

### Failing-test filtering

Tests that fail compilation or execution were removed before PIT analysis. This may discard tests that exercised relevant behavior.

**Mitigation in package:** Log removals in `logs/removed-tests.csv`.

## External validity

### Limited subject systems

The paper evaluates five Apache Commons Java/Maven projects. Results may not generalize to other domains, languages, frameworks, or architectures.

### Artifact distribution scope

The replication package is a **light artifact** by design: full methodology and published per-class metrics for all five projects, without bundled source code or test suites.

**Mitigation in package:** `docs/package-scope.md`, `config/package-scope.json`, `results/per-class/`, aggregated tables in `results/processed/`.

### Limited models

Opus 4.5, GPT-5.1 Codex Max, Sonnet 4.5 via Cursor Pro 2.1.39. Other models, versions, or integrations may differ.

### Tool and metric limitations

- Line coverage does not guarantee effective assertions.
- Mutation testing depends on PIT operators; some mutants may be equivalent.
- Test strength must be interpreted together with mutation coverage.

## Construct validity

No single metric fully characterizes test-suite quality. The study uses complementary structural (JaCoCo) and behavioral (PIT) metrics.

## Replication constraints

| Fully reproducible | Partially reproducible | Not reproducible without authors' environment |
|--------------------|------------------------|-----------------------------------------------|
| Project checkout | LLM-generated tests (if archived) | Exact LLM re-generation |
| Baseline metrics | Aggregated tables (if raw data present) | Cursor session context |
| JaCoCo/PIT collection | Figures from processed CSVs | Model stochasticity |

## Future work (from paper)

- More projects, languages, frameworks, LLMs
- Alternative prompting strategies
- Multiple independent generations per pair
- Hybrid LLM + mutation-guided feedback approaches
