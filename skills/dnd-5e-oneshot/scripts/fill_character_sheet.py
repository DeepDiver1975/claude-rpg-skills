#!/usr/bin/env python3
"""Render a D&D 5e (level-1) character sheet PDF from a character JSON file.

The sheet is an original HTML/CSS design rendered to PDF via WeasyPrint — no
Wizards of the Coast PDF is used. Labels are German; mechanical numbers are
computed here from the raw ability scores + proficiency lists in the JSON, so
the JSON never carries a modifier, total, or spell DC.
"""
import argparse
import json
from pathlib import Path

import jinja2

from render_pdf import data_uri, load_themed_css, render_html_to_pdf

SKILL_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = SKILL_DIR / "assets"
THEMES_DIR = ASSETS_DIR / "themes"

_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(ASSETS_DIR),
    autoescape=jinja2.select_autoescape(["html", "jinja"]),
)

_PORTRAIT_MIME_TYPES = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}

# Visual style presets (SKILL.md Step 2 / references/style-guide.md). Each key
# themes the sheet's palette + display font to match the run's chosen art style;
# the image-prompt style blocks live in references/style-guide.md, not here.
STYLE_PRESETS = {
    "classic-phb": "classic-phb.css",
    "painterly": "painterly.css",
    "bg3-cinematic": "bg3-cinematic.css",
    "flat-animated": "flat-animated.css",
    "grimdark": "grimdark.css",
}
DEFAULT_STYLE_PRESET = "classic-phb"

ABILITIES = ("STR", "DEX", "CON", "INT", "WIS", "CHA")

# German display names (official German SRD 5.2.1, see references/german-terminology.md).
# The three-letter STR/DEX/… abbreviations stay English per the glossary.
ABILITY_DE = {
    "STR": "Stärke", "DEX": "Geschicklichkeit", "CON": "Konstitution",
    "INT": "Intelligenz", "WIS": "Weisheit", "CHA": "Charisma",
}

# The 18 SRD skills → governing ability (English keys are the JSON contract) and
# their official German display names.
SKILL_ABILITY = {
    "Acrobatics": "DEX", "Animal Handling": "WIS", "Arcana": "INT",
    "Athletics": "STR", "Deception": "CHA", "History": "INT",
    "Insight": "WIS", "Intimidation": "CHA", "Investigation": "INT",
    "Medicine": "WIS", "Nature": "INT", "Perception": "WIS",
    "Performance": "CHA", "Persuasion": "CHA", "Religion": "INT",
    "Sleight of Hand": "DEX", "Stealth": "DEX", "Survival": "WIS",
}
SKILL_DE = {
    "Acrobatics": "Akrobatik", "Animal Handling": "Tierumgang", "Arcana": "Arkane Kunde",
    "Athletics": "Athletik", "Deception": "Täuschung", "History": "Geschichte",
    "Insight": "Menschenkenntnis", "Intimidation": "Einschüchtern",
    "Investigation": "Nachforschung", "Medicine": "Heilkunde", "Nature": "Naturkunde",
    "Perception": "Wahrnehmung", "Performance": "Auftreten", "Persuasion": "Überzeugen",
    "Religion": "Religion", "Sleight of Hand": "Fingerfertigkeit", "Stealth": "Heimlichkeit",
    "Survival": "Überlebenskunst",
}


def ability_modifier(score: int) -> int:
    return (score - 10) // 2


def _signed(n: int) -> str:
    return f"+{n}" if n >= 0 else str(n)


def _portrait_data_uri(portrait_image_path: str | None) -> str | None:
    if not portrait_image_path:
        return None
    path = Path(portrait_image_path)
    suffix = path.suffix.lower()
    mime = _PORTRAIT_MIME_TYPES.get(suffix)
    if mime is None:
        raise ValueError(f"unsupported portrait image type: {portrait_image_path!r}")
    if not path.is_file():
        raise ValueError(
            f"portrait image not found at {portrait_image_path!r} — generate it "
            "from the character's image-prompts/portrait-*.txt first, or set "
            '"portrait_image_path": null to render this sheet without a portrait.'
        )
    return data_uri(path, mime)


def _theme_css_path(style_preset: str) -> Path:
    theme_file = STYLE_PRESETS.get(style_preset)
    if theme_file is None:
        raise ValueError(
            f"unknown style_preset {style_preset!r} — must be one of {sorted(STYLE_PRESETS)}"
        )
    return THEMES_DIR / theme_file


def build_context(character: dict) -> dict:
    """Derive every printed value (modifiers, save/skill totals, passive
    perception, attack/damage, spell DC/attack) from the character's raw scores
    and proficiency lists. The JSON supplies scores + proficiencies only."""
    scores = character["ability_scores"]
    mods = {ab: ability_modifier(scores[ab]) for ab in ABILITIES}
    prof = character["proficiency_bonus"]

    abilities = [
        {"key": ab, "name_de": ABILITY_DE[ab], "score": scores[ab],
         "mod": _signed(mods[ab])}
        for ab in ABILITIES
    ]

    save_prof = set(character.get("saving_throw_proficiencies", []))
    saves = [
        {"key": ab, "name_de": ABILITY_DE[ab], "proficient": ab in save_prof,
         "total": _signed(mods[ab] + (prof if ab in save_prof else 0))}
        for ab in ABILITIES
    ]

    skill_prof = set(character.get("skill_proficiencies", []))
    skill_exp = set(character.get("skill_expertise", []))
    skills = []
    for name in sorted(SKILL_ABILITY, key=lambda n: SKILL_DE[n]):
        ab = SKILL_ABILITY[name]
        bonus = prof * 2 if name in skill_exp else prof if name in skill_prof else 0
        skills.append({
            "name_de": SKILL_DE[name], "ability": ab,
            "proficient": name in skill_prof, "expertise": name in skill_exp,
            "total": _signed(mods[ab] + bonus),
        })

    perception_bonus = (
        prof * 2 if "Perception" in skill_exp
        else prof if "Perception" in skill_prof else 0
    )
    passive_perception = 10 + mods["WIS"] + perception_bonus

    weapons = []
    for w in character.get("weapons", []):
        atk_ab = w["attack_ability"]
        extra = ", ".join(p for p in (w.get("properties", ""), w.get("mastery", "")) if p)
        weapons.append({
            "name": w["name"],
            "attack": _signed(mods[atk_ab] + prof),
            "damage": f"{w['damage_die']}{_signed(mods[atk_ab])} {w['damage_type']}",
            "properties": extra,
        })

    spellcasting = character.get("spellcasting")
    spells = None
    if spellcasting:
        ab = spellcasting["ability"]
        spells = {
            "ability": ab, "ability_de": ABILITY_DE[ab],
            "save_dc": 8 + prof + mods[ab],
            "attack": _signed(prof + mods[ab]),
            "cantrips": spellcasting.get("cantrips", []),
            "spells": spellcasting.get("spells_known_or_prepared", []),
            "slots": spellcasting.get("spell_slots", {}),
        }

    return {
        "character": character,
        "abilities": abilities,
        "saves": saves,
        "skills": skills,
        "passive_perception": passive_perception,
        "initiative": _signed(mods["DEX"]),
        "proficiency_bonus": _signed(prof),
        "weapons": weapons,
        "spells": spells,
        "coins": character.get("coins", {}),
        "portrait_data_uri": _portrait_data_uri(character.get("portrait_image_path")),
    }


def render_character_sheet_html(character: dict) -> str:
    """Render a character JSON dict into a self-contained HTML document string."""
    theme_css_path = _theme_css_path(character.get("style_preset", DEFAULT_STYLE_PRESET))
    context = build_context(character)
    template = _ENV.get_template("character_sheet.html.jinja")
    return template.render(
        css=load_themed_css(ASSETS_DIR / "character_sheet.css", theme_css_path, ASSETS_DIR / "fonts"),
        **context,
    )


def fill_character_sheet(character_json_path: Path, output_pdf: Path) -> None:
    character = json.loads(Path(character_json_path).read_text(encoding="utf-8"))
    html = render_character_sheet_html(character)
    render_html_to_pdf(html, output_pdf)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("character_json", type=Path)
    parser.add_argument("output_pdf", type=Path)
    args = parser.parse_args()
    fill_character_sheet(args.character_json, args.output_pdf)
    print(f"wrote {args.output_pdf}")


if __name__ == "__main__":
    main()
