import re
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TERMINOLOGY = SKILL_DIR / "references" / "german-terminology.md"
CLASSES = SKILL_DIR / "references" / "classes-and-subclasses.md"
SPELLS = SKILL_DIR / "references" / "spellcasting-summary.md"


def _extract_table_rows(markdown: str, heading: str) -> list[list[str]]:
    """Return the data rows (as cell-lists) of the first Markdown table under `heading`."""
    start = markdown.index(f"## {heading}")
    rows: list[list[str]] = []
    past_separator = False
    for line in markdown[start:].splitlines()[1:]:
        if line.startswith("##"):
            break
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(set(cell) <= {"-", ":"} for cell in cells):
            past_separator = True
            continue
        if past_separator:
            rows.append(cells)
    return rows


def _flex(text: str) -> str:
    """Regex for `text` that tolerates this repo's ~80-col word-wrapping
    (a space in the source may render as a newline in the wrapped .md)."""
    return r"\s+".join(re.escape(token) for token in text.split())


def test_every_subclass_has_a_verified_german_name():
    terminology = TERMINOLOGY.read_text(encoding="utf-8")
    rows = _extract_table_rows(terminology, "The 12 Subclasses (new — previously an unverified gap)")
    assert len(rows) == 12, "expected exactly 12 subclasses (one per SRD class)"
    glossary = {english: german for _class, english, german in rows}

    classes_text = CLASSES.read_text(encoding="utf-8")
    mentions = re.findall(r"Subclass: \*\*(.+?)\*\* \(German: \*\*(.+?)\*\*\)", classes_text)
    assert len(mentions) == 12, (
        "classes-and-subclasses.md must annotate every one of the 12 subclasses "
        "with its German name inline (SKILL.md Step 5 reads this file directly)"
    )
    for english, german in mentions:
        assert english in glossary, f"{english!r} subclass missing from german-terminology.md"
        assert glossary[english] == german, (
            f"{english!r} subclass: classes-and-subclasses.md says {german!r}, "
            f"german-terminology.md says {glossary[english]!r}"
        )


def test_every_curated_spell_has_a_verified_german_name():
    terminology = TERMINOLOGY.read_text(encoding="utf-8")
    rows = _extract_table_rows(
        terminology, "The Curated Spellcasting-Summary Shortlist (new — previously an unverified gap)"
    )
    assert len(rows) >= 30, "expected the full curated spellcasting shortlist"

    spells_text = SPELLS.read_text(encoding="utf-8")
    missing = []
    for english, german in rows:
        pattern = f"{_flex(german)}/{_flex(english)}\\b"
        if not re.search(pattern, spells_text):
            missing.append(english)
    assert not missing, (
        f"spellcasting-summary.md is missing a German/English pairing (as "
        f"'<German>/<English>') for: {missing} — a future SRD update that adds a "
        f"spell without updating both files should fail here, not silently ship "
        f"an English spell name in German-facing output"
    )
