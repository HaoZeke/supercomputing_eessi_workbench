# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Print the sample-size build list used by the live subject."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
lines = [
    line.strip()
    for line in (ROOT / "learners" / "sample-buildlist").read_text(encoding="utf-8").splitlines()
    if line.strip()
]
for line in lines:
    if not line.isdigit() or int(line) <= 0:
        raise SystemExit(f"not a sample size: {line}")
    print(line)
