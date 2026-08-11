#!/usr/bin/env python3
"""Pull page-ranged raw text for each rules section out of a user-owned CPR PDF.

This is the deterministic *text-pull* half of the hybrid extraction flow: it turns
the owner's core-rulebook PDF into per-section raw-text files under the skill's
`data/raw/` directory. Structuring that raw text into `data/<domain>.json` is done
by the skill (Claude) reading these files against `references/extraction-map.md`.

Copyright: the input PDF and everything written under `data/` are derived from
R. Talsorian's paid core rulebook. They are for the owner's personal use of a book
they possess and must never be committed or redistributed. A write-guard enforces
that this tool only ever writes inside `data/`.
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
# the printed (book) page range from the rulebook's Contents. Printed pages differ
# from physical PDF pages by a near-constant offset (~+9); the offset is calibrated
# per section by locating `heading` near the expected page, so these stay robust to
# reflow. Human/schema-facing companion: references/extraction-map.md.
SECTIONS = [
    {"name": "roles",             "heading": "Roles",                         "start": 29,  "end": 40},
    {"name": "statistics",        "heading": "What are Statistics?",          "start": 72,  "end": 81},
    {"name": "weapons-armor",     "heading": "Weapons and Armor",             "start": 91,  "end": 99},
    {"name": "gear",              "heading": "Your Outfit",                   "start": 99,  "end": 107},
    {"name": "cyberware",         "heading": "Cyberware",                     "start": 110, "end": 121},
    {"name": "difficulty-values", "heading": "Resolving Actions with Skills", "start": 128, "end": 130},
    {"name": "skills",            "heading": "Skill List",                    "start": 130, "end": 142},
    {"name": "role-abilities",    "heading": "Role Abilities",                "start": 142, "end": 167},
    {"name": "combat",            "heading": "Friday Night Firefight",        "start": 167, "end": 189},
    {"name": "vehicles",          "heading": "Vehicle Combat",                "start": 189, "end": 193},
    {"name": "netrunning",        "heading": "Netrunning",                    "start": 195, "end": 219},
    {"name": "critical-injuries", "heading": "Wound States and Critical Injuries", "start": 220, "end": 227},
    {"name": "drugs",             "heading": "Street Drugs",                  "start": 227, "end": 230},
]
SECTION_BY_NAME = {s["name"]: s for s in SECTIONS}

# Default guess for printed->PDF page offset, used to centre the heading search.
DEFAULT_OFFSET = 9
# How far on each side of the expected page to scan for the heading.
SEARCH_WINDOW = 12
# Extra pages appended past the computed end, so a section is never truncated.
END_MARGIN = 2


class WriteGuardError(Exception):
    """Raised when a write target escapes the data/ sandbox."""


def ensure_within_data(path: Path) -> Path:
    """Copyright safety: refuse to write anywhere outside the skill's data/ dir."""
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
    parser.add_argument("pdf", type=Path, help="path to your owned CPR core-rulebook PDF")
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
    print("Next: the skill reads data/raw/*.txt and writes data/<domain>.json.")


if __name__ == "__main__":
    main()
