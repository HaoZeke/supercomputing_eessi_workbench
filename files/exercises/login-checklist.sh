#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/../../.." && pwd)"
sample="${root}/episodes/files/ssh-config-sample"
host="$(awk '/^[[:space:]]*[Hh]ostName / { print $2 }' "$sample")"
if [[ "$host" != "snellius.surf.nl" ]]; then
  echo "expected HostName snellius.surf.nl, found ${host}" >&2
  exit 1
fi
echo "hostname=snellius.surf.nl"
