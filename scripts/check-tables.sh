#!/usr/bin/env bash
# A table with four or more columns needs its own scrolling box.
set -euo pipefail
cd "$(dirname "$0")/.."
python - << 'PY'
from pathlib import Path
import sys

def columns(line: str) -> int:
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    return len([cell for cell in cells if cell != "" or True])

fail = 0
for path in sorted(Path(".").glob("episodes/*.md")) + [Path("learners") / p.name for p in Path("learners").glob("*.md")] + [Path("index.md"), Path("instructors/instructor-notes.md")]:
    if not path.exists():
        continue
    lines = path.read_text(encoding="utf-8").splitlines()
    for index, line in enumerate(lines):
        if not line.startswith("|"):
            continue
        if set(line.replace("|", "").replace(":", "").replace("-", "").strip()) == set():
            continue
        # header row of a table is a pipe line followed by a separator
        if index + 1 >= len(lines) or not lines[index + 1].startswith("|"):
            continue
        sep = lines[index + 1]
        if "---" not in sep:
            continue
        width = len([cell for cell in line.strip().strip("|").split("|")])
        if width < 4:
            continue
        window = "\n".join(lines[max(0, index - 4): index + 1])
        end = "\n".join(lines[index: min(len(lines), index + 12)])
        if '<div class="table-responsive">' not in window or "</div>" not in end:
            print(f"{path}:{index + 1}: wide table is not in a scrolling box ({width} columns)")
            fail = 1
sys.exit(fail)
PY
