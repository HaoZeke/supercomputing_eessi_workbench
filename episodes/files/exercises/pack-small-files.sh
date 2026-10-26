#!/usr/bin/env bash
set -euo pipefail
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
mkdir -p "${work}/many"
i=0
while [[ "$i" -lt 50 ]]; do
  printf 'row %s\n' "$i" > "${work}/many/file-${i}.txt"
  i=$((i + 1))
done
files="$(find "${work}/many" -type f | wc -l | tr -d ' ')"
tar -C "$work" -cf "${work}/many.tar" many
members="$(tar -tf "${work}/many.tar" | grep -c -E 'file-[0-9]+\.txt$' || true)"
sha256sum "${work}/many.tar" > "${work}/many.tar.sha256"
if ! (cd "$work" && sha256sum -c many.tar.sha256 >/dev/null); then
  echo "checksum failed" >&2
  exit 1
fi
if [[ "$files" != "50" || "$members" != "50" ]]; then
  echo "files=${files} members=${members}" >&2
  exit 1
fi
echo "packed=50"
echo "checksum=ok"
