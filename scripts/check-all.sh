#!/usr/bin/env bash
# Run every check. Keep going after a failure.
set -u
cd "$(dirname "$0")/.."
fail=0
run() {
  echo "== $* =="
  if ! "$@"; then
    echo "FAILED: $*"
    fail=1
  fi
}
run uv run --script scripts/check-primitives.py
run bash scripts/check-drift.sh
run bash scripts/check-generated.sh
run bash scripts/check-exercises.sh
run bash scripts/check-links.sh
run uv run --script scripts/check-timing.py
run bash scripts/check-counts.sh
run uv run --script scripts/check-episode-three.py
run bash scripts/check-figures.sh
run bash scripts/check-slides.sh
run bash scripts/check-tables.sh
run uv run --script scripts/check-alt.py
run uv run --script scripts/check-matrix.py
run uv run --script scripts/check-output-blocks.py
exit "$fail"
