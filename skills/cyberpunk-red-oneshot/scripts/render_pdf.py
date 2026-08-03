"""Shared helpers: render a self-contained HTML document string to a PDF file,
and base64-encode local files (fonts, portraits) as embeddable data: URIs.
"""
import base64
from pathlib import Path

from weasyprint import HTML


def data_uri(path: Path, mime_type: str) -> str:
    """Read `path` and return it as a `data:<mime_type>;base64,...` URI.

    `mime_type` is caller-supplied rather than guessed from the file extension —
    the guess depends on the host's system MIME database, which isn't
    guaranteed consistent across the machines this skill runs on.
    """
    encoded = base64.b64encode(Path(path).read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def load_css_with_fonts(css_path: Path, fonts_dir: Path) -> str:
    """Read `css_path` and inline the bundled Noto Sans font files as data:
    URIs in place of the `__FONT_REGULAR_DATA_URI__` / `__FONT_BOLD_DATA_URI__`
    placeholders its @font-face rules use.
    """
    css = Path(css_path).read_text(encoding="utf-8")
    css = css.replace(
        "__FONT_REGULAR_DATA_URI__", data_uri(fonts_dir / "NotoSans-Regular.ttf", "font/ttf")
    )
    css = css.replace(
        "__FONT_BOLD_DATA_URI__", data_uri(fonts_dir / "NotoSans-Bold.ttf", "font/ttf")
    )
    return css


def render_html_to_pdf(html: str, output_pdf: Path) -> None:
    """Render `html` to `output_pdf` via WeasyPrint.

    `html` must be fully self-contained — stylesheet inlined via a <style> tag,
    fonts embedded via @font-face src: url(data:...), portrait embedded as an
    <img src="data:..."> — so no base_url or filesystem access is needed here.
    """
    HTML(string=html).write_pdf(str(output_pdf))
