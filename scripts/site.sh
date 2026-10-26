#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

if [[ "${1:-}" == "serve" ]]; then
  if [[ ! -d site/docs ]]; then
    echo "site/docs is missing. Run: pixi run site" >&2
    exit 1
  fi
  exec python -m http.server 8000 --directory site/docs
fi

Rscript scripts/build-lesson.R
python scripts/add-alt-html.py
if [[ -f site_assets/favicons/incubator/favicon.ico && -d site/docs ]]; then
  cp site_assets/favicons/incubator/favicon.ico site/docs/favicon.ico
fi
