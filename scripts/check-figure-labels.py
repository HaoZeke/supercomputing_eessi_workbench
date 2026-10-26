# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Node labels must match the enumerated facts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import repo_file

listed: dict[str, list[str]] = {}
for line in (repo_file.ROOT / "fig_src" / "figures.enumerates").read_text(encoding="utf-8").splitlines():
    if not line.strip() or line.startswith("#"):
        continue
    stem, label = line.split("\t", 1)
    listed.setdefault(stem, []).append(label)

fail = []
for stem in repo_file.figure_stems():
    labels = repo_file.dot_node_labels((repo_file.ROOT / "fig_src" / f"{stem}.dot").read_text(encoding="utf-8"))
    if labels != listed.get(stem, []):
        fail.append(f"{stem}: dot {labels} enumerated {listed.get(stem, [])}")

extra = sorted(set(listed) - set(repo_file.figure_stems()))
for stem in extra:
    fail.append(f"{stem} is enumerated but has no dot file")

if fail:
    print("\n".join(fail))
    sys.exit(1)
print(f"figure labels ok ({len(listed)} diagrams)")
