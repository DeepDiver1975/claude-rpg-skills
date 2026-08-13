import json
from pathlib import Path

import pytest

from fill_character_sheet import (
    STYLE_PRESETS,
    ability_modifier,
    build_context,
    fill_character_sheet,
    render_character_sheet_html,
)

SKILL_DIR = Path(__file__).resolve().parent.parent
FIGHTER = SKILL_DIR / "scripts" / "fixtures" / "sample_character.json"
WIZARD = SKILL_DIR / "scripts" / "fixtures" / "sample_wizard.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_ability_modifier_rounds_down():
    assert ability_modifier(16) == 3
    assert ability_modifier(8) == -1
    assert ability_modifier(10) == 0
    assert ability_modifier(13) == 1


def test_build_context_computes_saves_skills_passive_initiative():
    ctx = build_context(_load(FIGHTER))
    saves = {s["key"]: s for s in ctx["saves"]}
    assert saves["STR"]["total"] == "+5" and saves["STR"]["proficient"]  # +3 mod +2 prof
    assert saves["CON"]["total"] == "+4"
    assert saves["DEX"]["total"] == "+1" and not saves["DEX"]["proficient"]

    skills = {s["name_de"]: s for s in ctx["skills"]}
    assert skills["Athletik"]["total"] == "+5" and skills["Athletik"]["proficient"]  # STR
    assert skills["Wahrnehmung"]["total"] == "+1"  # WIS 13 -> +1, unproficient

    assert ctx["passive_perception"] == 11  # 10 + WIS(+1) + 0
    assert ctx["initiative"] == "+1"


def test_expertise_doubles_proficiency_bonus():
    character = _load(FIGHTER)
    character["skill_expertise"] = ["Athletics"]
    skills = {s["name_de"]: s for s in build_context(character)["skills"]}
    assert skills["Athletik"]["total"] == "+7"  # STR +3 + 2*prof(2)
    assert skills["Athletik"]["expertise"]


def test_caster_spell_dc_and_attack_are_computed():
    ctx = build_context(_load(WIZARD))
    assert ctx["spells"]["save_dc"] == 13  # 8 + prof 2 + INT 3
    assert ctx["spells"]["attack"] == "+5"
    assert "Magisches Geschoss" in ctx["spells"]["spells"]


def test_non_caster_has_no_spell_section():
    fighter_html = render_character_sheet_html(_load(FIGHTER))
    wizard_html = render_character_sheet_html(_load(WIZARD))
    assert '<div class="section-label">Zauber</div>' not in fighter_html
    assert '<div class="section-label">Zauber</div>' in wizard_html


def test_html_uses_german_labels():
    html = render_character_sheet_html(_load(FIGHTER))
    for label in ("Attribute", "Kampfwerte", "Rettungswürfe", "Fertigkeiten"):
        assert label in html
    assert "Athletik" in html and "Stärke" in html  # German skill/ability names


def test_default_style_preset_is_classic_phb():
    html = render_character_sheet_html(_load(FIGHTER))
    assert "--accent: #7a1f1f;" in html  # classic-phb palette token


def test_unknown_style_preset_raises():
    character = _load(FIGHTER)
    character["style_preset"] = "vaporwave"
    with pytest.raises(ValueError, match="vaporwave"):
        render_character_sheet_html(character)


def test_missing_portrait_file_raises_actionable_error(tmp_path):
    character = _load(FIGHTER)
    character["portrait_image_path"] = str(tmp_path / "not-generated-yet.png")
    with pytest.raises(ValueError, match="portrait"):
        render_character_sheet_html(character)


@pytest.mark.parametrize("preset", sorted(STYLE_PRESETS))
def test_every_style_preset_composes_and_renders(tmp_path, preset):
    character = _load(WIZARD)
    character["style_preset"] = preset
    character_json = tmp_path / "c.json"
    character_json.write_text(json.dumps(character, ensure_ascii=False), encoding="utf-8")
    out = tmp_path / f"{preset}.pdf"
    fill_character_sheet(character_json, out)
    assert out.exists() and out.stat().st_size > 0
