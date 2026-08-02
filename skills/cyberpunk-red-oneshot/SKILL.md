---
name: cyberpunk-red-oneshot
description: Use when the user wants to run a Cyberpunk RED one-shot session (a self-contained, single-session game with pregenerated characters) and needs pregenerated characters, a scenario, NPC/enemy stat blocks, and image prompts generated for it. Triggers on "Cyberpunk RED one-shot", "CPR one-shot", "generate a Cyberpunk RED session", or a GM asking to prep a Cyberpunk RED game.
---

# Cyberpunk RED One-Shot Generator

Generates a complete, ready-to-run Cyberpunk RED one-shot for a 3-5 player group:
pregenerated Rank 0 characters as filled official PDF sheets (with portraits) plus
Markdown, a linear scenario with GM notes, NPC/enemy Mook Sheets, and a consistent
set of image prompts. The GM plays this in German; every deliverable this skill
writes for players/GM must be German, with three exceptions: this document and
all `references/*` stay English; Role names (Solo, Netrunner, ...) and PDF field
labels stay in their original English CPR form even inside German text; and the
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
`references/cpr-rules-summary.md`).

## Step 5: Generate each PC

For each PC, using `references/cpr-rules-summary.md` (stats/skills/DVs) and
`references/roles-and-archetypes.md` (Role Ability) and
`references/weapons-armor-gear.md` (starting gear): write Rank 0 stats/skills/gear,
a lifepath-flavored German background tied to the crew concept and to the
scenario, and a portrait image prompt built from the GM's selected style preset
(Step 2) in `references/style-guide.md` plus its universal "Portrait-Specific
Additions". Assemble a character JSON matching the **Character JSON Schema**
below, write it to the run's output folder, then run:

```bash
python3 scripts/fill_character_sheet.py <character.json> <output-folder>/<handle-slug>.pdf
```

Portrait compositing is driven by the `portrait_image_path` key in the JSON itself
(set it to the portrait file's path before running the command above, or leave it
`null` to skip — there is no separate CLI flag for this).

Also write a Markdown version of the same character for quick reference.

### Character JSON Schema

All keys required except `portrait_image_path`. `skills` keys must be normalized
skill names present in `assets/skills_field_map.json` (57 entries covering the
sheet's primary skill list) — the script raises an error naming any skill you use
that isn't in that map, so treat that as a sign to pick a different/adjacent skill
name rather than inventing a field.

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
  "skills": {"Athletics": 4, "Shoulder Arms": 6},
  "weapons": [{"name": "Medium Pistol", "dmg": "2d6", "ammo": "10(c)", "rof": "2", "notes": ""}],
  "armor": {"head": {"sp": 0, "penalty": 0}, "body": {"sp": 11, "penalty": 0}, "shield": {"sp": 0, "penalty": 0}},
  "fashion": "string",
  "role_specific_lifepath": "string",
  "notes": "string",
  "portrait_image_path": "optional/path/to/portrait.png, or null"
}
```

Known constraint: the sheet's text fields do not auto-shrink, so a value that is
too long for its printed box is silently clipped in the rendered PDF (the stored
data stays correct — only the print is cut off). Keep `handle` to roughly 18
characters and `role_ability` to roughly 11 (e.g. "Combat Awareness" prints as
"Combat Awar"); wide or all-caps text clips even sooner, and German text tends to
run longer than English, so lean toward brevity.

Known constraint: umlauts (ä/ö/ü) in `weapons[].name`, `weapons[].notes`,
`fashion`, and `role_specific_lifepath` render correctly in mupdf-family viewers
(mutool, zathura) but may render as blank/mangled in poppler-based viewers
(evince, Okular) — a font-encoding limitation baked into the official PDF's
per-field widget resources, not something this skill's fill step can fix. The
stored field data is always correct regardless of viewer; only some renderers
mis-display it. Mention this to the GM if they use evince/Okular and see garbled
weapon names or fashion text.

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
and run:

```bash
python3 scripts/fill_mook_sheet.py <mook.json> <output-folder>/<name-slug>.pdf
```

For 1-2 more detailed named NPCs, write a fuller German Markdown stat block plus
an image prompt (the GM's selected style preset from `references/style-guide.md`,
no portrait-specific additions needed unless it's a portrait-framed NPC image).

### Mook JSON Schema

All fields required except `weapons` entries beyond the first, which may be
omitted (the sheet has 4 weapon slots; unused ones are simply left blank).

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
climax fight, and one regional overview map showing where in Night City
this one-shot takes place: write an English image-generation prompt
appending the GM's selected style preset from `references/style-guide.md`,
plus the relevant universal Portrait-, Battlemap-, or Map-Specific
Additions as applicable. The regional map plots every named location from
Step 6's scenes onto a single image in their scene sequence — see
"Map-Specific Additions" in the style guide for what to label and how.
Save all prompts into `<output-folder>/image-prompts/`, one file per image
(the map as `map-regional-overview.txt`), each labeled with the German
name/scene it belongs to, since these are meant to be run through the GM's
own external image tool. After writing the map prompt, add one line to the
GM guide directly below its premise section: "**Regionale Karte:** siehe
`image-prompts/map-regional-overview.txt`" — matching how NPC blocks
already point to their own image-prompt file.

## Step 9: Assemble the output folder

Write everything into a fresh dated folder: `oneshots/YYYY-MM-DD-<slug>/`
containing: character PDFs + Markdown, the GM guide (German — the single
scenario-plus-GM-notes document from Step 6, closed out with Step 10's gaps
section), Mook Sheet PDFs, and `image-prompts/`. If any PDF fill step
fails, report the failing field name and fall back to delivering that
character's Markdown sheet only — never silently ship an incomplete PDF without
saying so.

## Step 10: Report gaps

If any rule, Role Ability, skill, weapon stat, armor value, or gear item used in this
specific one-shot wasn't covered by the free reference material — flagged as
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
