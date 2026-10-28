"""Copyable course-cluster examples rendered from the learner lesson sources."""
from __future__ import annotations

import html
import os
import re
from pathlib import Path

from expand_sites import expand_text

ROOT = Path(__file__).resolve().parent.parent
FENCES = re.compile(r'^(`{3,})([^\n]*)\n(.*?)^\1[ \t]*$', re.M | re.S)


def render_commands(out, page, markdown_to_html, lessons):
    os.environ.setdefault('SUPERSURF_SITES', 'course')
    links = []
    total = 0
    for lesson in lessons:
        slug = lesson['slug']
        examples = []
        count = 0
        for episode in lesson['episodes']:
            path = ROOT / 'lessons' / slug / 'episodes' / episode['file']
            text = expand_text(path.read_text(encoding='utf-8'), path.parent.parent)
            blocks = list(FENCES.finditer(text))
            if not blocks:
                continue
            title = html.escape(episode['title'])
            href = '/' + slug + '/' + episode['stem'] + '.html'
            examples.append(f'<h2>{title}</h2><p><a href="{href}">Read this exercise in context</a></p>')
            for index, match in enumerate(blocks, 1):
                code = match.group(3).rstrip('\n')
                if not code.strip():
                    continue
                count += 1
                anchor = episode['stem'] + '-' + str(index)
                filename = slug + '-' + anchor + '.txt'
                folder = out / 'commands' / 'snippets'
                folder.mkdir(parents=True, exist_ok=True)
                (folder / filename).write_text(code + '\n', encoding='utf-8')
                language = match.group(2).strip() or 'example'
                examples.append(f'<section id="{html.escape(anchor, quote=True)}"><h3>{title}: block {index}</h3>'
                                f'<p>{html.escape(language)} · <a href="/commands/snippets/{filename}" download>Download text</a></p>'
                                '<pre><code>' + html.escape(code) + '</code></pre></section>')
        if not count:
            continue
        title = html.escape(lesson['title'])
        links.append(f'<li><a href="/commands/{slug}.html">{title}</a> ({count} blocks)</li>')
        (out / 'commands').mkdir(exist_ok=True)
        introduction = '<p><a href="/commands.html">All commands</a></p><p>These blocks come from the learner lessons with the course-cluster configuration. They include commands, templates and expected output. Follow the linked exercise for the working directory and the order of steps; replace placeholders such as JOBID.</p>'
        (out / 'commands' / (slug + '.html')).write_text(page(lesson['title'] + ': copyable examples', introduction + '\n'.join(examples)), encoding='utf-8')
        total += count
    quick = markdown_to_html((ROOT / 'site_src' / 'commands.md').read_text(encoding='utf-8'))
    body = quick + '<h2 id="all-examples">All lesson examples</h2><p>Generated from the course lesson sources, with one course-cluster configuration.</p><ul>' + ''.join(links) + '</ul>'
    (out / 'commands.html').write_text(page('Copy commands', body), encoding='utf-8')
    return total
