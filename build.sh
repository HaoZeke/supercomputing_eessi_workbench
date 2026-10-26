#!/usr/bin/env bash
# Export Org sources to Workbench Markdown and render the figures.
set -euo pipefail
cd "$(dirname "$0")"

bash scripts/render-figures.sh

while IFS= read -r org; do
  dest="$(python scripts/repo_file.py --md-for "$org")"
  mkdir -p "$(dirname "$dest")"
  WORKBENCH_TARGET=site pandoc \
    --from=org \
    --to=markdown-raw_tex-simple_tables-multiline_tables-grid_tables+pipe_tables+fenced_divs+raw_html \
    --shift-heading-level-by=1 \
    --wrap=none \
    --markdown-headings=atx \
    --lua-filter=scripts/drop-slides.lua \
    --lua-filter=slides/filters/carpentries.lua \
    -o "$dest" "$org"
done < <(python scripts/repo_file.py --list-org)

python scripts/add-alt.py
python scripts/make-favicons.py
