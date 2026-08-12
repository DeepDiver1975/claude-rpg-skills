#!/usr/bin/env python3
"""Pull page-ranged raw text for each SRD section out of the official German SRD PDF.

This is the deterministic *text-pull* half of the hybrid extraction flow (same
shape as the Cyberpunk RED skill's `extract_rules.py`): it turns the official
German System Reference Document 5.2.1 PDF into per-section raw-text files
under this skill's `data/raw/` directory. Structuring that raw text into the
skill's `references/*.md` files is done by the skill (Claude) reading these
files against `references/extraction-map-de.md`.

Unlike the Cyberpunk RED extraction (a paid book, never redistributed), the
German SRD 5.2.1 is released by Wizards of the Coast LLC under CC BY 4.0 — the
same license already covering this skill's English `references/*.md`. This
script's `data/` output still stays local/gitignored (it's an unreviewed raw
text dump, not the curated attributed summary meant for redistribution), but
there's no ownership gate: any GM can download the official PDF and run this.
A write-guard still restricts output to `data/`, matching the CPR pattern.
"""
import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
MANIFEST = DATA_DIR / "manifest.json"
TOOL_VERSION = "1"

# Facts-only section map: heading text as it appears in the PDF text layer, plus
# the printed (book) page range from the SRD's own Inhalt (Contents). Confirmed
# empirically: this PDF's physical page numbers equal its printed page numbers
# (no cover-page offset, unlike CPR's rulebook), so DEFAULT_OFFSET is 0 — kept
# as a parameter (with a small search window) for robustness against future
# SRD point releases that might reflow the front matter. Human/schema-facing
# companion: references/extraction-map-de.md.
SECTIONS = [
    {"name": "core-rules",       "heading": "Die Spielregeln",       "start": 5,   "end": 21},
    {"name": "classes",          "heading": "Klassen",               "start": 33,  "end": 92},
    {"name": "origins",          "heading": "Charakterherkunft",     "start": 93,  "end": 97},
    {"name": "equipment",        "heading": "Ausrüstung",            "start": 101, "end": 117},
    {"name": "spells",           "heading": "Zauber",                "start": 118, "end": 202},
    {"name": "rules-glossary",   "heading": "Regelglossar",          "start": 203, "end": 221},
    {"name": "monster-overview", "heading": "Monster",               "start": 295, "end": 299},
]
SECTION_BY_NAME = {s["name"]: s for s in SECTIONS}

# Default guess for printed->PDF page offset, used to centre the heading search.
DEFAULT_OFFSET = 0
# How far on each side of the expected page to scan for the heading.
SEARCH_WINDOW = 5
# Extra pages appended past the computed end, so a section is never truncated.
END_MARGIN = 2


class WriteGuardError(Exception):
    """Raised when a write target escapes the data/ sandbox."""


def ensure_within_data(path: Path) -> Path:
    """Repo hygiene: refuse to write anywhere outside the skill's data/ dir."""
    resolved = path.resolve()
    if resolved != DATA_DIR.resolve() and DATA_DIR.resolve() not in resolved.parents:
        raise WriteGuardError(f"refusing to write outside data/: {resolved}")
    return resolved


def page_text(pdf_path: Path, first: int, last: int) -> str:
    result = subprocess.run(
        ["pdftotext", "-f", str(first), "-l", str(last), str(pdf_path), "-"],
        check=True, capture_output=True, text=True,
    )
    return result.stdout


def pdf_page_count(pdf_path: Path) -> int:
    result = subprocess.run(
        ["pdfinfo", str(pdf_path)], check=True, capture_output=True, text=True,
    )
    for line in result.stdout.splitlines():
        if line.lower().startswith("pages:"):
            return int(line.split(":", 1)[1].strip())
    raise RuntimeError("could not read page count from pdfinfo")


def heading_on_page(text: str, heading: str) -> bool:
    """True if `heading` appears as its own line (case-insensitive) in `text`."""
    target = heading.strip().casefold()
    return any(line.strip().casefold() == target for line in text.splitlines())


def resolve_start_page(pdf_path: Path, section: dict, offset: int, page_count: int) -> int:
    """Find the PDF page where the section heading actually starts.

    Searches a window around (printed start + offset). Falls back to the naive
    offset if the heading line isn't found (some headings are stylised art).
    """
    centre = section["start"] + offset
    lo = max(1, centre - SEARCH_WINDOW)
    hi = min(page_count, centre + SEARCH_WINDOW)
    for page in range(lo, hi + 1):
        if heading_on_page(page_text(pdf_path, page, page), section["heading"]):
            return page
    return min(max(1, centre), page_count)


def extract_section(pdf_path: Path, section: dict, offset: int, page_count: int) -> dict:
    start_pdf = resolve_start_page(pdf_path, section, offset, page_count)
    # A heading can match a chapter-opener/art page that sits several pages ahead
    # of the real content, yielding a too-small self-calibrated offset. Take the
    # larger of that and the default guess (plus a margin) for the end so a section
    # is never truncated — over-extraction is harmless since the skill trims when
    # structuring, truncation silently loses rules.
    actual_offset = start_pdf - section["start"]
    end_pdf = section["end"] + max(actual_offset, offset) + END_MARGIN
    end_pdf = min(page_count, max(end_pdf, start_pdf))  # cap + guard inversion

    text = page_text(pdf_path, start_pdf, end_pdf)
    out_path = ensure_within_data(RAW_DIR / f"{section['name']}.txt")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")

    return {
        "heading": section["heading"],
        "printed_pages": [section["start"], section["end"]],
        "pdf_pages": [start_pdf, end_pdf],
        "chars": len(text),
        "raw_file": str(out_path.relative_to(DATA_DIR)),
    }


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_manifest(pdf_path: Path, results: dict[str, dict]) -> None:
    manifest = {
        "tool_version": TOOL_VERSION,
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "source_pdf": pdf_path.name,
        "source_sha256": sha256(pdf_path),
        "source_license": "CC BY 4.0 (System Reference Document 5.2.1, Wizards of the Coast LLC)",
        "sections": results,
    }
    ensure_within_data(MANIFEST)
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def run(pdf_path: Path, section_names: list[str], offset: int) -> dict[str, dict]:
    page_count = pdf_page_count(pdf_path)
    results: dict[str, dict] = {}
    for name in section_names:
        section = SECTION_BY_NAME[name]
        info = extract_section(pdf_path, section, offset, page_count)
        results[name] = info
        print(
            f"{name}: PDF pages {info['pdf_pages'][0]}-{info['pdf_pages'][1]} "
            f"({info['chars']} chars) -> data/{info['raw_file']}"
        )
    write_manifest(pdf_path, results)
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path, help="path to the official German SRD 5.2.1 PDF")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true", help="extract every mapped section")
    group.add_argument(
        "--section", action="append", metavar="NAME",
        help=f"extract one section (repeatable); one of: {', '.join(SECTION_BY_NAME)}",
    )
    parser.add_argument(
        "--offset", type=int, default=DEFAULT_OFFSET,
        help="printed->PDF page offset guess used to centre the heading search "
             f"(default {DEFAULT_OFFSET}; auto-calibrated per section)",
    )
    args = parser.parse_args()

    if not args.pdf.is_file():
        print(f"PDF not found: {args.pdf}", file=sys.stderr)
        raise SystemExit(1)

    names = list(SECTION_BY_NAME) if args.all else args.section
    unknown = [n for n in names if n not in SECTION_BY_NAME]
    if unknown:
        print(f"unknown section(s): {', '.join(unknown)}", file=sys.stderr)
        raise SystemExit(2)

    run(args.pdf, names, args.offset)
    print(f"\nwrote {len(names)} section(s) + manifest under {DATA_DIR}")
    print("Next: the skill reads data/raw/*.txt and writes references/*.md.")


if __name__ == "__main__":
    main()
