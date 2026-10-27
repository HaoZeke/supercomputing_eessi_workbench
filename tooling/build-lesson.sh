#!/usr/bin/env bash
# Build one lesson in a temporary copy and print the docs directory.
set -euo pipefail
if [[ $# -ne 1 ]]; then
  echo "usage: build-lesson.sh LESSON_DIR" >&2
  exit 2
fi
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LESSON="$(cd "$1" && pwd)"
RSCRIPT="${RSCRIPT:-Rscript}"
export RSCRIPT
bash "$ROOT/tooling/install-logo.sh"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
SLUG="$(basename "$LESSON")"
mkdir -p "$WORK/lessons"
# The expander finds sites/ by walking up to the parent of lessons/.
ln -s "$ROOT/sites" "$WORK/sites"
# Copy the lesson without a previous site build.
mkdir -p "$WORK/lessons/$SLUG"
tar -C "$LESSON" --exclude site --exclude .git -cf - . | tar -C "$WORK/lessons/$SLUG" -xf -
python3 "$ROOT/tooling/expand_sites.py" "$WORK/lessons/$SLUG"
# Sandpaper asks libgit2 for a repository. The build copy is not the checkout.
git -C "$WORK/lessons/$SLUG" init -q
git -C "$WORK/lessons/$SLUG" add -A
git -C "$WORK/lessons/$SLUG" -c user.name=build -c user.email=build@example.com commit -q -m "build copy" --allow-empty
# Sandpaper logs go to stderr. The only stdout is the docs path.
(
  cd "$WORK/lessons/$SLUG"
  "$RSCRIPT" "$ROOT/tooling/build-lesson.R"
) >&2
# The caller copies this path before the trap removes it, so leave the
# docs tree on stdout and disable the trap by moving it out.
DEST="$(mktemp -d)"
rm -rf "$DEST"
mkdir -p "$(dirname "$DEST")"
mv "$WORK/lessons/$SLUG/site/docs" "$DEST"
trap - EXIT
rm -rf "$WORK"
echo "$DEST"
