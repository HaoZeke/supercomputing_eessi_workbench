#!/usr/bin/env bash
# Prose report. With --full, include notes. Errors and voice warnings fail both ways.
set -euo pipefail
cd "$(dirname "$0")/.."
full=0
if [[ "${1:-}" == "--full" ]]; then
  full=1
fi
exec python - "$full" << 'PY'
import re
import sys
import tomllib
from pathlib import Path

full = sys.argv[1] == "1"
root = Path(".").resolve()
cfg = tomllib.loads((root / "proseguard.toml").read_text(encoding="utf-8"))
pages = []
for item in cfg["scope"]["pages"]:
    path = root / item
    if path.is_dir():
        pages.extend(sorted(path.glob("*.md")))
    elif path.exists():
        pages.append(path)

voice_roots = []
for item in cfg["voice"]["pages"]:
    path = root / item
    voice_roots.append(path if path.is_dir() else path)

def voice_applies(path: Path) -> bool:
    for item in voice_roots:
        if item.is_dir() and item in path.parents:
            return True
        if item == path:
            return True
    return False

def visible(text: str) -> str:
    text = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.S)
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`[^`\n]*`", "", text)
    text = re.sub(r"\[[^\]]+\]\([^)]+\)", " ", text)
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"<[^>]+>", " ", text)
    return text

errors = []
voices = []
notes = []
word_re = [(word, re.compile(rf"\b{re.escape(word)}\b", re.I)) for word in cfg["forbidden"]["words"]]
phrase_re = [(phrase, re.compile(re.escape(phrase), re.I)) for phrase in cfg["forbidden"]["phrases"]]
voice_re = [(phrase, re.compile(rf"\b{re.escape(phrase)}\b", re.I)) for phrase in cfg["voice"]["phrases"]]
chars = cfg["forbidden"]["chars"]
max_words = int(cfg["notes"]["max_paragraph_words"])

for path in pages:
    raw = path.read_text(encoding="utf-8")
    text = visible(raw)
    rel = path.relative_to(root)
    for lineno, line in enumerate(text.splitlines(), start=1):
        for char in chars:
            if char in line:
                errors.append(f"{rel}:{lineno}: forbidden character {char!r}")
        for word, pattern in word_re:
            if pattern.search(line):
                errors.append(f"{rel}:{lineno}: forbidden word {word}")
        for phrase, pattern in phrase_re:
            if pattern.search(line):
                errors.append(f"{rel}:{lineno}: forbidden phrase {phrase}")
        if voice_applies(path):
            for phrase, pattern in voice_re:
                if pattern.search(line):
                    voices.append(f"{rel}:{lineno}: voice warning {phrase}")
    for para in re.split(r"\n\s*\n", text):
        words = re.findall(r"[A-Za-z0-9']+", para)
        if len(words) > max_words:
            notes.append(f"{rel}: paragraph has {len(words)} words")

for line in errors:
    print(f"error: {line}")
for line in voices:
    print(f"voice: {line}")
if full:
    for line in notes:
        print(f"note: {line}")
print(f"{len(errors)} errors, {len(voices)} voice warnings, {len(notes)} notes")
if errors or voices:
    sys.exit(1)
PY
