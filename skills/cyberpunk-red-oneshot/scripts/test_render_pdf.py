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
    encoded = uri.split(",", 1)[1]
    assert base64.b64decode(encoded) == original


def test_load_css_with_fonts_replaces_font_placeholders(tmp_path):
    css_path = tmp_path / "fixture.css"
    css_path.write_text(
        '@font-face { src: url("__FONT:NotoSans-Regular.ttf__"); }\n'
        '@font-face { src: url("__FONT:NotoSans-Bold.ttf__"); }\n',
        encoding="utf-8",
    )

    css = load_css_with_fonts(css_path, FONTS_DIR)

    assert "__FONT:" not in css
    assert css.count("data:font/ttf;base64,") == 2


def test_load_css_with_fonts_covers_every_placeholder_used_by_the_real_stylesheets():
    # Guards against a typo'd filename in a real .css file's @font-face rules —
    # a missing font would silently fall back to a system default rather than
    # error, so this checks every placeholder resolves to a file that exists.
    # Includes every theme stylesheet (each declares its own display font).
    css_paths = [
        SKILL_DIR / "assets" / "character_sheet.css",
        SKILL_DIR / "assets" / "mook_sheet.css",
        *(SKILL_DIR / "assets" / "themes").glob("*.css"),
    ]
    for css_path in css_paths:
        load_css_with_fonts(css_path, FONTS_DIR)


def test_load_themed_css_appends_theme_after_structure_and_inlines_fonts(tmp_path):
    # The theme must come AFTER the structure so its treatment overrides win the
    # cascade (:root/@font-face are order-independent). Font placeholders in
    # either file are inlined the same way load_css_with_fonts does.
    structure = tmp_path / "structure.css"
    structure.write_text(".hazard-stripe { height: 6pt; }\n", encoding="utf-8")
    theme = tmp_path / "theme.css"
    theme.write_text(
        '@font-face { font-family: "X"; src: url("__FONT:NotoSans-Regular.ttf__"); }\n'
        ":root { --accent: #ff0000; }\n"
        ".hazard-stripe { height: 2pt; }\n",
        encoding="utf-8",
    )

    css = load_themed_css(structure, theme, FONTS_DIR)

    # structure first, theme (the override) last
    assert css.index("height: 6pt;") < css.index("height: 2pt;")
    assert "--accent: #ff0000;" in css
    assert "__FONT:" not in css
    assert "data:font/ttf;base64," in css


def test_render_html_to_pdf_produces_a_readable_pdf(tmp_path):
    output_pdf = tmp_path / "out.pdf"
    render_html_to_pdf(
        "<html><body><h1>Ünïcödé Ü ä ö ß Test</h1></body></html>", output_pdf
    )

    assert output_pdf.exists()
    reader = PdfReader(output_pdf)
    assert len(reader.pages) == 1
    assert "Ünïcödé" in reader.pages[0].extract_text()
