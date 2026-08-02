from pathlib import Path

from extract_fields import extract_fields

SKILL_DIR = Path(__file__).resolve().parent.parent
CHARACTER_SHEET = SKILL_DIR / "assets" / "RTG-CPR-CharacterSheet-Fillable.pdf"
MOOK_SHEET = SKILL_DIR / "assets" / "RTG-CPR-MooksSheetFormFillable.pdf"


def test_character_sheet_field_count():
    fields = extract_fields(CHARACTER_SHEET)
    assert len(fields) == 413


def test_character_sheet_has_character_image_button():
    fields = extract_fields(CHARACTER_SHEET)
    by_name = {f["name"]: f for f in fields}
    assert by_name["Character Image"]["type"] == "Button"


def test_character_sheet_has_skill_field():
    fields = extract_fields(CHARACTER_SHEET)
    names = {f["name"] for f in fields}
    assert "LVLAthletics DEX" in names


def test_mook_sheet_field_count():
    fields = extract_fields(MOOK_SHEET)
    assert len(fields) == 27


def test_mook_sheet_has_name_field():
    fields = extract_fields(MOOK_SHEET)
    names = {f["name"] for f in fields}
    assert "Name" in names
