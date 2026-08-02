# D&D 5e (2024) Spellcasting Summary

Source: System Reference Document 5.2.1 ("SRD 5.2.1") by Wizards of the Coast
LLC, licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Spellcasting mechanics summarized from `equipment.md`/`playing-the-game.md`;
spell entries summarized from `classes.md`'s per-class spell lists and
`spells.md`, both in
[downfallx/dnd-5e-srd-markdown](https://github.com/downfallx/dnd-5e-srd-markdown).

**This is a curated shortlist, not the full SRD spell list** (`spells.md`
alone is 300+ KB). It covers enough cantrips and level-1 spells to build a
level-1 pregen for each of the SRD's 8 caster classes. **If a one-shot needs
a spell not on this shortlist, fetch its exact text from `spells.md` (or the
official SRD PDF) before using it — never improvise a spell's mechanical
effect from memory.** If the spell isn't in the SRD's spell list at all
(several familiar 2014-era spells, e.g. Toll the Dead, aren't present in
SRD 5.2.1), that's a Step 10 gap, not something to reconstruct from an
older edition.

## Mechanics

- **Spellcasting ability** is fixed per class (see `classes-and-subclasses.md`
  — INT for Wizard, WIS for Cleric/Druid/Ranger, CHA for Bard/Paladin/
  Sorcerer/Warlock).
- **Spell save DC** = `8 + Proficiency Bonus + spellcasting ability modifier`.
- **Spell attack bonus** = `Proficiency Bonus + spellcasting ability modifier`.
- **Cantrips** are always available, cast at will, no spell slot consumed;
  several scale automatically at character levels 5/11/17 ("Cantrip
  Upgrade") — irrelevant for level-1 pregens.
- **Spell slots**: a level-1 caster has a small number of level-1 slots only
  (Wizard/Sorcerer/Cleric/Druid/Bard: 2; Paladin/Ranger: half-casters, no
  slots until level 2 — a level-1 Paladin/Ranger pregen has spellcasting
  listed as a class feature but no usable slots yet). Warlock uses a
  separate Pact Magic pool that recovers on a Short Rest instead of a Long
  Rest.
- **Known vs. prepared**: Bard/Sorcerer/Ranger/Warlock *know* a fixed list of
  spells; Cleric/Druid/Paladin/Wizard *prepare* a daily list drawn from
  their whole class spell list (Wizard: from the spellbook only).
- **Concentration** ("C" in spell lists below): only one Concentration spell
  active at a time; taking damage while concentrating requires a
  Constitution save (DC 10 or half the damage taken, whichever is higher).
- **Ritual** ("R"): a Ritual-tagged spell can be cast without a slot by
  spending an extra 10 minutes, if the caster has ritual casting (Bard,
  Cleric, Druid, Wizard).

## Bard (CHA)
**Cantrips**: Vicious Mockery (WIS save or 1d6 Psychic + Disadvantage on its
next attack), Mage Hand (spectral hand, minor manipulation, 30 ft, 10 lb
limit), Minor Illusion (minor sound or image), Message (silent whispered
exchange with one target), True Strike (attack with a weapon using your
spellcasting ability instead of STR/DEX).
**Level 1**: Healing Word (Bonus Action, 2d4+mod HP at range), Charm Person
(WIS save or Charmed 1 hr), Faerie Fire (DEX save or outlined/Advantage to
hit, C), Comprehend Languages (understand any language, 1 hr, R),
Dissonant Whispers (WIS save or damage + forced movement), Animal
Friendship (WIS save or a beast is Charmed 24 hr).

## Cleric (WIS)
**Cantrips**: Guidance (touch, +1d4 to one ability check, C), Sacred Flame
(DEX save or 1d8 Radiant, ignores cover), Thaumaturgy (minor divine wonder
effects), Spare the Dying (touch, stabilize a creature at 0 HP).
**Level 1**: Bless (up to 3 allies add 1d4 to attacks/saves, C), Cure Wounds
(touch, 2d8+mod HP), Healing Word (Bonus Action, 2d4+mod HP at range),
Command (WIS save or follow a one-word command), Detect Magic (sense magic
within 30 ft, C, R).

## Druid (WIS)
**Cantrips**: Druidcraft (minor nature effect), Guidance (+1d4 to one
ability check, C), Message, Spare the Dying.
**Level 1**: Cure Wounds, Faerie Fire (C), Entangle (20-ft difficult
terrain, C), Goodberry (10 berries, 1 HP + a day's food each), Animal
Friendship, Speak with Animals (talk to Beasts, 10 min), Longstrider (+10
ft Speed, 1 hr), Detect Magic (C, R).

## Paladin (CHA, half-caster — no cantrips, no usable slots until level 2)
**Level 1 (learned now, usable from level 2)**: Bless (C), Cure Wounds,
Command, Detect Magic (C, R).

## Ranger (WIS, half-caster — no cantrips, no usable slots until level 2)
**Level 1 (learned now, usable from level 2)**: Hunter's Mark (Bonus
Action, +1d6 Force per hit on marked target, C — also a class feature
Rangers have prepared for free, see `classes-and-subclasses.md`), Cure
Wounds, Goodberry, Speak with Animals, Entangle (C), Animal Friendship,
Longstrider, Detect Magic (C, R).

## Sorcerer (CHA)
**Cantrips**: Fire Bolt (ranged spell attack, 1d10 Fire), Mage Hand,
Minor Illusion, Prestidigitation (minor magic trick, up to 3 active
effects), True Strike.
**Level 1**: Magic Missile (3 darts, 1d4+1 Force each, auto-hit), Shield
(Reaction, +5 AC + Magic Missile immunity until your next turn), Charm
Person, Disguise Self (alter your appearance, 1 hr), Feather Fall (slow up
to 5 falling creatures), Sleep (WIS save or Incapacitated→Unconscious, C),
Detect Magic (C, R).

## Warlock (CHA)
**Cantrips**: Eldritch Blast (ranged spell attack, 1d10 Force, extra beams
at higher levels — irrelevant at level 1), Mage Hand, Minor Illusion,
Prestidigitation, True Strike.
**Level 1**: Charm Person, Comprehend Languages (R), Speak with Animals,
Detect Magic (C, R).

## Wizard (INT)
**Cantrips**: Fire Bolt, Mage Hand, Minor Illusion, Prestidigitation,
Message.
**Level 1**: Magic Missile, Shield, Detect Magic (C, R), Find Familiar
(summon a Beast-form spirit companion), Identify (learn a magic item's
properties, R), Silent Image (visual-only illusion up to a 15-ft cube, C),
Comprehend Languages (R), Sleep (C).
