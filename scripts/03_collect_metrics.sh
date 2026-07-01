#!/usr/bin/env bash
# Collect JaCoCo and PIT metrics for a project and origin.
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <project-id> <origin>"
  echo "  origin: developer | opus-4.5 | sonnet-4.5 | gpt-5.1-codex-max"
  exit 1
fi

PROJECT="$1"
ORIGIN="$2"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG="$ROOT/config/projects.json"

name=$(jq -r --arg id "$PROJECT" '.projects[] | select(.id==$id) | .name' "$CONFIG")
abs_project=$(python3 "$SCRIPT_DIR/resolve_project_path.py" "$PROJECT" "$ORIGIN")
raw_out="$ROOT/results/raw/$PROJECT/$ORIGIN"

if [[ ! -d "$abs_project" ]]; then
  echo "Project not found at '$abs_project'. Run scripts/00_setup.sh or add paths in config/artifact-locations.json."
  exit 1
fi
echo "[path] Using $abs_project"

mkdir -p "$raw_out"
cd "$abs_project"

echo "[maven] JaCoCo: $name / $ORIGIN"
mvn clean test jacoco:report

if [[ -d target/site/jacoco ]]; then
  rm -rf "$raw_out/jacoco"
  cp -r target/site/jacoco "$raw_out/jacoco"
fi

echo "[maven] PIT: $name / $ORIGIN (this may take a long time)"
mvn test org.pitest:pitest-maven:mutationCoverage

if [[ -d target/pit-reports ]]; then
  latest=$(ls -td target/pit-reports/*/ 2>/dev/null | head -1)
  if [[ -n "$latest" ]]; then
    rm -rf "$raw_out/pit"
    cp -r "$latest" "$raw_out/pit"
  fi
fi

echo "[metrics] Reports copied to $raw_out"
python3 "$SCRIPT_DIR/04_parse_results.py" --project "$PROJECT" --origin "$ORIGIN"
