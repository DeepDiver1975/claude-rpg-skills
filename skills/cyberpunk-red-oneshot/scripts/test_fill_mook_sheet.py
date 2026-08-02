import json
import subprocess
from pathlib import Path

from fill_mook_sheet import build_field_values, fill_mook_sheet

SKILL_DIR = Path(__file__).resolve().parent.parent
FIXTURE = SKILL_DIR / "scripts" / "fixtures" / "sample_mook.json"


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
    return ""


def test_build_field_values_maps_the_mook_schema():
    mook = json.loads(FIXTURE.read_text(encoding="utf-8"))
    values = build_field_values(mook)
    assert values["Name"] == "Corp-Wachmann"
    assert values["Hit Points"] == "20"
    assert values["Weapon 1"] == "Medium Pistol"
    assert values["Damage 1"] == "2d6"
    assert values["Weapon 2"] == "Schlagstock"


def test_fill_mook_sheet_produces_a_readable_pdf_with_correct_values(tmp_path):
    output_pdf = tmp_path / "mook.pdf"
    fill_mook_sheet(FIXTURE, output_pdf)
    assert output_pdf.exists()
    assert _dump_field_value(output_pdf, "Name") == "Corp-Wachmann"
    assert _dump_field_value(output_pdf, "Body SP") == "8"
