# �� Addono Agent Skills

> A curated catalog of AI agent skills — plug-and-play capabilities that supercharge your coding agents.

[![CI](https://github.com/Addono/skills/actions/workflows/validate.yml/badge.svg)](https://github.com/Addono/skills/actions/workflows/validate.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/format-Agent%20Skills-purple)](https://agentskills.io)
[![APM](https://img.shields.io/badge/compatible-microsoft%2Fapm-0078D4)](https://github.com/microsoft/apm)

## What Are Skills?

Skills are modular, self-contained packages that give AI coding agents specialized knowledge, workflows, and automation. Think of them as "onboarding guides" for agents — loaded on demand, only when relevant.

This repo houses both **novel skills** crafted here and **vendored upstream snapshots** of useful skills so installers like `apm` and `npx skills` receive complete skill directories.

## Available Skills

### 🔀 merge-dependabot-prs

Intelligently merge Dependabot PRs with full CI awareness and automatic triage of blockers.

**Use when:**
- You want to clear a backlog of Dependabot PRs safely
- CI is green but you haven't found time to click "Merge"
- Some Dependabot PRs are failing and you want a clear report of why

**Key capabilities:**
- Auto-detects the target repo from `git remote` / `gh` — no manual repo specification required
- Supports single repo, all repos for a user, or all repos in an org
- Merges all green PRs (with admin merge fallback when needed)
- Distinguishes trivial fixes (version bumps, simple API renames) from non-trivial ones
- Fixes trivial breaking changes automatically, then merges
- Reports a clean summary table for non-trivial blockers

[→ View skill](skills/merge-dependabot-prs/SKILL.md)

---

### 🛠️ create-skill

A meta-skill for creating new skills. The full upstream skill is vendored into this repository so package installers receive the entire skill directory, including `references/` content.

**Source:** [siviter-xyz/dot-agent](https://github.com/siviter-xyz/dot-agent/tree/main/skills/create-skill)
**Snapshot details:** [skills/create-skill/README.md](skills/create-skill/README.md)

[→ View skill](skills/create-skill/SKILL.md)

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
npx skills add Addono/skills
```

### Manual

Clone or copy any `skills/<name>/` directory into your project. The `SKILL.md` file is the entry point.

## Using Skills

Once installed, your agent will automatically pick up relevant skills. You can also invoke them explicitly:

```
Use the merge-dependabot-prs skill to clean up all green Dependabot PRs in this repo.
```

```
Use the merge-dependabot-prs skill across all repos in the Addono org.
```

## Contributing

Contributions are welcome! Please:

1. Use [conventional commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, etc.)
2. Follow the [Agent Skills specification](https://agentskills.io/specification)
3. Keep `SKILL.md` under 200 lines (use `references/` for longer content)
4. Open a PR — CI will validate your skill automatically

See [AGENTS.md](AGENTS.md) for guidance on working in this repo with an AI agent.

## License

[Apache 2.0](LICENSE) — free to use, modify, and redistribute.
