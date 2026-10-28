#!/usr/bin/env bash
# Build every lesson and assemble one site under site/docs.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export SUPERSURF_SITES="${SUPERSURF_SITES:-course}"
export RSCRIPT="${RSCRIPT:-Rscript}"
OUT="$ROOT/site/docs"
rm -rf "$OUT"
mkdir -p "$OUT"

python3 "$ROOT/tooling/check_sites.py"

shopt -s nullglob
found=0
for lesson in "$ROOT"/lessons/*; do
  [[ -f "$lesson/config.yaml" ]] || continue
  slug="$(basename "$lesson")"
  echo "== building $slug =="
  docs="$(bash "$ROOT/tooling/build-lesson.sh" "$lesson")"
  mkdir -p "$OUT/$slug"
  cp -a "$docs/." "$OUT/$slug/"
  if [[ -f "$docs/assets/images/orcid_icon.png" ]]; then
    install -Dm644 "$docs/assets/images/orcid_icon.png" "$OUT/assets/images/orcid_icon.png"
  fi
  rm -rf "$docs"
  found=$((found + 1))
done
shopt -u nullglob

if [[ "$found" -eq 0 ]]; then
  echo "no lessons to build" >&2
  exit 1
fi

if [[ -f "$ROOT/schedule.yaml" && -f "$ROOT/tooling/schedule.py" ]]; then
  python3 "$ROOT/tooling/schedule.py" "$OUT"
else
  cp "$ROOT/site_assets/assets/logo.svg" "$OUT/logo.svg"
  cat > "$OUT/index.html" <<EOF
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>supersurf</title>
</head>
<body>
<p>Lesson sites are under each slug. The workshop page is added with the schedule.</p>
</body>
</html>
EOF
fi

printf '%s\n' 'supersurf.rgoswami.me' > "$OUT/CNAME"
python3 "$ROOT/tooling/check_links.py" "$OUT"
echo "assembled $found lessons in $OUT"
