# One-Shot Generator — a Claude Code skill for use with Cyberpunk RED

A [Claude Code](https://claude.com/claude-code) skill that generates a
complete, ready-to-run one-shot session for the Cyberpunk RED tabletop RPG:
pregenerated Rank 0 characters as original, self-contained character sheet
PDFs (with portraits) generated from HTML/CSS templates, a linear scenario
with GM notes, NPC/enemy Mook Sheets, and a consistent set of
image-generation prompts. See [`SKILL.md`](SKILL.md) for the full process
the skill follows.

Rules content is sourced exclusively from R. Talsorian Games' free Cyberpunk
RED Easy Mode rules (the public Roll20 Compendium) — nothing here reproduces
paid core-rulebook content, and anywhere the free source doesn't cover
something, the skill flags it explicitly as unverified/estimated rather than
inventing it. See [`references/cpr-rules-summary.md`](references/cpr-rules-summary.md)
for the sourcing details.

## Fan content — not affiliated with R. Talsorian Games

This is unofficial, fan-made content distributed under R. Talsorian Games'
[Homebrew Content Policy](https://rtalsoriangames.com/homebrew-content-policy/).
It is not affiliated with, endorsed by, or reviewed by R. Talsorian Games.
Cyberpunk RED and Cyberpunk 2020 are trademarks of R. Talsorian Games, Inc.
This project is free to use and is not for sale, per the Homebrew Content
Policy.

The policy prohibits reproducing text from R. Talsorian's games, books, or
products. This skill generates its own original-layout character/Mook
sheets from HTML/CSS templates (`assets/*.html.jinja`, `assets/*.css`)
rather than filling in R. Talsorian's own PDFs, so it does not require or
include any of their official files.

## Setup

### 1. Install requirements

- Python 3.11+
- `pip install -r scripts/requirements.txt` — installs WeasyPrint (HTML→PDF
  rendering) and Jinja2 (templating), plus `pytest`, `pypdf`, and `Pillow`
  for running the test suite.
- WeasyPrint needs a few system libraries for text/font rendering: on
  Debian/Ubuntu, `apt install libpango-1.0-0 libpangocairo-1.0-0
  libgdk-pixbuf2.0-0 libffi-dev`; see the
  [WeasyPrint install docs](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation)
  for other platforms.

### 2. (Optional) Extract data from your own core rulebook

By default the skill uses only the free Easy Mode rules, so many values (Role
Abilities, several skill stats, all weapon/armor/gear numbers) are estimated and
flagged in each generated GM guide. **If you own the Cyberpunk RED core rulebook**,
you can replace those estimates with verified values from your own PDF:

```bash
# place your owned PDF here (gitignored — never committed):
cp /path/to/your/core-rulebook.pdf assets/cpr-corebook.pdf
python3 scripts/extract_rules.py assets/cpr-corebook.pdf --all
```

This writes page-ranged raw text to `data/raw/`; the skill then structures it into
`data/*.json` (schema in `references/extraction-map.md`) and prefers those verified
datasets automatically, collapsing the "Vor dem Spiel prüfen" gap list.

**This is strictly local.** Your PDF and everything under `data/` are derived from a
paid book — they are gitignored and must never be committed or shared. The
extraction tool refuses to write anywhere outside `data/`. Only use this with a book
you own; the repository ships only the extraction tooling and a facts-only page map,
never R. Talsorian's content. `pdftotext`/`pdfinfo` (from `poppler-utils`) are
required for extraction.

### 3. Install the skill

```bash
ln -s "$(pwd)/skills/cyberpunk-red-oneshot" ~/.claude/skills/cyberpunk-red-oneshot
```

Then invoke `/cyberpunk-red-oneshot` in Claude Code.

## Running the tests

```bash
cd scripts
pytest -v
```

The Character/Mook Sheet tests are self-contained — they render HTML→PDF and
read the result back, needing no external PDFs or system PDF tooling beyond
WeasyPrint's own dependencies (see Setup above). The rulebook-extraction tests
run without any PDF; their one real-PDF integration test skips cleanly unless
you've placed `assets/cpr-corebook.pdf` (step 2 above).

## License

The Python code (`scripts/*.py`) and HTML/CSS templates (`assets/*.jinja`,
`assets/*.css`) are original work. The bundled font
(`assets/fonts/NotoSans-*.ttf`) is Noto Sans by Google, licensed under the
SIL Open Font License 1.1 — see `assets/fonts/OFL.txt`. The reference material
(`references/*.md`) is derived and paraphrased from R. Talsorian's own free,
publicly published Cyberpunk RED Easy Mode rules, with citations back to the
source pages — it is not a verbatim reproduction of their text, but it also
isn't independently licensed apart from that sourcing. Nothing in this
skill, code included, may be sold, per R. Talsorian's Homebrew Content
Policy — if you fork or reuse this, that restriction carries with it.
