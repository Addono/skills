# Multi-Repo Scope & Discovery

## Scope Rules

By default, run only against the current working directory's repository.

If the user explicitly specifies a wider scope, follow these commands:

### Single Named Repository
```bash
gh pr list --repo <org/repo> ...
```

### All Repositories for User / Org
```bash
gh repo list <org> --no-archived --source --json nameWithOwner --jq '.[].nameWithOwner' | while read repo; do
  echo "Processing $repo..."
  # Run PR check & merge workflow
done
```

> ⚠️ Always process repositories sequentially to avoid triggering GitHub API rate limits.
