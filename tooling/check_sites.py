#!/usr/bin/env python3
"""Every site div has a Magic Castle snippet, and the course cluster is named."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import expand_sites as ex

ROOT = Path(__file__).resolve().parent.parent
COURSE = ROOT / "sites/SURF_Course_slurm"
COURSE_CUSTOM = (
    ROOT
    / "lessons/fundamentals/episodes/files/customization/SURF_Course_slurm"
)
REQUIRED = {
    COURSE / "snippets/cluster-identity.md": (
        "SURF Research Cloud",
        "welcome note",
        "rome",
    ),
    COURSE / "snippets/partition-request.md": (
        "SURF Research Cloud",
        "--partition=rome",
    ),
    COURSE / "snippets/ssh-login.md": (
        "SURF Research Cloud",
        "welcome note",
    ),
    COURSE / "snippets/mpifileutils.md": (
        "TODO(Rohit)",
        "mpiFileUtils",
    ),
    COURSE / "_config_options.yml": (
        "SURF Research Cloud workspace",
        'testing: "rome"',
        "--partition=rome",
    ),
}
# mpiFileUtils availability is still marked. Every other course-cluster
# file states the workspace and the rome partition.
SKIP_FORBIDDEN = {COURSE / "snippets/mpifileutils.md"}
FORBIDDEN = (
    "TODO(Rohit)",
    "thin_course",
    "Magic Castle",
    "does not choose",
    "does not pick",
    "--partition=PARTITION",
    "placeholder",
)


def referenced_names() -> set[str]:
    names = set()
    for path in (ROOT / "lessons").rglob("*"):
        if path.suffix.lower() not in {".md", ".rmd"}:
            continue
        if "customization" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for match in ex.SITE_DIV.finditer(text):
            names.add(match.group("name"))
        for match in ex.SNIPPET_CALL.finditer(text):
            names.add(match.group(1))
    return names


def course_files() -> list[Path]:
    files = []
    for root in (COURSE, COURSE_CUSTOM):
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in {".md", ".rmd", ".yml", ".yaml"}:
                files.append(path)
    return files


def main() -> int:
    errors = []
    for path, needles in REQUIRED.items():
        if not path.is_file():
            errors.append(f"missing {path}")
            continue
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"{path.relative_to(ROOT)} does not mention {needle}")
    for path in course_files():
        if path in SKIP_FORBIDDEN:
            continue
        text = path.read_text(encoding="utf-8")
        for needle in FORBIDDEN:
            if needle in text:
                errors.append(f"{path.relative_to(ROOT)} still contains {needle}")
    base = ROOT / "sites" / ex.BASE_SITE / "snippets"
    for name in sorted(referenced_names()):
        if "/" in name:
            # hpc-intro snippet paths live under the vendored customization tree.
            continue
        hits = list(base.glob(name)) + list(base.glob(name + ".md")) + list(base.glob(name + ".Rmd"))
        if not hits:
            errors.append(f"no Magic Castle snippet for {name}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"site checks ok ({len(referenced_names())} snippet names)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
