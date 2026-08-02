# German Display-Term Glossary

**Not an official Wizards of the Coast / Ulisses Spiele translation.** This
is a practical glossary of commonly-understood German tabletop-RPG
vocabulary for SRD 5.2.1 terms, used to keep player/GM-facing prose (the
Markdown sheets, GM guide, NPC stat blocks, and the values written into the
PDF's free-text fields) in German, per `SKILL.md`'s language rule. It is
**not** a rules source — always resolve mechanics from `dnd5e-rules-summary.md`,
`classes-and-subclasses.md`, `species-and-backgrounds.md`, `equipment.md`,
and `spellcasting-summary.md` (which stay English, citing SRD 5.2.1
directly); this file only supplies the German word to use when writing that
mechanic into German prose.

**Usage pattern**: when a term names something the GM might want to
cross-reference in `references/*` (a class, species, skill, weapon, or
condition), write it as `German term (English SRD term)` on first mention
in a given document, then the German term alone afterward. Flavor-only text
(personality traits, backstory, location descriptions) doesn't need the
parenthetical at all — it was never in English to begin with.

**Two things stay in their literal English SRD form regardless of this
glossary** — not out of a language preference but real mechanical
necessity, and both are already covered by `SKILL.md`'s own exception list,
not by anything below:
1. The **Character JSON schema's** `class`/`subclass`/`species`/`background`/
   `skill_proficiencies`/`skill_expertise`/`saving_throw_proficiencies`
   values — `fill_character_sheet.py` and `assets/skills_field_map.json`
   key off these exact strings; translating them breaks the script.
2. The **official PDF's own printed field labels** (e.g. "Race", "Athletics",
   "ClassLevel") — those are baked into the sheet's artwork, not something
   this skill writes, and there's no official German fillable AcroForm sheet
   to substitute (see `SKILL.md`'s known constraints).

Everything else — every string this skill actually writes into a PDF
free-text field, a Markdown sheet, a GM guide, or an NPC block — should use
the German terms below.

## The 6 Abilities

| English (SRD/JSON key) | German |
|---|---|
| Strength (STR) | Stärke |
| Dexterity (DEX) | Geschicklichkeit |
| Constitution (CON) | Konstitution |
| Intelligence (INT) | Intelligenz |
| Wisdom (WIS) | Weisheit |
| Charisma (CHA) | Charisma |

Keep the 3-letter abbreviations (STR/DEX/CON/INT/WIS/CHA) as-is even in
German text — they're used as compact table headers throughout this skill's
own output (e.g. the ability-score table in a Markdown sheet) and match the
PDF field-name prefixes (`STRmod`, `DEXmod `, etc.).

## The 12 Classes

| English (JSON `class`) | German |
|---|---|
| Barbarian | Barbar |
| Bard | Barde |
| Cleric | Kleriker |
| Druid | Druide |
| Fighter | Kämpfer |
| Monk | Mönch |
| Paladin | Paladin |
| Ranger | Waldläufer |
| Rogue | Schurke |
| Sorcerer | Zauberer |
| Warlock | Hexenmeister |
| Wizard | Magier |

## The 9 Species

| English (JSON `species`) | German |
|---|---|
| Dragonborn | Drachenblütiger |
| Dwarf | Zwerg |
| Elf | Elf |
| Gnome | Gnom |
| Goliath | Goliath |
| Halfling | Halbling |
| Human | Mensch |
| Orc | Ork |
| Tiefling | Tiefling |

## The 4 Backgrounds

| English (JSON `background`) | German |
|---|---|
| Acolyte | Akolyth |
| Criminal | Krimineller |
| Sage | Gelehrter |
| Soldier | Soldat |

## The 18 Skills

| English (JSON `skill_proficiencies` / PDF field) | German |
|---|---|
| Acrobatics | Akrobatik |
| Animal Handling | Tierumgang |
| Arcana | Arkane Kunde |
| Athletics | Athletik |
| Deception | Täuschung |
| History | Geschichte |
| Insight | Menschenkenntnis |
| Intimidation | Einschüchtern |
| Investigation | Nachforschung |
| Medicine | Heilkunde |
| Nature | Naturkunde |
| Perception | Wahrnehmung |
| Performance | Auftreten |
| Persuasion | Überzeugen |
| Religion | Religion |
| Sleight of Hand | Fingerfertigkeit |
| Stealth | Heimlichkeit |
| Survival | Überlebenskunst |

## Damage Types

| English | German |
|---|---|
| Bludgeoning | Wuchtschaden |
| Piercing | Stichschaden |
| Slashing | Hiebschaden |
| Acid | Säureschaden |
| Cold | Kälteschaden |
| Fire | Feuerschaden |
| Force | Kraftschaden |
| Lightning | Blitzschaden |
| Necrotic | Nekrotischer Schaden |
| Poison | Giftschaden |
| Psychic | Psychischer Schaden |
| Radiant | Strahlungsschaden |
| Thunder | Donnerschaden |

## Weapon Properties and Mastery Properties

| English | German |
|---|---|
| Ammunition | Munition |
| Finesse | Fingerfertig |
| Heavy | Schwer |
| Light | Leicht |
| Loading | Nachladen |
| Range | Reichweite |
| Reach | Weite Reichweite |
| Thrown | Wurfwaffe |
| Two-Handed | Zweihändig |
| Versatile | Vielseitig |
| Cleave | Spalten |
| Graze | Streifen |
| Nick | Kerbe |
| Push | Stoßen |
| Sap | Schwächen |
| Slow | Verlangsamen |
| Topple | Umwerfen |
| Vex | Ärgern |

## Common Weapons (from `equipment.md`)

| English | German |
|---|---|
| Club | Knüppel |
| Dagger | Dolch |
| Greatclub | Großknüppel |
| Handaxe | Wurfbeil |
| Javelin | Wurfspeer |
| Light Hammer | Wurfhammer |
| Mace | Streitkolben |
| Quarterstaff | Kampfstab |
| Sickle | Sichel |
| Spear | Speer |
| Dart | Wurfpfeil |
| Light Crossbow | Leichte Armbrust |
| Shortbow | Kurzbogen |
| Sling | Schleuder |
| Battleaxe | Streitaxt |
| Flail | Kriegsflegel |
| Glaive | Glefe |
| Greataxe | Großaxt |
| Greatsword | Zweihänder |
| Halberd | Hellebarde |
| Lance | Lanze |
| Longsword | Langschwert |
| Maul | Kriegshammer |
| Morningstar | Morgenstern |
| Pike | Pike |
| Rapier | Rapier |
| Scimitar | Krummsäbel |
| Shortsword | Kurzschwert |
| Trident | Dreizack |
| Warhammer | Kriegshammer |
| War Pick | Kriegspicke |
| Whip | Peitsche |
| Blowgun | Blasrohr |
| Hand Crossbow | Handarmbrust |
| Heavy Crossbow | Schwere Armbrust |
| Longbow | Langbogen |
| Musket | Muskete |
| Pistol | Pistole |

## Armor

| English | German |
|---|---|
| Padded Armor | Wattierte Rüstung |
| Leather Armor | Lederrüstung |
| Studded Leather Armor | Beschlagene Lederrüstung |
| Hide Armor | Fellrüstung |
| Chain Shirt | Kettenhemd |
| Scale Mail | Schuppenpanzer |
| Breastplate | Brustpanzer |
| Half Plate Armor | Halbplattenrüstung |
| Ring Mail | Ringpanzer |
| Chain Mail | Kettenrüstung |
| Splint Armor | Schienenpanzer |
| Plate Armor | Plattenrüstung |
| Shield | Schild |

## Common Adventuring Gear / Packs

| English | German |
|---|---|
| Backpack | Rucksack |
| Bedroll | Schlafrolle |
| Rope | Seil |
| Torch | Fackel |
| Waterskin | Wasserschlauch |
| Rations | Rationen |
| Tinderbox | Feuerstein-Set |
| Explorer's Pack | Entdeckerausrüstung |
| Dungeoneer's Pack | Verließausrüstung |
| Burglar's Pack | Einbrecherausrüstung |
| Priest's Pack | Priesterausrüstung |
| Scholar's Pack | Gelehrtenausrüstung |
| Entertainer's Pack | Unterhalterausrüstung |
| Holy Symbol | Heiliges Symbol |
| Thieves' Tools | Diebeswerkzeug |
| Arcane Focus | Arkaner Fokus |
| Spellbook | Zauberbuch |

## Creature Sizes and Types (for NPC/monster stat blocks)

| English | German |
|---|---|
| Tiny | Winzig |
| Small | Klein |
| Medium | Mittelgroß |
| Large | Groß |
| Huge | Riesig |
| Gargantuan | Gigantisch |
| Humanoid | Humanoid |
| Beast | Bestie |
| Undead | Untot |
| Fiend | Unhold |
| Celestial | Himmlisches Wesen |
| Fey | Fee |
| Construct | Konstrukt |
| Elemental | Elementar |
| Dragon | Drache |
| Giant | Riese |
| Monstrosity | Monstrosität |
| Ooze | Schleim |
| Plant | Pflanze |

## Common Conditions (from `dnd5e-rules-summary.md`)

| English | German |
|---|---|
| Blinded | Geblendet |
| Charmed | Bezaubert |
| Deafened | Betäubt (Gehör) |
| Exhaustion | Erschöpfung |
| Frightened | Verängstigt |
| Grappled | Gepackt |
| Incapacitated | Kampfunfähig |
| Invisible | Unsichtbar |
| Paralyzed | Gelähmt |
| Petrified | Versteinert |
| Poisoned | Vergiftet |
| Prone | Liegend |
| Restrained | Festgehalten |
| Stunned | Betäubt (Bewusstsein) |
| Unconscious | Bewusstlos |
| Concentration | Konzentration |
| Advantage | Vorteil |
| Disadvantage | Nachteil |
