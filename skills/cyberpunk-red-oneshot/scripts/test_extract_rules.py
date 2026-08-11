from pathlib import Path

import pytest

import extract_rules
from extract_rules import (
    SECTION_BY_NAME,
    WriteGuardError,
    ensure_within_data,
    heading_on_page,
    resolve_start_page,
)

SKILL_DIR = Path(__file__).resolve().parent.parent
COREBOOK = SKILL_DIR / "assets" / "cpr-corebook.pdf"


def test_heading_on_page_matches_own_line():
    text = "some flavor text\nWeapons and Armor\nfor Complete Package Characters"
    assert heading_on_page(text, "Weapons and Armor")


def test_heading_on_page_is_case_insensitive():
    assert heading_on_page("skill list\n", "Skill List")


def test_heading_on_page_ignores_inline_mentions():
    # The words appear, but not as a standalone heading line.
    text = "you consult the Skill List when making a check"
    assert not heading_on_page(text, "Skill List")


def test_write_guard_allows_data_dir():
    target = extract_rules.RAW_DIR / "weapons-armor.txt"
    assert ensure_within_data(target) == target.resolve()


def test_write_guard_rejects_outside_data(tmp_path):
    with pytest.raises(WriteGuardError):
        ensure_within_data(tmp_path / "escape.txt")


def test_write_guard_rejects_tracked_references(tmp_path):
    # A path that traverses back into the committed tree must be refused.
    with pytest.raises(WriteGuardError):
        ensure_within_data(SKILL_DIR / "references" / "leaked.json")


def test_resolve_start_page_finds_heading_via_search(monkeypatch):
    section = SECTION_BY_NAME["skills"]  # printed start 130
    # Heading actually renders 11 pages after printed start (offset 11, not the
    # default 9) — resolver must still find it inside the search window.
    heading_pdf_page = section["start"] + 11

    def fake_page_text(pdf_path, first, last):
        return "Skill List\n" if first == heading_pdf_page else "body text\n"

    monkeypatch.setattr(extract_rules, "page_text", fake_page_text)
    found = resolve_start_page(Path("dummy.pdf"), section, extract_rules.DEFAULT_OFFSET, 500)
    assert found == heading_pdf_page


def test_resolve_start_page_falls_back_to_offset(monkeypatch):
    section = SECTION_BY_NAME["cyberware"]

    monkeypatch.setattr(extract_rules, "page_text", lambda *a: "no heading here\n")
    found = resolve_start_page(Path("dummy.pdf"), section, extract_rules.DEFAULT_OFFSET, 500)
    assert found == section["start"] + extract_rules.DEFAULT_OFFSET


@pytest.mark.skipif(not COREBOOK.exists(), reason="user-owned core rulebook PDF not present")
def test_real_extraction_writes_raw_and_manifest():
    results = extract_rules.run(COREBOOK, ["weapons-armor"], extract_rules.DEFAULT_OFFSET)
    raw = extract_rules.DATA_DIR / results["weapons-armor"]["raw_file"]
    assert raw.exists() and raw.stat().st_size > 0
    assert extract_rules.MANIFEST.exists()
