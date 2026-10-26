"""Set figure alt text from fig_src/figures.alt."""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import repo_file


def load_alt() -> dict[str, str]:
    mapping = {}
    for line in (repo_file.ROOT / "fig_src" / "figures.alt").read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        name, alt = line.split("\t", 1)
        mapping[name] = alt
    return mapping


def apply_alt(text: str, mapping: dict[str, str]) -> str:
    def repl(match: re.Match[str]) -> str:
        src = match.group(2)
        name = Path(src).name
        if name in mapping:
            alt = mapping[name].replace("'", "")
            return f"![{mapping[name]}]({src}){{alt='{alt}'}}"
        return match.group(0)

    return re.sub(r"!\[(.*?)\]\(([^)\s]+)\)(?:\{alt='[^']*'\})?", repl, text)


def main() -> None:
    mapping = load_alt()
    for path in repo_file.generated_markdown():
        if not path.exists():
            continue
        original = path.read_text(encoding="utf-8")
        updated = apply_alt(original, mapping)
        if updated != original:
            path.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    main()
