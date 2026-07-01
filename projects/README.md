# Optional checkout directory (not used by this artifact)

This replication package **does not require** any project under `projects/`.

Included study artifacts live at the repository root:

- [`commons-bcel/`](../commons-bcel/README.md)
- [`commons-cli/`](../commons-cli/README.md)

Collections, Compress, and Lang from the paper are documented in [`config/projects.json`](../config/projects.json) for reference only. See [`docs/package-scope.md`](../docs/package-scope.md).

The script `scripts/00_setup.ps1` can still clone all five paper projects if you extend the study locally; it is **not** part of the reviewer workflow for this package.
