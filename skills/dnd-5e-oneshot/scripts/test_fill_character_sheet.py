import json
import subprocess
from pathlib import Path

import pytest

from fill_character_sheet import (
    ability_modifier,
    build_field_values,
    fill_character_sheet,
)

SKILL_DIR = Path(__file__).resolve().parent.parent
FIXTURE = SKILL_DIR / "scripts" / "fixtures" / "sample_character.json"


def _load_fixture() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    "score,expected",
    [(1, -5), (8, -1), (9, -1), (10, 0), (11, 0), (13, 1), (16, 3), (20, 5)],
)
def test_ability_modifier(score, expected):
    assert ability_modifier(score) == expected


def test_build_field_values_static_fields():
    values = build_field_values(_load_fixture())
    assert values["CharacterName"] == "Rurik"
    assert values["ClassLevel"] == "Fighter 1"
    assert values["Background"] == "Soldier"
    assert values["Race "] == "Dwarf"
    assert values["AC"] == "16"
    assert values["Speed"] == "30"
    assert values["HPMax"] == "13"


def test_build_field_values_ability_scores_and_mods():
    values = build_field_values(_load_fixture())
    # STR 16 -> mod +3
    assert values["STR"] == "16"
    assert values["STRmod"] == "+3"
    # CHA 8 -> mod -1 (sheet's own typo field name "CHamod", not "CHAmod")
    assert values["CHA"] == "8"
    assert values["CHamod"] == "-1"
    # DEX 12 -> mod +1
    assert values["DEXmod "] == "+1"


def test_build_field_values_initiative_uses_dex_mod():
    values = build_field_values(_load_fixture())
    assert values["Initiative"] == "+1"


def test_build_field_values_saving_throws():
    values = build_field_values(_load_fixture())
    # STR save: proficient, mod +3, PB +2 -> +5
    assert values["ST Strength"] == "+5"
    # CON save: proficient, mod +2, PB +2 -> +4
    assert values["ST Constitution"] == "+4"
    # DEX save: not proficient, mod +1 only -> +1
    assert values["ST Dexterity"] == "+1"


def test_build_field_values_skills():
    values = build_field_values(_load_fixture())
    # Athletics (STR, proficient): +3 mod + 2 PB = +5
    assert values["Athletics"] == "+5"
    # Intimidation (CHA, proficient): -1 mod + 2 PB = +1
    assert values["Intimidation"] == "+1"
    # Acrobatics (DEX, not proficient): +1 mod only
    assert values["Acrobatics"] == "+1"


def test_build_field_values_passive_perception():
    values = build_field_values(_load_fixture())
    # WIS 13 -> mod +1, not proficient in Perception -> 10 + 1 = 11
    assert values["Passive"] == "11"


def test_build_field_values_weapon_row():
    values = build_field_values(_load_fixture())
    assert values["Wpn Name"] == "Longsword (Versatile (1d10), Sap)"
    # STR mod +3, PB +2 -> +5
    assert values["Wpn1 AtkBonus"] == "+5"
    assert values["Wpn1 Damage"] == "1d8+3 slashing"


def test_build_field_values_no_spellcasting_fields_for_non_caster():
    values = build_field_values(_load_fixture())
    assert "Spellcasting Class 2" not in values


def test_build_field_values_spellcasting_fields_for_caster():
    character = _load_fixture()
    character["spellcasting"] = {
        "ability": "INT", "cantrips": ["Fire Bolt"],
        "spells_known_or_prepared": ["Magic Missile"], "spell_slots": {"1": 2},
    }
    character["ability_scores"]["INT"] = 16
    character["proficiency_bonus"] = 2
    values = build_field_values(character)
    # INT 16 -> mod +3; DC = 8 + 2 + 3 = 13; attack bonus = 2 + 3 = +5
    assert values["Spellcasting Class 2"] == "Fighter"
    assert values["SpellcastingAbility 2"] == "INT"
    assert values["SpellSaveDC  2"] == "13"
    assert values["SpellAtkBonus 2"] == "+5"


def _dump_field_value(pdf_path: Path, field_name: str) -> str:
    result = subprocess.run(
        ["pdftk", str(pdf_path), "dump_data_fields_utf8"],
        check=True, capture_output=True, text=True,
    )
    lines = result.stdout.splitlines()
    for i, line in enumerate(lines):
        if line == f"FieldName: {field_name}":
            for follow in lines[i:i + 6]:
                if follow.startswith("FieldValue:"):
                    return follow.split(":", 1)[1].strip()
    raise AssertionError(f"field {field_name!r} not found or has no value")


def test_fill_character_sheet_end_to_end(tmp_path):
    output_pdf = tmp_path / "rurik.pdf"
    fill_character_sheet(FIXTURE, output_pdf)
    assert output_pdf.exists()
    assert _dump_field_value(output_pdf, "CharacterName") == "Rurik"
    assert _dump_field_value(output_pdf, "STRmod") == "+3"

    dump = subprocess.run(
        ["pdftk", str(output_pdf), "dump_data"], check=True, capture_output=True, text=True,
    ).stdout
    assert "NumberOfPages: 3" in dump


def test_fill_character_sheet_renders_german_backstory_with_umlauts(tmp_path):
    output_pdf = tmp_path / "rurik.pdf"
    fill_character_sheet(FIXTURE, output_pdf)
    txt_path = tmp_path / "page2.txt"
    subprocess.run(
        ["mutool", "draw", "-F", "txt", "-o", str(txt_path), str(output_pdf), "2"],
        check=True, capture_output=True,
    )
    rendered = txt_path.read_text(encoding="utf-8", errors="replace")
    assert "Österreich" in rendered, f"umlaut missing from rendered page: {rendered!r}"


def test_fill_character_sheet_stamps_portrait(tmp_path):
    portrait = tmp_path / "portrait.png"
    subprocess.run(["magick", "-size", "400x400", "xc:#3355ff", str(portrait)], check=True, capture_output=True)

    character = _load_fixture()
    character["portrait_image_path"] = str(portrait)
    character_json = tmp_path / "character.json"
    character_json.write_text(json.dumps(character), encoding="utf-8")

    output_pdf = tmp_path / "rurik.pdf"
    fill_character_sheet(character_json, output_pdf)

    png_path = tmp_path / "rendered.png"
    subprocess.run(
        ["mutool", "draw", "-o", str(png_path), "-r", "100", str(output_pdf), "2"],
        check=True, capture_output=True,
    )
    result = subprocess.run(
        ["magick", str(png_path), "-format", "%[pixel:p{150,300}]", "info:"],
        check=True, capture_output=True, text=True,
    )
    pixel = result.stdout.strip()
    assert "51,85,255" in pixel or "3355FF".lower() in pixel.lower()


def test_build_field_values_raises_nothing_for_missing_optional_fields():
    # A character with no weapons/coins/features should still build without error.
    character = _load_fixture()
    character["weapons"] = []
    character["coins"] = {}
    character["features_and_traits"] = []
    values = build_field_values(character)
    assert values["Equipment"] == "\n".join(character["equipment"])
