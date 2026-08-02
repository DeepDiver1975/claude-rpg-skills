# Claude RPG Skills

A growing collection of [Claude Code](https://claude.com/claude-code) skills
for tabletop RPGs — session prep, one-shot generation, and other GM-facing
tooling. Each skill lives in its own self-contained subdirectory under
`skills/`.

## Available skills

| Skill | What it does |
|---|---|
| [`cyberpunk-red-oneshot`](skills/cyberpunk-red-oneshot/README.md) | Generates a complete Cyberpunk RED one-shot: pregenerated characters as filled official PDF sheets, a scenario with GM notes, NPC/enemy stat blocks, and image-generation prompts. |
| [`dnd-5e-oneshot`](skills/dnd-5e-oneshot/README.md) | Generates a complete D&D 5e (2024 rules / SRD 5.2.1) one-shot: pregenerated characters as filled official PDF sheets, a scenario with GM notes, NPC/monster Markdown stat blocks, and image-generation prompts. |

## Using a skill

Copy or symlink the skill's subdirectory into your Claude Code skills
directory:

```bash
ln -s "$(pwd)/skills/<skill-name>" ~/.claude/skills/<skill-name>
```

Then invoke it in Claude Code (e.g. `/cyberpunk-red-oneshot`). See each
skill's own README for setup requirements — some skills need external assets
(fonts, official PDFs, etc.) that aren't bundled here because of the source
game's licensing terms; check the skill's README before assuming
copy-and-go.

## Licensing note

Each skill targets a specific tabletop game system and may be bound by that
game publisher's own fan-content / homebrew policy, which is typically more
restrictive than a standard open-source license (e.g. no commercial resale
of the content, no reproduction of official rules text or assets). Code
(the Python/shell tooling itself) is original work; game-system-specific
reference content is not. See each skill's own README for the specifics
that apply to it — there is no single blanket license for this repo.
