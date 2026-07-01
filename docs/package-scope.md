# Replication Package Scope

This artifact is a **light replication package** for the full SAST 2026 empirical study.

## Included in this package

| Content | Location |
|---------|----------|
| Experimental protocol and Appendix A prompt | `docs/`, `prompts/` |
| Per-class JaCoCo/PIT metrics (5 projects × 4 origins) | `results/per-class/` |
| Aggregated Tables 2–4 | `results/processed/` |
| Reproduction scripts | `scripts/` |
| Study metadata (Table 1) | `config/projects.json` |

**20 experimental runs** (5 projects × 4 test-suite origins) with published metrics. Source code and test suites are **not** shipped.

## Not bundled

| Item | Reason |
|------|--------|
| Apache Commons source trees | Large; cloned locally via `scripts/00_setup.*` |
| LLM-generated test suites | Generated during reproduction with Cursor |
| Raw JaCoCo/PIT HTML reports | Optional output of local `03_collect_metrics.*` |

## Configuration

- Scope definition: [`config/package-scope.json`](../config/package-scope.json)
- Study metadata: [`config/projects.json`](../config/projects.json)

## For reviewers

You do **not** need to clone projects or re-run Maven to review the study results. Inspect `results/per-class/` and `results/processed/`. To reproduce the protocol end-to-end, run `scripts/00_setup.ps1` and follow [`docs/experimental-protocol.md`](experimental-protocol.md).
