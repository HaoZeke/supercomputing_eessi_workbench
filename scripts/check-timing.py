# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Instructor timing table against episode front matter."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import repo_file

notes = (repo_file.ROOT / "instructors" / "instructor-notes.md").read_text(encoding="utf-8")
rows = repo_file.parse_pipe_table(notes)
header = None
table = []
for row in rows:
    if [cell.lower() for cell in row[:3]] == ["page", "teaching", "exercises"]:
        header = row
        table = []
        continue
    if header and len(row) >= 3 and row[0].endswith(".md"):
        table.append(row)
if not table:
    raise SystemExit("instructor notes have no timing table")

by_page = {row[0]: (int(row[1]), int(row[2])) for row in table}
fail = []
total_t = 0
total_e = 0
for name in repo_file.config_episode_names():
    text = (repo_file.ROOT / "episodes" / name).read_text(encoding="utf-8")
    teaching, exercises = repo_file.front_matter_minutes(text)
    total = teaching + exercises
    total_t += teaching
    total_e += exercises
    if not 30 <= total <= 60:
        fail.append(f"{name} is {total} minutes, expected 30 to 60")
    if name not in by_page:
        fail.append(f"{name} is missing from the instructor timing table")
        continue
    if by_page[name] != (teaching, exercises):
        fail.append(f"{name} notes {by_page[name]} front matter {(teaching, exercises)}")

extra = sorted(set(by_page) - set(repo_file.config_episode_names()))
for name in extra:
    fail.append(f"timing table has unknown page {name}")

if fail:
    print("\n".join(fail))
    sys.exit(1)
print(f"timing ok, teaching {total_t}, exercises {total_e}")
