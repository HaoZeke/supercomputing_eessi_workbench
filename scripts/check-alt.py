# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Figure alt text must match figures.alt and name every node."""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import repo_file

mapping = {}
for line in (repo_file.ROOT / "fig_src" / "figures.alt").read_text(encoding="utf-8").splitlines():
    if not line.strip() or line.startswith("#"):
        continue
    name, alt = line.split("\t", 1)
    mapping[name] = alt

fail = []
seen = set()
for path in repo_file.generated_markdown():
    if not path.exists():
        continue
    for alt, src in re.findall(r"!\[(.*?)\]\(([^)\s]+)\)", path.read_text(encoding="utf-8")):
        name = Path(src).name
        if name not in mapping:
            continue
        seen.add(name)
        if alt != mapping[name]:
            fail.append(f"{path.name} alt for {name} does not match figures.alt")
        stem = Path(name).stem
        labels = repo_file.dot_node_labels(
            (repo_file.ROOT / "fig_src" / f"{stem}.dot").read_text(encoding="utf-8")
        )
        for label in labels:
            if label not in alt:
                fail.append(f"{name} alt is missing node {label}")

missing = sorted(set(mapping) - seen)
for name in missing:
    fail.append(f"{name} has alt text but is not used")

if fail:
    print("\n".join(fail))
    sys.exit(1)
print(f"alt text ok ({len(seen)} figures)")
