#!/usr/bin/env bash
# Clone Apache Commons projects at exact study versions.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG="$ROOT/config/projects.json"

if ! command -v jq &>/dev/null; then
  echo "Error: jq is required. Install jq or use 00_setup.ps1 on Windows."
  exit 1
fi

count=$(jq '.projects | length' "$CONFIG")
for i in $(seq 0 $((count - 1))); do
  id=$(jq -r ".projects[$i].id" "$CONFIG")
  name=$(jq -r ".projects[$i].name" "$CONFIG")
  url=$(jq -r ".projects[$i].git_url" "$CONFIG")
  tag=$(jq -r ".projects[$i].git_tag" "$CONFIG")
  dest=$(jq -r ".projects[$i].directory" "$CONFIG")
  dest_path="$ROOT/$dest"

  if [[ -d "$dest_path/.git" ]]; then
    echo "[skip] $name already cloned at $dest_path"
    continue
  fi

  echo "[clone] $name tag $tag -> $dest_path"
  mkdir -p "$dest_path"
  if ! git clone --depth 1 --branch "$tag" "$url" "$dest_path"; then
    echo "[retry] full clone + checkout for $id"
    rm -rf "$dest_path"
    git clone "$url" "$dest_path"
    (cd "$dest_path" && git checkout "$tag")
  fi
done

echo "Setup complete. Projects are under projects/"
