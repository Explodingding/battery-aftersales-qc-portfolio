"""Copy portfolio HTML to docs/ for GitHub Pages + patch standalone links."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "battery-aftersales-quality" / "html"
DOCS = ROOT / "docs"

# Pages that had legacy links to local application hub
PATCH_FILES = [
    "index.html",
    "repair-playbook.html",
    "battery-analytics.html",
    "start-here.html",
]


def patch_standalone_links(text: str) -> str:
    text = text.replace('href="../../html/index.html"', 'href="start-here.html"')
    text = text.replace("← Dokumenty aplikacyjne", "Start here")
    text = text.replace('href="../../html/case-studies.html"', 'href="start-here.html"')
    text = text.replace('href="../../html/working-method.html"', 'href="learn.html"')
    return text


def main() -> None:
    if DOCS.exists():
        shutil.rmtree(DOCS)
    shutil.copytree(SRC, DOCS)

    for name in PATCH_FILES:
        path = DOCS / name
        if path.exists():
            path.write_text(patch_standalone_links(path.read_text(encoding="utf-8")), encoding="utf-8")

    print(f"GitHub Pages root: {DOCS}")
    print(f"Files: {len(list(DOCS.rglob('*')))}")
    print("Entry point for newcomers: start-here.html")


if __name__ == "__main__":
    main()
