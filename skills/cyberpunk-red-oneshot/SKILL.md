---
name: cyberpunk-red-oneshot
description: Use when the user wants to run a Cyberpunk RED one-shot session (a self-contained, single-session game with pregenerated characters) and needs pregenerated characters, a scenario, NPC/enemy stat blocks, and image prompts generated for it. Triggers on "Cyberpunk RED one-shot", "CPR one-shot", "generate a Cyberpunk RED session", or a GM asking to prep a Cyberpunk RED game.
---

# Cyberpunk RED One-Shot Generator

Generates a complete, ready-to-run Cyberpunk RED one-shot for a 3-5 player group:
pregenerated Rank 0 characters as original character sheet PDFs (with portraits)
plus Markdown, a linear scenario with GM notes, NPC/enemy Mook Sheets, and a consistent
set of image prompts. The GM plays this in German; every deliverable this skill
writes for players/GM must be German, with three exceptions: this document and
all `references/*` stay English; Role names (Solo, Netrunner, ...) and character/
Mook sheet section labels stay in their original English CPR form even inside
German text; and the
image prompts written in Step 8 stay English (image-generation tools expect
English prompts), each one labeled with the German name/scene it belongs to.

**In-fiction naming stays independent of document language.** The document is
German, but Night City is still a North American setting — PC handles, NPC
names, gang names, and location names should default to English, exactly like
the official CPR pregens (Forty, Mover, Torch, Redtail, 24-7) and canon gangs
(Tyger Claws, Maelstrom, 6th Street). Give a character a non-English name only
when their in-fiction nationality/heritage explicitly justifies it (a
Mexican-heritage NPC can be "Esteban Ruiz", Chinatown streets can carry Chinese
names, an NPC explicitly written as a German expat can be "Voss") — never as a
default just because the table's language is German. When picking a handle,
name, or gang name in Steps 3, 5, and 7, ask: "does this character/place have
an explicit, stated reason to carry this name's language/culture?" If not,
default to English.

## Step 0: Use locally-extracted rulebook data if present (optional, one-time)

By default this skill draws game data from the free Easy Mode references only, so
Role Abilities, many skill→STAT mappings, and all weapon/armor/gear numbers are
estimated and get flagged in Step 10. A GM who **owns the Cyberpunk RED core
rulebook** can replace those estimates with verified values extracted from their
own PDF. This is one-time setup; once `data/*.json` exist, every future run reuses
them.

**Copyright:** the GM's PDF and everything the extraction writes under `data/` are
derived from a paid book — they are local only, gitignored, and must never be
committed or redistributed. `scripts/extract_rules.py` refuses to write outside
`data/`. Only use this with a book the GM owns.

At the start of a run, check whether `data/` holds structured datasets:

- **If `data/<domain>.json` files exist**, prefer them as verified sources
  throughout (Steps 4, 5, 7) and treat their domains as covered in Step 10.
- **If they do not exist**, offer the GM the one-time extraction, then fall back to
  the free-source `references/*.md` (current behaviour) if they decline:
  1. GM places their owned PDF at `assets/cpr-corebook.pdf` (never committed).
  2. Run `python3 scripts/extract_rules.py assets/cpr-corebook.pdf --all` to fill
     `data/raw/`.
  3. For each `data/raw/<section>.txt`, read it and write the corresponding
     `data/<domain>.json` following the schema in
     `references/extraction-map.md` — same verified/estimated honesty as the
     references, but every value now sourced from the book (tag each file's
     `"_source"` as `"Cyberpunk RED core rulebook (locally extracted)"`).

## Step 1: Get the premise from the GM

Ask for: party size (3-5; if outside that range, confirm rather than clamp), a
rough theme/tone (e.g. "corporate extraction gone wrong", "gang turf war"), and
optionally a specific edge/twist. If the premise is ambiguous, ask ONE clarifying
question rather than guessing a tone that might clash with the table.

## Step 2: Pick a visual style

Ask the GM which visual style preset from `references/style-guide.md` to use
for this run's image prompts — offer the five named presets (CPR Rulebook,
2020 Pulp Paperback, Night City Cinematic, Edgerunners Anime, Chrome Noir)
with a one-line description of each. If the GM has no preference, default to
CPR Rulebook. Use this preset's base style block for every image prompt
generated later in this run (Steps 5, 7, 8) — do not mix presets within a
single one-shot.

## Step 3: Generate the crew concept

Write a shared crew/faction hook: how this specific party already knows and
trusts each other (how they met, a past job together, a shared patron/gang/fixer).
This is what makes the "no time wasted on introductions" premise work — anchor
the scenario hook and every PC's personal hook to this shared history.

## Step 4: Pick a balanced Role spread

Read `references/roles-and-archetypes.md`'s "Balanced Party Selection" section.
Pick Roles sized to the party (one combat-capable, one tech/support, remaining
slots for social/utility) fitting the premise. Only pick Netrunner if the premise
explicitly calls for hacking (see the Netrunning gap note in
`references/cpr-rules-summary.md`). If `data/roles.json` exists (Step 0), use its
verified Role Abilities in place of the reference's five unverified ones, and
Netrunner is no longer a hard gap — `data/netrunning.json` covers its mechanics.

## Step 5: Generate each PC

For each PC, using `references/cpr-rules-summary.md` (stats/skills/DVs) and
`references/roles-and-archetypes.md` (Role Ability) and
`references/weapons-armor-gear.md` (starting gear) — or, when Step 0's extraction
was done, the verified `data/skills.json`, `data/roles.json`, `data/weapons.json`,
`data/armor.json`, `data/gear.json`, and `data/cyberware.json` in preference to
those references: write Rank 0 stats/skills/gear,
a lifepath-flavored German background tied to the crew concept and to the
scenario, and a portrait image prompt built from the GM's selected style preset
(Step 2) in `references/style-guide.md` plus its universal "Portrait-Specific
Additions". Assemble a character JSON matching the **Character JSON Schema**
below, write it to the run's `characters/` output subfolder (create the dated
output folder and its `characters/`, `npcs/`, `image-prompts/` subfolders first),
then run:

```bash
python3 scripts/fill_character_sheet.py <character.json> <output-folder>/characters/<handle-slug>.pdf
```

Portrait compositing is driven by the `portrait_image_path` key in the JSON itself
(set it to the portrait file's path before running the command above, or leave it
`null` to skip — there is no separate CLI flag for this).

Also write a Markdown version of the same character for quick reference.

### Character JSON Schema

All keys required except `portrait_image_path`, `reputation`, `cyberware`,
`gear`, `money`, `ip`, and `addictions`.
`skills` keys must be normalized skill names present in
`scripts/fill_character_sheet.py`'s `SKILL_GOVERNING_STAT` (60 entries covering
the sheet's primary skill list, each mapped to the stat it rolls against) or
one of `CATEGORY_SKILLS` — "Local Expert" and "Play Instrument" are CPR "pick
a specialization" skills, so name the specific area/instrument in parens, e.g.
`"Local Expert (Combat Zone)"` or `"Play Instrument (Guitar)"` — the script
raises an error naming any skill you use that isn't in either set, so treat
that as a sign to pick a different/adjacent skill name rather than inventing
one. You only list the skills a character has *trained* (level > 0); the sheet
prints the **full** CPR skill list regardless — trained skills are highlighted,
and every untrained skill is shown dimmed at its base total (its governing stat,
level 0), since it's still rollable. Each skill's LVL and rolled TOTAL
(stat + level) are printed automatically — don't compute or write the total
yourself.

`reputation` defaults to 2 (CPR's starting Reputation for a new character) if
omitted. `seriously_wounded` (Seriously Wounded Threshold) and `death_save`
are computed automatically from `hp.max` and `stats.BODY` — don't add them to
the JSON. The following sections print only when their (optional) key is
present, so omit any that don't apply: `cyberware` (list of `{name, effect}`),
`gear` (list of `{name, notes}`), `addictions` (free-text string), `money`
(any of `cash`/`rent`/`housing`/`lifestyle`), and `ip` (Improvement Points,
`{current, total}`).

```json
{
  "handle": "string",
  "role": "string (one of the 10 CPR Role names, English)",
  "role_ability": "string",
  "role_ability_rank": 4,
  "stats": {"INT": 5, "REF": 6, "DEX": 5, "TECH": 4, "COOL": 6, "WILL": 5, "LUCK": 5, "MOVE": 5, "BODY": 5, "EMP": 4},
  "hp": {"current": 35, "max": 35},
  "humanity": {"current": 50, "max": 50},
  "luck": {"current": 5, "max": 5},
  "reputation": 2,
  "skills": {"Athletics": 4, "Shoulder Arms": 6},
  "weapons": [{"name": "Medium Pistol", "dmg": "2d6", "ammo": "10(c)", "rof": "2", "notes": ""}],
  "armor": {"head": {"sp": 0, "penalty": 0}, "body": {"sp": 11, "penalty": 0}, "shield": {"sp": 0, "penalty": 0}},
  "cyberware": [{"name": "Cybereye (Infrared)", "effect": "string"}],
  "gear": [{"name": "Agent (Pocket-KI)", "notes": "string"}],
  "money": {"cash": 500, "rent": 200, "housing": "string", "lifestyle": "string"},
  "ip": {"current": 0, "total": 0},
  "addictions": "string",
  "fashion": "string",
  "role_specific_lifepath": "string",
  "notes": "string",
  "portrait_image_path": "optional/path/to/portrait.png, or null"
}
```

## Step 6: Generate the scenario as the GM guide

Write 3-5 linear scenes (hook -> approach -> complication -> climax ->
resolution) with likely branch points called out. For each scene, write GM notes:
suggested skill checks with DVs (from `references/cpr-rules-summary.md`'s DV
table), NPC motivations/secrets, complications, and how the scene connects back
to a specific PC's personal hook. Write this as a single German Markdown
document — the GM guide — combining the scenario and its GM notes; this is the
only scenario/GM document this skill produces (Step 10 later appends a gaps
section to it, not a separate file).

## Step 7: Generate NPC/enemy stat blocks

For antagonists, build Mook JSON files matching the **Mook JSON Schema** below
and run (drawing weapon/armor stats from `data/weapons.json` and `data/armor.json`
when Step 0's extraction was done, otherwise from `references/weapons-armor-gear.md`):

```bash
python3 scripts/fill_mook_sheet.py <mook.json> <output-folder>/npcs/<name-slug>.pdf
```

For 1-2 more detailed named NPCs, write a fuller German Markdown stat block plus
an image prompt (the GM's selected style preset from `references/style-guide.md`,
no portrait-specific additions needed unless it's a portrait-framed NPC image).

### Mook JSON Schema

All fields required except `weapons` entries beyond the first, which may be
omitted — the sheet's weapon table grows to fit however many entries you give it.

```json
{
  "name": "string",
  "stats": {"INT": 5, "REF": 6, "DEX": 5, "TECH": 4, "COOL": 6, "WILL": 5, "LUCK": 5, "MOVE": 5, "BODY": 5, "EMP": 4},
  "hit_points": 20,
  "seriously_wounded": 10,
  "death_save": 5,
  "skill_bases": "string, e.g. 'Handgun +5, Stealth +4'",
  "weapons": [{"name": "string", "damage": "string"}],
  "armor_type": "string",
  "head_sp": 0,
  "body_sp": 8,
  "cyberware_special_equipment": "string"
}
```

## Step 8: Generate image prompts

For every PC portrait, major NPC, key location, 1-2 battlemaps for the
climax fight, and two regional overview maps showing where in Night City
this one-shot takes place — one GM-facing, one player-facing — write an
English image-generation prompt appending the GM's selected style preset
from `references/style-guide.md`, plus the relevant universal Portrait-,
Battlemap-, or Map-Specific Additions as applicable. The GM map plots
every named location from Step 6's scenes onto a single image in their
scene sequence, exactly as before; the player map instead shows only
locations that are common public knowledge independent of this specific
plot (general district geography, well-known public landmarks, and the
crew's own starting location) — see "Map-Specific Additions" in the style
guide, now split into a "GM Map" and "Player Map" subsection, for exactly
what each may and may not show. Save all prompts into
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
containing a `characters/` subfolder (each PC's PDF + Markdown), an `npcs/`
subfolder (Mook Sheet PDFs and/or the Markdown NPC stat blocks from Step 7), the
GM guide (German — the single scenario-plus-GM-notes document from Step 6, closed
out with Step 10's gaps section) at the folder root, and an `image-prompts/`
subfolder. When a document in a subfolder points at a file in another subfolder,
use a correct relative path (e.g. the GM guide at the root links `npcs/…` and
`image-prompts/…`; an NPC file under `npcs/` links `../image-prompts/…`). If any PDF render step
fails, report the error and fall back to delivering that
character's Markdown sheet only — never silently ship an incomplete PDF without
saying so.

## Step 10: Report gaps

A domain sourced from Step 0's locally-extracted `data/*.json` counts as
**verified** — do not flag it, and where useful cite it in the GM guide as
"Cyberpunk RED core rulebook (locally extracted)". Only report gaps for the domains
still coming from the free references. So if extraction was done, most of the list
below collapses; if it wasn't, flag exactly as before.

If any rule, Role Ability, skill, weapon stat, armor value, or gear item used in this
specific one-shot wasn't covered by verified data — flagged as
unverified/estimated anywhere in `references/cpr-rules-summary.md`,
`references/roles-and-archetypes.md`, or `references/weapons-armor-gear.md`
(which is almost entirely estimated — check it as carefully as the other two) —
list those gaps explicitly at the end of the GM guide under a "Vor dem Spiel
prüfen" (check before playing) heading, rather than leaving them silently
unverified. If a PC's weapon, armor, or gear came from `weapons-armor-gear.md`'s
estimated content, name it here too, not just Role Abilities and Netrunning.
The same applies to skills: `cpr-rules-summary.md`'s cross-check comment lists 21
skills (e.g. Martial Arts, Autofire, Demolitions) whose governing STAT was read
off the PDF field name and is explicitly not confirmed against any free source —
if a PC has a rank in one of those, flag it here just like Netrunning.
