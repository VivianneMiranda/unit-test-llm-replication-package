# Local project checkout directory

This directory is **empty in the git repository**. It is populated locally when reproducing the study:

```powershell
.\scripts\00_setup.ps1
```

Each subdirectory matches `config/projects.json`:

| Directory | Paper version |
|-----------|---------------|
| `projects/commons-collections` | 4.6.0 |
| `projects/commons-compress` | 1.29.0 |
| `projects/commons-lang` | 3.20.1 |
| `projects/commons-cli` | 1.11.0 |
| `projects/commons-bcel` | 6.13.0 |

Published study metrics are in [`results/per-class/`](../results/README.md). You do not need to clone these projects to review the paper results.

See [`docs/package-scope.md`](../docs/package-scope.md) and [`docs/experimental-protocol.md`](../docs/experimental-protocol.md).
