# Cyberpunk RED — Weapons, Armor, and Starting Gear

Sourced from R. Talsorian Games' free Cyberpunk RED Easy Mode rules on the
public Roll20 Compendium, the same source used by `cpr-rules-summary.md` and
`roles-and-archetypes.md`. For this file, the following pages were actually
fetched and read: the Pregenerated Characters index
(<https://roll20.net/compendium/cpunk/Rules:Pregenerated%20Characters?expansion=0>),
each of the five individual pregen character pages it links to (Forty/Rockerboy,
Mover/Solo, Torch/Tech, Redtail/Medtech, 24-7/Media — e.g.
<https://roll20.net/compendium/cpunk/Rules:Forty?expansion=0>), the five free
Role pages (Rockerboy, Solo, Tech, Medtech, Media — already fetched in Task 6),
[Reading Your Character Sheet](https://roll20.net/compendium/cpunk/Rules:Reading%20Your%20Character%20Sheet?expansion=0),
[Playing the Game](https://roll20.net/compendium/cpunk/Rules:Playing%20the%20Game?expansion=0),
and the [Dirty Cop NPC stat block](https://roll20.net/compendium/cpunk/NPCs:Dirty%20Cop?expansion=0).

**The honest result of that research: the free Easy Mode compendium does not
publish a weapons table, an armor table, or an itemized starting-gear list for
any pregenerated character or Role.** The Pregenerated Characters index and
all five individual pregen pages (Forty, Mover, Torch, Redtail, 24-7) contain
only narrative background text about each character — no weapon/armor stat
blocks, no gear lists. None of the five free Role pages list starting
equipment either. This was checked with repeated, differently-worded fetches
against each page — for two of the five pregen pages (Forty, Mover), that
included an explicit request for verbatim page content — to make sure a table
wasn't simply being summarized away. The pages genuinely don't contain
weapon/armor stat data in the free tier.

## What the Free Source Actually Confirms

This is the complete set of concrete weapon/armor/gear data points found
anywhere in the free source:

- **Weapon existence, no stats**: the Playing the Game page uses "Heavy
  Pistol" and "machete" as example weapon names in prose (e.g. drawing a
  "Heavy Pistol in your left hand ... then walk down that disgusting hallway
  to stab your victim with the machete") — confirms these items exist as
  weapon types in the setting, but gives no DMG, ROF, or ammo values for
  either.
- **One full NPC loadout**: the `NPCs:Dirty%20Cop` stat block (not a PC
  pregen — a generic NPC) lists: weapon `Very Heavy Pistol`; ammo
  `Basic Very Heavy Pistol Bullets [16]`; armor `Kevlar®, SP: 7`; gear
  `Radio Communicator`. No DMG or ROF number is given for the Very Heavy
  Pistol on that page — only its name, and its ammo type's name. The
  `Kevlar® SP: 7` value is the one directly-confirmed numeric armor value in
  this entire file.
- **Column semantics, no example values**: Reading Your Character Sheet
  explains what belongs in each weapons-table column — weapon type, "DMG (how
  many d6s you roll then add up to determine damage)", ammo capacity, "ROF
  (Rate of Fire ...)", and "any notes" — and states armor is listed as "type
  and SP" — but supplies no actual weapon or armor with numbers filled in.
- **ROF/SP game mechanics** (not specific items): Playing the Game confirms
  the general ROF and armor-SP-degradation mechanics already documented in
  `cpr-rules-summary.md`'s Basic Combat Sequence section.
- **Media gear flavor text**: the `24-7` pregen page (Media Role) states,
  in narrative prose, "You've got a vidlink and a press pass, and you're not
  afraid to use them" — confirms these two items as this specific pregen's
  gear flavor, though not as a mechanical/itemized gear-table entry with any
  stats attached.

Everything below this point that isn't one of the data points above is
**explicitly estimated from general published knowledge of Cyberpunk RED, not
verified against any free source**, and is labeled accordingly. GMs should
confirm exact numbers against the core rulebook before treating them as
mechanically exact — the same caveat `roles-and-archetypes.md` gives for its
five unverified Roles.

## Common Starting Weapons

`(estimated — not verified against free rules, except the "Very Heavy Pistol"
row's WEAPON name and AMMO type name, which are confirmed per NPCs:Dirty Cop
above; its DMG and ROF values are still estimated)`

Columns match the Character Sheet PDF's weapon-row fields
(`WEAPONRow{n}`/`DMGRow{n}`/`AMMORow{n}`/`ROFRow{n}`/`NOTESRow{n}`,
confirmed present in `assets/character_sheet_fields.json`, Task 2).

| WEAPON | DMG | AMMO | ROF | NOTES |
|---|---|---|---|---|
| Medium Pistol | 2d6 | Medium Pistol | 2 | Sidearm |
| Heavy Pistol | 3d6 | Heavy Pistol | 2 | Named on the free source (Playing the Game), no stats given there |
| Very Heavy Pistol | 4d6 | Very Heavy Pistol | 1 | Weapon name + ammo type name confirmed via `NPCs:Dirty Cop` |
| SMG | 2d6 | Medium Pistol | 3 | Autofire-capable in the core rules; Autofire itself is unverified (see `cpr-rules-summary.md`) |
| Shotgun | 5d6 | Shotgun Shell | 1 | Close-range |
| Assault Rifle | 5d6 | Rifle | 3 | Two-handed |
| Sniper Rifle | 5d6 | Rifle | 1 | Two-handed, aimed shots |
| Knife | 1d6 | — | 2 | Melee |
| Machete | 2d6 | — | 2 | Melee; named on the free source (Playing the Game), no stats given there |
| Baseball Bat | 2d6 | — | 2 | Melee, improvised-weapon flavor |

## Armor

`(estimated — not verified against free rules, except the Kevlar SP value,
which is directly confirmed per NPCs:Dirty Cop above)`

Columns match the Character Sheet PDF's per-location armor fields
(`SPHead`/`PENALTYHead`, `SPBody`/`PENALTYBody`, `SPShield`/`PENALTYShield`,
plus the separate `Head Armor`/`Body Armor`/`Shield` name fields — all
confirmed present in `assets/character_sheet_fields.json`, Task 2).

| Location | Armor | SP | PENALTY |
|---|---|---|---|
| Body | Kevlar® | 7 | 0 |
| Body | Leather Jacket | 4 | 0 |
| Body | Light Armorjacket | 11 | -2 |
| Head | Kevlar Helmet | 7 | 0 |
| Head | Light Helmet | 11 | -2 |
| Shield | Riot Shield | 12 | 0 |

The Body row's `Kevlar® / SP 7` entry is the only directly-sourced value in
this table (`Kevlar® SP: 7` on `NPCs:Dirty Cop`). Every other row, and the
`PENALTY` column entirely, is estimated from general published knowledge of
Cyberpunk RED's armor tiers, not confirmed against any free source.

## Gear-by-Role Starting Loadouts

**All ten Roles below are marked `(estimated — not verified against free
rules)`.** As documented above, none of the five free pregen character pages
(which cover Rockerboy, Solo, Tech, Medtech, and Media) list itemized starting
gear — they're narrative-only — and none of the five free Role pages list
starting equipment either. There is therefore no free-source basis for any
Role's starting loadout, verified or otherwise. Where a Role's flavor text
draws on its Role Ability, that Role Ability description itself may be
verified per `roles-and-archetypes.md` (noted below) — but the gear list
attached to it here is still an estimate, not sourced.

Each entry lists 2-4 sensible Rank 0 items: one weapon, one armor piece, and
one Role-flavored gear item tied to that Role's ability or theme.

### Rockerboy `(estimated — not verified against free rules)`

Role Ability verified per `roles-and-archetypes.md`: Charismatic Impact.

- Weapon: Heavy Pistol
- Armor: Leather Jacket (SP 4)
- Gear: Portable amp/speaker rig, or recording gear for spoken-word/poetry

### Solo `(estimated — not verified against free rules)`

Role Ability verified per `roles-and-archetypes.md`: Combat Awareness.

- Weapon: Very Heavy Pistol (name/ammo verified per `NPCs:Dirty Cop`; loadout
  pairing is estimated) and a Knife as backup
- Armor: Light Armorjacket (SP 11)
- Gear: Combat medical kit (Stabilize action support)

### Tech `(estimated — not verified against free rules)`

Role Ability verified per `roles-and-archetypes.md`: Maker.

- Weapon: Medium Pistol
- Armor: Leather Jacket (SP 4)
- Gear: Toolkit (Electronics/Security Tech), spare cybertech parts

### Medtech `(estimated — not verified against free rules)`

Role Ability verified per `roles-and-archetypes.md`: Medicine.

- Weapon: Medium Pistol
- Armor: Leather Jacket (SP 4)
- Gear: Medtech bag (First Aid/Paramedic supplies), trauma team pager

### Media `(estimated — not verified against free rules)`

Role Ability verified per `roles-and-archetypes.md`: Credibility.

- Weapon: Medium Pistol (concealed)
- Armor: none by default, or a concealed Leather Jacket (SP 4)
- Gear: Vidlink/recorder and press pass — both directly referenced in the
  `24-7` pregen's narrative text ("a vidlink and a press pass"), though only
  as flavor text, not as itemized mechanical gear entries

### Netrunner `(estimated — not verified against free rules)`

Role Ability unverified per `roles-and-archetypes.md`: Interface
(best-effort description; no free-source page exists for this Role).

- Weapon: Medium Pistol
- Armor: Leather Jacket (SP 4)
- Gear: Cyberdeck and NET-architecture programs — mechanically unsupported by
  the free rules (see the Netrunning gap in `cpr-rules-summary.md`); treat
  any Netrunner one-shot content as GM-adjudicated

### Exec `(estimated — not verified against free rules)`

Role Ability unverified per `roles-and-archetypes.md`: Teamwork
(best-effort description; no free-source page exists for this Role).

- Weapon: Medium Pistol
- Armor: Light Armorjacket (SP 11)
- Gear: Corporate credentials/agent, encrypted commlink

### Fixer `(estimated — not verified against free rules)`

Role Ability unverified per `roles-and-archetypes.md`: Operator
(best-effort description; no free-source page exists for this Role).

- Weapon: Heavy Pistol
- Armor: Leather Jacket (SP 4)
- Gear: Black-market contact list/burner phones, cred-chip stash

### Lawman `(estimated — not verified against free rules)`

Role Ability unverified per `roles-and-archetypes.md`: Backup
(best-effort description; no free-source page exists for this Role).

- Weapon: Heavy Pistol, matching the confirmed `NPCs:Dirty Cop` NPC's
  `Very Heavy Pistol` in spirit (weapon choice itself is estimated)
- Armor: Kevlar® (SP 7 — verified value per `NPCs:Dirty Cop`, paired here
  with a Lawman by estimated inference only)
- Gear: Badge, Radio Communicator (item name verified per `NPCs:Dirty Cop`,
  its assignment to the Lawman Role here is estimated)

### Nomad `(estimated — not verified against free rules)`

Role Ability unverified per `roles-and-archetypes.md`: Moto
(best-effort description; no free-source page exists for this Role).

- Weapon: Shotgun
- Armor: Leather Jacket (SP 4)
- Gear: Vehicle toolkit, family/pack contact info

## Notes for Task 10 (`fixtures/sample_character.json`)

- Weapon rows should populate `WEAPONRow{n}`/`DMGRow{n}`/`AMMORow{n}`/
  `ROFRow{n}`/`NOTESRow{n}` pairs (6 rows available on the sheet).
- Armor should populate `Head Armor`/`SPHead`/`PENALTYHead`,
  `Body Armor`/`SPBody`/`PENALTYBody`, and `Shield`/`SPShield`/`PENALTYShield`.
- Any weapon, armor, or gear item drawn from this file that isn't the
  directly-verified Kevlar/SP7 or Very Heavy Pistol name/ammo entries should
  be treated by the fixture/GM guide as an estimate, not a rules-verified
  fact — consistent with the flags in this file.
