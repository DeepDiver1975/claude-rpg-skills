import base64
from pathlib import Path

from pypdf import PdfReader

from render_pdf import data_uri, load_css_with_fonts, load_themed_css, render_html_to_pdf

SKILL_DIR = Path(__file__).resolve().parent.parent
FONTS_DIR = SKILL_DIR / "assets" / "fonts"


def test_data_uri_round_trips_exact_bytes(tmp_path):
    original = b"\x89PNG\r\n\x1a\nnot a real png, just some bytes"
    path = tmp_path / "fixture.bin"
    path.write_bytes(original)

    uri = data_uri(path, "application/octet-stream")

    assert uri.startswith("data:application/octet-stream;base64,")
    assert base64.b64decode(uri.split(",", 1)[1]) == original


def test_load_themed_css_appends_theme_after_structure_and_inlines_fonts(tmp_path):
    structure = tmp_path / "structure.css"
    structure.write_text(".sheet-rule { height: 6pt; }\n", encoding="utf-8")
    theme = tmp_path / "theme.css"
    theme.write_text(
        '@font-face { font-family: "X"; src: url("__FONT:CrimsonText-Regular.ttf__"); }\n'
        ":root { --accent: #ff0000; }\n"
        ".sheet-rule { height: 2pt; }\n",
        encoding="utf-8",
    )

    css = load_themed_css(structure, theme, FONTS_DIR)

    assert css.index("height: 6pt;") < css.index("height: 2pt;")  # structure first
    assert "--accent: #ff0000;" in css
    assert "__FONT:" not in css
    assert "data:font/ttf;base64," in css


def test_font_placeholders_resolve_in_structure_and_every_theme():
    css_paths = [
        SKILL_DIR / "assets" / "character_sheet.css",
        *(SKILL_DIR / "assets" / "themes").glob("*.css"),
    ]
    for css_path in css_paths:
        load_css_with_fonts(css_path, FONTS_DIR)  # raises if a font file is missing


def test_render_html_to_pdf_produces_a_readable_pdf(tmp_path):
    output_pdf = tmp_path / "out.pdf"
    render_html_to_pdf(
        "<html><body><h1>Ünïcödé Ü ä ö ß Test</h1></body></html>", output_pdf
    )
    assert output_pdf.exists()
    reader = PdfReader(output_pdf)
    assert "Ünïcödé" in reader.pages[0].extract_text()
