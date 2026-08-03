#!/usr/bin/env python3
"""Render a Cyberpunk RED character sheet PDF from a character JSON file."""
import argparse
import json
import math
from pathlib import Path

import jinja2

from render_pdf import data_uri, load_css_with_fonts, render_html_to_pdf

SKILL_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = SKILL_DIR / "assets"

_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(ASSETS_DIR),
    autoescape=jinja2.select_autoescape(["html", "jinja"]),
)

_PORTRAIT_MIME_TYPES = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}

# The sheet's primary skill list, mapped to its governing stat — sourced from
# the official sheet's own AcroForm field names (e.g. "LVLAthletics DEX"),
# which is the same provenance SKILL.md Step 10 already flags as unverified
# for ~21 of these. Kept as an explicit allow-list (rather than accepting any
# string) so a typo'd or invented skill name fails loudly instead of silently
# printing on the sheet.
SKILL_GOVERNING_STAT = {
    "Accounting": "INT", "Acting": "COOL", "Air Vehicle Tech": "TECH",
    "Animal Handling": "INT", "Archery": "REF", "Athletics": "DEX",
    "Autofire (x2)": "REF", "Basic Tech": "TECH", "Brawling": "DEX",
    "Bribery": "COOL", "Bureaucracy": "INT", "Business": "INT",
    "Composition": "INT", "Contortionist": "DEX", "Conversation": "EMP",
    "Criminology": "INT", "Cryptography": "INT", "Cybertech": "TECH",
    "Dance": "DEX", "Deduction": "INT", "Demolitions (x2)": "TECH",
    "Drive Land Vehicle": "REF", "Education": "INT",
    "Electronics/Security Tech (x2)": "TECH", "Endurance": "WILL",
    "Evasion": "DEX", "First Aid": "TECH", "Forgery": "TECH",
    "Heavy Weapons (x2)": "REF", "Human Perception": "EMP",
    "Interrogation": "COOL", "Land Vehicle Tech": "TECH",
    "Library Search": "INT", "Lip Reading": "INT", "Martial Arts (x2)": "DEX",
    "Melee Weapon": "DEX", "Paint/Draw/Sculpt": "TECH", "Paramedic (x2)": "TECH",
    "Perception": "INT", "Personal Grooming": "COOL", "Persuasion": "COOL",
    "Photography/Film": "TECH", "Pick Lock": "TECH", "Pick Pocket": "TECH",
    "Pilot Air Vehicle (x2)": "REF", "Pilot Sea Vehicle": "REF",
    "Resist Torture/Drugs": "WILL", "Riding": "REF", "Sea Vehicle Tech": "TECH",
    "Shoulder Arms": "REF", "Stealth": "DEX", "Streetwise": "COOL",
    "Tactics": "INT", "Tracking": "INT", "Trading": "COOL",
    "Wardrobe & Style": "COOL", "Wilderness Survival": "INT",
}
VALID_SKILLS = set(SKILL_GOVERNING_STAT)

# CPR's starting Reputation for a new character (not covered by the free
# reference material this skill sources from — see README/SKILL.md's
# unverified-content policy); used only when a character JSON predates the
# `reputation` field.
DEFAULT_REPUTATION = 2


def _portrait_data_uri(portrait_image_path: str | None) -> str | None:
    if not portrait_image_path:
        return None
    suffix = Path(portrait_image_path).suffix.lower()
    mime = _PORTRAIT_MIME_TYPES.get(suffix)
    if mime is None:
        raise ValueError(f"unsupported portrait image type: {portrait_image_path!r}")
    return data_uri(Path(portrait_image_path), mime)


def render_character_sheet_html(character: dict) -> str:
    """Render a character JSON dict into a self-contained HTML document string."""
    unknown_skills = set(character["skills"]) - VALID_SKILLS
    if unknown_skills:
        raise ValueError(
            f"skill(s) {sorted(unknown_skills)!r} not in VALID_SKILLS — "
            "add them there (Task 9) before using a sheet that uses them"
        )

    stats = character["stats"]
    skills = [
        {
            "name": name,
            "stat": SKILL_GOVERNING_STAT[name],
            "level": level,
            "total": level + stats[SKILL_GOVERNING_STAT[name]],
        }
        for name, level in sorted(character["skills"].items())
    ]

    template = _ENV.get_template("character_sheet.html.jinja")
    return template.render(
        character=character,
        skills=skills,
        seriously_wounded=math.ceil(character["hp"]["max"] / 2),
        death_save=stats["BODY"],
        reputation=character.get("reputation", DEFAULT_REPUTATION),
        cyberware=character.get("cyberware", []),
        portrait_data_uri=_portrait_data_uri(character.get("portrait_image_path")),
        css=load_css_with_fonts(ASSETS_DIR / "character_sheet.css", ASSETS_DIR / "fonts"),
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
