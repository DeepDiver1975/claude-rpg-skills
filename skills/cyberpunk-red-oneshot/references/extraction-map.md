# Cyberpunk RED — Core Rulebook Extraction Map

This file is the schema-and-provenance companion to `scripts/extract_rules.py`. It
is used **only** when a GM who owns the Cyberpunk RED core rulebook opts into the
local extraction flow (see SKILL.md "Step 0"). It replaces the free-source
estimates in `cpr-rules-summary.md`, `roles-and-archetypes.md`, and
`weapons-armor-gear.md` with values read from the GM's own book.

## Copyright — read first

This file contains **only facts about the book's structure** (section headings and
printed page numbers, which are not copyrightable expression) plus the *target
shape* for the data. It reproduces none of R. Talsorian's rules text, so it is safe
to ship.

The book's actual content — the PDF, the raw text pulled from it under `data/raw/`,
and the structured `data/*.json` — is derived from a paid product and is **local
only**: never commit it, never redistribute it. `data/` is gitignored and
`extract_rules.py` refuses to write anywhere else. Use this only with a book you own.

## How the two halves fit together

1. `scripts/extract_rules.py` (the authoritative section list lives there) pulls
   page-ranged raw text into `data/raw/<section>.txt` and writes provenance to
   `data/manifest.json`.
2. The skill (Claude) reads each `data/raw/<section>.txt` and structures it into the
   `data/<domain>.json` shape below, following the same verified/estimated honesty
   the reference files already use — but now every value is sourced from the book.

**Printed vs PDF pages:** the page numbers below are the book's *printed* Contents
numbers. They differ from physical PDF pages by a near-constant offset (~+9), and
some chapters open on a stylised art page several pages before their real content.
The script therefore locates each section by searching for its heading line near
the expected page and extends the end generously, rather than trusting fixed pages.

## Sections and their target files

| Section (`--section`) | Heading in text layer | Printed pp. | Structured output |
|---|---|---|---|
| `roles` | Roles | 29–40 | `roles.json` (overview) |
| `statistics` | What are Statistics? | 72–81 | `stats.json` |
| `weapons-armor` | Weapons and Armor | 91–99 | `weapons.json`, `armor.json` |
| `gear` | Your Outfit | 99–107 | `gear.json` |
| `cyberware` | Cyberware | 110–121 | `cyberware.json` |
| `difficulty-values` | Resolving Actions with Skills | 128–130 | `difficulty-values.json` |
| `skills` | Skill List | 130–142 | `skills.json` |
| `role-abilities` | Role Abilities | 142–167 | `roles.json` (ability detail) |
| `combat` | Friday Night Firefight | 167–189 | `combat.json` |
| `vehicles` | Vehicle Combat | 189–193 | `vehicles.json` |
| `netrunning` | Netrunning | 195–219 | `netrunning.json` |
| `critical-injuries` | Wound States and Critical Injuries | 220–227 | `critical-injuries.json` |
| `drugs` | Street Drugs | 227–230 | `drugs.json` |

## Target JSON schemas

Keep keys and column names aligned with the existing references and the PDF field
maps so the fill scripts (`fill_character_sheet.py`, `fill_mook_sheet.py`) consume
them unchanged. Every file should carry a `"_source"` string, e.g.
`"Cyberpunk RED core rulebook (locally extracted)"`, so the GM guide can cite it.

### `skills.json`
Full `{skill: STAT}` map — supersedes the 41 free-source skills and resolves the 21
skill→STAT mappings `cpr-rules-summary.md` flags as unverified.
```json
{"_source": "...", "skills": {"Autofire": "REF", "Handgun": "REF", "Martial Arts": "DEX"}}
```

### `stats.json`
The ten stats, and any derived-stat formulas (HP, Humanity, etc.) the book defines.
```json
{"_source": "...", "stats": {"INT": "Intelligence — ..."}, "derived": {"hp": "formula"}}
```

### `difficulty-values.json`
The named DV ladder plus any task-specific DV tables.
```json
{"_source": "...", "ladder": [{"name": "Everyday", "dv": 13}], "tasks": {"...": 15}}
```

### `weapons.json`
Full weapon catalogue. Columns mirror the sheet fields
(`WEAPONRow{n}`/`DMGRow{n}`/`AMMORow{n}`/`ROFRow{n}`/`NOTESRow{n}`).
```json
{"_source": "...", "weapons": [
  {"name": "Medium Pistol", "dmg": "2d6", "ammo": "Medium Pistol", "rof": 2, "hands": 1, "type": "Pistol", "notes": ""}
]}
```

### `armor.json`
Full armor catalogue. Mirrors the per-location sheet fields (`SP*`/`PENALTY*`).
```json
{"_source": "...", "armor": [
  {"name": "Light Armorjack", "sp": 11, "penalty": 0, "locations": ["Head", "Body"]}
]}
```

### `gear.json`
General gear/outfit items and per-Role starting loadouts (weapon + armor + gear).
```json
{"_source": "...", "gear": [{"name": "Agent", "notes": "..."}],
 "role_loadouts": {"Solo": {"weapons": ["..."], "armor": "...", "gear": ["..."]}}}
```

### `roles.json`
All ten Roles, each with its Role Ability name, description, and rank mechanics —
supersedes the five unverified Roles in `roles-and-archetypes.md`.
```json
{"_source": "...", "roles": [
  {"role": "Solo", "ability": "Combat Awareness", "description": "...", "rank_mechanics": "..."}
]}
```

### `cyberware.json`
```json
{"_source": "...", "cyberware": [
  {"name": "Cyberaudio Suite", "humanity_loss": "2d6", "install": "...", "effect": "..."}
]}
```

### `combat.json`
Actions, ranged/melee resolution, ROF, and anything the free
`cpr-rules-summary.md` combat section only sketches.
```json
{"_source": "...", "actions": [{"name": "Aimed Shot", "effect": "..."}], "ranged": "...", "melee": "..."}
```

### `vehicles.json`
```json
{"_source": "...", "vehicles": [{"name": "...", "sdp": 0, "seats": 0, "speed": "...", "notes": ""}]}
```

### `netrunning.json`
Programs, NET actions, and Interface mechanics — closes the Netrunning gap
`cpr-rules-summary.md` cannot cover from the free source.
```json
{"_source": "...", "programs": [{"name": "...", "class": "Attacker", "atk": 0, "def": 0, "effect": "..."}],
 "net_actions": [{"name": "...", "effect": "..."}], "interface": "..."}
```

### `critical-injuries.json`
```json
{"_source": "...", "wound_states": [{"name": "...", "effect": "..."}],
 "critical_injuries": [{"roll": "2", "name": "...", "effect": "..."}]}
```

### `drugs.json`
```json
{"_source": "...", "drugs": [{"name": "...", "effect": "...", "duration": "...", "side_effects": "..."}]}
```
