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

### 2. Install requirements

- `pdftk` — PDF form filling
- ImageMagick (`magick`/`convert`) — portrait image compositing
- `mutool` (from `mupdf-tools`) — used by the test suite to verify rendering
- Python 3 and `pytest` (stdlib only otherwise — no PyPI packages required)

### 3. Install the skill

```bash
ln -s "$(pwd)/skills/dnd-5e-oneshot" ~/.claude/skills/dnd-5e-oneshot
```

Then invoke `/dnd-5e-oneshot` in Claude Code.

## Running the tests

```bash
cd scripts
pytest -v
```

31 tests total. Nearly all of them fill and render the real character sheet
PDF, so they'll fail until step 1 above is done — that's expected, not a
bug.

## License

The Python code (`scripts/*.py`) is original work. The reference material
(`references/*.md`) is summarized/rewritten from the System Reference
Document 5.2.1 by Wizards of the Coast LLC, licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — each file cites
its source per that license's attribution requirement. The official
character sheet PDF (not included, see Setup) remains Wizards of the
Coast's own copyrighted work, provided by them free for personal use.
