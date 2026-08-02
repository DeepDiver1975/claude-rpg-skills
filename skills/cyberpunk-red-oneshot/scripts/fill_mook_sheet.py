#!/usr/bin/env python3
"""Fill an official Cyberpunk RED Mook Sheet PDF from an NPC/enemy JSON file."""
import argparse
import json
from pathlib import Path

from pdf_form import fill_text_fields

SKILL_DIR = Path(__file__).resolve().parent.parent
BLANK_SHEET = SKILL_DIR / "assets" / "RTG-CPR-MooksSheetFormFillable.pdf"


def build_field_values(mook: dict) -> dict[str, str]:
    values: dict[str, str] = {
        "Name": mook["name"],
        "Hit Points": str(mook["hit_points"]),
        "Seriously Wounded": str(mook["seriously_wounded"]),
        "Death Save": str(mook["death_save"]),
        "Skill Bases": mook["skill_bases"],
        "Armor Type": mook["armor_type"],
        "Head SP": str(mook["head_sp"]),
        "Body SP": str(mook["body_sp"]),
        "Cyberware & Special Equipment": mook["cyberware_special_equipment"],
    }
    for stat_name, stat_value in mook["stats"].items():
        values[stat_name] = str(stat_value)

    for i, weapon in enumerate(mook["weapons"], start=1):
        values[f"Weapon {i}"] = weapon["name"]
        values[f"Damage {i}"] = weapon["damage"]

    return values


def fill_mook_sheet(mook_json_path: Path, output_pdf: Path) -> None:
    mook = json.loads(Path(mook_json_path).read_text(encoding="utf-8"))
    values = build_field_values(mook)
    fill_text_fields(BLANK_SHEET, output_pdf, values)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mook_json", type=Path)
    parser.add_argument("output_pdf", type=Path)
    args = parser.parse_args()
    fill_mook_sheet(args.mook_json, args.output_pdf)
    print(f"wrote {args.output_pdf}")


if __name__ == "__main__":
    main()
