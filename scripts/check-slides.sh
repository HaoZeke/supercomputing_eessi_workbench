#!/usr/bin/env bash
# Each episode figure must survive into the deck built from that episode.
set -euo pipefail
cd "$(dirname "$0")/.."
bash scripts/slides.sh
fail=0
for md in episodes/*.md; do
  stem="$(basename "$md" .md)"
  tex="slides/${stem}.tex"
  if [[ ! -f "$tex" || ! -f "slides/${stem}.pdf" ]]; then
    echo "missing deck for ${stem}"
    fail=1
    continue
  fi
  while IFS= read -r svg; do
    [[ -n "$svg" ]] || continue
    png="$(basename "$svg" .svg).png"
    if ! grep -q -F "$png" "$tex"; then
      echo "${tex} dropped ${png}"
      fail=1
    fi
  done < <(grep -o 'fig/[A-Za-z0-9_-]*\.svg' "$md" | sort -u)
done
if [[ ! -f slides/rgcourse.pdf ]]; then
  echo "missing slides/rgcourse.pdf"
  fail=1
fi
exit "$fail"
