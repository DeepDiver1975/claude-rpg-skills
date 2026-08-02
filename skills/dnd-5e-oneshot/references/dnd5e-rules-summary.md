# D&D 5e (2024) Core Rules Summary

Source: System Reference Document 5.2.1 ("SRD 5.2.1") by Wizards of the Coast
LLC, licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Content below is summarized/rewritten from the SRD's "Playing the Game" and
"Rules Glossary" sections; convenience source consulted:
[downfallx/dnd-5e-srd-markdown](https://github.com/downfallx/dnd-5e-srd-markdown)
(`playing-the-game.md`, `rules-glossary.md`), itself a CC BY 4.0 Markdown
conversion of the official SRD. Unlike the free-tier situation this project
hit with Cyberpunk RED, SRD 5.2.1 is the *complete, official* core-rules
reference — nothing in this file is estimated or unverified.

## Core Mechanic: D20 Tests

Three kinds of rolls all work the same way: **ability checks**, **saving
throws**, and **attack rolls**.

1. Roll 1d20 (two d20s if you have Advantage or Disadvantage — take the
   higher for Advantage, the lower for Disadvantage; if both apply, roll
   just one d20 with neither).
2. Add the relevant ability modifier.
3. Add your Proficiency Bonus, if you're proficient in whatever's being
   used (a skill, a saving-throw type, a weapon, a tool, a spell).
4. Compare the total to a target number: a **DC** (Difficulty Class) for
   checks and saves, or a target's **AC** (Armor Class) for attack rolls.
   Meet or beat it to succeed.

A natural 20 on an attack roll always hits; a natural 1 always misses.
Ability checks/saves have no such auto-success/-fail rule in the base game.

## The Six Abilities

| Ability | Measures | Typical check use | Typical save use | Attack use |
|---|---|---|---|---|
| Strength (STR) | Physical might | Lift/push/pull/break | Physically resist force | Melee weapon/Unarmed Strike |
| Dexterity (DEX) | Agility, reflexes, balance | Move nimbly/quietly | Dodge out of harm's way | Ranged weapon |
| Constitution (CON) | Health, stamina | Push body past limits | Endure a toxic hazard | — (no attacks use CON) |
| Intelligence (INT) | Reasoning, memory | Reason or remember | Recognize an illusion | Some spells |
| Wisdom (WIS) | Perceptiveness, mental fortitude | Notice things | Resist a mental assault | Some spells |
| Charisma (CHA) | Confidence, poise, charm | Influence/entertain/deceive | Assert your identity | Some spells |

**Ability modifier** = `floor((score - 10) / 2)`. Reference table:

| Score | Mod | Score | Mod |
|---|---|---|---|
| 1 | −5 | 16–17 | +3 |
| 2–3 | −4 | 18–19 | +4 |
| 4–5 | −3 | 20–21 | +5 |
| 6–7 | −2 | 22–23 | +6 |
| 8–9 | −1 | 24–25 | +7 |
| 10–11 | +0 | 26–27 | +8 |
| 12–13 | +1 | 28–29 | +9 |
| 14–15 | +2 | 30 | +10 |

Level-1 pregens use scores in the 8–17 range in practice.

## Difficulty Class (DC) Ladder

| Task difficulty | DC | Task difficulty | DC |
|---|---|---|---|
| Very easy | 5 | Very hard | 25 |
| Easy | 10 | Nearly impossible | 30 |
| Medium | 15 | | |
| Hard | 20 | | |

Use this for any ability check the GM guide calls for (Step 6 of SKILL.md).

## Proficiency Bonus by Level

| Level | Bonus | Level | Bonus |
|---|---|---|---|
| 1–4 | +2 | 17–20 | +6 |
| 5–8 | +3 | 21–24 | +7 |
| 9–12 | +4 | 25–28 | +8 |
| 13–16 | +5 | 29–30 | +9 |

Level-1 pregens (this skill's default, see SKILL.md Step 1) always use +2.
The bonus is never added twice to the same roll, even if two separate
proficiencies would both apply. **Expertise** (a Rogue/Bard feature) doubles
the Proficiency Bonus for one specific skill check.

## The 18 Skills and Their Governing Ability

| Skill | Ability | Example use |
|---|---|---|
| Acrobatics | DEX | Stay on your feet, acrobatic stunts |
| Animal Handling | WIS | Calm or train an animal |
| Arcana | INT | Recall lore about spells/magic items/planes |
| Athletics | STR | Jump, swim, break something |
| Deception | CHA | Tell a convincing lie, wear a disguise |
| History | INT | Recall lore about historical events/nations |
| Insight | WIS | Discern a person's mood/intentions |
| Intimidation | CHA | Awe or threaten someone |
| Investigation | INT | Find obscure info, deduce how something works |
| Medicine | WIS | Diagnose an illness, determine cause of death |
| Nature | INT | Recall lore about terrain/plants/animals/weather |
| Perception | WIS | Notice something easy to miss |
| Performance | CHA | Act, tell a story, perform music/dance |
| Persuasion | CHA | Honestly convince someone of something |
| Religion | INT | Recall lore about gods/rituals/holy symbols |
| Sleight of Hand | DEX | Pick a pocket, conceal a handheld object |
| Stealth | DEX | Escape notice, hide |
| Survival | WIS | Track, forage, find a trail, avoid hazards |

A skill check total = ability modifier + Proficiency Bonus (only if the
character is proficient in that skill) + any circumstantial bonus.
**Passive Perception** = `10 + Perception check total` (no roll).

## Turn Structure and Combat Basics

A round ≈ 6 seconds. Combat: (1) establish positions, (2) everyone rolls
**Initiative** = `1d20 + DEX modifier` (surprised combatants roll with
Disadvantage), (3) take turns in Initiative order (highest first) until the
fight ends. On your turn: move up to your Speed and take one action, in
either order (can split movement around the action); some features also
grant a Bonus Action or Reaction. Melee reach is 5 ft by default; leaving a
foe's reach without Disengaging provokes an Opportunity Attack.

**Grid convention**: 1 square = 5 feet. This skill's battlemap image prompts
(SKILL.md Step 8) must specify a 5-foot-per-square grid — this is 5e's actual
default unit, not a stylistic choice, so don't copy a different grid size
from another game's convention.

**Cover**: Half cover = +2 AC/DEX-save; Three-Quarters cover = +5 AC/DEX-save;
Total cover = can't be targeted directly.

## Hit Points, Damage, and Death

- **HP loss**: subtract damage from current HP; no other effect until 0 HP.
  At half HP or fewer, a creature is "Bloodied" (flavor only, no mechanical
  penalty by itself).
- **Critical hit** (natural 20 on an attack): roll all the attack's damage
  dice twice, add modifiers once.
- **Resistance** halves damage of that type (round down); **Vulnerability**
  doubles it; **Immunity** negates it entirely. Multiple instances of the
  same type don't stack.
- **Dropping to 0 HP**: a PC falls Unconscious (not dead) and starts making
  **Death Saving Throws** at the start of each of their turns: roll 1d20,
  no ability modifier — 10+ is a success, below 10 is a failure. Three
  successes = Stable; three failures = dead. A natural 1 counts as two
  failures; a natural 20 immediately regains 1 HP. Taking any damage at 0 HP
  is an automatic failure (two failures if it's a critical hit); damage at
  0 HP that equals/exceeds HP maximum kills outright (Massive Damage).
  A monster, by contrast, simply dies at 0 HP unless the GM rules otherwise.
- **Temporary HP**: absorbed before real HP is touched; doesn't stack (keep
  the higher pool, don't add); lost at the end of a Long Rest if unused.
- **Healing**: restored HP can't exceed HP maximum; excess is lost.

## Condensed Conditions Glossary

| Condition | Key effects |
|---|---|
| Blinded | Can't see (auto-fail sight-based checks); attackers have Advantage against you, your attacks have Disadvantage |
| Charmed | Can't attack/target the charmer with harmful effects; charmer has Advantage on social checks against you |
| Deafened | Can't hear (auto-fail hearing-based checks) |
| Exhaustion (levels 1–6) | Cumulative; each level: −2×level on all D20 Tests, Speed −5ft×level; level 6 = death; a Long Rest removes 1 level |
| Frightened | Disadvantage on checks/attacks while the fear source is in sight; can't willingly move closer to it |
| Grappled | Speed 0; Disadvantage on attacks against anyone but the grappler |
| Incapacitated | Can't take actions/Bonus Actions/Reactions; Concentration breaks; can't speak; Disadvantage on Initiative if incapacitated when rolling it |
| Invisible | Unseen unless special senses apply; attacks against you have Disadvantage, yours have Advantage |
| Paralyzed | Incapacitated; Speed 0; auto-fail STR/DEX saves; attacks against you have Advantage and auto-crit within 5 ft (core combat rule) |
| Petrified | Turned to stone; Incapacitated; Speed 0; weight ×10 |
| Poisoned | Disadvantage on attack rolls and ability checks |
| Prone | Movement limited to crawling (or spend half Speed to stand); Disadvantage on your attacks; attackers within 5 ft have Advantage against you, others have Disadvantage |
| Restrained | Speed 0; attacks against you have Advantage, yours have Disadvantage; Disadvantage on DEX saves |
| Stunned | Incapacitated; auto-fail STR/DEX saves; attacks against you have Advantage |
| Unconscious | Incapacitated + Prone; drops what it's holding; attacks against you have Advantage and auto-crit within 5 ft; makes Death Saving Throws if at 0 HP |

## Gap-Reporting Note

Everything above is drawn directly from the official, complete SRD 5.2.1 —
there is no "estimated" content in this file (contrast with the Cyberpunk RED
skill's equivalent reference, which had to guess at large portions of its
own rules). If a one-shot needs a rule genuinely outside the SRD's scope
(e.g. a specific optional rule from "Gameplay Toolbox" that this summary
doesn't cover), flag it per SKILL.md Step 10 rather than improvising it.
