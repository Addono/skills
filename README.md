# Addono Agent Skills

> A curated catalog of AI agent skills — plug-and-play capabilities that supercharge your coding agents.

[![CI](https://github.com/Addono/skills/actions/workflows/validate.yml/badge.svg)](https://github.com/Addono/skills/actions/workflows/validate.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/format-Agent%20Skills-purple)](https://agentskills.io)
[![APM](https://img.shields.io/badge/compatible-microsoft%2Fapm-0078D4)](https://github.com/microsoft/apm)

## What Are Skills?

Skills are modular, self-contained packages that give AI coding agents specialized knowledge, workflows, and automation. Think of them as "onboarding guides" for agents — loaded on demand, only when relevant.

This repo houses both **novel skills** crafted here and **vendored upstream snapshots** of useful skills so installers like `apm` and `npx skills` receive complete skill directories. Vendored skills are generated from `/vendored-skills.json` by `python3 scripts/sync-vendored-skills.py`, which also writes attribution metadata and notices.

## Available Skills

### 🔀 merge-dependency-prs

Safely process and merge automated dependency bump PRs across all tools (Dependabot, Renovate, Depfu, etc.) with CI regression monitoring and blocker tracking in PR comments.

**Use when:**
- You want to clear a backlog of dependency bump PRs from any bot safely
- CI is green and PRs are ready to merge
- You want blocker decisions documented directly in PR comments for future re-evaluation
- You want to verify base branch CI to guard against post-merge regressions

**Key capabilities:**
- Multi-bot support: works with Dependabot, Renovate, Depfu, and labeled dependency PRs
- Baseline and post-merge regression detection on the default branch
- Merges green PRs in safe order (oldest first) and triggers bot rebases
- Documents structured blocker reasons and re-evaluation criteria on unmerged PRs
- Reports a clean summary of merged PRs, documented blockers, and base branch status

[→ View skill](skills/merge-dependency-prs/SKILL.md)

---

### ⚙️ probot-settings

Create or update `.github/settings.yml` for the Repository Settings GitHub App / Probot Settings
app using live repository data, safe defaults, and Addono-flavoured examples.

**Use when:**
- You want to manage repository settings as code in `.github/settings.yml`
- A repo already has `settings.yml` and you want a careful update instead of a rewrite
- You want guidance grounded in real Addono examples and upstream app rules

**Key capabilities:**
- Detects current repository metadata and labels with `gh`
- Preserves existing intent and only expands into advanced sections when necessary
- Encodes upstream gotchas for labels, branch protection, environments, and org-only permissions
- Calls out security implications and review safeguards for sensitive changes

[→ View skill](skills/probot-settings/SKILL.md)

---

### 🛠️ create-skill

A meta-skill for creating new skills. The full upstream skill is vendored into this repository from a pinned snapshot so package installers receive the entire skill directory, including `references/` content.

**Source:** [siviter-xyz/dot-agent](https://github.com/siviter-xyz/dot-agent/tree/main/skills/create-skill)
**Attribution:** [skills/create-skill/ATTRIBUTION.md](skills/create-skill/ATTRIBUTION.md)

[→ View skill](skills/create-skill/SKILL.md)

---

### 📝 documentation-writer

A Diátaxis-oriented documentation skill for drafting software docs with a clear document type, audience, scope, and reviewable outline before writing.

**Source:** [github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/documentation-writer)
**Attribution:** [skills/documentation-writer/ATTRIBUTION.md](skills/documentation-writer/ATTRIBUTION.md)

[→ View skill](skills/documentation-writer/SKILL.md)

---

## Installation

### Using APM (recommended)

```bash
# Install APM
curl -fsSL https://aka.ms/apm-unix | sh

# Add this package to your project
apm install Addono/skills
```

### Using skills.sh / npx

```bash
# Add this package to the current project
npx skills add Addono/skills

# Install for all projects on this machine
npx skills add Addono/skills --global
```

### Manual

Clone or copy any `skills/<name>/` directory into your project. The `SKILL.md` file is the entry point.

## Using Skills

Once installed, your agent will automatically pick up relevant skills. You can also invoke them explicitly:

```
Use the merge-dependency-prs skill to clean up all green dependency PRs in this repo.
```

```
Use the merge-dependency-prs skill across all repos in the Addono org.
```

```
Use the probot-settings skill to create a .github/settings.yml for this repo based on the
current GitHub settings and Addono conventions.
```

## Contributing

Contributions are welcome! Please:

1. Use [conventional commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, etc.)
2. Follow the [Agent Skills specification](https://agentskills.io/specification)
3. Keep `SKILL.md` under 200 lines (use `references/` for longer content)
4. Refresh vendored snapshots with `python3 scripts/sync-vendored-skills.py` after changing `/vendored-skills.json`
5. Open a PR — CI will validate your skill automatically

See [AGENTS.md](AGENTS.md) for guidance on working in this repo with an AI agent.

## License

[Apache 2.0](LICENSE) — free to use, modify, and redistribute.
