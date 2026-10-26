# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Strong-scaling efficiency for the worked timing table."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import repo_file

path = repo_file.ROOT / "episodes" / "files" / "timings.csv"
with path.open(encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle))
t1 = float(rows[0]["seconds"])
if int(rows[0]["cores"]) != 1:
    raise SystemExit("the first timing row must be one core")
for row in rows:
    cores = int(row["cores"])
    seconds = float(row["seconds"])
    eff = repo_file.efficiency(t1, cores, seconds)
    print(f"{cores} {seconds:.1f} {eff:.3f}")
