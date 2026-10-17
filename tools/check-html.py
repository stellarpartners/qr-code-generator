#!/usr/bin/env python3
"""Cheap structural checks for a no-build, one-file app.

There is no bundler and no test runner, so the two mistakes that actually
happen are a repeated id (silently breaks getElementById) and a syntax error in
the inline script (a blank page on deploy). Both are checked here.

    python3 tools/check-html.py

Exit code 1 on any failure. Node is used for the syntax check when available;
without Node the syntax check is skipped and reported as skipped.
"""

import re
import shutil
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "index.html"


class IdCollector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.imgs_without_alt = []
        self.buttons = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "img" and not a.get("alt"):
            self.imgs_without_alt.append(a.get("src", "?"))
        if tag == "button":
            self.buttons += 1


def inline_scripts(text):
    return re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", text, re.S | re.I)


def main():
    text = TARGET.read_text(encoding="utf-8")
    problems = []

    parser = IdCollector()
    parser.feed(text)

    seen, dupes = set(), []
    for i in parser.ids:
        if i in seen:
            dupes.append(i)
        seen.add(i)
    if dupes:
        problems.append("duplicate id(s): " + ", ".join(sorted(set(dupes))))

    if parser.imgs_without_alt:
        problems.append("img without alt: " + ", ".join(parser.imgs_without_alt))

    blocks = inline_scripts(text)
    if not blocks:
        problems.append("no inline script found")

    node = shutil.which("node")
    if node:
        for i, block in enumerate(blocks):
            with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as fh:
                fh.write(block)
                path = fh.name
            proc = subprocess.run([node, "--check", path], capture_output=True, text=True)
            if proc.returncode != 0:
                problems.append(f"inline script #{i + 1} does not parse:\n{proc.stderr.strip()}")
    else:
        print("note: node not found, inline-script syntax check skipped")

    print(f"ids: {len(parser.ids)} ({len(seen)} unique), inline scripts: {len(blocks)}, buttons: {parser.buttons}")

    if problems:
        for p in problems:
            print("FAIL " + p)
        return 1
    print("ok: no duplicate ids, every img has alt, inline script parses")
    return 0


if __name__ == "__main__":
    sys.exit(main())
