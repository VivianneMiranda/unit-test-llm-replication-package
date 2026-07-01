#!/usr/bin/env bash
# Remove all existing tests to prepare for LLM generation.
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <project-id> [--force]"
  exit 1
fi

PROJECT="$1"
FORCE="${2:-}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG="$ROOT/config/projects.json"

project_dir=$(jq -r --arg id "$PROJECT" '.projects[] | select(.id==$id) | .directory' "$CONFIG")
name=$(jq -r --arg id "$PROJECT" '.projects[] | select(.id==$id) | .name' "$CONFIG")
test_dir="$ROOT/$project_dir/src/test/java"

if [[ ! -d "$ROOT/$project_dir" ]]; then
  echo "Project not found. Run scripts/00_setup.sh first."
  exit 1
fi

if [[ "$FORCE" != "--force" ]]; then
  read -r -p "Delete all tests under $test_dir? [y/N] " ans
  [[ "$ans" =~ ^[yY] ]] || exit 0
fi

rm -rf "$test_dir"
mkdir -p "$test_dir"
echo "[prepare] Removed all tests from $name. Ready for LLM generation."
