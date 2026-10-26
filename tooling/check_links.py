#!/usr/bin/env python3
"""Check that local links in the assembled site resolve."""

from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs: list[tuple[str, str]] = []

    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        if tag == "a" and attr.get("href"):
            self.refs.append(("href", attr["href"]))
        elif tag in {"img", "script", "source"} and attr.get("src"):
            self.refs.append(("src", attr["src"]))
        elif tag == "link" and attr.get("href"):
            self.refs.append(("href", attr["href"]))


def resolve(page: Path, root: Path, ref: str) -> Path | None:
    parsed = urlparse(ref)
    if parsed.scheme in {"http", "https", "mailto", "javascript"}:
        return None
    if ref.startswith("#"):
        return None
    path = unquote(parsed.path)
    if not path:
        return None
    if path.startswith("/"):
        target = root / path.lstrip("/")
    else:
        target = page.parent / path
    return target.resolve()


def exists(target: Path, root: Path) -> bool:
    try:
        target.relative_to(root)
    except ValueError:
        return False
    if target.is_file():
        return True
    if target.is_dir() and ((target / "index.html").is_file() or (target / "index.htm").is_file()):
        return True
    # Extensionless lesson URLs: /slug/episode -> episode.html
    if target.with_suffix(".html").is_file():
        return True
    return False


def main(argv: list[str]) -> int:
    root = Path(argv[1]).resolve()
    missing = []
    pages = 0
    links = 0
    for page in root.rglob("*.html"):
        pages += 1
        parser = LinkParser()
        try:
            parser.feed(page.read_text(encoding="utf-8", errors="replace"))
        except Exception as exc:  # noqa: BLE001
            missing.append(f"{page}: parse error {exc}")
            continue
        for _kind, ref in parser.refs:
            links += 1
            target = resolve(page, root, ref)
            if target is None:
                continue
            if not exists(target, root):
                missing.append(f"{page.relative_to(root)} -> {ref}")
    print(f"checked {links} links in {pages} pages")
    if missing:
        print(f"{len(missing)} broken local links", file=sys.stderr)
        for line in missing[:80]:
            print(line, file=sys.stderr)
        if len(missing) > 80:
            print(f"... {len(missing) - 80} more", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
