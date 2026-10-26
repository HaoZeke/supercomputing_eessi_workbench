#!/usr/bin/env bash
# Render fig_src/*.dot to PNG, SVG, and a dark SVG.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p episodes/fig
shopt -s nullglob
for dotfile in fig_src/*.dot; do
  stem="$(basename "$dotfile" .dot)"
  dot -Tpng -Gdpi=144 -o "episodes/fig/${stem}.png" "$dotfile"
  dot -Tsvg -o "episodes/fig/${stem}.svg" "$dotfile"
  dot -Tsvg \
    -Gbgcolor="#1c1c1c" \
    -Nfillcolor="#2c2c2c" \
    -Nfontcolor="#f2f2f2" \
    -Ncolor="#f2f2f2" \
    -Ecolor="#d0d0d0" \
    -Efontcolor="#f2f2f2" \
    -o "episodes/fig/${stem}-dark.svg" "$dotfile"
done
