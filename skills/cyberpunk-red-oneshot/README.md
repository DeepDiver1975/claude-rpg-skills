# One-Shot Generator — a Claude Code skill for use with Cyberpunk RED

A [Claude Code](https://claude.com/claude-code) skill that generates a
complete, ready-to-run one-shot session for the Cyberpunk RED tabletop RPG:
pregenerated Rank 0 characters as filled official character sheet PDFs (with
portraits), a linear scenario with GM notes, NPC/enemy Mook Sheets, and a
consistent set of image-generation prompts. See [`SKILL.md`](SKILL.md) for
the full process the skill follows.

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
products. Accordingly, **this repository does not include R. Talsorian's
official character sheet PDFs** — see Setup below for how to obtain them
yourself, directly from R. Talsorian, before using this skill.

## Setup

### 1. Get the two official free PDFs

Download these two files yourself from R. Talsorian Games' own
[downloadable content page](https://rtalsoriangames.com/downloadable-content/)
and save them at these **exact filenames**, since the scripts reference them
directly:

- `assets/RTG-CPR-CharacterSheet-Fillable.pdf`
- `assets/RTG-CPR-MooksSheetFormFillable.pdf`

### 2. Install requirements

- `pdftk` — PDF form filling
- ImageMagick (`magick`/`convert`) — portrait image compositing
- `mutool` (from `mupdf-tools`) — used by the test suite to verify rendering
- Python 3 and `pytest` (stdlib only otherwise — no PyPI packages required)

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

14 tests total. 5 of them fill and render the real Character/Mook Sheet
PDFs, so they'll fail until step 1 above is done — that's expected, not a
bug.

## License

The Python code (`scripts/*.py`) is original work. The reference material
(`references/*.md`) is derived and paraphrased from R. Talsorian's own free,
publicly published Cyberpunk RED Easy Mode rules, with citations back to the
source pages — it is not a verbatim reproduction of their text, but it also
isn't independently licensed apart from that sourcing. Nothing in this
skill, code included, may be sold, per R. Talsorian's Homebrew Content
Policy — if you fork or reuse this, that restriction carries with it.
