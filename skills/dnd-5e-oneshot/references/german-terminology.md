# German Terminology (sourced from the official SRD 5.2.1 German translation)

Source: the official German translation of the System Reference Document
5.2.1 (`DE_SRD_CC_v5.2.1.pdf`), released by Wizards of the Coast LLC under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Every term below
was extracted or verified directly against that PDF's text — see
`extraction-map-de.md` for the page-by-page provenance and verification
method. This supersedes the previous version of this file, which was
explicitly a hand-built, unverified glossary ("not an official Wizards of
the Coast / Ulisses Spiele translation"); several of its guesses turned out
to differ from the real book (noted inline below where it matters).

Mechanics still resolve from `dnd5e-rules-summary.md`, `classes-and-
subclasses.md`, `species-and-backgrounds.md`, `equipment.md`, and
`spellcasting-summary.md` (numbers/DCs/slots don't change between language
editions of the same ruleset, so those stay sourced from the English SRD).
This file supplies the official German vocabulary to use when writing those
mechanics into German prose, a PDF free-text field, or a Markdown sheet.

**Usage pattern**: when a term names something the GM might want to
cross-reference in `references/*` (a class, species, skill, weapon, or
condition), write it as `German term (English SRD term)` on first mention
in a given document, then the German term alone afterward. Flavor-only text
(personality traits, backstory, location descriptions) doesn't need the
parenthetical at all — it was never in English to begin with.

**Two things still stay in their literal English SRD form regardless of
this glossary** — real mechanical necessity, not a coverage gap anymore
(see `SKILL.md`'s own exception list):
1. The **Character JSON schema's** `skill_proficiencies`/`skill_expertise`/
   `saving_throw_proficiencies` values — `fill_character_sheet.py` and
   `assets/skills_field_map.json` key off these exact English strings;
   translating them breaks the script.
2. The **official PDF's own printed field labels** (e.g. "Race",
   "Athletics", "ClassLevel") — baked into the sheet's artwork, not
   something this skill writes, and there's no official German fillable
   AcroForm sheet to substitute.

`class`, `subclass`, `species`, `background`, spell names, weapon/armor/gear
names, and everything else this skill writes into a PDF free-text field, a
Markdown sheet, a GM guide, or an NPC block should now use the terms below
— including `subclass` and spell names, previously left in English for lack
of a verified source (see `classes-and-subclasses.md` and
`spellcasting-summary.md`, both updated alongside this file).

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
own output and match the PDF field-name prefixes (`STRmod`, `DEXmod `, etc.).

## The 12 Classes

Unchanged from the prior glossary — verified against the SRD's own Inhalt
(Contents) and class headings, all 12 already matched.

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

## The 12 Subclasses (new — previously an unverified gap)

Every SRD class has exactly one subclass, gained at level 3 (see
`classes-and-subclasses.md`). These are now sourced from the book, closing
the gap that previously left `subclass` in English on every generated
character.

| Class | English subclass | German subclass |
|---|---|---|
| Barbarian | Path of the Berserker | Pfad des Berserkers |
| Bard | College of Lore | Schule des Wissens |
| Cleric | Life Domain | Domäne des Lebens |
| Druid | Circle of the Land | Zirkel des Landes |
| Fighter | Champion | Champion |
| Monk | Warrior of the Open Hand | Krieger der Offenen Hand |
| Paladin | Oath of Devotion | Schwur der Hingabe |
| Ranger | Hunter | Jäger |
| Rogue | Thief | Dieb |
| Sorcerer | Draconic Sorcery | Drakonische Zauberei |
| Warlock | Fiend Patron | Unhold-Schutzherr |
| Wizard | Evoker | Hervorrufer |

## The 9 Species

Unchanged from the prior glossary — verified, all 9 already matched.

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

| English (JSON `background`) | German | Correction |
|---|---|---|
| Acolyte | Akolyth | — |
| Criminal | Krimineller | — |
| Sage | **Weiser** | was "Gelehrter" — wrong |
| Soldier | Soldat | — |

## The 18 Skills

| English (JSON `skill_proficiencies` / PDF field) | German | Correction |
|---|---|---|
| Acrobatics | Akrobatik | — |
| Animal Handling | **Mit Tieren umgehen** | was "Tierumgang" — wrong |
| Arcana | Arkane Kunde | — |
| Athletics | Athletik | — |
| Deception | **Täuschen** | was "Täuschung" — wrong |
| History | Geschichte | — |
| Insight | **Motiv erkennen** | was "Menschenkenntnis" — wrong |
| Intimidation | Einschüchtern | — |
| Investigation | **Nachforschungen** | was "Nachforschung" (singular) — wrong |
| Medicine | Heilkunde | — |
| Nature | Naturkunde | — |
| Perception | Wahrnehmung | — |
| Performance | Auftreten | — |
| Persuasion | Überzeugen | — |
| Religion | Religion | — |
| Sleight of Hand | Fingerfertigkeit | — |
| Stealth | Heimlichkeit | — |
| Survival | Überlebenskunst | — |

## Damage Types

The book's own base nouns (used directly in weapon-table damage columns,
e.g. `1W8 Hieb`) are given first; the natural-prose `-schaden` compound
(used in narrative text, stat blocks, and this skill's own output) follows.

| English | German base noun | German (as written in prose) | Correction |
|---|---|---|---|
| Bludgeoning | Wucht | Wuchtschaden | — |
| Piercing | Stich | Stichschaden | — |
| Slashing | Hieb | Hiebschaden | — |
| Acid | Säure | Säureschaden | — |
| Cold | Kälte | Kälteschaden | — |
| Fire | Feuer | Feuerschaden | — |
| Force | Energie | **Energieschaden** | was "Kraftschaden" — wrong |
| Lightning | Blitz | Blitzschaden | — |
| Necrotic | Nekrotisch | Nekrotischer Schaden | — |
| Poison | Gift | Giftschaden | — |
| Psychic | Psychisch | Psychischer Schaden | — |
| Radiant | Gleißend | **Gleißender Schaden** | was "Strahlungsschaden" — wrong |
| Thunder | Schall | **Schallschaden** | was "Donnerschaden" — wrong |

## Weapon Properties and Mastery Properties

| English | German | Correction |
|---|---|---|
| Ammunition | Geschosse | was "Munition" — "Munition" names the ammo items themselves, "Geschosse" is the weapon-table property |
| Finesse | **Finesse** | was "Fingerfertig" — the SRD keeps this one in English |
| Heavy | Schwer | — |
| Light | Leicht | — |
| Loading | **Laden** | was "Nachladen" — wrong |
| Range (section heading) | Fernkampfreichweite | — |
| Reach | **Weitreichend** | was "Weite Reichweite" — wrong |
| Thrown | Wurfwaffe | — |
| Two-Handed | Zweihändig | — |
| Versatile | Vielseitig | — |
| Cleave | Spalten | — |
| Graze | Streifen | — |
| Nick | **Einkerben** | was "Kerbe" — wrong |
| Push | Stoßen | — |
| Sap | **Auslaugen** | was "Schwächen" — wrong |
| Slow | Verlangsamen | — |
| Topple | **Umstoßen** | was "Umwerfen" — wrong |
| Vex | **Plagen** | was "Ärgern" — wrong |

## Common Weapons (from `equipment.md`)

| English | German | Correction |
|---|---|---|
| Club | Knüppel | — |
| Dagger | Dolch | — |
| Greatclub | **Zweihandknüppel** | was "Großknüppel" — wrong |
| Handaxe | **Beil** | was "Wurfbeil" — wrong |
| Javelin | Wurfspeer | — |
| Light Hammer | **Leichter Hammer** | was "Wurfhammer" — wrong |
| Mace | Streitkolben | — |
| Quarterstaff | Kampfstab | — |
| Sickle | Sichel | — |
| Spear | Speer | — |
| Dart | Wurfpfeil | — |
| Light Crossbow | Leichte Armbrust | — |
| Shortbow | Kurzbogen | — |
| Sling | Schleuder | — |
| Battleaxe | Streitaxt | — |
| Flail | **Flegel** | was "Kriegsflegel" — wrong |
| Glaive | Glefe | — |
| Greataxe | **Zweihandaxt** | was "Großaxt" — wrong |
| Greatsword | **Zweihandschwert** | was "Zweihänder" — wrong |
| Halberd | Hellebarde | — |
| Lance | Lanze | — |
| Longsword | Langschwert | — |
| Maul | **Zweihandhammer** | was "Kriegshammer" — wrong (and previously duplicated Warhammer's term) |
| Morningstar | Morgenstern | — |
| Pike | Pike | — |
| Rapier | Rapier | — |
| Scimitar | Krummsäbel | — |
| Shortsword | Kurzschwert | — |
| Trident | Dreizack | — |
| Warhammer | Kriegshammer | — |
| War Pick | Kriegspicke | — |
| Whip | Peitsche | — |
| Blowgun | Blasrohr | — |
| Hand Crossbow | Handarmbrust | — |
| Heavy Crossbow | Schwere Armbrust | — |
| Longbow | Langbogen | — |
| Musket | Muskete | — |
| Pistol | Pistole | — |

## Armor

| English | German | Correction |
|---|---|---|
| Padded Armor | **Gepolsterte Rüstung** | was "Wattierte Rüstung" — wrong |
| Leather Armor | Lederrüstung | — |
| Studded Leather Armor | Beschlagene Lederrüstung | — |
| Hide Armor | Fellrüstung | — |
| Chain Shirt | Kettenhemd | — |
| Scale Mail | Schuppenpanzer | — |
| Breastplate | **Brustplatte** | was "Brustpanzer" — wrong |
| Half Plate Armor | **Plattenpanzer** | was "Halbplattenrüstung" — wrong |
| Ring Mail | Ringpanzer | — |
| Chain Mail | **Kettenpanzer** | was "Kettenrüstung" — wrong |
| Splint Armor | Schienenpanzer | — |
| Plate Armor | **Ritterrüstung** | was "Plattenrüstung" — wrong (that name belongs to Half Plate's "Plattenpanzer", easily confused) |
| Shield | Schild | — |

## Common Adventuring Gear / Packs

| English | German | Correction |
|---|---|---|
| Backpack | Rucksack | — |
| Bedroll | **Schlafsack** | was "Schlafrolle" — wrong |
| Rope | Seil | — |
| Torch | Fackel | — |
| Waterskin | **Trinkschlauch** | was "Wasserschlauch" — wrong |
| Rations | Rationen | — |
| Tinderbox | **Zunderkästchen** | was "Feuerstein-Set" — wrong |
| Explorer's Pack | Entdeckerausrüstung | — |
| Dungeoneer's Pack | **Gewölbeforscherausrüstung** | was "Verließausrüstung" — wrong |
| Burglar's Pack | Einbrecherausrüstung | — |
| Priest's Pack | Priesterausrüstung | — |
| Scholar's Pack | Gelehrtenausrüstung | — |
| Entertainer's Pack | **Unterhaltungskünstler-Ausrüstung** | was "Unterhalterausrüstung" — wrong |
| Holy Symbol | Heiliges Symbol | — |
| Thieves' Tools | Diebeswerkzeug | — |
| Arcane Focus | Arkaner Fokus | — |
| Spellbook | Zauberbuch | — |

## Creature Sizes and Types (for NPC/monster stat blocks)

| English | German | Correction |
|---|---|---|
| Tiny | Winzig | — |
| Small | Klein | — |
| Medium | Mittelgroß | — |
| Large | Groß | — |
| Huge | Riesig | — |
| Gargantuan | Gigantisch | — |
| Humanoid | Humanoid | — |
| Beast | **Tier** | was "Bestie" — wrong |
| Undead | Untot | — |
| Fiend | Unhold | — |
| Celestial | **Celestisches Wesen** | was "Himmlisches Wesen" — wrong |
| Fey | **Feenwesen** | was "Fee" — wrong |
| Construct | Konstrukt | — |
| Elemental | Elementar | — |
| Dragon | Drache | — |
| Giant | Riese | — |
| Monstrosity | Monstrosität | — |
| Ooze | **Schlick** | was "Schleim" — wrong |
| Plant | Pflanze | — |

## Common Conditions (from `dnd5e-rules-summary.md`)

| English | German | Correction |
|---|---|---|
| Blinded | **Blind** | was "Geblendet" — wrong |
| Charmed | Bezaubert | — |
| Deafened | **Taub** | was "Betäubt (Gehör)" — wrong; "Betäubt" alone is Stunned, not Deafened |
| Exhaustion | Erschöpfung | — |
| Frightened | Verängstigt | — |
| Grappled | Gepackt | — |
| Incapacitated | Kampfunfähig | — |
| Invisible | Unsichtbar | — |
| Paralyzed | Gelähmt | — |
| Petrified | Versteinert | — |
| Poisoned | Vergiftet | — |
| Prone | Liegend | — |
| Restrained | **Festgesetzt** | was "Festgehalten" — wrong |
| Stunned | **Betäubt** | was "Betäubt (Bewusstsein)" — the plain word, no qualifier needed |
| Unconscious | Bewusstlos | — |
| Concentration | Konzentration | — |
| Advantage | Vorteil | — |
| Disadvantage | Nachteil | — |

## The Curated Spellcasting-Summary Shortlist (new — previously an unverified gap)

Every cantrip/1st-level spell in `spellcasting-summary.md`'s curated
shortlist, now sourced from the official German spell descriptions. This
closes the gap that previously left every spell name in English on every
generated caster PC. Full mechanical text stays in
`spellcasting-summary.md` (English SRD) — this is the name mapping only.

| English | German |
|---|---|
| Vicious Mockery | Gehässiger Spott |
| Mage Hand | Magierhand |
| Minor Illusion | Einfache Illusion |
| Message | Botschaft |
| True Strike | Zielsicherer Schlag |
| Healing Word | Heilendes Wort |
| Charm Person | Person bezaubern |
| Faerie Fire | Feenfeuer |
| Comprehend Languages | Sprachen verstehen |
| Dissonant Whispers | Dissonantes Flüstern |
| Animal Friendship | Tierfreundschaft |
| Guidance | Göttliche Führung |
| Sacred Flame | Heilige Flamme |
| Thaumaturgy | Thaumaturgie |
| Spare the Dying | Verschonung der Sterbenden |
| Bless | Segnen |
| Cure Wounds | Wunden heilen |
| Command | Befehl |
| Detect Magic | Magie entdecken |
| Druidcraft | Druidenkunst |
| Entangle | Verstricken |
| Goodberry | Gute Beeren |
| Speak with Animals | Mit Tieren sprechen |
| Longstrider | Lange Schritte |
| Hunter's Mark | Fesselnder Schlag |
| Fire Bolt | Feuerpfeil |
| Prestidigitation | Taschenspielerei |
| Magic Missile | Magisches Geschoss |
| Shield | Schild |
| Disguise Self | Selbstverkleidung |
| Feather Fall | Federfall |
| Sleep | Schlaf |
| Eldritch Blast | Schauriger Strahl |
| Find Familiar | Vertrauten finden |
| Identify | Identifizieren |
| Silent Image | Lautloses Trugbild |

If a one-shot needs a spell not on this list, its German name isn't
verified here — fetch it from `data/raw/spells.txt` (if you've run the
extraction) or the official PDF directly before using it, the same
gap-reporting discipline `spellcasting-summary.md` already calls for on the
English side.
