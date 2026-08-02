from pathlib import Path

from extract_fields import extract_fields

SKILL_DIR = Path(__file__).resolve().parent.parent
CHARACTER_SHEET = SKILL_DIR / "assets" / "5E_CharacterSheet_Fillable.pdf"


def test_character_sheet_field_count():
    fields = extract_fields(CHARACTER_SHEET)
    assert len(fields) == 334


def test_character_sheet_has_character_image_button():
    fields = extract_fields(CHARACTER_SHEET)
    by_name = {f["name"]: f for f in fields}
    assert by_name["CHARACTER IMAGE"]["type"] == "Button"


def test_character_sheet_has_skill_field():
    fields = extract_fields(CHARACTER_SHEET)
    names = {f["name"] for f in fields}
    assert "Athletics" in names


def test_character_sheet_preserves_field_names_with_trailing_spaces():
    # This sheet has real AcroForm field names with a genuine trailing space
    # (e.g. "Race ", "Perception "); a naive .strip() during extraction would
    # silently produce a name that no longer matches the PDF's actual field,
    # so fill_form would drop that value without any error. See the
    # comment in extract_fields.py's parsing loop.
    fields = extract_fields(CHARACTER_SHEET)
    names = {f["name"] for f in fields}
    assert "Race " in names
    assert "Perception " in names
    assert "Wpn3 AtkBonus  " in names
