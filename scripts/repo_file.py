"""Shared path rules for the Org to Workbench pipeline."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SITE_FROM = "org"
SITE_TO = (
    "markdown-raw_tex-simple_tables-multiline_tables-grid_tables"
    "+pipe_tables+fenced_divs+raw_html"
)
SITE_SHIFT = "1"
FILTERS = ("scripts/drop-slides.lua", "slides/filters/carpentries.lua")
BUILD_SNIPPETS = (
    "--from=org",
    "--shift-heading-level-by=1",
    "--wrap=none",
    "scripts/drop-slides.lua",
    "slides/filters/carpentries.lua",
    "scripts/render-figures.sh",
    "scripts/add-alt.py",
)

ORG_TREES = {
    "episodes": ROOT / "org_src" / "episodes",
    "learners": ROOT / "org_src" / "learners",
    "instructors": ROOT / "org_src" / "instructors",
    "profiles": ROOT / "org_src" / "profiles",
}


def org_sources() -> list[Path]:
    sources = [ROOT / "org_src" / "index.org"]
    for folder in ("episodes", "learners", "instructors", "profiles"):
        sources.extend(sorted(ORG_TREES[folder].glob("*.org")))
    return sources


def org_to_md(org: Path) -> Path:
    org = Path(org)
    if org.name == "index.org":
        return ROOT / "index.md"
    return ROOT / org.parent.name / f"{org.stem}.md"


def figure_stems() -> list[str]:
    return sorted(path.stem for path in (ROOT / "fig_src").glob("*.dot"))


def figure_outputs(stem: str) -> list[Path]:
    fig = ROOT / "episodes" / "fig"
    return [
        fig / f"{stem}.png",
        fig / f"{stem}.svg",
        fig / f"{stem}-dark.svg",
    ]


def generated_markdown() -> list[Path]:
    return [org_to_md(path) for path in org_sources()]


def slide_stems() -> list[str]:
    return sorted(path.stem for path in (ROOT / "org_src" / "episodes").glob("*.org"))


def pandoc_version_from_lock(text: str | None = None) -> str:
    if text is None:
        text = (ROOT / "pixi.lock").read_text(encoding="utf-8")
    found = sorted(set(re.findall(r"pandoc-(\d+\.\d+\.\d+)-", text)))
    if len(found) != 1:
        raise SystemExit(f"expected one pandoc version in the lock, found {found}")
    return found[0]


def parse_output_blocks(text: str) -> list[tuple[str, str, str]]:
    """Return (runner, script, expected) for each bash block followed by output."""
    pattern = re.compile(
        r"#\+begin_src bash\n(.*?)#\+end_src\s*#\+begin_output\n(.*?)#\+end_output",
        re.S,
    )
    blocks = []
    for script, expected in pattern.findall(text):
        runner = "local"
        lines = script.splitlines()
        if lines and lines[0].startswith("# runner:"):
            runner = lines[0].split(":", 1)[1].strip()
            script = "\n".join(lines[1:]) + "\n"
        blocks.append((runner, script, expected.strip("\n")))
    return blocks


def dot_node_labels(text: str) -> list[str]:
    labels = re.findall(r"(?m)^\s*[A-Za-z0-9_]+\s*\[label=\"([^\"]+)\"\]", text)
    return labels


def parse_pipe_table(text: str) -> list[list[str]]:
    rows = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        rows.append(cells)
    return rows


def front_matter_minutes(text: str) -> tuple[int, int]:
    teaching = re.search(r"(?m)^teaching:\s*(\d+)\s*$", text)
    exercises = re.search(r"(?m)^exercises:\s*(\d+)\s*$", text)
    if not teaching or not exercises:
        raise ValueError("missing teaching or exercises")
    return int(teaching.group(1)), int(exercises.group(1))


def efficiency(t1: float, cores: int, tn: float) -> float:
    return t1 / (cores * tn)


def main(argv: list[str]) -> None:
    if argv == ["--list-org"]:
        for path in org_sources():
            print(path.relative_to(ROOT))
        return
    if argv == ["--list-md"]:
        for path in generated_markdown():
            print(path.relative_to(ROOT))
        return
    if len(argv) == 2 and argv[0] == "--md-for":
        print(org_to_md(ROOT / argv[1]).relative_to(ROOT))
        return
    if argv == ["--pandoc-version-from-lock"]:
        print(pandoc_version_from_lock())
        return
    if argv == ["--build-snippets"]:
        for snippet in BUILD_SNIPPETS:
            print(snippet)
        return
    raise SystemExit("usage: repo_file.py --list-org|--list-md|--md-for PATH|--pandoc-version-from-lock|--build-snippets")


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])


def config_episode_names(text: str | None = None) -> list[str]:
    if text is None:
        text = (ROOT / "config.yaml").read_text(encoding="utf-8")
    lines = text.splitlines()
    items: list[str] = []
    in_episodes = False
    for line in lines:
        if re.match(r"^episodes:\s*$", line):
            in_episodes = True
            continue
        if in_episodes:
            if line.startswith("- "):
                items.append(line[2:].strip())
            elif line.strip() and not line.startswith(" "):
                break
    return items
