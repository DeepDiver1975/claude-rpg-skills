# D&D 5e (2024) Spellcasting Summary

Source: System Reference Document 5.2.1 ("SRD 5.2.1") by Wizards of the Coast
LLC, licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Spellcasting mechanics summarized from `equipment.md`/`playing-the-game.md`;
spell entries summarized from `classes.md`'s per-class spell lists and
`spells.md`, both in
[downfallx/dnd-5e-srd-markdown](https://github.com/downfallx/dnd-5e-srd-markdown).
Each spell's German name below (in parentheses on first mention) is sourced
from the official German SRD PDF — see `german-terminology.md` and
`extraction-map-de.md` for provenance. Write the German name in generated
output (per SKILL.md's language rule); the parenthetical English SRD name is
here only so the mechanics below stay traceable to the source spell.

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
**Cantrips**: Gehässiger Spott/Vicious Mockery (WIS save or 1d6 Psychic +
Disadvantage on its next attack), Magierhand/Mage Hand (spectral hand, minor
manipulation, 30 ft, 10 lb limit), Einfache Illusion/Minor Illusion (minor
sound or image), Botschaft/Message (silent whispered exchange with one
target), Zielsicherer Schlag/True Strike (attack with a weapon using your
spellcasting ability instead of STR/DEX).
**Level 1**: Heilendes Wort/Healing Word (Bonus Action, 2d4+mod HP at
range), Person bezaubern/Charm Person (WIS save or Charmed 1 hr),
Feenfeuer/Faerie Fire (DEX save or outlined/Advantage to hit, C), Sprachen
verstehen/Comprehend Languages (understand any language, 1 hr, R),
Dissonantes Flüstern/Dissonant Whispers (WIS save or damage + forced
movement), Tierfreundschaft/Animal Friendship (WIS save or a beast is
Charmed 24 hr).

## Cleric (WIS)
**Cantrips**: Göttliche Führung/Guidance (touch, +1d4 to one ability check,
C), Heilige Flamme/Sacred Flame (DEX save or 1d8 Radiant, ignores cover),
Thaumaturgie/Thaumaturgy (minor divine wonder effects), Verschonung der
Sterbenden/Spare the Dying (touch, stabilize a creature at 0 HP).
**Level 1**: Segnen/Bless (up to 3 allies add 1d4 to attacks/saves, C),
Wunden heilen/Cure Wounds (touch, 2d8+mod HP), Heilendes Wort/Healing Word
(Bonus Action, 2d4+mod HP at range), Befehl/Command (WIS save or follow a
one-word command), Magie entdecken/Detect Magic (sense magic within 30 ft,
C, R).

## Druid (WIS)
**Cantrips**: Druidenkunst/Druidcraft (minor nature effect), Göttliche
Führung/Guidance (+1d4 to one ability check, C), Botschaft/Message,
Verschonung der Sterbenden/Spare the Dying.
**Level 1**: Wunden heilen/Cure Wounds, Feenfeuer/Faerie Fire (C),
Verstricken/Entangle (20-ft difficult terrain, C), Gute Beeren/Goodberry
(10 berries, 1 HP + a day's food each), Tierfreundschaft/Animal Friendship,
Mit Tieren sprechen/Speak with Animals (talk to Beasts, 10 min), Lange
Schritte/Longstrider (+10 ft Speed, 1 hr), Magie entdecken/Detect Magic
(C, R).

## Paladin (CHA, half-caster — no cantrips, no usable slots until level 2)
**Level 1 (learned now, usable from level 2)**: Segnen/Bless (C), Wunden
heilen/Cure Wounds, Befehl/Command, Magie entdecken/Detect Magic (C, R).

## Ranger (WIS, half-caster — no cantrips, no usable slots until level 2)
**Level 1 (learned now, usable from level 2)**: Fesselnder Schlag/Hunter's
Mark (Bonus Action, +1d6 Force per hit on marked target, C — also a class
feature Rangers have prepared for free, see `classes-and-subclasses.md`),
Wunden heilen/Cure Wounds, Gute Beeren/Goodberry, Mit Tieren sprechen/Speak
with Animals, Verstricken/Entangle (C), Tierfreundschaft/Animal Friendship,
Lange Schritte/Longstrider, Magie entdecken/Detect Magic (C, R).

## Sorcerer (CHA)
**Cantrips**: Feuerpfeil/Fire Bolt (ranged spell attack, 1d10 Fire),
Magierhand/Mage Hand, Einfache Illusion/Minor Illusion,
Taschenspielerei/Prestidigitation (minor magic trick, up to 3 active
effects), Zielsicherer Schlag/True Strike.
**Level 1**: Magisches Geschoss/Magic Missile (3 darts, 1d4+1 Force each,
auto-hit), Schild/Shield (Reaction, +5 AC + Magic Missile immunity until
your next turn), Person bezaubern/Charm Person, Selbstverkleidung/Disguise
Self (alter your appearance, 1 hr), Federfall/Feather Fall (slow up to 5
falling creatures), Schlaf/Sleep (WIS save or Incapacitated→Unconscious,
C), Magie entdecken/Detect Magic (C, R).

## Warlock (CHA)
**Cantrips**: Schauriger Strahl/Eldritch Blast (ranged spell attack, 1d10
Force, extra beams at higher levels — irrelevant at level 1),
Magierhand/Mage Hand, Einfache Illusion/Minor Illusion,
Taschenspielerei/Prestidigitation, Zielsicherer Schlag/True Strike.
**Level 1**: Person bezaubern/Charm Person, Sprachen
verstehen/Comprehend Languages (R), Mit Tieren sprechen/Speak with
Animals, Magie entdecken/Detect Magic (C, R).

## Wizard (INT)
**Cantrips**: Feuerpfeil/Fire Bolt, Magierhand/Mage Hand, Einfache
Illusion/Minor Illusion, Taschenspielerei/Prestidigitation,
Botschaft/Message.
**Level 1**: Magisches Geschoss/Magic Missile, Schild/Shield, Magie
entdecken/Detect Magic (C, R), Vertrauten finden/Find Familiar (summon a
Beast-form spirit companion), Identifizieren/Identify (learn a magic
item's properties, R), Lautloses Trugbild/Silent Image (visual-only
illusion up to a 15-ft cube, C), Sprachen verstehen/Comprehend Languages
(R), Schlaf/Sleep (C).
