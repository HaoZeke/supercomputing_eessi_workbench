#!/usr/bin/env bash
# Build every lesson and assemble the course site.
set -euo pipefail
cd "$(dirname "$0")"
exec bash tooling/assemble-site.sh
