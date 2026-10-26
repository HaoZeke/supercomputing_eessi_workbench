#!/usr/bin/env bash
# One Beamer deck per episode, plus the course opener.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p slides
export TEXINPUTS="./theme:${TEXINPUTS:-}"

while IFS= read -r org; do
  case "$org" in
    org_src/episodes/*.org) ;;
    *) continue ;;
  esac
  stem="$(basename "$org" .org)"
  title="$(sed -n 's/^title: "\(.*\)"/\1/p' "$org" | head -n 1)"
  WORKBENCH_TARGET=slides pandoc \
    --from=org \
    --to=beamer \
    --slide-level=1 \
    -M "title=${title}" \
    -M "author=Rohit Goswami" \
    --lua-filter=scripts/drop-slides.lua \
    --lua-filter=slides/filters/carpentries.lua \
    --include-in-header=slides/preamble.tex \
    --resource-path=episodes \
    -o "slides/${stem}.tex" "$org"
  (cd slides && tectonic --outdir . "${stem}.tex")
done < <(python scripts/repo_file.py --list-org)

(cd slides && tectonic --outdir . rgcourse.tex)
