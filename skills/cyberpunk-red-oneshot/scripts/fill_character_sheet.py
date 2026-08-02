#!/usr/bin/env python3
"""Fill an official Cyberpunk RED Core Character Sheet PDF from a character JSON file."""
import argparse
import json
import tempfile
from pathlib import Path

from pdf_form import fill_text_fields, stamp_image_on_page

SKILL_DIR = Path(__file__).resolve().parent.parent
BLANK_SHEET = SKILL_DIR / "assets" / "RTG-CPR-CharacterSheet-Fillable.pdf"
SKILLS_FIELD_MAP = json.loads(
    (SKILL_DIR / "assets" / "skills_field_map.json").read_text(encoding="utf-8")
)

CHARACTER_IMAGE_PAGE = 1
CHARACTER_IMAGE_PAGE_SIZE_PT = (828.0, 648.0)
CHARACTER_IMAGE_RECT_PT = (58.2635, 455.736, 202.264, 593.526)


def build_field_values(character: dict) -> dict[str, str]:
    values: dict[str, str] = {
        "Handle": character["handle"],
        "Role": character["role"],
        "Role Ability": character["role_ability"],
        "Role Ability Rank": str(character["role_ability_rank"]),
        "Current HP": str(character["hp"]["current"]),
        "Max HP": str(character["hp"]["max"]),
        "Current Humanity": str(character["humanity"]["current"]),
        "Max Humanity": str(character["humanity"]["max"]),
        "LUCK CURRENT": str(character["luck"]["current"]),
        "LUCK MAX": str(character["luck"]["max"]),
        "FASHION": character["fashion"],
        "ROLE SPECIFIC LIFEPATH": character["role_specific_lifepath"],
        "Notes": character["notes"],
    }
    for stat_name, stat_value in character["stats"].items():
        if stat_name == "LUCK":
            # LUCK has no bare field on the sheet — only "LUCK CURRENT"/"LUCK MAX"
            # exist (set above from character["luck"]); skip it here rather than
            # writing a value pdftk would just silently discard.
            continue
        values[stat_name] = str(stat_value)

    for skill_name, level in character["skills"].items():
        field_name = SKILLS_FIELD_MAP.get(skill_name)
        if field_name is None:
            raise ValueError(
                f"skill {skill_name!r} has no entry in skills_field_map.json — "
                "add it (Task 9) before filling a sheet that uses it"
            )
        values[field_name] = str(level)

    for i, weapon in enumerate(character["weapons"], start=1):
        values[f"WEAPONRow{i}"] = weapon["name"]
        values[f"DMGRow{i}"] = weapon["dmg"]
        values[f"AMMORow{i}"] = weapon["ammo"]
        values[f"ROFRow{i}"] = weapon["rof"]
        values[f"NOTESRow{i}"] = weapon.get("notes", "")

    for location, field_prefix in (("head", "Head"), ("body", "Body"), ("shield", "Shield")):
        armor = character["armor"][location]
        values[f"SP{field_prefix}"] = str(armor["sp"])
        values[f"PENALTY{field_prefix}"] = str(armor["penalty"])

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
