#!/usr/bin/env python3
"""Render the course landing page into the assembled site."""

from __future__ import annotations

import html
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def parse_yaml(text: str):
    """Small YAML reader: nested dicts, lists of dicts, and scalars."""
    lines = []
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        lines.append((indent, raw.strip()))

    def scalar(value: str):
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            return value[1:-1]
        return value

    def parse_block(index: int, indent: int):
        if index >= len(lines):
            return {}, index
        if lines[index][1].startswith("- "):
            items = []
            while index < len(lines) and lines[index][0] == indent and lines[index][1].startswith("- "):
                item_line = lines[index][1][2:]
                index += 1
                if ":" in item_line and not item_line.startswith(("http://", "https://")):
                    key, _, rest = item_line.partition(":")
                    child = {}
                    rest = rest.strip()
                    if rest:
                        child[key.strip()] = scalar(rest)
                    if index < len(lines) and lines[index][0] > indent:
                        nested, index = parse_block(index, lines[index][0])
                        if isinstance(nested, dict):
                            child.update(nested)
                        else:
                            raise SystemExit(f"expected a mapping under {key}")
                    items.append(child)
                else:
                    items.append(scalar(item_line))
            return items, index
        mapping = {}
        while index < len(lines) and lines[index][0] == indent:
            key, _, rest = lines[index][1].partition(":")
            key = key.strip()
            rest = rest.strip()
            index += 1
            if rest == "":
                if index < len(lines) and lines[index][0] > indent:
                    mapping[key], index = parse_block(index, lines[index][0])
                else:
                    mapping[key] = ""
            else:
                mapping[key] = scalar(rest)
        return mapping, index

    data, index = parse_block(0, lines[0][0] if lines else 0)
    if index != len(lines):
        raise SystemExit(f"schedule.yaml: stopped at {lines[index][1]}")
    return data


def episode_order(config_text: str) -> list[str]:
    names = []
    in_list = False
    for line in config_text.splitlines():
        if re.match(r"^episodes:\s*$", line):
            in_list = True
            continue
        if not in_list:
            continue
        if re.match(r"^\s*-\s+", line):
            names.append(line.split("-", 1)[1].strip())
            continue
        if line.strip() == "" or line.strip().startswith("#"):
            continue
        break
    return names


def front_matter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    block = text[3:end]
    data = {}
    for line in block.splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        key, _, value = line.partition(":")
        data[key.strip()] = value.strip().strip("'\"")
    return data


def session_slug_order(sessions: list) -> list[str]:
    order = []
    for session in sessions:
        for part in str(session.get("slugs", "")).split(","):
            slug = part.strip()
            if slug and slug not in order:
                order.append(slug)
    return order


def lesson_rows(cut_first: dict, slug_order: list[str] | None = None) -> list[dict]:
    rows = []
    for config in sorted((ROOT / "lessons").glob("*/config.yaml")):
        slug = config.parent.name
        order = episode_order(config.read_text(encoding="utf-8"))
        title = ""
        for line in config.read_text(encoding="utf-8").splitlines():
            if line.startswith("title:"):
                title = line.split(":", 1)[1].strip().strip("'\"")
                break
        episodes = []
        for name in order:
            path = config.parent / "episodes" / name
            meta = front_matter(path)
            episodes.append(
                {
                    "file": name,
                    "stem": Path(name).stem,
                    "title": meta.get("title", Path(name).stem),
                    "teaching": meta.get("teaching", ""),
                    "exercises": meta.get("exercises", ""),
                    "cut": cut_first.get(slug) == name,
                }
            )
        rows.append({"slug": slug, "title": title, "episodes": episodes})
    if slug_order is None:
        return rows
    by_slug = {row["slug"]: row for row in rows}
    missing = [slug for slug in slug_order if slug not in by_slug]
    extra = [row["slug"] for row in rows if row["slug"] not in slug_order]
    if missing or extra:
        raise SystemExit(
            "lesson list does not match schedule.yaml sessions: "
            + ", ".join(missing + extra)
        )
    return [by_slug[slug] for slug in slug_order]


def link_text(text: str) -> str:
    parts = []
    position = 0
    for match in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", text):
        parts.append(html.escape(text[position : match.start()]))
        parts.append(
            f'<a href="{html.escape(match.group(2), quote=True)}">{html.escape(match.group(1))}</a>'
        )
        position = match.end()
    parts.append(html.escape(text[position:]))
    return "".join(parts)


def inline_from_raw(text: str) -> str:
    bits = text.split("`")
    out = []
    for index, bit in enumerate(bits):
        if index % 2 == 1:
            out.append("<code>" + html.escape(bit) + "</code>")
        else:
            out.append(link_text(bit))
    return "".join(out)


def markdown_to_html(text: str) -> str:
    lines = text.splitlines()
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            buff = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                buff.append(lines[i])
                i += 1
            i += 1
            out.append("<pre><code>" + html.escape("\n".join(buff)) + "</code></pre>")
            continue
        if line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            title = line[level:].strip()
            out.append(f"<h{level}>{inline_from_raw(title)}</h{level}>")
            i += 1
            continue
        if line.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append(f"<li>{inline_from_raw(lines[i][2:])}</li>")
                i += 1
            out.append("<ul>" + "".join(items) + "</ul>")
            continue
        if not line.strip():
            i += 1
            continue
        buff = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(("#", "-", "```")):
            buff.append(lines[i])
            i += 1
        out.append("<p>" + inline_from_raw(" ".join(buff)) + "</p>")
    return "\n".join(out)


PAGE_CSS = """
body { font-family: system-ui, sans-serif; max-width: 52rem; margin: 2rem auto; padding: 0 1rem; line-height: 1.5; color: #123044; }
a { color: #0b6e6a; }
header { display: flex; align-items: center; gap: 1rem; }
header img { width: 64px; height: 64px; }
nav a { margin-right: 1rem; }
table { border-collapse: collapse; width: 100%; margin: 1rem 0; }
th, td { border-bottom: 1px solid #d5dde3; text-align: left; padding: 0.35rem 0.4rem; vertical-align: top; }
.cut { color: #5c6b76; }
pre { background: #f4f7f8; padding: 0.8rem; overflow: auto; }
"""


def page(title: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>{PAGE_CSS}</style>
</head>
<body>
<header>
<a href="/"><img src="/logo.svg" id="supersurf-logo" alt="supersurf"></a>
<div>
<p><a href="/">supersurf</a></p>
<h1>{html.escape(title)}</h1>
</div>
</header>
<nav>
<a href="/">Home</a>
<a href="/setup.html">Setup</a>
<a href="/instructors.html">Instructors</a>
</nav>
{body}
</body>
</html>
"""


def redirect_page(target: str, label: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="0; url={html.escape(target, quote=True)}">
<link rel="canonical" href="https://supersurf.rgoswami.me{html.escape(target, quote=True)}">
<title>Moved</title>
</head>
<body>
<p>This page moved to <a href="{html.escape(target, quote=True)}">{html.escape(label)}</a>.</p>
</body>
</html>
"""


def part_one_table(data: dict) -> str:
    rows = []
    end = 0
    for block in data["part_one"]:
        first, last = block["elapsed"].split("-")
        start_hour, start_minute = map(int, first.split(":"))
        end_hour, end_minute = map(int, last.split(":"))
        start = 60 * start_hour + start_minute
        finish = 60 * end_hour + end_minute
        minutes = int(block["minutes"])
        if start != end or finish - start != minutes or minutes <= 0:
            raise ValueError("Part I blocks must be contiguous and match their durations")
        end = finish
        rows.append(
            "<tr>"
            f"<td>{html.escape(block['elapsed'])}</td>"
            f"<td>{minutes}</td>"
            f"<td>{html.escape(block['topic'])}</td>"
            "</tr>"
        )
    if end != 240:
        raise ValueError("Part I must include exactly 240 minutes")
    return (
        '<h2 id="part-one">Part I: four-hour Introduction to HPC</h2>'
        '<p>Elapsed times include the break. Start with this route, rather than '
        'the complete episode estimates below. The <a href="/instructors.html">'
        'instructor guide</a> names slide pages, commands, answers and stopping points.</p>'
        '<table><thead><tr><th>Elapsed</th><th>Minutes</th><th>Block</th></tr></thead>'
        '<tbody>' + "".join(rows) + '</tbody></table>'
        '<p><a href="/downloads/intro-teacher-workbook.pdf">Teacher workbook (PDF)</a>'
        ' | <a href="/downloads/introduction-slides.zip">Matching slide pack</a></p>'
    )


def render(out: Path) -> None:
    data = parse_yaml((ROOT / "schedule.yaml").read_text(encoding="utf-8"))
    part_one = part_one_table(data)
    cut = data.get("cut_first") or {}
    sessions = data["sessions"]
    lessons = lesson_rows(cut, session_slug_order(sessions))
    by_slug = {row["slug"]: row for row in lessons}

    session_rows = []
    for session in sessions:
        slugs = [part.strip() for part in session["slugs"].split(",")]
        links = ", ".join(
            f'<a href="/{html.escape(slug)}/">{html.escape(by_slug[slug]["title"])}</a>'
            for slug in slugs
        )
        session_rows.append(
            "<tr>"
            f"<td>{html.escape(session['title'])}</td>"
            f"<td>{html.escape(str(session['hours']))}</td>"
            f"<td>{html.escape(session['focus'])}</td>"
            f"<td>{links}</td>"
            "</tr>"
        )

    episode_sections = []
    for row in lessons:
        body = []
        for episode in row["episodes"]:
            mark = " cut first" if episode["cut"] else ""
            css = ' class="cut"' if episode["cut"] else ""
            href = f"/{row['slug']}/{episode['stem']}.html"
            body.append(
                f"<tr{css}>"
                f'<td><a href="{html.escape(href, quote=True)}">{html.escape(episode["title"])}</a>{html.escape(mark)}</td>'
                f"<td>{html.escape(episode['teaching'])}</td>"
                f"<td>{html.escape(episode['exercises'])}</td>"
                "</tr>"
            )
        episode_sections.append(
            f'<h3><a href="/{html.escape(row["slug"])}/">{html.escape(row["title"])}</a></h3>'
            "<table><thead><tr><th>Episode</th><th>Teaching (min)</th><th>Exercises (min)</th></tr></thead>"
            "<tbody>"
            + "".join(body)
            + "</tbody></table>"
        )

    profiles = markdown_to_html((ROOT / "site_src" / "learner-profiles.md").read_text(encoding="utf-8"))
    # The file's own h1 repeats the page heading. Drop the first h1.
    profiles = re.sub(r"^<h1>.*?</h1>\n?", "", profiles, count=1)

    home = page(
        data["title"],
        f"""
<p>Seven lessons, one site. Each lesson is a Carpentries Workbench lesson at <code>https://supersurf.rgoswami.me/&lt;slug&gt;/</code>. The workshop is three sessions of four hours. A lesson keeps every episode. The schedule below is what a session teaches, and the rows marked "cut first" are the ones to drop when the clock runs out.</p>
<p>Commands that differ by machine are in tabs: Snellius, the course cluster, and a generic Magic Castle cluster with EESSI. The course cluster is a SURF Research Cloud workspace, and its tab requests <code>--partition=rome</code>. See the <a href="/setup.html">setup page</a>.</p>
{part_one}
<h2>All three sessions</h2>
<table>
<thead><tr><th>Session</th><th>Hours</th><th>Focus</th><th>Lessons</th></tr></thead>
<tbody>
{''.join(session_rows)}
</tbody>
</table>
<h2>Complete lesson episode estimates</h2>
<p>These estimates cover each entire lesson. Part I uses the selected route above.</p>
{''.join(episode_sections)}
<h2>Who the day is for</h2>
{profiles}
<h2>Source</h2>
<p>The course text is <a href="https://github.com/sara-nl/introduction-to-supercomputing">sara-nl/introduction-to-supercomputing</a> and Rohit's fork <a href="https://github.com/HaoZeke/introduction-to-supercomputing">HaoZeke/introduction-to-supercomputing</a>. Deck branches used here: <code>fix/slides-fundamentals-source</code>, <code>fix/slides-fs-source</code>, <code>fix/slides-qcg-source</code>, <code>fix/slides-performance-source</code>, <code>feat/workflow-alternatives</code>, <code>feat/data-movement-deck</code>, and <code>src/eessi-notes</code>.</p>
<p>Fundamentals vendors <a href="https://github.com/carpentries-incubator/hpc-intro">carpentries-incubator/hpc-intro</a> at <code>7081080674aceeb0a4bc57b9348da22d876af802</code>. That lesson is CC-BY 4.0, Copyright (c) The Carpentries. Authors are in <code>lessons/fundamentals/AUTHORS</code>.</p>
<h2>License</h2>
<p>Lesson text is CC-BY 4.0. The hybrid MPI and OpenMP lesson is adapted from Introducción a la Supercomputación by José Luis Bosque, Borja Pérez, Ramón Beivide, and Carmen Martínez, Universidad de Cantabria, by the EuroCC NL team at SURF.</p>
""",
    )
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(home, encoding="utf-8")
    (out / "setup.html").write_text(
        page("Setup", markdown_to_html((ROOT / "site_src" / "setup.md").read_text(encoding="utf-8")).replace("<h1>Setup</h1>\n", "", 1)),
        encoding="utf-8",
    )
    (out / "instructors.html").write_text(
        page(
            "Instructors",
            markdown_to_html((ROOT / "site_src" / "instructors.md").read_text(encoding="utf-8")).replace("<h1>Instructors</h1>\n", "", 1),
        ),
        encoding="utf-8",
    )
    shutil.copytree(ROOT / "site_assets" / "downloads", out / "downloads", dirs_exist_ok=True)
    shutil.copyfile(ROOT / "site_assets" / "assets" / "logo.svg", out / "logo.svg")

    for name, target in (data.get("redirects") or {}).items():
        label = target.strip("/") or "home"
        (out / f"{name}.html").write_text(redirect_page(target, label), encoding="utf-8")

    both = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>File systems and moving data</title>
</head>
<body>
<p>This page was one episode. It is now two lessons.</p>
<ul>
<li><a href="/filesystems/">File systems</a></li>
<li><a href="/data-movement/">Moving data</a></li>
</ul>
</body>
</html>
"""
    (out / "filesystems-and-data.html").write_text(both, encoding="utf-8")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: schedule.py OUT_DIR", file=sys.stderr)
        return 2
    render(Path(argv[1]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
