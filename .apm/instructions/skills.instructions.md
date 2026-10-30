---
description: Requirements for SKILL.md frontmatter description field and skill authoring
applyTo: "skills/**"
---

# Skill Description Guidelines

When authoring or updating skills in `skills/`:

## The `description` Field

- **Purpose**: The frontmatter `description` field is used exclusively by AI agents and consumers to determine **when to use the skill**. It should describe user intent, relevant scenarios, and activation triggers.
- **Do Not Include Implementation Details**: Do not use the description to capture what the skill does internally, how it achieves its goal, or step-by-step operational details (e.g., approving PRs, specific flags, or internal triage procedures). Put operational procedures and decision rules in the body of `SKILL.md` or in `references/`.
- **Keep Descriptions Short**: Keep the description concise. Overly long descriptions are subject to truncation by agent platforms and registries, which degrades the consumer's ability to trigger and activate the skill when it is relevant.
