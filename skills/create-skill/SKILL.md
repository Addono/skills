---
name: create-skill
description: >
  Guide for creating effective skills following best practices. Use when creating or
  updating skills that extend agent capabilities. Triggers on: "create a skill",
  "add a skill", "write a SKILL.md", "update this skill".
external:
  source: https://skills.sh/siviter-xyz/dot-agent/create-skill
  repository: https://github.com/siviter-xyz/dot-agent/tree/main/skills/create-skill
  license: MIT
---

# create-skill *(external)*

> This skill is hosted externally. Install it directly for the full content:
>
> ```
> npx skills add siviter-xyz/dot-agent/create-skill
> ```
> or with APM: add `siviter-xyz/dot-agent/skills/create-skill` to your `apm.yml`.

## What It Does

Guides agents through creating high-quality skills following the
[Agent Skills specification](https://agentskills.io/specification):

- Correct `SKILL.md` structure and YAML frontmatter
- Progressive disclosure: keep SKILL.md under 200 lines, overflow to `references/`
- Choosing the right level of agent freedom (instructions vs. scripts vs. pseudocode)
- Bundled resource layout (`scripts/`, `references/`, `assets/`)

## Use This Skill When

- Creating a new skill from scratch
- Refactoring an existing skill to follow best practices
- Reviewing a skill for structure and quality

## Source

Full skill content lives at:
[github.com/siviter-xyz/dot-agent/skills/create-skill](https://github.com/siviter-xyz/dot-agent/tree/main/skills/create-skill)
