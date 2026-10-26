#!/usr/bin/env bash
# A second model of the pipeline, compared with repo_file.py and with build.sh.
set -euo pipefail
cd "$(dirname "$0")/.."
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

python scripts/repo_file.py --list-md | sed 's#^\./##' | sort > "$tmp/py-md"
{
  echo index.md
  for org in org_src/episodes/*.org org_src/learners/*.org org_src/instructors/*.org org_src/profiles/*.org; do
    base="$(basename "$org" .org)"
    folder="$(basename "$(dirname "$org")")"
    echo "${folder}/${base}.md"
  done
} | sort > "$tmp/sh-md"
diff -u "$tmp/sh-md" "$tmp/py-md"

python scripts/repo_file.py --build-snippets | sort > "$tmp/py-snip"
printf '%s\n' \
  --from=org \
  --shift-heading-level-by=1 \
  --wrap=none \
  scripts/drop-slides.lua \
  slides/filters/carpentries.lua \
  scripts/render-figures.sh \
  scripts/add-alt.py \
  | sort > "$tmp/sh-snip"
diff -u "$tmp/sh-snip" "$tmp/py-snip"

while IFS= read -r snippet; do
  if ! grep -F -q -- "$snippet" build.sh; then
    echo "build.sh is missing ${snippet}"
    exit 1
  fi
done < "$tmp/py-snip"

python - << 'PY'
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
import repo_file as rf

text = Path("scripts/render-figures.sh").read_text(encoding="utf-8")
for needle in ("${stem}.png", "${stem}.svg", "${stem}-dark.svg"):
    if needle not in text:
        raise SystemExit(f"render-figures.sh is missing {needle}")
expected = []
for stem in rf.figure_stems():
    for path in rf.figure_outputs(stem):
        expected.append(path.name)
print(f"drift ok ({len(expected)} figure outputs)")
PY
