#!/usr/bin/env python3
"""Fill the official D&D 5e Character Sheet PDF from a character JSON file."""
import argparse
import json
import tempfile
from pathlib import Path

from pdf_form import fill_text_fields, stamp_image_on_page

SKILL_DIR = Path(__file__).resolve().parent.parent
BLANK_SHEET = SKILL_DIR / "assets" / "5E_CharacterSheet_Fillable.pdf"
SKILLS_FIELD_MAP = json.loads(
    (SKILL_DIR / "assets" / "skills_field_map.json").read_text(encoding="utf-8")
)

# Empirically measured (see scripts/test_pdf_form.py) — page 2 holds the
# personal-characteristics/backstory content, including the portrait box.
CHARACTER_IMAGE_PAGE = 2
CHARACTER_IMAGE_PAGE_SIZE_PT = (612.0, 792.0)
CHARACTER_IMAGE_RECT_PT = (36.4791, 443.398, 199.172, 661.497)

ABILITIES = ("STR", "DEX", "CON", "INT", "WIS", "CHA")
# This sheet's per-ability modifier fields don't follow one consistent naming
# scheme — most are "<ABILITY>mod" but Charisma's is the sheet's own typo
# "CHamod" (missing the second A), preserved verbatim like the CPR skill
# preserved its own sheet's field-name quirks.
ABILITY_MOD_FIELD = {
    "STR": "STRmod", "DEX": "DEXmod ", "CON": "CONmod",
    "INT": "INTmod", "WIS": "WISmod", "CHA": "CHamod",
}
SAVE_FIELD = {
    "STR": "ST Strength", "DEX": "ST Dexterity", "CON": "ST Constitution",
    "INT": "ST Intelligence", "WIS": "ST Wisdom", "CHA": "ST Charisma",
}
SKILL_ABILITY = {
    "Acrobatics": "DEX", "Animal Handling": "WIS", "Arcana": "INT",
    "Athletics": "STR", "Deception": "CHA", "History": "INT",
    "Insight": "WIS", "Intimidation": "CHA", "Investigation": "INT",
    "Medicine": "WIS", "Nature": "INT", "Perception": "WIS",
    "Performance": "CHA", "Persuasion": "CHA", "Religion": "INT",
    "Sleight of Hand": "DEX", "Stealth": "DEX", "Survival": "WIS",
}
# This sheet has only 3 weapon/attack rows (the CPR sheet had 4); extra
# weapons beyond the first 3 are omitted from the PDF (still present in the
# parallel Markdown sheet SKILL.md Step 5 requires alongside the PDF).
MAX_WEAPON_ROWS = 3
WEAPON_ROW_FIELDS = [
    ("Wpn Name", "Wpn1 AtkBonus", "Wpn1 Damage"),
    ("Wpn Name 2", "Wpn2 AtkBonus ", "Wpn2 Damage "),
    ("Wpn Name 3", "Wpn3 AtkBonus  ", "Wpn3 Damage "),
]


def ability_modifier(score: int) -> int:
    return (score - 10) // 2


def _signed(n: int) -> str:
    return f"+{n}" if n >= 0 else str(n)


def build_field_values(character: dict) -> dict[str, str]:
    ability_scores = character["ability_scores"]
    mods = {ab: ability_modifier(ability_scores[ab]) for ab in ABILITIES}
    prof_bonus = character["proficiency_bonus"]

    values: dict[str, str] = {
        "CharacterName": character["name"],
        "CharacterName 2": character["name"],
        "ClassLevel": f"{character['class']} {character['level']}",
        "Background": character["background"],
        # 2024/SRD-5.2.1 characters have a "Species", not a "Race" — this
        # sheet is the 2014-rules layout (see SKILL.md's known-limitations
        # section), so the Species value is deliberately written into the
        # sheet's own "Race " field (trailing space preserved verbatim).
        "Race ": character["species"],
        "Alignment": character.get("alignment", ""),
        "ProfBonus": _signed(prof_bonus),
        "AC": str(character["ac"]),
        "Initiative": _signed(mods["DEX"]),
        "Speed": str(character["speed"]),
        "HPMax": str(character["hp"]["max"]),
        "HPCurrent": str(character["hp"]["current"]),
        "HPTemp": str(character["hp"]["temp"]),
        # Best-effort: this sheet doesn't clearly separate "hit dice count"
        # from "hit dice type" the way the schema does, so both fields get
        # the same combined "<total><die>" notation (e.g. "1d10").
        "HD": character["hit_dice"]["die"],
        "HDTotal": character["hit_dice"]["die"],
        "PersonalityTraits ": character.get("personality_traits", ""),
        "Ideals": character.get("ideals", ""),
        "Bonds": character.get("bonds", ""),
        "Flaws": character.get("flaws", ""),
        "Backstory": character.get("backstory", ""),
        "Features and Traits": "\n".join(character.get("features_and_traits", [])),
        "Equipment": "\n".join(character.get("equipment", [])),
    }

    for ability in ABILITIES:
        values[ability] = str(ability_scores[ability])
        values[ABILITY_MOD_FIELD[ability]] = _signed(mods[ability])

    save_proficiencies = set(character.get("saving_throw_proficiencies", []))
    for ability in ABILITIES:
        total = mods[ability] + (prof_bonus if ability in save_proficiencies else 0)
        values[SAVE_FIELD[ability]] = _signed(total)

    skill_proficiencies = set(character.get("skill_proficiencies", []))
    skill_expertise = set(character.get("skill_expertise", []))
    for skill_name, level in SKILLS_FIELD_MAP.items():
        governing_ability = SKILL_ABILITY[skill_name]
        bonus = 0
        if skill_name in skill_expertise:
            bonus = prof_bonus * 2
        elif skill_name in skill_proficiencies:
            bonus = prof_bonus
        total = mods[governing_ability] + bonus
        values[level] = _signed(total)

    perception_total = mods["WIS"] + (
        prof_bonus * 2 if "Perception" in skill_expertise
        else prof_bonus if "Perception" in skill_proficiencies
        else 0
    )
    values["Passive"] = str(10 + perception_total)

    coins = character.get("coins", {})
    for denom in ("cp", "sp", "ep", "gp", "pp"):
        if denom in coins:
            values[denom.upper()] = str(coins[denom])

    for (name_field, atk_field, dmg_field), weapon in zip(
        WEAPON_ROW_FIELDS, character.get("weapons", [])[:MAX_WEAPON_ROWS]
    ):
        attack_mod = mods[weapon["attack_ability"]] + prof_bonus
        weapon_name = weapon["name"]
        extra = ", ".join(
            part for part in (weapon.get("properties", ""), weapon.get("mastery", "")) if part
        )
        if extra:
            weapon_name = f"{weapon_name} ({extra})"
        values[name_field] = weapon_name
        values[atk_field] = _signed(attack_mod)
        values[dmg_field] = f"{weapon['damage_die']}{_signed(mods[weapon['attack_ability']])} {weapon['damage_type']}"

    spellcasting = character.get("spellcasting")
    if spellcasting:
        ability = spellcasting["ability"]
        spell_dc = 8 + prof_bonus + mods[ability]
        spell_atk = prof_bonus + mods[ability]
        values["Spellcasting Class 2"] = character["class"]
        values["SpellcastingAbility 2"] = ability
        values["SpellSaveDC  2"] = str(spell_dc)
        values["SpellAtkBonus 2"] = _signed(spell_atk)

    return values


def fill_character_sheet(character_json_path: Path, output_pdf: Path) -> None:
    character = json.loads(Path(character_json_path).read_text(encoding="utf-8"))
    values = build_field_values(character)

    # The portrait is stamped onto the blank sheet *before* the fields are
    # filled, so filling is always the last step. pdftk's cat/stamp operations
    # drop the AcroForm NeedAppearances flag that fill_text_fields sets, and
    # without that flag renderers fall back to pdftk's own appearance streams,
    # which silently drop umlauts from the printed page (see pdf_form.py).
    with tempfile.TemporaryDirectory() as tmp:
        source_pdf = BLANK_SHEET
        portrait_path = character.get("portrait_image_path")
        if portrait_path:
            source_pdf = Path(tmp) / "with_portrait.pdf"
            stamp_image_on_page(
                BLANK_SHEET, source_pdf,
                CHARACTER_IMAGE_PAGE, CHARACTER_IMAGE_PAGE_SIZE_PT, CHARACTER_IMAGE_RECT_PT,
                Path(portrait_path),
            )
        fill_text_fields(source_pdf, output_pdf, values)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("character_json", type=Path)
    parser.add_argument("output_pdf", type=Path)
    args = parser.parse_args()
    fill_character_sheet(args.character_json, args.output_pdf)
    print(f"wrote {args.output_pdf}")


if __name__ == "__main__":
    main()
