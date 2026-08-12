#!/usr/bin/env python3
"""Render a Cyberpunk RED character sheet PDF from a character JSON file."""
import argparse
import json
import math
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

# Visual style presets (SKILL.md Step 2 / references/style-guide.md). The GM's
# chosen preset themes the character sheet's own palette + fonts, matching the
# look of the art generated for the same run. Each key maps to a theme
# stylesheet under assets/themes/; the structural character_sheet.css is
# composed after it (see render_pdf.load_themed_css). The image-prompt style
# blocks live in references/style-guide.md, not here.
STYLE_PRESETS = {
    "cpr-rulebook": "cpr-rulebook.css",
    "pulp-2020": "pulp-2020.css",
    "night-city-cinematic": "night-city-cinematic.css",
    "edgerunners-anime": "edgerunners-anime.css",
    "chrome-noir": "chrome-noir.css",
}
DEFAULT_STYLE_PRESET = "cpr-rulebook"

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
    # These five are in the skill's own sourced free-rules list
    # (references/cpr-rules-summary.md) but were missed when the AcroForm-era
    # skill map was built, because the official PDF names their fields
    # outside the "LVL<Skill> <STAT>" pattern that map was built from — see
    # cpr-rules-summary.md:133-143 for the (self-documented) full story.
    "Handgun": "REF", "Concentration": "WILL", "Conceal/Reveal Object": "INT",
}

# CPR "pick a specialization" skills: the bare skill name is meaningless
# without naming the specific area/instrument, so these are matched by
# prefix (e.g. "Local Expert (Combat Zone)") in addition to the bare name.
CATEGORY_SKILLS = {"Local Expert": "INT", "Play Instrument": "TECH"}

VALID_SKILLS = set(SKILL_GOVERNING_STAT) | set(CATEGORY_SKILLS)


def _governing_stat(skill_name: str) -> str | None:
    if skill_name in SKILL_GOVERNING_STAT:
        return SKILL_GOVERNING_STAT[skill_name]
    base_name = skill_name.split(" (", 1)[0]
    return CATEGORY_SKILLS.get(base_name)


# CPR's starting Reputation for a new character (not covered by the free
# reference material this skill sources from — see README/SKILL.md's
# unverified-content policy); used only when a character JSON predates the
# `reputation` field.
DEFAULT_REPUTATION = 2


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
    """Resolve a style-preset key to its theme stylesheet, failing loudly (like
    the skill-name guardrail) on an unknown preset."""
    theme_file = STYLE_PRESETS.get(style_preset)
    if theme_file is None:
        raise ValueError(
            f"unknown style_preset {style_preset!r} — must be one of "
            f"{sorted(STYLE_PRESETS)}"
        )
    return THEMES_DIR / theme_file


def build_skill_rows(skills: dict[str, int], stats: dict[str, int]) -> list[dict]:
    """Return sorted display rows for the FULL CPR skill list, not only the
    trained ones — an untrained skill is still rollable at its base stat, so the
    sheet lists every skill with its rolled total (stat + level) and a `trained`
    flag. The character's chosen category-skill specializations (e.g.
    "Local Expert (Combat Zone)") are merged in alongside the canonical list.

    Raises ValueError naming any skill name that isn't a recognized skill or
    a "category skill (specialization)" (e.g. "Local Expert (Combat Zone)").
    """
    unknown_skills = {name for name in skills if _governing_stat(name) is None}
    if unknown_skills:
        raise ValueError(
            f"skill(s) {sorted(unknown_skills)!r} not in VALID_SKILLS — "
            "add them there (Task 9) before using a sheet that uses them"
        )

    # The canonical list plus any specialization the character actually named
    # (bare category skills like "Local Expert" are excluded from the default
    # list — they're meaningless without an area, so they show only if chosen).
    specializations = {name for name in skills if name not in SKILL_GOVERNING_STAT}
    all_names = set(SKILL_GOVERNING_STAT) | specializations

    return [
        {
            "name": name,
            "stat": (stat := _governing_stat(name)),
            "level": (level := skills.get(name, 0)),
            "total": level + stats[stat],
            "trained": name in skills,
        }
        for name in sorted(all_names)
    ]


def render_character_sheet_html(character: dict) -> str:
    """Render a character JSON dict into a self-contained HTML document string."""
    stats = character["stats"]
    skills = build_skill_rows(character["skills"], stats)
    theme_css_path = _theme_css_path(character.get("style_preset", DEFAULT_STYLE_PRESET))

    template = _ENV.get_template("character_sheet.html.jinja")
    return template.render(
        character=character,
        skills=skills,
        seriously_wounded=math.ceil(character["hp"]["max"] / 2),
        death_save=stats["BODY"],
        reputation=character.get("reputation", DEFAULT_REPUTATION),
        cyberware=character.get("cyberware", []),
        addictions=character.get("addictions"),
        gear=character.get("gear", []),
        money=character.get("money", {}),
        ip=character.get("ip"),
        portrait_data_uri=_portrait_data_uri(character.get("portrait_image_path")),
        css=load_themed_css(ASSETS_DIR / "character_sheet.css", theme_css_path, ASSETS_DIR / "fonts"),
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
