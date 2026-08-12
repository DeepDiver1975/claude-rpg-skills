---
name: dnd-5e-oneshot
description: Use when the user wants to run a D&D 5e (2024 rules / SRD 5.2.1) one-shot session (a self-contained, single-session game with pregenerated characters) and needs pregenerated characters, a scenario, NPC/monster stat blocks, and image prompts generated for it. Triggers on "D&D one-shot", "D&D 5e one-shot", "generate a D&D session", or a GM asking to prep a Dungeons & Dragons game.
---

# D&D 5e One-Shot Generator

Generates a complete, ready-to-run D&D 5e (2024 rules) one-shot for a 3-6
player group: pregenerated level 1 characters as filled official PDF sheets
(with portraits) plus Markdown, a linear scenario with GM notes, NPC/monster
Markdown stat blocks, and a consistent set of image prompts. The GM plays
this in German; every deliverable this skill writes for players/GM must be
German — that includes class/subclass/species/background names,
weapon/armor/gear names, damage types, spell names, and skill names
appearing in prose (Markdown sheets, the GM guide, NPC blocks), not just
narrative text. Use `references/german-terminology.md` for the German term
to use — every term in it is sourced from the official German SRD 5.2.1 PDF
(see `references/extraction-map-de.md` for provenance), not a guess.
Numeric/mechanical resolution (ability scores, DCs, HP dice, spell slots,
class features) still comes from the English `references/*` files below,
since those numbers don't change between language editions of the same
ruleset. A short, specific list of things stay in their literal English SRD
form, each for a concrete mechanical or sourcing reason spelled out in full
where it matters (Step 5): the Character JSON schema's
`skill_proficiencies`/`skill_expertise`/`saving_throw_proficiencies`
entries (the script looks these up by exact name); the official PDF's own
printed field labels, baked into its artwork and not something this skill
writes; and the image prompts written in Step 8 (image-generation tools
expect English prompts), each one labeled with the German name/scene it
belongs to. This document and all `references/*` also stay English.

**In-fiction naming defaults to German, not English.** This is the opposite
default from the Cyberpunk RED skill, deliberately: Night City is a real,
canonically English-speaking setting, so CPR's PC handles/NPC names default
to English. D&D's homebrew fantasy world has no such real-world anchor, so
absent a stated reason otherwise, names should follow the table's own
language — a German-speaking table's PCs, NPCs, places, and factions
default to German or German-flavored fantasy names (e.g. "Roland
Wolfsbach", "Talgrund", "Die Graue Klinge"), not English ones. Deviate only
when the GM's premise from Step 1 establishes a specific in-fiction culture
that justifies a different naming convention for a particular
character/place (a coastal trade-city NPC could plausibly carry a
Mediterranean-flavored name if the premise sets up that region, for
instance) — never default to English just because SRD reference material
happens to be in English. When picking a name in Steps 3, 5, and 7, ask:
"does this character/place have an explicit, stated reason to carry a name
from a different culture?" If not, default to German.

## Step 1: Get the premise from the GM

Ask for: party size (3-6; if outside that range, confirm rather than
clamp), a rough theme/tone (e.g. "dungeon crawl", "heist", "political
intrigue"), and optionally a starting level (default: **level 1** — every
PC generated in Step 5 assumes level 1 unless the GM asks for higher). If
the premise is ambiguous, ask ONE clarifying question rather than guessing
a tone that might clash with the table.

## Step 2: Pick a visual style

Ask the GM which visual style preset from `references/style-guide.md` to
use for this run's image prompts — offer the five named presets (Classic
PHB Illustration, Painterly Classic Fantasy, Cinematic BG3-Style Concept
Art, Flat-Color Animated-Series Style, Moody Grimdark Realism) with a
one-line description of each. If the GM has no preference, default to
Classic PHB Illustration. Use this preset's base style block for every
image prompt generated later in this run (Steps 5, 7, 8) — do not mix
presets within a single one-shot.

## Step 3: Generate the party's shared adventuring hook

Write a shared hook: how this specific party already knows and trusts each
other (a shared patron, guild, mercenary company, prior job, order they all
belong to). This is what makes the "no time wasted on introductions"
premise work — anchor the scenario hook and every PC's personal hook to
this shared history.

## Step 4: Pick a balanced class spread

Read `references/classes-and-subclasses.md`'s "Balanced Party Selection"
section. Pick classes sized to the party (at least one tank-capable class,
at least one healer/support class, remaining slots for damage-strikers or
utility-casters) fitting the premise. Every PC defaults to the SRD's single
listed subclass for their class — but at level 1 (this skill's default
starting level), **no class has subclass features yet** (every SRD class
grants its subclass at level 3), so this is a narrative-identity choice
only unless the GM opted for a level-3+ start in Step 1. A request for any
subclass other than the SRD's listed one is a Step 10 gap.

## Step 5: Generate each PC

For each PC, using `references/dnd5e-rules-summary.md` (core mechanics/DC
ladder/skills), `references/classes-and-subclasses.md` (class features),
`references/species-and-backgrounds.md` (species/background), and
`references/equipment.md` (starting gear) — plus `references/
spellcasting-summary.md` for any caster: write level 1 ability
scores/features/gear, a background-flavored German backstory tied to the
crew concept and to the scenario, and a portrait image prompt built from
the GM's selected style preset (Step 2) in `references/style-guide.md` plus
its universal "Portrait-Specific Additions". Assemble a character JSON
matching the **Character JSON Schema** below, write it to the run's output
folder, then run:

```bash
python3 scripts/fill_character_sheet.py <character.json> <output-folder>/<name-slug>.pdf
```

Portrait compositing is driven by the `portrait_image_path` key in the JSON
itself (set it to the portrait file's path before running the command
above, or leave it `null` to skip — there is no separate CLI flag for
this). `fill_character_sheet.py` computes every derived number itself
(ability modifiers, save/skill totals, initiative, passive Perception,
spell save DC/attack bonus) from the raw ability scores and proficiency
lists in the JSON — don't pre-compute these in the JSON, the script owns
that arithmetic.

Also write a Markdown version of the same character for quick reference.

### Character JSON Schema

All keys required except `alignment` (optional flavor — 2024 rules
de-emphasize it), `spellcasting` (`null` for non-casters), and
`portrait_image_path`.

**Which fields stay English and which are German**: only
`saving_throw_proficiencies`, `skill_proficiencies`, and `skill_expertise`
must stay the SRD's literal English terms — `fill_character_sheet.py`
looks these up by exact name (`skills_field_map.json`, `SKILL_ABILITY`), so
translating them breaks the script. `class`, `subclass`, `species`, and
`background` are, perhaps surprisingly, **not** looked up anywhere in the
script — it writes them straight into `ClassLevel`/`Race `/`Background`
with zero parsing — so there's no mechanical reason to keep them English,
and they should be the German term from `references/german-terminology.md`
or `references/classes-and-subclasses.md` (e.g. "Kämpfer", "Zwerg",
"Soldat", "Domäne des Lebens" for `subclass`), matching what actually ends
up on the PDF and Markdown sheet.
`weapons[].name`/`.properties`/`.mastery`/`.damage_type`, `armor.name`,
`equipment[]`, and `features_and_traits[]` are pure display text the
script never parses either, so write those in German too. The example
below shows all of this together:

```json
{
  "name": "string",
  "species": "string (German term, e.g. \"Zwerg\" — see german-terminology.md)",
  "class": "string (German term, e.g. \"Kämpfer\")",
  "subclass": "string (German term from classes-and-subclasses.md, e.g. \"Domäne des Lebens\")",
  "level": 1,
  "background": "string (German term, e.g. \"Soldat\")",
  "alignment": "string, optional",
  "ability_scores": {"STR": 16, "DEX": 12, "CON": 14, "INT": 10, "WIS": 13, "CHA": 8},
  "proficiency_bonus": 2,
  "hp": {"current": 12, "max": 12, "temp": 0},
  "hit_dice": {"die": "1d10", "total": 1},
  "ac": 16,
  "speed": 30,
  "saving_throw_proficiencies": ["STR", "CON"],
  "skill_proficiencies": ["Athletics", "Intimidation"],
  "skill_expertise": [],
  "weapons": [{"name": "Langschwert", "attack_ability": "STR", "damage_die": "1d8", "damage_type": "Hiebschaden", "properties": "Vielseitig (1d10)", "mastery": "Schwächen"}],
  "armor": {"name": "Kettenrüstung", "ac_base": 16, "stealth_disadvantage": true},
  "equipment": ["Schild", "Entdeckerausrüstung"],
  "coins": {"cp": 0, "sp": 0, "ep": 0, "gp": 10, "pp": 0},
  "features_and_traits": ["Zweiter Atem (1×/Rast, heilt 1d10 + Stufe)"],
  "spellcasting": null,
  "personality_traits": "string",
  "ideals": "string",
  "bonds": "string",
  "flaws": "string",
  "backstory": "string",
  "portrait_image_path": "optional/path/to/portrait.png, or null"
}
```

`spellcasting`, when the class is a caster (see
`references/spellcasting-summary.md`):

```json
{"ability": "INT", "cantrips": ["Feuerpfeil", "Magierhand"], "spells_known_or_prepared": ["Magisches Geschoss", "Schild"], "spell_slots": {"1": 2}}
```

Spell names should be the German term from `references/spellcasting-
summary.md`'s curated shortlist (sourced from the official German SRD PDF,
see `references/german-terminology.md`). If a one-shot needs a spell not
on that shortlist, its German name isn't verified there — fetch it from
the official German SRD PDF (or `data/raw/spells.txt`, if the extraction
in `references/extraction-map-de.md` has been run) before using it, rather
than guessing; that's a Step 10 gap like any other unverified term.

`skill_proficiencies`/`skill_expertise` keys must be normalized skill names
present in `assets/skills_field_map.json` (the 18 SRD skills) — the script
raises an error naming any skill you use that isn't in that map. This is
the one place the English JSON term doesn't automatically become German
output: the PDF's own printed skill labels are unavoidably English (see the
next constraint below), and the **Markdown sheet's skill line should show
the German term from `references/german-terminology.md` with the English
SRD term in parentheses**, e.g. "Athletik (Athletics) +5" — write it that
way explicitly, don't just copy the JSON's `"Athletics"` into the Markdown
verbatim.

**Known constraint — sheet is 2014-layout, data is 2024/SRD-5.2.1**: the
official fillable PDF this skill uses
(`assets/5E_CharacterSheet_Fillable.pdf`) is the 2014-rules character sheet
— it was the only official, genuinely form-fillable (AcroForm) sheet
available; the newer 2024-rules PDF has no real form fields at all, only
Acrobat "Fill & Sign" support, which this skill's `pdftk`-based pipeline
can't drive. Practically this means: a 2024 "Species" value is written into
the sheet's own field literally named `Race ` (trailing space preserved,
this is the actual PDF field name); Weapon Mastery properties have no
dedicated column on this sheet, so they're folded into the weapon's Name
field in parentheses instead. Both are handled automatically by
`fill_character_sheet.py` — no action needed when writing the JSON, just be
aware the printed PDF's field label still literally says "RACE" in English
(unavoidable, it's baked into the sheet's artwork) even though the value
printed next to it — the character's `species`, per the schema above — is
written in German (e.g. "Zwerg"), same as `class`/`background`. Only the
field's own printed label is stuck in English; everything this skill
actually writes into the page (species/class/subclass/background values,
weapon names, equipment, features, backstory, personality) is German.

**Known constraint — text fields auto-shrink, they don't clip**: unlike the
Cyberpunk RED skill's character sheet (which hard-clips overlong text),
this sheet's text fields are set to auto-size their font, so long values
shrink to fit rather than getting cut off — but an entire paragraph crammed
into a short field (e.g. `ClassLevel`, `Background`) will render at a
barely-legible tiny size. Keep short fields short; reserve full sentences
for `backstory`/`features_and_traits`, which map to generously sized boxes.
The Markdown sheet is always the reliable fallback for anything that prints
too small to read comfortably.

**Known constraint — skill/save proficiency checkboxes are not filled**:
this sheet has 124 checkbox fields (mostly skill/save proficiency dots),
many with generic, non-descriptive names (e.g. `Check Box 12`) that would
require positional/rect analysis rather than name matching to map
correctly. `fill_character_sheet.py` deliberately skips them in v1 —
proficiency is still fully reflected in each skill/save's printed *total*
(the computed number already includes the Proficiency Bonus where
applicable), and the Markdown sheet lists which skills/saves are proficient
explicitly. Don't try to hand-edit the checkboxes in the JSON; there's no
field for them.

**Known constraint — only 3 weapon rows**: the sheet has 3 attack rows
(`Wpn Name`/`Wpn Name 2`/`Wpn Name 3`), one fewer than the Cyberpunk RED
sheet's 4. If a PC has more than 3 weapons, only the first 3 are filled on
the PDF; the Markdown sheet always lists all of them.

## Step 6: Generate the scenario as the GM guide

Write 3-5 linear scenes (hook -> approach -> complication -> climax ->
resolution) with likely branch points called out. For each scene, write GM
notes: suggested ability checks with DCs (from `references/
dnd5e-rules-summary.md`'s DC ladder), NPC motivations/secrets,
complications, and how the scene connects back to a specific PC's personal
hook. Write this as a single German Markdown document — the GM guide —
combining the scenario and its GM notes; this is the only scenario/GM
document this skill produces (Step 10 later appends a gaps section to it,
not a separate file).

## Step 7: Generate NPC/monster stat blocks

Unlike the Cyberpunk RED skill's Mook Sheet PDFs, **NPC/monster stat blocks
in this skill are Markdown-only — there is no PDF-fill step for them.** No
free, official, or clearly-licensed fillable "monster stat block" PDF
exists anywhere (checked against DMs Guild/Gumroad/Scribd during this
skill's design — only paid or unclear-license third-party templates were
found), so this is a deliberate scope decision, not a corner cut.

For every antagonist/NPC (both generic reused enemies and detailed named
NPCs), write a German Markdown stat block following this format, matching
the SRD's own monster stat-block shape:

```markdown
# <Name> — <one-line German role description>

*<size> <type>, <alignment>*

**Rüstungsklasse (AC)** X (source)
**Trefferpunkte (HP)** X (XdY+Z)
**Geschwindigkeit** 30 ft.

| STR | DEX | CON | INT | WIS | CHA |
|---|---|---|---|---|---|
| 16 (+3) | 14 (+2) | 15 (+2) | 10 (+0) | 12 (+1) | 8 (-1) |

**Rettungswürfe** (only if proficient in any)
**Fertigkeiten** (only if any)
**Sinne** passive Wahrnehmung X
**Sprachen** ...
**Herausforderungsgrad (CR)** X (XP; PB +Y)

***<Trait Name>.*** Beschreibung.

## Aktionen
***<Action Name>.*** *Angriff:* +X, Reichweite/Distanz, ein Ziel. *Treffer:* X (XdY+Z) <Schadensart>.
```

Field labels (AC, HP, CR) stay in their English abbreviation form even in
German headings, per the language rule above — but everything else in the
block (name, size/type line, traits, action names/descriptions, damage
types) is German, using `references/german-terminology.md` for creature
types and damage types. NPC/monster names follow the same flipped naming
default as Step 3/5 (German/German-flavored by default). For a generic
enemy type meant to be reused across multiple identical instances (e.g.
"3× Bandit"), write one stat block file and note in the GM guide that it's
reused — don't generate a separate near-identical file per instance.

For 1-2 more detailed named NPCs, add extra German prose sections on top of
the same mechanical block: `## Motivation`, `## Geheimnis` (secret, ideally
tied to a specific PC), `## Spielleitung` (GM roleplay notes), plus a
`## Bild-Prompt` line pointing at its `image-prompts/` file.

## Step 8: Generate image prompts

For every PC portrait, major NPC, key location, 1-2 battlemaps for the
climax fight, and two regional overview maps showing where in the world
this one-shot takes place — one GM-facing, one player-facing — write an
English image-generation prompt appending the GM's selected style preset
from `references/style-guide.md`, plus the relevant universal Portrait-,
Battlemap-, or Map-Specific Additions as applicable — note the Battlemap
Addition specifies a **5-foot-per-square grid** (5e's actual default
unit; don't substitute a different game's grid convention). The GM map
plots every named location from Step 6's scenes onto a single image in
their scene sequence, exactly as before; the player map instead shows
only locations that are common public knowledge independent of this
specific plot (general regional geography, well-known public landmarks,
and the party's own starting location) — see "Map-Specific Additions" in
the style guide, now split into a "GM Map" and "Player Map" subsection,
for exactly what each may and may not show. Save all prompts into
`<output-folder>/image-prompts/`, one file per image (the two maps as
`map-gm.txt` and `map-player.txt`), each labeled with the German
name/scene it belongs to, since these are meant to be run through the
GM's own external image tool. After writing both map prompts, add two
lines to the GM guide directly below its premise section: "**Regionale
Karte (GM, mit Spoilern):** siehe `image-prompts/map-gm.txt`" and
"**Regionale Karte (Spieler:innen, spoilerfrei — direkt am Tisch
zeigbar):** siehe `image-prompts/map-player.txt`" — matching how NPC
blocks already point to their own image-prompt file.

## Step 9: Assemble the output folder

Write everything into a fresh dated folder: `oneshots/YYYY-MM-DD-<slug>/`
containing:

```
oneshots/<date>-<slug>/
├── gm-guide.md
├── characters/
│   ├── <name-slug>.json
│   ├── <name-slug>.md
│   └── <name-slug>.pdf
├── npcs/
│   └── <name-slug>.md
└── image-prompts/
    ├── portrait-<name>.txt
    ├── npc-<name>.txt
    ├── location-<name>.txt
    ├── battlemap-<scene>.txt
    ├── map-gm.txt
    └── map-player.txt
```

If any character's PDF fill step fails, report the failing field name and
fall back to delivering that character's Markdown sheet only — never
silently ship an incomplete PDF without saying so.

## Step 10: Report gaps

If any class feature, subclass, species trait, background, feat, spell,
weapon/armor property, or monster used in this specific one-shot goes
beyond what's covered in `references/*` — most commonly: a subclass other
than the SRD's single listed one for that class (`classes-and-subclasses.md`),
a species/background not in the SRD's 9/4 (`species-and-backgrounds.md`), a
spell not on the curated shortlist in `spellcasting-summary.md` (fetch its
real text from the source before using it rather than skip this check), or
any equipment/monster genuinely outside the SRD's scope — list those gaps
explicitly at the end of the GM guide under a "Vor dem Spiel prüfen" (check
before playing) heading, rather than leaving them silently unverified.

Note the difference in framing from the Cyberpunk RED skill: SRD 5.2.1 is a
complete, official, CC BY 4.0 source (not a hobbyist's best-effort summary
of scattered free web pages), so this list will typically be much shorter
— it's a *scope* flag (SRD vs. the full Player's Handbook/Monster Manual),
not a *reliability* flag on the reference material itself.
