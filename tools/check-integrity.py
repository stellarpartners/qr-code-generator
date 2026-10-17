#!/usr/bin/env python3
"""Check, or print, the Subresource Integrity hashes for the CDN libraries.

The app loads qr-code-styling and jsPDF from unpkg and pins both a version and
an SRI hash. Every integrity attribute in index.html and tools/*.html must match
the bytes unpkg really serves, or the browser refuses to run the script and the
page dies with no visible reason.

    python3 tools/check-integrity.py            # print the hashes
    python3 tools/check-integrity.py --verify   # exit 1 on a mismatch (CI)

Standard library only: no curl, no openssl, works on Windows, Linux and macOS.
"""

import base64
import hashlib
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = [ROOT / "index.html", *sorted((ROOT / "tools").glob("*.html"))]

TAG = re.compile(r"<script\b[^>]*>", re.I | re.S)
SRC = re.compile(r'src="([^"]+)"')
INTEGRITY = re.compile(r'integrity="(sha(?:256|384|512)-[^"]+)"')
URL = re.compile(r"https://unpkg\.com/([^/]+)@([^/]+)/(.+)")


def sri(url, algo="sha384"):
    with urllib.request.urlopen(url, timeout=30) as resp:
        digest = hashlib.new(algo, resp.read()).digest()
    return f"{algo}-{base64.b64encode(digest).decode()}"


def pinned_scripts():
    """Yield (file, url, integrity) for every pinned third-party script."""
    for path in SOURCES:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for tag in TAG.findall(text):
            src, integ = SRC.search(tag), INTEGRITY.search(tag)
            if src and integ:
                yield path.relative_to(ROOT), src.group(1), integ.group(1)


def print_hashes():
    seen = {}
    for _, url, _ in pinned_scripts():
        seen.setdefault(url, None)
    if not seen:
        print("no pinned scripts found")
        return 0
    for url in seen:
        m = URL.match(url)
        if not m:
            print(url)
            continue
        name, version, _path = m.groups()
        algo = "sha384"
        print(f"{name} {version}")
        print(f"  url:  {url}")
        print(f"  hash: {sri(url, algo)}")
        print()
    print("Compare these with the integrity attributes in index.html.")
    return 0


def verify():
    failed = 0
    checked = 0
    for path, url, integ in pinned_scripts():
        checked += 1
        algo = integ.split("-", 1)[0]
        actual = sri(url, algo)
        if actual == integ:
            print(f"ok    {path}: {url}")
        else:
            failed += 1
            print(f"FAIL  {path}: {url}")
            print(f"      in repo: {integ}")
            print(f"      live:    {actual}")
    if not checked:
        print("no pinned scripts found - nothing to verify")
        return 1
    print()
    print(f"{checked - failed}/{checked} pinned scripts match")
    return 1 if failed else 0


def main(argv):
    if "--verify" in argv:
        return verify()
    return print_hashes()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
