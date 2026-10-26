# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""The tool table on the page is taught as bullets in the deck."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import repo_file

page = (repo_file.ROOT / "episodes" / "many-tasks.md").read_text(encoding="utf-8")
rows = repo_file.parse_pipe_table(page)
tools = []
for row in rows:
    if row and row[0] == "Tool":
        continue
    if row and row[0] in {"QCG-PilotJob", "HyperQueue", "Snakemake", "Slurm array", "FireWorks"}:
        tools.append(row[0])
if len(tools) != 5:
    raise SystemExit(f"expected 5 tools in the page table, found {tools}")

tex_path = repo_file.ROOT / "slides" / "many-tasks.tex"
if not tex_path.exists():
    raise SystemExit("slides/many-tasks.tex is missing. Run slides first.")
items = []
for line in tex_path.read_text(encoding="utf-8").splitlines():
    if "\\item" in line:
        items.append(line)
blob = "\n".join(items)
missing = [tool for tool in tools if tool not in blob]
if missing:
    raise SystemExit(f"deck bullets are missing {missing}")
print("matrix ok")
