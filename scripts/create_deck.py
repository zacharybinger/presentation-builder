#!/usr/bin/env python3
"""Copy the dependency-free interactive deck starter and customize title/theme."""
from __future__ import annotations
import argparse
import html
from pathlib import Path
import shutil
import sys

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE.parent / "templates" / "interactive-deck"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title", default="Interactive Presentation", help="Page title")
    parser.add_argument("--style", choices=["signal", "explainer", "nocturne"], default="signal")
    parser.add_argument("--output", type=Path, required=True, help="New empty target folder")
    args = parser.parse_args()
    output = args.output.expanduser().resolve()
    if output.is_dir() and any(output.iterdir()):
        parser.error(f"Output folder not empty: {output} (refusing to overwrite)")
    if output.exists() and not output.is_dir():
        parser.error(f"Output path is not a directory: {output}")
    output.mkdir(parents=True, exist_ok=True)
    for f in TEMPLATE.iterdir():
        if not f.is_file():
            continue
        s = f.read_text(encoding="utf-8")
        s = s.replace("__DEFAULT_THEME__", args.style)
        if f.name == "index.html":
            s = s.replace("__DECK_TITLE__", html.escape(args.title, quote=True))
        (output / f.name).write_text(s, encoding="utf-8")
    print(f"Created: {output}")
    print(f"Edit the sources, then publish: python {HERE / 'export_deck.py'} {output} --out <final-directory>")
    return 0


if __name__ == "__main__":
    sys.exit(main())
