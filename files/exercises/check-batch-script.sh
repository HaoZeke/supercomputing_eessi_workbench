#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/../../.." && pwd)"
script="${root}/episodes/files/pi-snellius.sh"
bash -n "$script"
for flag in --job-name --partition --cpus-per-task --time --output; do
  if ! grep -q -F "#SBATCH ${flag}" "$script"; then
    echo "missing ${flag}" >&2
    exit 1
  fi
done
if ! grep -q -F "module load 2025" "$script"; then
  echo "missing module load 2025" >&2
  exit 1
fi
echo "batch-script=ok"
