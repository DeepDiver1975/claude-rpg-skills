#!/usr/bin/env python3
"""Render a Cyberpunk RED character sheet PDF from a character JSON file."""
import argparse
import json
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

# The sheet's primary skill list. Kept as an explicit allow-list (rather than
# accepting any string) so a typo'd or invented skill name fails loudly instead
# of silently printing on the sheet — same guardrail the old AcroForm field map
# gave us for free, now that there's no field map to check membership against.
VALID_SKILLS = {
    "Accounting", "Acting", "Air Vehicle Tech", "Animal Handling", "Archery",
    "Athletics", "Autofire (x2)", "Basic Tech", "Brawling", "Bribery",
    "Bureaucracy", "Business", "Composition", "Contortionist", "Conversation",
    "Criminology", "Cryptography", "Cybertech", "Dance", "Deduction",
    "Demolitions (x2)", "Drive Land Vehicle", "Education",
    "Electronics/Security Tech (x2)", "Endurance", "Evasion", "First Aid",
    "Forgery", "Heavy Weapons (x2)", "Human Perception", "Interrogation",
    "Land Vehicle Tech", "Library Search", "Lip Reading", "Martial Arts (x2)",
    "Melee Weapon", "Paint/Draw/Sculpt", "Paramedic (x2)", "Perception",
    "Personal Grooming", "Persuasion", "Photography/Film", "Pick Lock",
    "Pick Pocket", "Pilot Air Vehicle (x2)", "Pilot Sea Vehicle",
    "Resist Torture/Drugs", "Riding", "Sea Vehicle Tech", "Shoulder Arms",
    "Stealth", "Streetwise", "Tactics", "Tracking", "Trading",
    "Wardrobe & Style", "Wilderness Survival",
}


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

    template = _ENV.get_template("character_sheet.html.jinja")
    return template.render(
        character=character,
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
