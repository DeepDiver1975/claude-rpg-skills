# D&D 5e SRD 5.2.1 (German) — Extraction Map

This file is the schema-and-provenance companion to `scripts/extract_srd_de.py`.
It documents where each piece of official German terminology in this skill's
`references/*.md` was sourced from, so the extraction can be re-run and
re-verified (e.g. after a future SRD point release) without redoing the
research from scratch.

## Source and license

`DE_SRD_CC_v5.2.1.pdf` — the official German translation of the System
Reference Document 5.2.1, released by Wizards of the Coast LLC under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), downloaded from
<https://media.dndbeyond.com/compendium-images/srd/5.2/DE_SRD_CC_v5.2.1.pdf>.
Save it at `assets/DE_SRD_CC_v5.2.1.pdf` before running the extraction script
(see README.md Setup). Unlike the Cyberpunk RED core rulebook, this is a
freely downloadable, CC-licensed document — no ownership gate, and the
curated terms extracted from it are meant to be committed with attribution,
same as this skill's existing English `references/*.md`.

**Page numbering:** empirically confirmed (see `extract_srd_de.py`'s
`DEFAULT_OFFSET = 0`) that this PDF's physical page numbers equal its
printed page numbers — no cover-page shift, unlike CPR's rulebook. All page
numbers below are both at once.

## How the two halves fit together

1. `scripts/extract_srd_de.py` (the authoritative section list lives there)
   pulls page-ranged raw text into `data/raw/<section>.txt` and writes
   provenance to `data/manifest.json`.
2. The skill (Claude) reads each `data/raw/<section>.txt` and cross-checks
   or rebuilds the relevant `references/*.md` content from it, replacing
   guessed/unverified German terms with the book's actual wording.

## Sections and what each sourced

| Section (`--section`) | Heading | Printed pp. | Sourced content |
|---|---|---|---|
| `core-rules` | Die Spielregeln | 5–21 | Ability names (p.5), the 18-skill table (p.10), DC ladder (p.9), damage-type cross-reference (p.19) |
| `classes` | Klassen | 33–92 | All 12 classes' names (already matched the existing glossary — no changes), all 12 subclasses' names + taglines + level-3 headline features, recommended-cantrip/1st-level-spell callouts embedded in each class's Spellcasting feature text (the fastest reliable way to get exact official spell names, since they're quoted verbatim rather than reconstructed from alphabetical spell-list tables that `pdftotext` reflows unreliably across this PDF's two-column layout) |
| `origins` | Charakterherkunft | 93–97 | The 4 backgrounds' names + stat/skill/tool grants, the 9 species' names |
| `equipment` | Ausrüstung | 101–117 | Weapon table (name/damage/properties/mastery/weight/cost), armor table, weapon properties (Finesse/Heavy/Light/Loading/Reach/Thrown/Two-Handed/Versatile — confirmed as their own description headings), adventuring gear and pack names |
| `spells` | Zauber | 118–202 | Full alphabetical spell descriptions (`Beschreibungen der Zauber`) — used to confirm exact German names for `spellcasting-summary.md`'s curated shortlist by matching each spell's mechanical fingerprint (range/duration/effect) against the known English text, and to find the handful of names not surfaced via the class-chapter recommended-spell callouts (e.g. Minor Illusion → `Einfache Illusion`, True Strike → `Zielsicherer Schlag`) |
| `rules-glossary` | Regelglossar | 203–221 | All condition names (entries suffixed `(Zustand)` in the glossary), the 13 damage-type base nouns (table under the `Schaden` entry, p.214) |
| `monster-overview` | Monster | 295–299 | Creature size categories (p.295) and creature type names (p.295–296), both used in NPC/monster stat blocks (SKILL.md Step 7) |

## Verification method

Every term below is either (a) quoted directly as a heading in the PDF's
text layer (spell names, subclass names, background names, weapon/armor
names — verified via `grep` against `data/raw/*.txt`), or (b) confirmed by
reading the surrounding mechanical description and matching it against the
already-documented English SRD mechanics in this skill's other
`references/*.md` (e.g. confirming `Feuerpfeil` is Fire Bolt by matching
"1d10 fire damage, ranged spell attack, upgrades at 5th/11th/17th" against
the German text's `1W10 Feuerschaden`, `Fernkampf-Zauberangriff`, and the
same three upgrade levels). No term in `german-terminology.md` was invented
or guessed — every entry traces back to a specific page in the official PDF.

Where this extraction **corrected** a prior guess in `german-terminology.md`
(the old file was explicitly labeled "not an official translation"), the
official term is used and the prior guess is dropped — see that file's own
notes for anything worth flagging as a surprising correction (e.g. "Force"
damage is `Energieschaden`, not a literal `Kraftschaden`; "Deafened" is
`Taub`, not a disambiguated `Betäubt (Gehör)` — `Betäubt` alone is
"Stunned").
