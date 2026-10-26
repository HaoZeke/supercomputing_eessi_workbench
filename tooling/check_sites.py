#!/usr/bin/env python3
"""Every site div has a Magic Castle snippet, and the open questions stay marked."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import expand_sites as ex

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_TODOS = {
    ROOT / "sites/SURF_Course_slurm/snippets/cluster-identity.md": (
        "TODO(Rohit)",
        "thin_course",
        "rome",
    ),
    ROOT / "sites/SURF_Course_slurm/snippets/partition-request.md": (
        "TODO(Rohit)",
        "thin_course",
        "PARTITION",
    ),
    ROOT / "sites/SURF_Course_slurm/snippets/mpifileutils.md": (
        "TODO(Rohit)",
        "mpiFileUtils",
    ),
}


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


def main() -> int:
    errors = []
    for path, needles in REQUIRED_TODOS.items():
        if not path.is_file():
            errors.append(f"missing {path}")
            continue
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"{path.name} does not mention {needle}")
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
