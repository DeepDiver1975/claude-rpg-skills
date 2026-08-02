# Cyberpunk RED Visual Style Guide

This guide defines five selectable visual style presets. A new step in
SKILL.md asks the GM to pick one for the run; append that preset's Style
Block, verbatim, to the end of every generated image prompt (portraits,
NPCs, locations, battlemaps, the regional maps) in that run — never mix
presets within one run. The Portrait-Specific, Battlemap-Specific, and
Map-Specific Additions below are universal: they apply after any preset's
base block, regardless of which one was picked, since they describe
framing/composition, not rendering technique.

## Style Presets

### Preset A: CPR Rulebook (default)

Evokes the Cyberpunk RED core rulebook's own interior art.

> Style: gritty 1980s-90s cyberpunk illustration in the vein of the Cyberpunk RED
> core rulebook's interior art — high-contrast digital painting, bold black
> linework, dramatic rim lighting. Palette: neon magenta, cyan, and acid yellow
> accents against desaturated concrete grays and rust. Recurring motifs: visible
> cybernetic augmentation (chrome limbs, ocular implants, neural ports), layered
> streetwear and corp-logo fashion, neon signage and holographic ads in the
> background, rain-slicked or grime-streaked surfaces. Framing: cinematic,
> slightly low angle, subject sharply in focus against a busier out-of-focus
> Night City backdrop. No photorealism — painterly/graphic-novel rendering only.

### Preset B: 2020 Pulp Paperback

Evokes the original Cyberpunk 2020 tabletop rulebook and late-80s/early-90s
cyberpunk paperback cover art.

> Style: airbrushed/oil-painted retro-futurist illustration in the style of the
> original Cyberpunk 2020 tabletop rulebook's cover and interior art and
> late-1980s/early-1990s cyberpunk paperback book covers — smooth gradient
> airbrush technique, soft-edged glows, visible grainy print texture as if
> scanned from an offset-printed cover. Palette: bold, saturated primary-color
> lighting (hot pink, electric blue, sunset orange) washing over glossy
> surfaces, with heavy chiaroscuro contrast. Recurring motifs: sleek chrome
> vehicles and hardware rendered with mirror-bright highlights, dramatic
> silhouettes against oversized city skylines, retro-futurist poster-style
> composition (subject posed centrally, larger than life), evoking Syd
> Mead-style concept art. Framing: heroic, slightly worm's-eye angle, bold
> poster-like composition. Painterly and stylized throughout — no
> photorealism.

### Preset C: Night City Cinematic (2077-inspired)

Evokes Cyberpunk 2077 (CD Projekt Red)'s promotional and cinematic concept
art.

> Style: glossy semi-realistic digital concept art in the style of Cyberpunk
> 2077 (CD Projekt Red)'s promotional and cinematic key art — believable human
> proportions and materials rendered with high production-value finish,
> detailed chrome and glass reflections, wet-asphalt streets throwing back
> saturated neon reflections. Palette: vivid HDR-bright neon (cyan, magenta,
> gold) cutting through cool blue-and-teal ambient shadow. Recurring motifs:
> dense vertical megacity architecture, holographic billboards and signage
> layered into the environment, visible high-end cyberware integrated
> seamlessly into skin and clothing. Framing: cinematic wide-to-medium shots
> with dramatic color grading, lens-flare and bloom around light sources,
> subject rendered with idealized, poster-quality polish rather than
> documentary realism.

### Preset D: Edgerunners Anime

Evokes Cyberpunk: Edgerunners (Studio Trigger).

> Style: cel-shaded anime illustration in the style of Cyberpunk: Edgerunners
> (Studio Trigger) — bold, clean black outlines around every form, flat
> saturated color fields with minimal gradient shading (hard shadow shapes
> rather than painterly blending), dynamic exaggerated posing and perspective
> evoking the show's action choreography. Palette: high-saturation neon (hot
> pink, toxic green, electric blue) against flat dark-navy or black
> backgrounds. Recurring motifs: sharp angular character design, exaggerated
> proportions on cybernetic limbs and weapons, glitch-artifact and speed-line
> VFX accents layered over the scene, spiky dynamic hair and fashion
> silhouettes. Framing: dynamic action-oriented angles, dramatic
> foreshortening. No photorealism, no painterly rendering — flat cel-shaded
> animation look only.

### Preset E: Chrome Noir

Evokes Blade Runner 2049's neon-noir cinematography, photorealistic.

> Style: photorealistic cinematic photography in the neon-noir mode of Blade
> Runner 2049 — realistic human anatomy, skin, fabric, and metal textures
> rendered with accurate light behavior, shallow depth of field (subject in
> crisp focus, background softly defocused), shot as if on a full-frame
> camera with a fast prime lens. Palette: desaturated, muted base tones
> (steel blue, charcoal, muted amber) cut through by isolated, realistic
> neon-sign color casts and practical lighting sources, visible fine film
> grain. Recurring motifs: rain-slicked streets and wet reflective surfaces,
> atmospheric haze and fog diffusing light sources, subtly integrated
> cyberware that reads as a real prosthetic or implant rather than a
> stylized design element. Framing: naturalistic handheld-feeling camera
> angles, believable real-world staging. Fully photorealistic throughout —
> no painterly, illustrative, or animated rendering.

## Portrait-Specific Additions

Applies regardless of which preset was selected above. Append to the chosen
base style block for character/NPC portraits: "chest-up portrait, character
facing three-quarters toward camera, neutral-to-confident expression matching
their role."

Portraits are composited into a roughly square (~1:1) box on the character sheet
and are centre-cropped to fit, so prefer square or near-square framing — a tall
portrait loses its top and bottom to the crop.

## Battlemap-Specific Additions

Applies regardless of which preset was selected above. Append to the chosen
base style block for battlemaps: "top-down orthographic view, grid-friendly
composition (assume a 1m-per-square grid), key cover/terrain elements clearly
delineated and labeled, no character figures — environment only."

## Map-Specific Additions

Applies regardless of which preset was selected above. Two separate maps
are generated per one-shot — write each as its own image-prompt file, both
using the same style preset so they visually match, but differing in what
content they're allowed to show.

### GM Map

Save as `map-gm.txt`. Append to the chosen base style block: "stylized
graphic district/transit map of Night City in the tradition of corporate
transit maps and gang-territory intel maps — bird's-eye/schematic angle
(not a photorealistic aerial photo), bold labeled district and street
names, clean iconography for key landmarks rendered as simplified
pictograms rather than detailed illustration." Night City's real district
names (Watson, Heywood, Westbrook, Pacifica, Santo Domingo, City Center,
Northside, Combat Zone, Badlands) may be used to place the scenario
geographically; if the scenario's locations don't map cleanly onto real
Night City geography, keep the map schematic/abstract rather than
inventing precise geographic claims.

Label every named location that appears in the GM guide's scenes (Step 6)
directly on the map, and connect them with a visible route or numbered
markers matching scene order (1 = hook location, 2 = next scene, etc.) so
a GM can trace the crew's path across the session at a glance. Mark the
crew's starting location (Scene 1) with a distinct "you are here"-style
icon or highlight, separate from the later scene markers. This file is
for the GM's own reference only — full plot content is expected: name
locations by their plot-relevant identity (a corp's covert front, a
gang's hidden stash house), and include faction/gang-territory color
overlays wherever they help a GM read who secretly controls what.

This is not a battlemap: no combat grid, no scale callout, and — unlike
the Battlemap Addition's "no character figures — environment only"
restriction — small stylized landmark icons, vehicle silhouettes, or
gang-territory color overlays are welcome if they aid readability. The
goal is a legible "where are we in Night City" reference image, not
tactical accuracy.

### Player Map

Save as `map-player.txt`. This file is safe to display or hand out
directly at the table, so it must contain nothing that reveals this
one-shot's plot. Append to the same chosen base style block: "stylized
graphic district/transit map of Night City in the tradition of corporate
transit maps and tourist/civic district maps — bird's-eye/schematic angle
(not a photorealistic aerial photo), bold labeled district and street
names, clean iconography for landmarks rendered as simplified pictograms
rather than detailed illustration." Night City's real district names
(Watson, Heywood, Westbrook, Pacifica, Santo Domingo, City Center,
Northside, Combat Zone, Badlands) may be used the same way as on the GM
map, to place the scenario in the city; well-known public landmarks (a
stadium, a mall, a transit line, a well-known corp plaza) may also be
labeled if they help orient the map, since these are common knowledge to
any Night City local.

Show only locations and details that are genuinely common knowledge
independent of this specific job — general district and street geography,
public landmarks — and explicitly exclude any location whose relevance is
a plot discovery: a hideout the crew finds mid-investigation, a front
company's covert identity, a gang's secret stash house, or any other
location named or labeled specifically because of what this one-shot's
scenes reveal about it. If a real place is both geographically real and
plot-relevant (e.g. a dockside warehouse whose owner is a Scene 3 reveal),
it may appear on the player map only as unlabeled scenery or under a
generic, non-revealing label ("a warehouse," "the docks") — never under
the name or role the crew learns during play. The crew's own starting
location (their usual hangout, a fixer's known storefront, their home
turf) may still be marked with a "you are here"-style icon exactly as on
the GM map, since the party already knows where they start — that's
orientation, not a spoiler.

Omit entirely, regardless of how minor it seems: scene-order numbering,
route lines or markers connecting scenes, gang-territory color overlays
that reveal who secretly controls a location, and any hint — even vague,
unlabeled, or easy to miss — of an off-screen element the plot hasn't
revealed yet. When in doubt whether a detail counts as common knowledge,
leave it off the player map; it's better to under-include than to leak a
discovery. This is not a battlemap: no combat grid, no scale callout, but
small stylized landmark icons or vehicle silhouettes are welcome if they
aid readability. The goal is a legible, spoiler-free "where are we in
Night City" reference the GM can hand to players without hesitation.
