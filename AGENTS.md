# Addono Skills — Agent Instructions

## Overview

This repository houses AI agent skills following the [Agent Skills](https://agentskills.io/specification) format.
It is compatible with [skills.sh](https://skills.sh) and [microsoft/apm](https://github.com/microsoft/apm).

## Skills Authoring

- Every skill lives in `skills/<skill-name>/` and **must** have a `SKILL.md`.
- `SKILL.md` must include YAML frontmatter with at least `name` and `description`.
- Keep `SKILL.md` under **200 lines**. Move longer content to `references/` files.
- Upstream third-party skills should be vendored into this repo as full snapshots so installers receive the complete skill contents.

## Skill Structure

```
skills/
└── <skill-name>/
    ├── SKILL.md          # Required. Frontmatter + concise instructions (<200 lines)
    ├── README.md         # Optional. Human-facing documentation
    ├── references/       # Optional. Detailed references loaded on demand
    └── scripts/          # Optional. Helper scripts
```

## Working in This Repo

- Use the `create-skill` skill from `skills/create-skill/` when creating or updating skills.
- Use [conventional commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `docs:`, `chore:`, etc.
- Run CI locally before pushing: `bash scripts/validate-skills.sh`

## References

- Agent Skills specification: https://agentskills.io/specification
- microsoft/apm documentation: https://microsoft.github.io/apm/
- skills.sh: https://skills.sh
