import json
import subprocess
from pathlib import Path

from fill_character_sheet import build_field_values, fill_character_sheet

SKILL_DIR = Path(__file__).resolve().parent.parent
FIXTURE = SKILL_DIR / "scripts" / "fixtures" / "sample_character.json"


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


def test_build_field_values_maps_skills_through_the_field_map():
    character = json.loads(FIXTURE.read_text(encoding="utf-8"))
    values = build_field_values(character)
    assert values["Handle"] == 'Rüdiger "Rook" Straße'
    assert values["Role"] == "Solo"
    assert values["LVLAthletics DEX"] == "4"
    assert values["LVLShoulder Arms REF"] == "6"
    assert values["Current HP"] == "35"
    assert values["Max HP"] == "35"


def test_fill_character_sheet_produces_a_readable_pdf_with_correct_values(tmp_path):
    output_pdf = tmp_path / "character.pdf"
    fill_character_sheet(FIXTURE, output_pdf)
    assert output_pdf.exists()
    assert _dump_field_value(output_pdf, "Handle") == 'Rüdiger "Rook" Straße'
    assert _dump_field_value(output_pdf, "LVLShoulder Arms REF") == "6"


def _page_count(pdf_path: Path) -> int:
    dump = subprocess.run(
        ["pdftk", str(pdf_path), "dump_data"], check=True, capture_output=True, text=True,
    ).stdout
    line = next(l for l in dump.splitlines() if l.startswith("NumberOfPages"))
    return int(line.split(":")[1].strip())


def _render_page_to_text(pdf_path: Path, page_number: int, tmp_path: Path) -> str:
    txt_path = tmp_path / f"page{page_number}.txt"
    subprocess.run(
        ["mutool", "draw", "-F", "txt", "-o", str(txt_path), str(pdf_path), str(page_number)],
        check=True, capture_output=True,
    )
    return txt_path.read_text(encoding="utf-8", errors="replace")


def test_fill_character_sheet_with_a_portrait_keeps_values_and_page_count(tmp_path):
    # Exercises the portrait branch — the fixture leaves portrait_image_path
    # null, so without this test that code path is never run. It also guards the
    # ordering of the two pdftk steps: stamping after filling would strip the
    # AcroForm NeedAppearances flag and re-break umlauts on the printed page.
    portrait = tmp_path / "portrait.png"
    subprocess.run(
        ["magick", "-size", "400x600", "xc:#3355ff", str(portrait)],
        check=True, capture_output=True,
    )
    character = json.loads(FIXTURE.read_text(encoding="utf-8"))
    character["portrait_image_path"] = str(portrait)
    character_json = tmp_path / "character.json"
    character_json.write_text(json.dumps(character, ensure_ascii=False), encoding="utf-8")

    output_pdf = tmp_path / "character.pdf"
    fill_character_sheet(character_json, output_pdf)

    assert output_pdf.exists()
    assert _dump_field_value(output_pdf, "Handle") == 'Rüdiger "Rook" Straße'
    assert _dump_field_value(output_pdf, "LVLShoulder Arms REF") == "6"
    assert _page_count(output_pdf) == 3

    rendered = _render_page_to_text(output_pdf, 2, tmp_path)
    assert "Militärstiefel" in rendered, (
        f"umlaut missing from the rendered page of a portrait sheet: {rendered!r}"
    )

    portrait_png = tmp_path / "rendered.png"
    subprocess.run(
        ["mutool", "draw", "-o", str(portrait_png), "-r", "72", str(output_pdf), "1"],
        check=True, capture_output=True,
    )
    pixel = subprocess.run(
        ["magick", str(portrait_png), "-format", "%[pixel:p{100,100}]", "info:"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    assert "51,85,255" in pixel, f"portrait not visible in the portrait box: {pixel}"
