"""Write a small set of favicons from the lesson mark."""

from __future__ import annotations

import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "site_assets" / "favicons" / "incubator"


def chunk(tag: bytes, data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)


def png(size: int) -> bytes:
    raw = bytearray()
    for y in range(size):
        raw.append(0)
        for x in range(size):
            edge = min(x, y, size - 1 - x, size - 1 - y) < max(1, size // 16)
            band = abs((x - size // 2) + (y - size // 2)) < max(1, size // 10)
            if edge or band:
                raw.extend((31, 78, 121, 255))
            else:
                raw.extend((244, 241, 234, 255))
    return b"".join(
        [
            b"\x89PNG\r\n\x1a\n",
            chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)),
            chunk(b"IDAT", zlib.compress(bytes(raw), 9)),
            chunk(b"IEND", b""),
        ]
    )


def ico(png32: bytes) -> bytes:
    # A one-image ICO that stores the PNG payload.
    header = struct.pack("<HHH", 0, 1, 1)
    entry = struct.pack("<BBBBHHII", 32, 32, 0, 0, 1, 32, len(png32), 22)
    return header + entry + png32


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    images = {
        "favicon-16x16.png": png(16),
        "favicon-32x32.png": png(32),
        "apple-touch-icon.png": png(180),
        "android-chrome-192x192.png": png(192),
        "android-chrome-512x512.png": png(512),
    }
    for name, data in images.items():
        (OUT / name).write_bytes(data)
    (OUT / "favicon.ico").write_bytes(ico(images["favicon-32x32.png"]))
    (OUT / "safari-pinned-tab.svg").write_text(
        (ROOT / "site_assets" / "assets" / "logo.svg").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (OUT / "site.webmanifest").write_text(
        """{
  "name": "Supercomputing with EESSI",
  "icons": [
    {"src": "android-chrome-192x192.png", "sizes": "192x192", "type": "image/png"},
    {"src": "android-chrome-512x512.png", "sizes": "512x512", "type": "image/png"}
  ]
}
""",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
