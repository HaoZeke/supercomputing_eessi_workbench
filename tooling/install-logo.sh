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

# The navbar logo is the SVG above. These files are what the page head links.
FAV="$("$RSCRIPT" -e 'cat(system.file("pkgdown", "assets", "favicons", package = "varnish"))')"
if [[ -z "$FAV" || ! -d "$FAV" ]]; then
  echo "varnish favicon directory not found" >&2
  exit 1
fi
DEST="$FAV/supersurf"
mkdir -p "$DEST"
LOGO="$ROOT/site_assets/assets/logo.svg"
cp "$LOGO" "$DEST/safari-pinned-tab.svg"
rsvg-convert -w 180 -h 180 "$LOGO" -o "$DEST/apple-touch-icon.png"
rsvg-convert -w 32 -h 32 "$LOGO" -o "$DEST/favicon-32x32.png"
rsvg-convert -w 16 -h 16 "$LOGO" -o "$DEST/favicon-16x16.png"
rsvg-convert -w 192 -h 192 "$LOGO" -o "$DEST/android-chrome-192x192.png"
rsvg-convert -w 512 -h 512 "$LOGO" -o "$DEST/android-chrome-512x512.png"
cat > "$DEST/site.webmanifest" <<'EOF'
{"name":"supersurf","short_name":"supersurf","icons":[{"src":"android-chrome-192x192.png","sizes":"192x192","type":"image/png"},{"src":"android-chrome-512x512.png","sizes":"512x512","type":"image/png"}],"theme_color":"#123044","background_color":"#ffffff","display":"standalone"}
EOF
