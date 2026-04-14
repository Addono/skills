# create-skill

This directory vendors the upstream
[`siviter-xyz/dot-agent/skills/create-skill`](https://github.com/siviter-xyz/dot-agent/tree/33762551d4dfa2e757fa1b43417c7dab528a215f/skills/create-skill)
skill so package installers such as `npx skills add Addono/skills` receive the full skill contents.

## Upstream source

- Repository: `siviter-xyz/dot-agent`
- Path: `skills/create-skill`
- Snapshot: `33762551d4dfa2e757fa1b43417c7dab528a215f`

Symlinks and Git submodules were not used because the `skills` CLI discovers skills from a shallow clone without initializing submodules, and it does not treat symlinked skill directories as installable skills.
