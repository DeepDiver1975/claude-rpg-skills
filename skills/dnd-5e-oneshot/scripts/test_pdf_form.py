import subprocess
from pathlib import Path

from pdf_form import fill_text_fields, stamp_image_on_page

SKILL_DIR = Path(__file__).resolve().parent.parent
CHARACTER_SHEET = SKILL_DIR / "assets" / "5E_CharacterSheet_Fillable.pdf"

# Empirically confirmed (see fill_character_sheet.py's CHARACTER_IMAGE_* constants):
# page 2 holds the personal-characteristics/backstory content, including the
# portrait box; "Backstory " is a real multi-line text field on that same page,
# used below to exercise the umlaut-on-page render check.
BACKSTORY_PAGE = 2

CHARACTER_IMAGE_PAGE = 2
CHARACTER_IMAGE_PAGE_SIZE_PT = (612.0, 792.0)
CHARACTER_IMAGE_RECT_PT = (36.4791, 443.398, 199.172, 661.497)


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
    raise AssertionError(f"field {field_name!r} not found or has no value")


def test_fill_text_fields_sets_ascii_values(tmp_path):
    output_pdf = tmp_path / "filled.pdf"
    fill_text_fields(CHARACTER_SHEET, output_pdf, {"CharacterName": "Rook", "ClassLevel": "Fighter 1"})
    assert _dump_field_value(output_pdf, "CharacterName") == "Rook"
    assert _dump_field_value(output_pdf, "ClassLevel") == "Fighter 1"


def test_fill_text_fields_round_trips_german_umlauts(tmp_path):
    output_pdf = tmp_path / "filled.pdf"
    fill_text_fields(CHARACTER_SHEET, output_pdf, {"CharacterName": "Rüdiger Straße Söldner"})
    assert _dump_field_value(output_pdf, "CharacterName") == "Rüdiger Straße Söldner"


def test_fill_text_fields_handles_field_name_with_trailing_space(tmp_path):
    # Several of this sheet's real AcroForm field names carry a genuine
    # trailing space (e.g. "Race ", "Perception ") — see extract_fields.py's
    # comment on why a naive .strip() would silently break this.
    output_pdf = tmp_path / "filled.pdf"
    fill_text_fields(CHARACTER_SHEET, output_pdf, {"Race ": "Human"})
    assert _dump_field_value(output_pdf, "Race ") == "Human"


def _render_page_to_text(pdf_path: Path, page_number: int, tmp_path: Path) -> str:
    txt_path = tmp_path / f"page{page_number}.txt"
    subprocess.run(
        ["mutool", "draw", "-F", "txt", "-o", str(txt_path), str(pdf_path), str(page_number)],
        check=True, capture_output=True,
    )
    return txt_path.read_text(encoding="utf-8", errors="replace")


def test_fill_text_fields_renders_umlauts_on_the_page(tmp_path):
    # Guards against pdftk's own appearance streams silently dropping non-ASCII
    # glyphs: the stored field value stays correct, but the *printed* page shows
    # "Milit?rstiefel". Only a render-level check catches that, so this test
    # extracts the text layer of the rendered page rather than the form data.
    output_pdf = tmp_path / "filled.pdf"
    fill_text_fields(CHARACTER_SHEET, output_pdf, {"Backstory": "Ein Söldner aus Österreich, geübt im Nahkampf."})
    assert _dump_field_value(output_pdf, "Backstory") == "Ein Söldner aus Österreich, geübt im Nahkampf."

    rendered = _render_page_to_text(output_pdf, BACKSTORY_PAGE, tmp_path)
    assert "Söldner" in rendered and "Österreich" in rendered, (
        f"umlaut missing from the rendered page; extracted text was: {rendered!r}"
    )


def test_stamp_image_on_page_places_visible_pixels_in_the_portrait_box(tmp_path):
    portrait = tmp_path / "portrait.png"
    subprocess.run(["magick", "-size", "400x400", "xc:#3355ff", str(portrait)], check=True, capture_output=True)

    output_pdf = tmp_path / "stamped.pdf"
    stamp_image_on_page(
        CHARACTER_SHEET, output_pdf,
        CHARACTER_IMAGE_PAGE, CHARACTER_IMAGE_PAGE_SIZE_PT, CHARACTER_IMAGE_RECT_PT,
        portrait,
    )
    png_path = tmp_path / "rendered.png"
    subprocess.run(
        ["mutool", "draw", "-o", str(png_path), "-r", "100", str(output_pdf), str(CHARACTER_IMAGE_PAGE)],
        check=True, capture_output=True,
    )
    result = subprocess.run(
        ["magick", str(png_path), "-format", "%[pixel:p{150,300}]", "info:"],
        check=True, capture_output=True, text=True,
    )
    pixel = result.stdout.strip()
    assert "51,85,255" in pixel or "3355FF".lower() in pixel.lower()


def test_stamp_image_on_page_leaves_other_pages_untouched(tmp_path):
    portrait = tmp_path / "portrait.png"
    subprocess.run(["magick", "-size", "400x400", "xc:#3355ff", str(portrait)], check=True, capture_output=True)

    output_pdf = tmp_path / "stamped.pdf"
    stamp_image_on_page(
        CHARACTER_SHEET, output_pdf,
        CHARACTER_IMAGE_PAGE, CHARACTER_IMAGE_PAGE_SIZE_PT, CHARACTER_IMAGE_RECT_PT,
        portrait,
    )
    original = subprocess.run(
        ["pdftk", str(CHARACTER_SHEET), "dump_data"], check=True, capture_output=True, text=True,
    ).stdout
    stamped = subprocess.run(
        ["pdftk", str(output_pdf), "dump_data"], check=True, capture_output=True, text=True,
    ).stdout
    assert "NumberOfPages: 3" in original
    assert "NumberOfPages: 3" in stamped
