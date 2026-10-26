#!/usr/bin/env bash
# Copy the supersurf mark into varnish so carpentry: supersurf resolves.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RSCRIPT="${RSCRIPT:-Rscript}"
IMG="$("$RSCRIPT" -e 'cat(system.file("pkgdown", "assets", "assets", "images", package = "varnish"))')"
if [[ -z "$IMG" || ! -d "$IMG" ]]; then
  echo "varnish image directory not found" >&2
  exit 1
fi
cp "$ROOT/site_assets/assets/logo.svg" "$IMG/supersurf-logo.svg"
cp "$ROOT/site_assets/assets/logo.svg" "$IMG/supersurf-logo-sm.svg"
