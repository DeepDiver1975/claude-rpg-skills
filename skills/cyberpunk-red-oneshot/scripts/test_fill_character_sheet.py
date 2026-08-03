import base64
import json
from pathlib import Path

import pytest
from PIL import Image
from pypdf import PdfReader

from fill_character_sheet import build_skill_rows, fill_character_sheet, render_character_sheet_html

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


def test_previously_missing_free_source_skills_are_now_valid():
    # Handgun, Concentration, and Conceal/Reveal Object are all in the skill's
    # own sourced free-rules list (references/cpr-rules-summary.md) but were
    # never added to the AcroForm-era skill map because the official PDF names
    # their fields outside the "LVL<Skill> <STAT>" pattern the map was built
    # from (documented as an open TODO in cpr-rules-summary.md:133-143).
    character = _character()
    character["skills"] = {"Handgun": 5, "Concentration": 2, "Conceal/Reveal Object": 3}
    html = render_character_sheet_html(character)
    assert "Handgun" in html and "Concentration" in html


def test_category_skills_accept_a_named_specialization():
    # Local Expert and Play Instrument are CPR "pick a specialization" skills
    # — a bare "Local Expert" is meaningless without naming the area/instrument.
    character = _character()
    character["skills"] = {
        "Local Expert (Combat Zone)": 4,
        "Play Instrument (Guitar)": 3,
    }
    stats = character["stats"]
    skills = {s["name"]: s for s in build_skill_rows(character["skills"], stats)}
    assert skills["Local Expert (Combat Zone)"]["total"] == 4 + stats["INT"]
    assert skills["Play Instrument (Guitar)"]["total"] == 3 + stats["TECH"]


def test_category_skill_without_specialization_still_valid():
    character = _character()
    character["skills"] = {"Local Expert": 4}
    render_character_sheet_html(character)  # must not raise


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
    # Check the first page specifically, not a document-wide count: WeasyPrint
    # can place the image XObject in a resources dict shared across pages, so
    # pypdf's per-page `.images` may list it on a later page too even though
    # it's only ever painted in the header on page 1.
    assert len(reader.pages[0].images) == 1
