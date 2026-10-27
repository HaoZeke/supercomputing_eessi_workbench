#!/usr/bin/env python3
"""Expand site customizations into one page of grouped tabs.

Lessons name a snippet. This reads each site's copy, fills in that site's
_config_options.yml, and writes a Workbench group-tab when the copies differ.
One site (SUPERSURF_SITES=snellius, or the site id) skips the tabs.

Search order for a snippet, per site:

1. lessons/<slug>/episodes/files/customization/<Site>/snippets/
2. sites/<Site>/snippets/ at the repository root

A missing copy falls back to the Magic Castle snippet, with the requesting
site's values filled in. That is the hpc-intro overlay rule: a site directory
holds only the files that differ.

hpc-intro writes `` `r config$a$b` ``, `` `r site$a$b` ``, and ``{{ site.a.b }}``.
A leading ``site.`` is the same path as the config root. A few inline
expressions (home path, optional account line, optional qos line, Slurm
separator) are filled here so knitr never sees them.
"""

from __future__ import annotations

import os
import re
import sys
from copy import deepcopy
from pathlib import Path

BASE_SITE = "HPCC_MagicCastle_slurm"
ORDER_NAMES = (
    "SURF_Snellius_slurm",
    "SURF_Course_slurm",
    "HPCC_MagicCastle_slurm",
)
LABELS = {
    "SURF_Snellius_slurm": "Snellius",
    "SURF_Course_slurm": "Course cluster",
    "HPCC_MagicCastle_slurm": "Magic Castle",
}

SITE_DIV = re.compile(
    r"^(?P<fence>:{3,})\s+sites\s+(?P<name>[A-Za-z0-9_./-]+)\s*$",
    re.M,
)
R_CHUNK = re.compile(r"^```\{r[^}]*\}\n(?P<body>.*?)\n```", re.M | re.S)
SNIPPET_CALL = re.compile(r"""snippets\(\s*['"]([^'"]+)['"]\s*\)""")
INLINE_CONFIG = re.compile(
    r"`r (?:config|site)\$((?:[A-Za-z0-9_]+\$)*[A-Za-z0-9_]+)`"
)
MUSTACHE = re.compile(r"\{\{\s*([A-Za-z0-9_.]+)\s*\}\}")
# hpc-intro inline R that is not a single config lookup.
HOME_PASTE = re.compile(
    r"`r paste\(config\$remote\$fs\$home,config\$remote\$user,sep=\"/\"\)`"
)
QOS_LINE = re.compile(
    r"`r if \(!is\.null\(config\$sched\$flag\$qos\)\) paste\(config\$sched\$comment,config\$sched\$flag\$qos\) else \"\"`"
)
SLURM_SEP = re.compile(
    r"`r if\(config\$sched\$name == \"Slurm\"\) \{print\(\" \"\)\} else \{print\(\"=\"\)\}`"
)
ACCOUNT_LINE = re.compile(
    r"`r if \(!is\.null\(config\$sched\$account\)\) \{paste0\(config\$remote\$shebang, \"\\n\", config\$sched\$comment, \" \", config\$sched\$flag\$account, \"=\", config\$sched\$account\)\} else \{paste0\(config\$remote\$shebang\)\}`"
)
CODE_FENCE = re.compile(r"^(?P<fence>`{3,}|~{3,})(?P<info>[^\n]*)\n(?P<body>.*?)\n(?P=fence)\s*$", re.M | re.S)


class ExpandError(Exception):
    pass


def parse_yaml(text: str):
    """Parse the small YAML subset used by site configs."""
    lines = text.splitlines()
    root: dict = {}
    stack: list[tuple[int, object]] = [(-1, root)]

    def new_container(line: str):
        stripped = line.lstrip()
        if stripped.startswith("- "):
            return []
        return {}

    i = 0
    while i < len(lines):
        raw = lines[i]
        if not raw.strip() or raw.lstrip().startswith("#"):
            i += 1
            continue
        if raw.strip() == "---":
            i += 1
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if line.startswith("- "):
            if not isinstance(parent, list):
                raise ExpandError(f"list item outside a list: {line}")
            parent.append(parse_scalar(line[2:].strip()))
            i += 1
            continue
        if ":" not in line:
            raise ExpandError(f"expected key: {line}")
        key, _, rest = line.partition(":")
        key = key.strip()
        rest = rest.strip()
        if rest == "":
            # Peek at the next content line to choose dict or list.
            j = i + 1
            while j < len(lines) and (not lines[j].strip() or lines[j].lstrip().startswith("#")):
                j += 1
            child: object = {}
            if j < len(lines):
                nxt = lines[j].strip()
                if nxt.startswith("- "):
                    child = []
            if isinstance(parent, dict):
                parent[key] = child
            else:
                raise ExpandError(f"nested key under a list: {key}")
            stack.append((indent, child))
        else:
            if isinstance(parent, dict):
                parent[key] = parse_scalar(rest)
            else:
                raise ExpandError(f"scalar under a list without a dash: {key}")
        i += 1
    return root


def parse_scalar(text: str):
    if text in ("null", "~", ""):
        return None
    if (text.startswith('"') and text.endswith('"')) or (
        text.startswith("'") and text.endswith("'")
    ):
        return text[1:-1]
    if text in ("true", "True"):
        return True
    if text in ("false", "False"):
        return False
    return text


def lookup(cfg: dict, path: str):
    path = path.replace("$", ".")
    if path.startswith("site."):
        path = path[len("site.") :]
    cur = cfg
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def need(cfg: dict, path: str):
    value = lookup(cfg, path)
    if value is None:
        raise ExpandError(f"missing config value {path}")
    return value


def deep_merge(base: dict, overlay: dict) -> dict:
    out = deepcopy(base)
    for key, value in overlay.items():
        if key in out and isinstance(out[key], dict) and isinstance(value, dict):
            out[key] = deep_merge(out[key], value)
        else:
            out[key] = deepcopy(value)
    return out


def load_yaml_file(path: Path) -> dict:
    if not path.is_file():
        return {}
    data = parse_yaml(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ExpandError(f"{path} is not a mapping")
    return data


def repo_root_from(lesson: Path) -> Path:
    # lessons/<slug> lives directly under the repo root.
    if lesson.parent.name == "lessons":
        return lesson.parent.parent
    return lesson


def config_for(site_id: str, lesson: Path, root: Path) -> dict:
    base_paths = [
        root / "sites" / BASE_SITE / "_config_options.yml",
        lesson / "episodes" / "files" / "customization" / BASE_SITE / "_config_options.yml",
    ]
    cfg: dict = {}
    for path in base_paths:
        cfg = deep_merge(cfg, load_yaml_file(path))
    if site_id != BASE_SITE:
        for path in (
            root / "sites" / site_id / "_config_options.yml",
            lesson / "episodes" / "files" / "customization" / site_id / "_config_options.yml",
        ):
            cfg = deep_merge(cfg, load_yaml_file(path))
    return cfg


def snippet_candidates(site_id: str, name: str, lesson: Path, root: Path) -> list[Path]:
    names = [name]
    stem = name
    if name.endswith(".Rmd"):
        names.append(name[: -len(".Rmd")] + ".md")
    elif name.endswith(".md"):
        names.append(name[: -len(".md")] + ".Rmd")
    else:
        names.extend((name + ".md", name + ".Rmd"))
        stem = name
    dirs = [
        lesson / "episodes" / "files" / "customization" / site_id / "snippets",
        root / "sites" / site_id / "snippets",
    ]
    found = []
    for directory in dirs:
        for candidate in names:
            path = directory / candidate
            if path.is_file():
                found.append(path)
    return found


def read_snippet(site_id: str, name: str, lesson: Path, root: Path) -> str | None:
    hits = snippet_candidates(site_id, name, lesson, root)
    if hits:
        return hits[0].read_text(encoding="utf-8")
    if site_id != BASE_SITE:
        base_hits = snippet_candidates(BASE_SITE, name, lesson, root)
        if base_hits:
            return base_hits[0].read_text(encoding="utf-8")
    return None


def apply_hpc_expressions(text: str, cfg: dict) -> str:
    """Fill the inline R expressions hpc-intro uses besides a single lookup."""

    def home(_match: re.Match) -> str:
        return f"{need(cfg, 'remote.fs.home')}/{need(cfg, 'remote.user')}"

    def qos(_match: re.Match) -> str:
        flag = lookup(cfg, "sched.flag.qos")
        if not flag:
            return ""
        return f"{need(cfg, 'sched.comment')} {flag}"

    def sep(_match: re.Match) -> str:
        return " " if need(cfg, "sched.name") == "Slurm" else "="

    def account(_match: re.Match) -> str:
        shebang = str(need(cfg, "remote.shebang"))
        account_name = lookup(cfg, "sched.account")
        if not account_name:
            return shebang
        comment = need(cfg, "sched.comment")
        flag = need(cfg, "sched.flag.account")
        return f"{shebang}\n{comment} {flag}={account_name}"

    text = HOME_PASTE.sub(home, text)
    text = QOS_LINE.sub(qos, text)
    text = SLURM_SEP.sub(sep, text)
    text = ACCOUNT_LINE.sub(account, text)
    return text


def fill_config(text: str, cfg: dict) -> str:
    def inline(match: re.Match) -> str:
        value = lookup(cfg, match.group(1))
        if value is None:
            raise ExpandError(f"missing config value config${match.group(1)}")
        return str(value)

    def mustache(match: re.Match) -> str:
        value = lookup(cfg, match.group(1))
        if value is None:
            raise ExpandError(f"missing config value {{{{{match.group(1)}}}}}")
        return str(value)

    text = apply_hpc_expressions(text, cfg)
    text = INLINE_CONFIG.sub(inline, text)
    text = MUSTACHE.sub(mustache, text)
    return text


def fence_for(body: str) -> str:
    # Longer than a callout (`:::`) so a tab can contain one.
    # Callers that wrap a tab in another div need a still longer fence.
    longest = 5
    for match in re.finditer(r":{3,}", body):
        longest = max(longest, len(match.group(0)))
    return ":" * (longest + 1)


def group_tab(parts: list[tuple[str, str]]) -> str:
    bodies = [text.strip("\n") for _, text in parts]
    if len(set(bodies)) == 1:
        return bodies[0] + "\n"
    fence = fence_for("\n".join(bodies))
    chunks = [f"{fence} group-tab\n"]
    for label, text in parts:
        chunks.append(f"\n### {label}\n\n")
        chunks.append(text.strip("\n"))
        chunks.append("\n")
    chunks.append(f"\n{fence}\n")
    return "".join(chunks)


def selected_sites() -> list[str]:
    raw = os.environ.get("SUPERSURF_SITES", "").strip()
    if not raw:
        return list(ORDER_NAMES)
    wanted = []
    for token in re.split(r"[\s,]+", raw):
        if not token:
            continue
        key = token.lower().replace("-", "_")
        match = None
        for site_id, label in LABELS.items():
            if key in (site_id.lower(), label.lower(), label.lower().replace(" ", "")):
                match = site_id
                break
        aliases = {
            "snellius": "SURF_Snellius_slurm",
            "course": "SURF_Course_slurm",
            "course_cluster": "SURF_Course_slurm",
            "magic": "HPCC_MagicCastle_slurm",
            "magic_castle": "HPCC_MagicCastle_slurm",
            "eessi": "HPCC_MagicCastle_slurm",
        }
        match = match or aliases.get(key)
        if match is None:
            raise ExpandError(f"unknown site {token!r}")
        if match not in wanted:
            wanted.append(match)
    return wanted


class LessonSites:
    def __init__(self, lesson: Path):
        self.lesson = lesson
        self.root = repo_root_from(lesson)
        self.ids = selected_sites()
        self.configs = {site_id: config_for(site_id, lesson, self.root) for site_id in self.ids}

    def render_named(self, name: str) -> str:
        parts = []
        for site_id in self.ids:
            raw = read_snippet(site_id, name, self.lesson, self.root)
            if raw is None:
                raise ExpandError(
                    f"{self.lesson}: snippet {name!r} is missing for {site_id} and for {BASE_SITE}"
                )
            parts.append((LABELS[site_id], fill_config(raw, self.configs[site_id])))
        return group_tab(parts)

    def render_text(self, text: str) -> str:
        parts = []
        for site_id in self.ids:
            parts.append((LABELS[site_id], fill_config(text, self.configs[site_id])))
        return group_tab(parts)


def render_portal_chunk(sites: LessonSites) -> str:
    parts = []
    for site_id in sites.ids:
        cfg = sites.configs[site_id]
        portal = lookup(cfg, "remote.portal")
        if portal is not None and str(portal).strip():
            text = (
                f"Visit [{portal}]({portal}) to upload your SSH public key. "
                "(Remember, it's the one ending in `.pub`!)"
            )
        else:
            text = (
                "No SSH key upload portal is configured for this cluster. "
                "If supported, `ssh-copy-id` or `scp` can be used for registering "
                "or transferring the public key."
            )
        parts.append((LABELS[site_id], text + "\n"))
    return group_tab(parts)


def render_scp_chunk(sites: LessonSites) -> str:
    parts = []
    for site_id in sites.ids:
        cfg = sites.configs[site_id]
        prompt = lookup(cfg, "local.prompt")
        user = lookup(cfg, "remote.user")
        login = lookup(cfg, "remote.login")
        block = f"```bash\n{prompt} scp ~/.ssh/id_ed25519.pub {user}@{login}:~/\n```\n"
        parts.append((LABELS[site_id], block))
    return group_tab(parts)


def expand_r_chunks(text: str, sites: LessonSites) -> str:
    def repl(match: re.Match) -> str:
        body = match.group("body").strip()
        call = SNIPPET_CALL.fullmatch(body)
        if call:
            return sites.render_named(call.group(1)).rstrip("\n")
        if "remote$portal" in body or "SSH key upload portal" in body:
            return render_portal_chunk(sites).rstrip("\n")
        if "scp ~/.ssh" in body:
            return render_scp_chunk(sites).rstrip("\n")
        loose = SNIPPET_CALL.search(body)
        if loose and body.strip().startswith("snippets"):
            return sites.render_named(loose.group(1)).rstrip("\n")
        raise ExpandError(f"unexpanded R chunk in {sites.lesson}:\n{body[:240]}")

    return R_CHUNK.sub(repl, text)


def expand_site_divs(text: str, sites: LessonSites) -> str:
    lines = text.splitlines(keepends=True)
    out = []
    i = 0
    while i < len(lines):
        match = SITE_DIV.match(lines[i])
        if not match:
            out.append(lines[i])
            i += 1
            continue
        fence = match.group("fence")
        name = match.group("name")
        i += 1
        while i < len(lines) and lines[i].strip() != fence:
            i += 1
        if i >= len(lines):
            raise ExpandError(f"unclosed sites div for {name}")
        i += 1  # consume closing fence
        rendered = sites.render_named(name)
        if out and not out[-1].endswith("\n"):
            out.append("\n")
        out.append(rendered)
        if not rendered.endswith("\n"):
            out.append("\n")
    return "".join(out)


def expand_code_fences(text: str, sites: LessonSites) -> str:
    def repl(match: re.Match) -> str:
        info = match.group("info")
        body = match.group("body")
        fence = match.group("fence")
        if "config$" not in body and "{{" not in body:
            return match.group(0)
        parts = []
        for site_id in sites.ids:
            filled = fill_config(body, sites.configs[site_id])
            block = f"{fence}{info}\n{filled}\n{fence}\n"
            parts.append((LABELS[site_id], block))
        return group_tab(parts).rstrip("\n")

    return CODE_FENCE.sub(repl, text)


def expand_expressions(text: str, sites: LessonSites) -> str:
    """Fill hpc-intro expressions that sit outside a code fence."""

    def repl(match: re.Match) -> str:
        parts = []
        for site_id in sites.ids:
            filled = apply_hpc_expressions(match.group(0), sites.configs[site_id])
            parts.append((LABELS[site_id], filled + "\n"))
        return group_tab(parts).rstrip("\n")

    for pattern in (HOME_PASTE, QOS_LINE, SLURM_SEP, ACCOUNT_LINE):
        text = pattern.sub(repl, text)
    return text


def expand_mustache(text: str, sites: LessonSites) -> str:
    def repl(match: re.Match) -> str:
        path = match.group(1)
        values = []
        for site_id in sites.ids:
            value = lookup(sites.configs[site_id], path)
            if value is None:
                raise ExpandError(f"missing config {path} for {site_id}")
            values.append((LABELS[site_id], f"{value}"))
        if len({item[1] for item in values}) == 1:
            return values[0][1]
        rendered = [(label, f"`{value}`\n") for label, value in values]
        return "\n\n" + group_tab(rendered).rstrip("\n") + "\n\n"

    return MUSTACHE.sub(repl, text)


def expand_inline(text: str, sites: LessonSites) -> str:
    def repl(match: re.Match) -> str:
        path = match.group(1)
        values = []
        for site_id in sites.ids:
            value = lookup(sites.configs[site_id], path)
            if value is None:
                raise ExpandError(f"missing config ${path} for {site_id}")
            values.append((LABELS[site_id], f"`{value}`\n"))
        if len({item[1] for item in values}) == 1:
            return values[0][1].strip()
        return "\n\n" + group_tab(values).rstrip("\n") + "\n\n"

    return INLINE_CONFIG.sub(repl, text)


def expand_text(text: str, lesson: Path) -> str:
    sites = LessonSites(lesson)
    text = expand_r_chunks(text, sites)
    text = expand_site_divs(text, sites)
    text = expand_code_fences(text, sites)
    text = expand_expressions(text, sites)
    text = expand_mustache(text, sites)
    text = expand_inline(text, sites)
    leftover = INLINE_CONFIG.search(text) or re.search(r"```\{r", text) or SITE_DIV.search(text)
    if leftover:
        raise ExpandError(f"site markup left in {lesson}: {leftover.group(0)[:80]}")
    return text


def expand_tree(lesson: Path) -> None:
    """Expand episode and instructor sources in place. Used on a build copy."""
    for folder in ("episodes", "instructors", "learners", "profiles"):
        directory = lesson / folder
        if not directory.is_dir():
            continue
        for path in sorted(directory.rglob("*")):
            if path.suffix.lower() not in {".md", ".rmd"}:
                continue
            if "customization" in path.parts or "snippets" in path.parts:
                continue
            original = path.read_text(encoding="utf-8")
            expanded = expand_text(original, lesson)
            if expanded != original:
                path.write_text(expanded, encoding="utf-8")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: expand_sites.py LESSON_DIR", file=sys.stderr)
        return 2
    lesson = Path(argv[1]).resolve()
    expand_tree(lesson)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except ExpandError as exc:
        print(f"expand_sites: {exc}", file=sys.stderr)
        sys.exit(1)
