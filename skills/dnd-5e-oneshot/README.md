# One-Shot Generator — a Claude Code skill for use with D&D 5e (2024 rules)

A [Claude Code](https://claude.com/claude-code) skill that generates a
complete, ready-to-run one-shot session for D&D 5e (2024 rules): pregenerated
level 1 characters as filled official character sheet PDFs (with portraits),
a linear scenario with GM notes, NPC/monster Markdown stat blocks, and a
consistent set of image-generation prompts. See [`SKILL.md`](SKILL.md) for
the full process the skill follows.

Rules content is sourced from the official **System Reference Document 5.2.1
("SRD 5.2.1")**, released by Wizards of the Coast LLC under the
[Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/)
— a complete, official ruleset, not a hobbyist's best-effort summary of
scattered free web pages. See each file under
[`references/`](references/) for exact sourcing and attribution. Anything a
one-shot needs that falls outside SRD 5.2.1's scope (a non-SRD subclass,
feat, spell, or monster) is flagged explicitly by the skill rather than
invented — see `SKILL.md`'s Step 10.

## Not affiliated with Wizards of the Coast

This is unofficial, fan-made content. It is not affiliated with, endorsed
by, or reviewed by Wizards of the Coast. Dungeons & Dragons, D&D, Wizards of
the Coast, and their logos are trademarks of Wizards of the Coast LLC.

**This repository does not include Wizards of the Coast's official
character sheet PDF** — see Setup below for how to obtain it yourself,
directly from Wizards of the Coast, before using this skill.

## Setup

### 1. Get the official fillable character sheet PDF

Download this file yourself and save it at this **exact filename**, since
the scripts reference it directly:

- `assets/5E_CharacterSheet_Fillable.pdf` — from
  <https://media.wizards.com/2016/dnd/downloads/5E_CharacterSheet_Fillable.pdf>

This is the 2014-rules character sheet layout — it's the only official D&D
5e character sheet PDF that's a genuine fillable AcroForm (the newer
2024-rules PDF has no real form fields, only Acrobat "Fill & Sign" support,
which this skill's `pdftk`-based pipeline can't drive). `fill_character_sheet.py`
maps 2024/SRD-5.2.1 character data onto this sheet's field names; see
`SKILL.md`'s "Known constraint" notes for the practical implications (e.g. a
2024 "Species" value is written into the sheet's own field literally named
`Race `).

### 2. (Optional) Get the official German SRD PDF, to re-verify/extend terminology

This skill's German output already uses official terms — every entry in
`references/german-terminology.md` was sourced from the official German
translation of the SRD and is committed to this repo (see
`references/extraction-map-de.md` for provenance). You only need this step
if you want to re-run or extend that extraction (e.g. to cover a spell
outside the curated shortlist, or re-verify after a future SRD point
release):

- `assets/DE_SRD_CC_v5.2.1.pdf` — from
  <https://media.dndbeyond.com/compendium-images/srd/5.2/DE_SRD_CC_v5.2.1.pdf>,
  released by Wizards of the Coast LLC under
  [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Freely
  downloadable — no ownership gate, unlike the Cyberpunk RED skill's paid
  core rulebook.

Then run:

```bash
python3 scripts/extract_srd_de.py assets/DE_SRD_CC_v5.2.1.pdf --all
```

This writes page-ranged raw text into `data/raw/*.txt` (gitignored — an
unreviewed extraction scratch, not meant for redistribution). Read those
files against `references/extraction-map-de.md` to update
`references/german-terminology.md`, `classes-and-subclasses.md`, or
`spellcasting-summary.md`.

### 4. Install requirements

- `pdftk` — PDF form filling
- ImageMagick (`magick`/`convert`) — portrait image compositing
- `mutool` (from `mupdf-tools`) — used by the test suite to verify rendering
- `pdftotext`/`pdfinfo` (from `poppler-utils`) — only needed for step 2's
  extraction script
- Python 3 and `pytest` (stdlib only otherwise — no PyPI packages required)

### 5. Install the skill

```bash
ln -s "$(pwd)/skills/dnd-5e-oneshot" ~/.claude/skills/dnd-5e-oneshot
```

Then invoke `/dnd-5e-oneshot` in Claude Code.

## Running the tests

```bash
cd scripts
pytest -v
```

33 tests total. Most of them fill and render the real character sheet PDF,
so they'll fail until step 1 above is done — that's expected, not a bug.
The two `test_terminology_de.py` tests don't need any PDF; they just check
that `references/classes-and-subclasses.md` and
`references/spellcasting-summary.md` stay in sync with
`references/german-terminology.md`.

## License

The Python code (`scripts/*.py`) is original work. The reference material
(`references/*.md`) is summarized/rewritten from the System Reference
Document 5.2.1 by Wizards of the Coast LLC, licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — each file cites
its source per that license's attribution requirement.
`references/german-terminology.md` and the German subclass/spell names in
`classes-and-subclasses.md`/`spellcasting-summary.md` are sourced from the
official German translation of the same SRD 5.2.1, under the same license
(see `references/extraction-map-de.md`). The official character sheet PDF
(not included, see Setup) remains Wizards of the Coast's own copyrighted
work, provided by them free for personal use.
