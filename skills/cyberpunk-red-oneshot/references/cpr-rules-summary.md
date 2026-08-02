# Cyberpunk RED — Core Rules Summary

Sourced exclusively from R. Talsorian Games' free Cyberpunk RED Easy Mode rules,
as published on the public Roll20 Compendium
(<https://roll20.net/compendium/cpunk/Free%20Basic%20Rules>). Nothing in this
file is drawn from the paid core rulebook or from general knowledge of the
system — where the free source doesn't cover something, that gap is called out
explicitly (see **Netrunning** below) rather than filled in by guesswork.

## Core Dice Mechanic

STAT + Skill + 1d10. Opposed checks: attacker's total vs. defender's total,
defender wins ties. Task resolution: attacker's total vs. a Difficulty Value (DV).
Critical Success on a natural 10 (roll an extra 1d10 and add). Critical Failure on
a natural 1 (roll an extra 1d10 and subtract).

## The Ten Stats

| Abbreviation | Name | Description |
|---|---|---|
| INT | Intelligence | General brightness and awareness |
| REF | Reflexes | Response time and coordination; used for ranged weapons |
| DEX | Dexterity | Athletic ability; used for melee and brawling |
| TECH | Technique | Ability to manipulate tools and instruments |
| COOL | Cool | Ability to impress and influence others |
| WILL | Will | Determination and courage |
| LUCK | Luck | Special stat for resource expenditure |
| MOVE | Movement | Speed when running, swimming, climbing |
| BODY | Body | Raw strength and endurance |
| EMP | Empathy | Ability to relate to and understand others |

## Difficulty Values

| Difficulty | Description | DV |
|---|---|---|
| Everyday | Most people can do this | 13 |
| Difficult | Hard without training | 15 |
| Professional | Requires actual training | 17 |
| Heroic | Only the best can accomplish | 21 |
| Incredible | Olympian-level feat | 24 |

## Basic Combat Sequence

1. Initiative: each combatant rolls REF + 1d10, acts in descending order.
2. Per turn: 1 Move Action + 1 other Action.
3. Move Action: move up to MOVE x 2 meters.
4. Other Actions: Attack, Grab, Choke, Throw, Get Up, Reload, Run, Stabilize, Use
   Skill, Use Object, Hold Action.
5. Attack resolution differs by type: ranged (REF-based), melee (DEX-based),
   brawling.
6. Damage: attacker rolls weapon damage; defender's armor (SP) reduces it; armor
   loses 1 SP per hit taken.
7. Wound states: Lightly Wounded (no penalty) -> Seriously Wounded (-2 to all
   actions) -> Mortally Wounded (-4 to checks, -6 MOVE, must make Death Saves).

## Skills

Source: [Playing the Game](https://roll20.net/compendium/cpunk/Rules:Playing%20the%20Game?expansion=0)
(Skills section), Cyberpunk RED Easy Mode, Roll20 Compendium. This is the
complete skill list published on that free page — 41 skills. `Skill (STAT)`:

| Skill | Stat |
|---|---|
| Accounting | INT |
| Acting | COOL |
| Athletics | DEX |
| Brawling | DEX |
| Bribery | COOL |
| Bureaucracy | INT |
| Business | INT |
| Composition | INT |
| Conceal/Reveal Object | INT |
| Concentration | WILL |
| Conversation | EMP |
| Criminology | INT |
| Cryptography | INT |
| Deduction | INT |
| Drive Land Vehicle | REF |
| Education | INT |
| Electronics/Security Tech | TECH |
| Evasion | DEX |
| First Aid | TECH |
| Forgery | TECH |
| Handgun | REF |
| Human Perception | EMP |
| Interrogation | COOL |
| Library Search | INT |
| Local Expert | INT |
| Melee Weapon | DEX |
| Paramedic | TECH |
| Perception | INT |
| Persuasion | COOL |
| Photography/Film | TECH |
| Pick Lock | TECH |
| Pick Pocket | TECH |
| Play Instrument | TECH |
| Resist Torture/Drugs | WILL |
| Shoulder Arms | REF |
| Stealth | DEX |
| Streetwise | COOL |
| Tactics | INT |
| Tracking | INT |
| Trading | COOL |
| Wardrobe & Style | COOL |

<!-- verify: cross-checked against the 67 `LVL<Skill Name> <STAT>`-pattern fields
     in assets/character_sheet_fields.json (Task 2). The official Fillable
     Character Sheet PDF is the FULL Cyberpunk RED core-rulebook character
     sheet, not the Easy Mode sheet, so it carries a number of skills the free
     Easy Mode rules text above does not define anywhere. The following
     `LVL<Skill Name> <STAT>` fields have NO corresponding entry in the table
     above (stat below is read off the PDF field name itself, not confirmed
     against any free-source rules text -- do not treat these as verified):
     Air Vehicle Tech (TECH), Animal Handling (INT), Archery (REF),
     Autofire (REF), Basic Tech (TECH), Contortionist (DEX), Cybertech (TECH),
     Dance (DEX), Demolitions (TECH), Endurance (WILL), Heavy Weapons (REF),
     Land Vehicle Tech (TECH), Lip Reading (INT), Martial Arts (DEX),
     Paint/Draw/Sculpt (TECH), Personal Grooming (COOL),
     Pilot Air Vehicle (REF) [PDF field literally reads "LVLPilor Air Vehicle x2
     REF" -- "Pilor" appears to be a typo in the official PDF for "Pilot"],
     Pilot Sea Vehicle (REF), Riding (REF), Sea Vehicle Tech (TECH),
     Wilderness Survival (INT). Any one-shot content that calls for these
     skills should be flagged in the GM guide as "not verified against free
     rules -- confirm against your core rulebook", the same treatment given to
     Netrunning below.

     Separately, three fields in the catalog ("LVL", "LVLStreetslang",
     "LVLYour Home") plus seven numbered fields ("LVL_2".."LVL_8") do not
     correspond to named skills at all -- they read as blank/custom
     skill-entry rows and non-skill Lifepath fields that happen to share the
     sheet's "LVL" field-name prefix, not skills missing from this table.

     Also note for whoever builds assets/skills_field_map.json (Task 9):
     Handgun (REF) above IS on the free-source list, but on the PDF it exists
     only as a bare "Handgun" field tied to the Weapons table (alongside
     "Weaponstech" and "Melee Weapon Total"), not as a
     "LVLHandgun REF"-pattern master-skill-list field. Likewise Concentration,
     Conceal/Reveal Object, Local Expert, and Play Instrument above ARE present
     on the PDF, but under field names outside the "LVL<Skill Name> <STAT>"
     pattern (e.g. "Concentration Level", "Conceal/Reveal LVL",
     "Local Expert 1"/"Local Expert 2"/"Local Expert 3", "Instrument 1"/
     "Instrument 2") -- they were missed by a search scoped to fields starting
     with "LVL" and will need separate handling when the field map is built. -->

## Netrunning

R. Talsorian's free Cyberpunk RED Easy Mode rules do **not** include
Netrunning / NET architecture rules. No page for this exists at the expected
location in the free Roll20 Compendium; the Easy Mode "Playing the Game" page
itself states that Headshots, Martial Arts, Netrunning, and Vehicle Combat are
covered only in the paid Cyberpunk RED Core Book
(<https://roll20.net/compendium/cpunk/Rules:Playing%20the%20Game?expansion=0>),
and the free rules index
(<https://roll20.net/compendium/cpunk/Free%20Basic%20Rules>) links to no
Netrunning-specific page.

Any one-shot that includes a Netrunner PC or a NET-based scene must have its
Netrunning mechanics flagged in the GM guide as **"not verified against free
rules — confirm against your core rulebook"** rather than having Netrunning
rules invented wholesale for this skill.
