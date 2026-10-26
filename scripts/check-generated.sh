#!/usr/bin/env bash
# Regenerated pages must match what is committed, and pandoc must match the lock.
set -euo pipefail
cd "$(dirname "$0")/.."
bash build.sh
status="$(git status --porcelain -- index.md episodes learners instructors profiles)"
if [[ -n "$status" ]]; then
  echo "$status"
  echo "generated pages differ from the committed tree"
  exit 1
fi
have="$(pandoc -v | awk 'NR==1 {print $2}')"
want="$(python scripts/repo_file.py --pandoc-version-from-lock)"
if [[ "$have" != "$want" ]]; then
  echo "pandoc is ${have}, lock has ${want}"
  exit 1
fi
echo "generated pages match pandoc ${have}"
