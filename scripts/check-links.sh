#!/usr/bin/env bash
# Fetch every external URL. A redirect is a failure, and so is a soft 404.
set -euo pipefail
cd "$(dirname "$0")/.."
exec python - << 'PY'
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

class Redirected(Exception):
    def __init__(self, code: int, url: str) -> None:
        self.code = code
        self.url = url

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise Redirected(code, newurl)

opener = urllib.request.build_opener(NoRedirect)
urls = []
for path in list(Path(".").rglob("*.md")) + list(Path("org_src").rglob("*.org")):
    if any(part in {".pixi", "site", "preview", ".git"} for part in path.parts):
        continue
    text = path.read_text(encoding="utf-8", errors="replace")
    urls.extend(re.findall(r"https?://[^\s)\]>\"']+", text))

seen = []
for url in urls:
    url = url.rstrip(".,;")
    if url not in seen:
        seen.append(url)

soft = re.compile(r"page not found|404 not found|does not exist", re.I)
fail = []
for url in seen:
    request = urllib.request.Request(url, headers={"User-Agent": "supercomputing-eessi-workbench-link-check"})
    try:
        with opener.open(request, timeout=30) as response:
            body = response.read(200_000).decode("utf-8", errors="replace")
            code = response.status
    except Redirected as exc:
        fail.append(f"{exc.code} redirect {url} -> {exc.url}")
        continue
    except urllib.error.HTTPError as exc:
        fail.append(f"{exc.code} {url}")
        continue
    except Exception as exc:
        fail.append(f"error {url} ({exc})")
        continue
    if code != 200:
        fail.append(f"{code} {url}")
        continue
    if soft.search(body[:5000]):
        fail.append(f"soft 404 {url}")

if fail:
    print("\n".join(fail))
    sys.exit(1)
print(f"links ok ({len(seen)})")
PY
