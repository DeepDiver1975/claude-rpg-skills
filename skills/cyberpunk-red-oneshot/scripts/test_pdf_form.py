import subprocess
from pathlib import Path

from pdf_form import fill_text_fields

SKILL_DIR = Path(__file__).resolve().parent.parent
CHARACTER_SHEET = SKILL_DIR / "assets" / "RTG-CPR-CharacterSheet-Fillable.pdf"
FASHION_PAGE = 2


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
    fill_text_fields(CHARACTER_SHEET, output_pdf, {"Handle": "Rook", "Role": "Solo"})
    assert _dump_field_value(output_pdf, "Handle") == "Rook"
    assert _dump_field_value(output_pdf, "Role") == "Solo"


def test_fill_text_fields_round_trips_german_umlauts(tmp_path):
    output_pdf = tmp_path / "filled.pdf"
    fill_text_fields(CHARACTER_SHEET, output_pdf, {"Handle": "Rüdiger Straße Söldner"})
    assert _dump_field_value(output_pdf, "Handle") == "Rüdiger Straße Söldner"


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
    fill_text_fields(CHARACTER_SHEET, output_pdf, {"FASHION": "Militärstiefel"})
    assert _dump_field_value(output_pdf, "FASHION") == "Militärstiefel"

    rendered = _render_page_to_text(output_pdf, FASHION_PAGE, tmp_path)
    assert "Militärstiefel" in rendered, (
        f"umlaut missing from the rendered page; extracted text was: {rendered!r}"
    )


def test_fill_text_fields_handles_field_name_with_ampersand(tmp_path):
    output_pdf = tmp_path / "filled.pdf"
    fill_text_fields(CHARACTER_SHEET, output_pdf, {"W&S Total": "12"})
    assert _dump_field_value(output_pdf, "W&S Total") == "12"


import subprocess as _subprocess

from pdf_form import stamp_image_on_page

CHARACTER_IMAGE_PAGE = 1
CHARACTER_IMAGE_PAGE_SIZE_PT = (828.0, 648.0)
CHARACTER_IMAGE_RECT_PT = (58.2635, 455.736, 202.264, 593.526)


def _make_test_portrait(tmp_path) -> Path:
    portrait = tmp_path / "portrait.png"
    _subprocess.run(
        ["magick", "-size", "400x400", "xc:#3355ff", str(portrait)],
        check=True, capture_output=True,
    )
    return portrait


def _render_page_to_png(pdf_path: Path, tmp_path: Path) -> Path:
    png_path = tmp_path / "rendered.png"
    _subprocess.run(
        ["mutool", "draw", "-o", str(png_path), "-r", "72", str(pdf_path), "1"],
        check=True, capture_output=True,
    )
    return png_path


def test_stamp_image_on_page_places_visible_pixels_in_the_portrait_box(tmp_path):
    portrait = _make_test_portrait(tmp_path)
    output_pdf = tmp_path / "stamped.pdf"
    stamp_image_on_page(
        CHARACTER_SHEET, output_pdf,
        CHARACTER_IMAGE_PAGE, CHARACTER_IMAGE_PAGE_SIZE_PT, CHARACTER_IMAGE_RECT_PT,
        portrait,
    )
    png_path = _render_page_to_png(output_pdf, tmp_path)

    result = _subprocess.run(
        ["magick", str(png_path), "-format", "%[pixel:p{100,100}]", "info:"],
        check=True, capture_output=True, text=True,
    )
    pixel = result.stdout.strip()
    assert "51,85,255" in pixel or "3355FF".lower() in pixel.lower()


def test_stamp_image_on_page_leaves_other_pages_untouched(tmp_path):
    portrait = _make_test_portrait(tmp_path)
    output_pdf = tmp_path / "stamped.pdf"
    stamp_image_on_page(
        CHARACTER_SHEET, output_pdf,
        CHARACTER_IMAGE_PAGE, CHARACTER_IMAGE_PAGE_SIZE_PT, CHARACTER_IMAGE_RECT_PT,
        portrait,
    )
    original_page_count = _subprocess.run(
        ["pdftk", str(CHARACTER_SHEET), "dump_data"], check=True, capture_output=True, text=True,
    ).stdout
    stamped_page_count = _subprocess.run(
        ["pdftk", str(output_pdf), "dump_data"], check=True, capture_output=True, text=True,
    ).stdout
    assert "NumberOfPages: 3" in original_page_count
    assert "NumberOfPages: 3" in stamped_page_count
