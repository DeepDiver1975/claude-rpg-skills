"""Shared helpers for filling CPR PDF forms and stamping portrait images onto them."""
import subprocess
import tempfile
from pathlib import Path


def _fdf_hex(value: str) -> str:
    # UTF-16BE hex encoding with BOM (FE FF) to ensure proper interpretation
    return "FEFF" + value.encode("utf-16-be").hex().upper()


def fill_text_fields(input_pdf: Path, output_pdf: Path, values: dict[str, str]) -> None:
    """Fill AcroForm text fields on input_pdf, writing the result to output_pdf.

    Both field names and values are UTF-16BE hex-encoded in the generated FDF, so
    German umlauts/eszett and field names containing "&" or other special
    characters round-trip correctly without manual escaping.

    `need_appearances` is passed to pdftk so viewers/renderers regenerate the
    field appearance streams themselves. Without it pdftk builds the appearance
    streams and silently drops non-ASCII glyphs (ä/ö/ü vanish from the printed
    page on several fields, e.g. FASHION) even though the stored field value is
    correct — see test_fill_text_fields_renders_umlauts_on_the_page.
    """
    entries = "\n".join(
        f"<</T<{_fdf_hex(name)}>/V<{_fdf_hex(value)}>>>"
        for name, value in values.items()
    )
    fdf = (
        "%FDF-1.2\n"
        "1 0 obj<</FDF<</Fields[\n"
        f"{entries}\n"
        "]>>>>\n"
        "endobj\n"
        "trailer<</Root 1 0 R>>\n"
        "%%EOF\n"
    )
    with tempfile.TemporaryDirectory() as tmp:
        fdf_path = Path(tmp) / "data.fdf"
        fdf_path.write_text(fdf, encoding="latin1")
        subprocess.run(
            [
                "pdftk", str(input_pdf), "fill_form", str(fdf_path),
                "output", str(output_pdf), "need_appearances",
            ],
            check=True, capture_output=True,
        )


def stamp_image_on_page(
    input_pdf: Path,
    output_pdf: Path,
    page_number: int,
    page_size_pt: tuple[float, float],
    rect_pt: tuple[float, float, float, float],
    image_path: Path,
) -> None:
    """Composite image_path into rect_pt on the given 1-based page_number of input_pdf.

    Other pages are left untouched. rect_pt is (x0, y0, x1, y1) in PDF coordinates
    (origin bottom-left), matching a pdftk-reported AcroForm widget /Rect. Uses
    ImageMagick to build a transparent same-size overlay page at 72 DPI (so pixels
    equal points), then pdftk `stamp` (composites on top of existing page content —
    `background` composites underneath and is invisible behind this sheet's opaque
    portrait-box artwork).
    """
    page_w, page_h = page_size_pt
    x0, y0, x1, y1 = rect_pt
    box_w, box_h = x1 - x0, y1 - y0
    top_left_x, top_left_y = x0, page_h - y1

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        overlay_pdf = tmp_path / "overlay.pdf"
        subprocess.run(
            [
                "magick", "-size", f"{int(page_w)}x{int(page_h)}", "xc:none",
                "(", str(image_path),
                # Crop-to-fill, not stretch-to-fit: "^" scales so the image covers
                # the box while keeping its aspect ratio, then a centred -extent
                # crops it to the exact box. Using "!" here would squash a
                # non-square portrait into this near-square box and distort faces.
                "-resize", f"{int(box_w)}x{int(box_h)}^",
                "-gravity", "center", "-extent", f"{int(box_w)}x{int(box_h)}",
                ")",
                # reset gravity so the -geometry offset below stays top-left based
                "-gravity", "none",
                "-geometry", f"+{int(top_left_x)}+{int(top_left_y)}",
                "-compose", "over", "-composite",
                "-units", "PixelsPerInch", "-density", "72",
                str(overlay_pdf),
            ],
            check=True, capture_output=True,
        )

        page_pdf = tmp_path / "page.pdf"
        subprocess.run(
            ["pdftk", str(input_pdf), "cat", str(page_number), "output", str(page_pdf)],
            check=True, capture_output=True,
        )
        stamped_pdf = tmp_path / "page_stamped.pdf"
        subprocess.run(
            ["pdftk", str(page_pdf), "stamp", str(overlay_pdf), "output", str(stamped_pdf)],
            check=True, capture_output=True,
        )

        dump = subprocess.run(
            ["pdftk", str(input_pdf), "dump_data"], check=True, capture_output=True, text=True,
        ).stdout
        total_pages = int(
            next(line for line in dump.splitlines() if line.startswith("NumberOfPages"))
            .split(":")[1].strip()
        )

        parts = []
        if page_number > 1:
            before_pdf = tmp_path / "before.pdf"
            subprocess.run(
                ["pdftk", str(input_pdf), "cat", f"1-{page_number - 1}", "output", str(before_pdf)],
                check=True, capture_output=True,
            )
            parts.append(before_pdf)
        parts.append(stamped_pdf)
        if page_number < total_pages:
            after_pdf = tmp_path / "after.pdf"
            subprocess.run(
                ["pdftk", str(input_pdf), "cat", f"{page_number + 1}-end", "output", str(after_pdf)],
                check=True, capture_output=True,
            )
            parts.append(after_pdf)

        labels = "ABCDEFGH"[: len(parts)]
        cat_args = [f"{label}={part}" for label, part in zip(labels, parts)]
        subprocess.run(
            ["pdftk", *cat_args, "cat", *labels, "output", str(output_pdf)],
            check=True, capture_output=True,
        )
