#!/usr/bin/env bash
# Run the offline exercises.
set -euo pipefail
cd "$(dirname "$0")/.."
fail=0
for script in episodes/files/exercises/*.sh; do
  echo "-- $script"
  if ! bash "$script"; then
    echo "FAILED $script"
    fail=1
  fi
done
venv="${TMPDIR:-/tmp}/scew-exercise-venv"
if [[ ! -x "${venv}/bin/python" ]] || ! "${venv}/bin/python" -c 'import qcg' 2>/dev/null; then
  python -m venv "$venv"
  "${venv}/bin/pip" install -q qcg-pilotjob
fi
for script in episodes/files/exercises/*.py; do
  echo "-- $script"
  if ! "${venv}/bin/python" "$script"; then
    echo "FAILED $script"
    fail=1
  fi
done
exit "$fail"
