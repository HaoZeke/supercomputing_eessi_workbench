"""Copy figure alt text onto img tags in built HTML."""

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
        mapping[Path(name).stem] = alt
    return mapping


def patch(html: str, mapping: dict[str, str]) -> str:
    def repl(match: re.Match[str]) -> str:
        tag = match.group(0)
        src_match = re.search(r'src="([^"]+)"', tag)
        if not src_match:
            return tag
        stem = Path(src_match.group(1)).stem
        stem = stem.removesuffix("-dark")
        if stem not in mapping:
            return tag
        alt = mapping[stem].replace('"', "&quot;")
        if re.search(r'\salt="', tag):
            return re.sub(r'\salt="[^"]*"', f' alt="{alt}"', tag, count=1)
        return tag[:-1] + f' alt="{alt}">'

    return re.sub(r"<img\b[^>]*>", repl, html)


def main() -> None:
    mapping = load_alt()
    roots = [repo_file.ROOT / "site", repo_file.ROOT / "preview"]
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*.html"):
            original = path.read_text(encoding="utf-8")
            updated = patch(original, mapping)
            if updated != original:
                path.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    main()
