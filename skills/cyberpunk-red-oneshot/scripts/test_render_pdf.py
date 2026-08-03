import base64
from pathlib import Path

from pypdf import PdfReader

from render_pdf import data_uri, load_css_with_fonts, render_html_to_pdf

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


def test_load_css_with_fonts_replaces_both_placeholders():
    css_path = SKILL_DIR / "assets" / "character_sheet.css"
    css = load_css_with_fonts(css_path, FONTS_DIR)

    assert "__FONT_REGULAR_DATA_URI__" not in css
    assert "__FONT_BOLD_DATA_URI__" not in css
    assert css.count("data:font/ttf;base64,") == 2


def test_render_html_to_pdf_produces_a_readable_pdf(tmp_path):
    output_pdf = tmp_path / "out.pdf"
    render_html_to_pdf(
        "<html><body><h1>Ünïcödé Ü ä ö ß Test</h1></body></html>", output_pdf
    )

    assert output_pdf.exists()
    reader = PdfReader(output_pdf)
    assert len(reader.pages) == 1
    assert "Ünïcödé" in reader.pages[0].extract_text()
