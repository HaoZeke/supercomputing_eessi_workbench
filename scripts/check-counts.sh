#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python - << 'PY'
import sys
from pathlib import Path
sys.path.insert(0, "scripts")
import repo_file

fail = []
episodes = repo_file.config_episode_names()
index = Path("index.md").read_text(encoding="utf-8")
if len(episodes) != 6:
    fail.append(f"config has {len(episodes)} episodes, expected 6")
if "six episodes" not in index:
    fail.append("index.md does not say six episodes")

tsv = Path("episodes/files/filesystems.tsv").read_text(encoding="utf-8")
fs = Path("episodes/filesystems-and-data.md").read_text(encoding="utf-8")
for token in ("200 GiB", "14 days", "6 days"):
    if token not in tsv or token not in fs:
        fail.append(f"{token} missing from the filesystem table or episode")

perf = Path("episodes/performance-first-steps.md").read_text(encoding="utf-8")
import subprocess
table = subprocess.check_output([sys.executable, "scripts/density-table.py"], text=True)
for line in table.splitlines():
    eff = line.split()[-1]
    if eff not in perf:
        fail.append(f"performance episode is missing efficiency {eff}")

sizes = [line for line in Path("learners/sample-buildlist").read_text(encoding="utf-8").splitlines() if line.strip()]
live = Path("learners/a-live-subject.md").read_text(encoding="utf-8")
if len(sizes) != 4:
    fail.append(f"sample build list has {len(sizes)} lines")
if "four sample sizes" not in live:
    fail.append("live subject does not say four sample sizes")

if fail:
    print("\n".join(fail))
    sys.exit(1)
print("counts ok")
PY
