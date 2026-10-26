# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Every cell of episode 3's directive table against its source file."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import repo_file

episodes = repo_file.config_episode_names()
if len(episodes) < 3:
    raise SystemExit("config has fewer than three episodes")
name = episodes[2]
if name != "slurm-jobs.md":
    raise SystemExit(f"episode 3 is {name}, expected slurm-jobs.md")

source = repo_file.ROOT / "episodes" / "files" / "slurm-directives.tsv"
with source.open(encoding="utf-8", newline="") as handle:
    expected = list(csv.reader(handle, delimiter="\t"))

text = (repo_file.ROOT / "episodes" / name).read_text(encoding="utf-8")
tables = []
current: list[list[str]] = []
for line in text.splitlines():
    if line.startswith("|"):
        current.append(line)
    elif current:
        tables.append("\n".join(current))
        current = []
if current:
    tables.append("\n".join(current))

found = None
for raw in tables:
    rows = repo_file.parse_pipe_table(raw)
    if rows and rows[0] == expected[0]:
        found = rows
        break
if found is None:
    raise SystemExit("episode 3 has no table with the directive header")
if found != expected:
    print("table:")
    for row in found:
        print(row)
    print("source:")
    for row in expected:
        print(row)
    raise SystemExit("episode 3 table does not match slurm-directives.tsv")
print(f"episode 3 table ok ({len(found) - 1} rows)")
