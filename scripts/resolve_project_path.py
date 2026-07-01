#!/usr/bin/env python3
"""Resolve project directory for a given project id."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def resolve_project_dir(project_id: str) -> Path:
    with open(ROOT / "config" / "projects.json", encoding="utf-8") as f:
        config = json.load(f)
    for project in config["projects"]:
        if project["id"] == project_id:
            return ROOT / project["directory"]

    raise SystemExit(f"Unknown project id: {project_id}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Resolve project directory path")
    parser.add_argument("project")
    parser.add_argument("origin", nargs="?", help="Ignored; kept for script compatibility")
    args = parser.parse_args()
    print(resolve_project_dir(args.project))


if __name__ == "__main__":
    main()
