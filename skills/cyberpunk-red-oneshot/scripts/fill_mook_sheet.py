#!/usr/bin/env python3
"""Render a Cyberpunk RED Mook Sheet PDF from an NPC/enemy JSON file."""
import argparse
import json
from pathlib import Path

import jinja2

from render_pdf import load_css_with_fonts, render_html_to_pdf

SKILL_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = SKILL_DIR / "assets"

_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(ASSETS_DIR),
    autoescape=jinja2.select_autoescape(["html", "jinja"]),
)


def render_mook_sheet_html(mook: dict) -> str:
    """Render a mook JSON dict into a self-contained HTML document string."""
    template = _ENV.get_template("mook_sheet.html.jinja")
    return template.render(
        mook=mook,
        css=load_css_with_fonts(ASSETS_DIR / "mook_sheet.css", ASSETS_DIR / "fonts"),
    )


def fill_mook_sheet(mook_json_path: Path, output_pdf: Path) -> None:
    mook = json.loads(Path(mook_json_path).read_text(encoding="utf-8"))
    html = render_mook_sheet_html(mook)
    render_html_to_pdf(html, output_pdf)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mook_json", type=Path)
    parser.add_argument("output_pdf", type=Path)
    args = parser.parse_args()
    fill_mook_sheet(args.mook_json, args.output_pdf)
    print(f"wrote {args.output_pdf}")


if __name__ == "__main__":
    main()
