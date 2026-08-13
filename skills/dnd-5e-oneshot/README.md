# One-Shot Generator — a Claude Code skill for use with D&D 5e (2024 rules)

A [Claude Code](https://claude.com/claude-code) skill that generates a
complete, ready-to-run one-shot session for D&D 5e (2024 rules): pregenerated
level 1 characters as original, self-contained character-sheet PDFs (German,
with portraits, rendered from HTML/CSS templates), a linear scenario with GM
notes, NPC/monster Markdown stat blocks, and a
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

This skill renders its **own** original character-sheet design from HTML/CSS
templates (`assets/character_sheet.html.jinja` + `assets/*.css`) — it does not
require or include any Wizards of the Coast PDF.

## Setup

### 1. Install requirements

- Python 3.11+
- `pip install -r scripts/requirements.txt` — installs WeasyPrint (HTML→PDF
  rendering) and Jinja2 (templating), plus `pytest`, `pypdf`, and `Pillow`
  for the test suite.
- WeasyPrint needs a few system libraries for text/font rendering: on
  Debian/Ubuntu, `apt install libpango-1.0-0 libpangocairo-1.0-0
  libgdk-pixbuf2.0-0 libffi-dev`; see the
  [WeasyPrint install docs](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation)
  for other platforms. `pdftotext`/`pdfinfo` (from `poppler-utils`) are only
  needed for step 2's optional extraction.

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

The character-sheet tests are self-contained — they render HTML→PDF and read
the result back, needing no external PDF or system PDF tooling beyond
WeasyPrint's own dependencies (see Setup). The `test_terminology_de.py` tests
check that `references/classes-and-subclasses.md` and
`references/spellcasting-summary.md` stay in sync with
`references/german-terminology.md`.

## License

The Python code (`scripts/*.py`) and the HTML/CSS sheet templates
(`assets/character_sheet.*`, `assets/themes/*.css`) are original work; the
bundled fonts (`assets/fonts/*.ttf`) are SIL OFL 1.1 (each family's `OFL-*.txt`
is included). The reference material
(`references/*.md`) is summarized/rewritten from the System Reference
Document 5.2.1 by Wizards of the Coast LLC, licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — each file cites
its source per that license's attribution requirement.
`references/german-terminology.md` and the German subclass/spell names in
`classes-and-subclasses.md`/`spellcasting-summary.md` are sourced from the
official German translation of the same SRD 5.2.1, under the same license
(see `references/extraction-map-de.md`).
