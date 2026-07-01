#!/usr/bin/env python3
"""Resolve project directory for a given project id and test-suite origin."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def resolve_project_dir(project_id: str, origin: str | None = None) -> Path:
    locations_path = ROOT / "config" / "artifact-locations.json"
    if origin and locations_path.exists():
        with open(locations_path, encoding="utf-8") as f:
            locations = json.load(f)
        project_map = locations.get(project_id)
        if isinstance(project_map, dict) and origin in project_map:
            candidate = ROOT / project_map[origin]
            if candidate.exists():
                return candidate

    with open(ROOT / "config" / "projects.json", encoding="utf-8") as f:
        config = json.load(f)
    for project in config["projects"]:
        if project["id"] == project_id:
            return ROOT / project["directory"]

    raise SystemExit(f"Unknown project id: {project_id}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Resolve project directory path")
    parser.add_argument("project")
    parser.add_argument("origin", nargs="?")
    args = parser.parse_args()
    print(resolve_project_dir(args.project, args.origin))


if __name__ == "__main__":
    main()
