# Replication Package Scope

This artifact is a **subset** of the full SAST 2026 empirical study.

## Included in this package

| Project | Version | Variants | Location |
|---------|---------|----------|----------|
| Apache Commons BCEL | 6.13.0 | developer + 3 LLMs | [`commons-bcel/`](../commons-bcel/README.md) |
| Apache Commons CLI | 1.11.0 | developer + 3 LLMs | [`commons-cli/`](../commons-cli/README.md) |

**8 experimental runs** (2 projects × 4 origins) with archived test code and local metric outputs under each variant's `target/` directory.

## Not included (paper only)

| Project | Version | Reason |
|---------|---------|--------|
| Commons Collections | 4.6.0 | Artifacts no longer available |
| Commons Compress | 1.29.0 | Artifacts no longer available |
| Commons Lang | 3.20.1 | Artifacts no longer available |

Aggregated statistics in the paper (Tables 2–4, Figures 2–5) combine **all five projects**. This package can reproduce the **methodology** and **per-class metrics for BCEL and CLI** after archiving/parsing local reports. It does **not** recreate paper-wide aggregates that depend on the three missing projects.

## Configuration

- Scope definition: [`config/package-scope.json`](../config/package-scope.json)
- Full study metadata (all 5 projects): [`config/projects.json`](../config/projects.json)
- Included snapshots: [`config/included-artifacts.json`](../config/included-artifacts.json)

## For reviewers

You do **not** need Collections, Compress, or Lang to exercise this artifact. Clone the repository, inspect `commons-bcel/` and `commons-cli/`, and optionally re-run or parse metrics using `scripts/` for those two projects only.
