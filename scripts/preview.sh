#!/usr/bin/env bash
# Readable pages with pandoc alone. No R.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p preview
css="site_assets/assets/css/brand.css"

while IFS= read -r md; do
  [[ -f "$md" ]] || continue
  out="preview/${md%.md}.html"
  mkdir -p "$(dirname "$out")"
  depth="$(printf '%s' "$out" | awk -F/ '{print NF-1}')"
  rel=""
  i=0
  while [[ "$i" -lt "$depth" ]]; do
    rel="../${rel}"
    i=$((i + 1))
  done
  pandoc "$md" links.md \
    --from=markdown \
    --to=html5 \
    --standalone \
    --css="${rel}${css}" \
    --resource-path=".:episodes:learners:instructors:profiles" \
    -o "$out"
done < <(python scripts/repo_file.py --list-md)

python scripts/add-alt-html.py
echo "preview/index.html"
