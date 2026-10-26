"""Check the worked strong-scaling efficiencies."""

import csv
from pathlib import Path

root = Path(__file__).resolve().parents[2]
rows = list(csv.DictReader((root / "files" / "timings.csv").open(encoding="utf-8")))
t1 = float(rows[0]["seconds"])
if int(rows[0]["cores"]) != 1:
    raise SystemExit("first row must be 1 core")
for row in rows:
    cores = int(row["cores"])
    seconds = float(row["seconds"])
    eff = t1 / (cores * seconds)
    print(f"{cores} {eff:.3f}")
last = t1 / (int(rows[-1]["cores"]) * float(rows[-1]["seconds"]))
if abs(last - 0.625) > 1e-9:
    raise SystemExit(f"expected 0.625, got {last}")
