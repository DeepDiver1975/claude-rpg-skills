import json
from pathlib import Path

from pypdf import PdfReader

from fill_mook_sheet import fill_mook_sheet, render_mook_sheet_html

SKILL_DIR = Path(__file__).resolve().parent.parent
FIXTURE = SKILL_DIR / "scripts" / "fixtures" / "sample_mook.json"


def _mook() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_render_mook_sheet_html_includes_core_fields():
    html = render_mook_sheet_html(_mook())
    assert "Corp-Wachmann" in html
    assert "Medium Pistol" in html
    assert "Schlagstock" in html
    assert "Funkgerät" in html


def test_fill_mook_sheet_produces_a_readable_pdf_with_correct_values(tmp_path):
    output_pdf = tmp_path / "mook.pdf"
    fill_mook_sheet(FIXTURE, output_pdf)

    assert output_pdf.exists()
    reader = PdfReader(output_pdf)
    text = "".join(page.extract_text() for page in reader.pages)
    assert "Corp-Wachmann" in text
    assert "8" in text
