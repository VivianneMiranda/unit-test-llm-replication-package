#!/usr/bin/env bash
# Run developer baseline metrics for one project.
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <project-id>"
  echo "  project-id: bcel | cli | collections | compress | lang"
  exit 1
fi

PROJECT="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/03_collect_metrics.sh" "$PROJECT" developer
