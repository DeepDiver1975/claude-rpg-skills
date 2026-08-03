import base64
import json
from pathlib import Path

import pytest
from PIL import Image
from pypdf import PdfReader

from fill_character_sheet import fill_character_sheet, render_character_sheet_html

SKILL_DIR = Path(__file__).resolve().parent.parent
FIXTURE = SKILL_DIR / "scripts" / "fixtures" / "sample_character.json"


def _character() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_render_character_sheet_html_includes_core_fields():
    html = render_character_sheet_html(_character())
    # The literal quotes around "Rook" are HTML-escaped (&#34;) by Jinja2's
    # autoescaping, so check the surrounding text rather than the raw quotes.
    assert "Rüdiger" in html and "Straße" in html
    assert "Solo" in html
    assert "Combat Awareness" in html
    assert "Militärstiefel" in html
    assert "Shoulder Arms" in html
    # No separate stored-value-vs-rendered-appearance split exists for an
    # HTML/DOM renderer — a substring check on the returned markup already
    # proves the umlaut round-trip, unlike the old AcroForm appearance-stream
    # pipeline where the stored value and the printed page could disagree.


def test_render_character_sheet_html_rejects_unknown_skill():
    character = _character()
    character["skills"] = {"Not A Real Skill": 4}
    with pytest.raises(ValueError, match="Not A Real Skill"):
        render_character_sheet_html(character)


def test_render_character_sheet_html_embeds_portrait_as_exact_data_uri(tmp_path):
    portrait_path = tmp_path / "portrait.png"
    Image.new("RGB", (10, 10), color=(51, 85, 255)).save(portrait_path)
    original_bytes = portrait_path.read_bytes()

    character = _character()
    character["portrait_image_path"] = str(portrait_path)
    html = render_character_sheet_html(character)

    start = html.index('src="data:image/png;base64,') + len('src="data:image/png;base64,')
    end = html.index('"', start)
    assert base64.b64decode(html[start:end]) == original_bytes


def test_render_character_sheet_html_without_portrait_has_no_img_tag():
    character = _character()
    character["portrait_image_path"] = None
    html = render_character_sheet_html(character)
    assert "<img" not in html


def test_fill_character_sheet_produces_a_readable_pdf_with_correct_values(tmp_path):
    output_pdf = tmp_path / "character.pdf"
    fill_character_sheet(FIXTURE, output_pdf)

    assert output_pdf.exists()
    reader = PdfReader(output_pdf)
    text = "".join(page.extract_text() for page in reader.pages)
    assert 'Rüdiger "Rook" Straße' in text
    assert "Shoulder Arms" in text
    assert "6" in text


def test_fill_character_sheet_with_a_portrait_embeds_the_image(tmp_path):
    portrait_path = tmp_path / "portrait.png"
    Image.new("RGB", (400, 600), color=(51, 85, 255)).save(portrait_path)

    character = _character()
    character["portrait_image_path"] = str(portrait_path)
    character_json = tmp_path / "character.json"
    character_json.write_text(json.dumps(character, ensure_ascii=False), encoding="utf-8")

    output_pdf = tmp_path / "character.pdf"
    fill_character_sheet(character_json, output_pdf)

    assert output_pdf.exists()
    reader = PdfReader(output_pdf)
    all_images = [img for page in reader.pages for img in page.images]
    assert len(all_images) == 1
