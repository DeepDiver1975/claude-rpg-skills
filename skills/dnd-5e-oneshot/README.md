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
- Python 3 and `pytest` (stdlib only otherwise — no required PyPI packages)
- **Optional, only for direct image generation:** `pip install google-genai`
  plus a `GEMINI_API_KEY` or `GOOGLE_API_KEY` environment variable — see
  "Optional: generate images directly (Google Gemini)" below. Not needed if
  you only want the `.txt` image prompts (the default).

### 3. Install the skill

```bash
ln -s "$(pwd)/skills/dnd-5e-oneshot" ~/.claude/skills/dnd-5e-oneshot
```

Then invoke `/dnd-5e-oneshot` in Claude Code.

### 4. Optional: enable direct image generation (Google Gemini)

By default this skill only ever *writes* English image-generation prompts
as `.txt` files — no network access, no API key needed. To have it call
the Google Gemini image API directly and save actual `.png` files next to
those prompts instead:

1. `pip install google-genai`
2. Set your own Gemini API key — get one from
   [Google AI Studio](https://aistudio.google.com/apikey) — as either the
   `GEMINI_API_KEY` or `GOOGLE_API_KEY` environment variable, **or** in a
   `.env` file in your project's root directory — wherever you run `claude`
   from (**not** inside the skill's own installed folder under
   `~/.claude/skills/`, which is often a shared symlink and a bad place for
   a per-project secret): `echo 'GEMINI_API_KEY=your-key-here' > .env`.
   Make sure your project's `.gitignore` excludes `.env` so it's never
   committed by accident, and `scripts/generate_image.py` reads it
   directly — no need to `export` anything into your shell. A real
   environment variable always takes precedence over the `.env` file if
   both are set. This calls a paid, per-image API; nothing here manages
   billing or spending limits for you.
3. When you run the skill, if a key is available (either way) it will ask
   you once, near the start of the run, whether to auto-generate images
   for this one-shot. Answer no (or leave no key configured) to keep the
   original prompts-only behavior.

See `scripts/generate_image.py` for the script this drives, and
`scripts/test_generate_image.py` for its test coverage (fully mocked — no
real API calls, no `google-genai` install required to run the tests).

## Running the tests

```bash
cd scripts
pytest -v
```

44 tests total. Nearly all of the PDF-related ones fill and render the
real character sheet PDF, so they'll fail until step 1 above is done —
that's expected, not a bug. The `test_generate_image.py` tests need no
setup at all (no API key, no `google-genai` install) since they mock the
Gemini client entirely.

## License

The Python code (`scripts/*.py`) is original work. The reference material
(`references/*.md`) is summarized/rewritten from the System Reference
Document 5.2.1 by Wizards of the Coast LLC, licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — each file cites
its source per that license's attribution requirement. The official
character sheet PDF (not included, see Setup) remains Wizards of the
Coast's own copyrighted work, provided by them free for personal use.
