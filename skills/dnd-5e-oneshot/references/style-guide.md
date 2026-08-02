# D&D 5e Visual Style Guide

This guide defines five selectable visual style presets. A step in SKILL.md
asks the GM to pick one for the run; append that preset's Style Block,
verbatim, to the end of every generated image prompt (portraits, NPCs,
locations, battlemaps, the regional maps) in that run — never mix presets
within one run. The Portrait-Specific, Battlemap-Specific, and Map-Specific
Additions below are universal: they apply after any preset's base block,
regardless of which one was picked, since they describe framing/composition,
not rendering technique.

## Style Presets

### Preset A: Classic PHB Illustration (default)

Evokes the 2024 Player's Handbook's own interior art.

> Style: painterly digital illustration in the vein of the 2024 D&D Player's
> Handbook's interior art — confident heroic poses, warm rim lighting
> catching armor edges and fabric folds, richly detailed materials (worn
> leather, etched steel, embroidered cloth). Palette: high-fantasy jewel
> tones (deep crimson, forest green, royal blue) accented with warm gold
> highlights against earthy neutral backgrounds. Recurring motifs: ornate
> but grounded equipment (no gratuitous spikes or oversized weapons),
> environmental storytelling in the background (ruins, dungeon architecture,
> wilderness), a sense of scale between character and setting. Framing:
> dynamic three-quarter angle, subject in crisp focus against a softer
> painted backdrop. Painterly and crisp — no photorealism, no flat cel
> shading.

### Preset B: Painterly Classic Fantasy

Evokes early-20th-century golden-age adventure illustration (N.C. Wyeth,
Howard Pyle lineage).

> Style: oil-painting-textured illustration in the tradition of golden-age
> adventure book illustration (N.C. Wyeth, Howard Pyle) — visible confident
> brushwork, atmospheric aerial perspective, dramatic but naturalistic
> directional lighting (low sun, torchlight, or overcast sky). Palette:
> muted earthy tones (ochre, umber, forest green, slate gray) with
> selective warm highlights where light sources are strongest. Recurring
> motifs: weathered cloaks and traveling gear, weather and terrain playing
> a visible role in the composition, figures posed with narrative intent
> rather than pure action-heroics. Framing: classic
> book-illustration composition, often a wider establishing view with the
> subject integrated into the landscape rather than isolated against it.
> Painterly throughout — no photorealism, no digital-flat rendering.

### Preset C: Cinematic BG3-Style Concept Art

Evokes Baldur's Gate 3 (Larian)'s promotional and cinematic key art.

> Style: glossy semi-realistic digital concept art in the style of Baldur's
> Gate 3's promotional and cinematic key art — believable proportions and
> materials rendered with high production-value finish, detailed skin/metal/
> fabric texture work, moody atmospheric color grading. Palette: cool
> shadow tones (deep teal, charcoal, indigo) cut through by warm dramatic
> accent lighting (firelight, magic-glow, torchlight). Recurring motifs:
> richly detailed environmental storytelling, magic effects rendered with
> tangible glow and particle detail, characters posed with cinematic
> gravitas. Framing: cinematic medium-to-wide shots, dramatic rim lighting,
> shallow environmental depth of field. High production-value polish
> without full photorealism.

### Preset D: Flat-Color Animated-Series Style

Evokes a modern animated-fantasy-series look (Dragon Prince/Arcane-adjacent).

> Style: flat-shaded digital illustration in the style of a modern animated
> fantasy series — bold clean linework, flat-to-lightly-gradient color
> fields with minimal painterly blending, stylized slightly exaggerated
> proportions. Palette: punchy saturated colors (vivid teal, magenta,
> gold) with confident color-blocking between light and shadow rather than
> soft gradients. Recurring motifs: expressive dynamic posing, simplified
> but readable silhouettes, magic/action effects rendered as clean stylized
> shapes rather than realistic particle detail. Framing: dynamic
> action-oriented angles, dramatic foreshortening. No photorealism, no
> painterly rendering — flat animated-series look only.

### Preset E: Moody Grimdark Realism

Evokes a low-fantasy/grimdark cinematic-trailer look (Witcher 3-adjacent).

> Style: near-photorealistic cinematic rendering in a low-fantasy/grimdark
> mode — realistic human anatomy, weathered and lived-in gear textures,
> naturalistic light behavior, shallow depth of field. Palette: desaturated
> muted tones (steel gray, mud brown, faded green) cut through by isolated
> warm firelight or torchlight as the dominant color accent. Recurring
> motifs: mud, rust, and wear on armor and clothing, harsh unglamorous
> environments (rain, fog, cold light), a grounded unheroic sense of danger
> rather than poster-heroic composition. Framing: naturalistic
> handheld-feeling camera angles, believable real-world staging. Fully
> photorealistic to near-photorealistic throughout — no painterly,
> illustrative, or flat-shaded rendering.

## Portrait-Specific Additions

Applies regardless of which preset was selected above. Append to the chosen
base style block for character/NPC portraits: "chest-up portrait, character
facing three-quarters toward camera, expression matching their class/role
(e.g. a grim Fighter vs. a wry Rogue vs. a serene Cleric)."

Portraits are composited into a tall, portrait-oriented box on the
character sheet (roughly 3:4, taller than wide) and are centre-cropped to
fit, so prefer a vertically-framed composition — a wide landscape framing
loses its sides to the crop.

## Battlemap-Specific Additions

Applies regardless of which preset was selected above. Append to the chosen
base style block for battlemaps: "top-down orthographic view, grid-friendly
composition (assume a 5-foot-per-square grid, per `dnd5e-rules-summary.md`),
key cover/terrain elements clearly delineated and labeled, no character
figures — environment only."

## Map-Specific Additions

Applies regardless of which preset was selected above. Two separate maps
are generated per one-shot — write each as its own image-prompt file, both
using the same style preset so they visually match, but differing in what
content they're allowed to show.

### GM Map

Save as `map-gm.txt`. Append to the chosen base style block: "hand-drawn
fantasy cartography in the tradition of a Player's Handbook regional map
or an in-world explorer's map — aged parchment or vellum texture,
ink-and-watercolor linework, a decorative compass rose and rustic border,
hand-lettered place names in a fantasy-appropriate script." Since D&D's
homebrew world has no fixed canonical geography, invent place names and
their spatial relationships purely from what this specific one-shot's
scenario established in Steps 3, 6, and 7 — don't borrow real-world or
published-setting geography.

Label every named location that appears in the GM guide's scenes (Step 6)
directly on the map, and connect them with a visible path or road, or
numbered markers, matching scene order (1 = hook location, 2 = next scene,
etc.) so a GM can trace the party's route across the session at a glance.
Mark the party's starting location (Scene 1) with a distinct "you are
here"-style icon or flag, separate from the later scene markers. This
file is for the GM's own reference only — full plot content is expected:
label secret or hidden locations by their true plot-relevant identity (a
villain's hidden lair, a cultist shrine discovered mid-scenario), and
include any off-screen hint (a distant unlabeled landmark pointing toward
an antagonist's origin, etc.) that helps the GM keep the wider world
consistent.

This is not a battlemap: no combat grid, no 5-foot-per-square scale
callout, and — unlike the Battlemap Addition's "no character figures —
environment only" restriction — small stylized landmark icons (a mine
entrance, a town's walls, a forest treeline) are welcome if they aid
readability. The goal is a legible "where are we in the world" reference
image, not tactical accuracy.

### Player Map

Save as `map-player.txt`. This file is safe to display or hand out
directly at the table, so it must contain nothing that reveals this
one-shot's plot. Append to the same chosen base style block: "hand-drawn
fantasy cartography in the tradition of a Player's Handbook regional map
or an in-world explorer's map — aged parchment or vellum texture,
ink-and-watercolor linework, a decorative compass rose and rustic border,
hand-lettered place names in a fantasy-appropriate script." Invent the
same underlying geography as the GM map (same town names, same rough
layout) so the two maps clearly depict the same world, but restrict what
gets labeled: only settlements, roads, and natural landmarks that would
be common knowledge to anyone living in or traveling through the region
— the town the party starts in, a nearby market town, a well-known road,
river, forest, or mountain range by its ordinary regional name.

Explicitly exclude any location whose relevance is a plot discovery: a
monster's lair found via investigation, a hidden temple or ritual
chamber, a villain's true hideout, or any location labeled with
information the party only learns during play (a dungeon entrance may
appear as an unlabeled hill or cave mouth, if it would be visible terrain
at all, but never labeled with its plot-relevant name or purpose). The
party's own starting location (their home village, the inn they set out
from) may still be marked with a "you are here"-style icon or flag
exactly as on the GM map, since the party already knows where they
start — that's orientation, not a spoiler.

Omit entirely, regardless of how minor it seems: scene-order numbering,
paths or roads drawn specifically to connect scenes, and any hint — even
vague, unlabeled, or easy to miss — of an off-screen element the plot
hasn't revealed yet (an unlabeled temple icon hinting at a distant
antagonist's origin is exactly the kind of detail that must be cut, not
softened). When in doubt whether a detail counts as common knowledge,
leave it off the player map; it's better to under-include than to leak a
discovery. This is not a battlemap: no combat grid, no 5-foot-per-square
scale callout, but small stylized landmark icons (a town's walls, a
forest treeline) are welcome if they aid readability. The goal is a
legible, spoiler-free "where are we in the world" reference the GM can
hand to players without hesitation.
