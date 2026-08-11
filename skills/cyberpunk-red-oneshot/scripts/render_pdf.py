"""Shared helpers: render a self-contained HTML document string to a PDF file,
and base64-encode local files (fonts, portraits) as embeddable data: URIs.
"""
import base64
import re
from pathlib import Path

from weasyprint import HTML

_FONT_PLACEHOLDER_RE = re.compile(r"__FONT:([\w.\-]+)__")


def data_uri(path: Path, mime_type: str) -> str:
    """Read `path` and return it as a `data:<mime_type>;base64,...` URI.

    `mime_type` is caller-supplied rather than guessed from the file extension —
    the guess depends on the host's system MIME database, which isn't
    guaranteed consistent across the machines this skill runs on.
    """
    encoded = base64.b64encode(Path(path).read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def load_css_with_fonts(css_path: Path, fonts_dir: Path) -> str:
    """Read `css_path` and inline every bundled font file it references as a
    data: URI. Its @font-face rules reference fonts as
    `src: url("__FONT:<filename>__")`; each placeholder is replaced with that
    exact file's contents from `fonts_dir`.
    """
    css = Path(css_path).read_text(encoding="utf-8")
    return _FONT_PLACEHOLDER_RE.sub(
        lambda m: data_uri(fonts_dir / m.group(1), "font/ttf"), css
    )


def load_themed_css(structure_css_path: Path, theme_css_path: Path, fonts_dir: Path) -> str:
    """Compose the structural stylesheet with a theme stylesheet and inline every
    bundled font both reference.

    The structure file lays out the sheet in terms of theme tokens; the theme
    file supplies the run's palette (`:root` token values), its display
    `@font-face`, and any per-preset treatment overrides (e.g. a different
    `.hazard-stripe`). The theme is concatenated **last** so those overrides win
    the cascade over the structural defaults — `:root` custom properties and
    `@font-face` are order-independent, so appending the theme costs nothing
    there. Font placeholders (`__FONT:<filename>__`) in either file are inlined
    from `fonts_dir` exactly as `load_css_with_fonts` does.
    """
    combined = (
        Path(structure_css_path).read_text(encoding="utf-8")
        + "\n"
        + Path(theme_css_path).read_text(encoding="utf-8")
    )
    return _FONT_PLACEHOLDER_RE.sub(
        lambda m: data_uri(fonts_dir / m.group(1), "font/ttf"), combined
    )


def render_html_to_pdf(html: str, output_pdf: Path) -> None:
    """Render `html` to `output_pdf` via WeasyPrint.

    `html` must be fully self-contained — stylesheet inlined via a <style> tag,
    fonts embedded via @font-face src: url(data:...), portrait embedded as an
    <img src="data:..."> — so no base_url or filesystem access is needed here.
    """
    HTML(string=html).write_pdf(str(output_pdf))
