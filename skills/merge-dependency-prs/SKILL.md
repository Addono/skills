---
name: merge-dependency-prs
description: >
  Safely merge automated dependency bump PRs across all tools (Dependabot, Renovate, Depfu, etc.):
  discover PRs, merge green ones, track blocker decisions/re-evaluations via PR comments, and
  monitor post-merge base branch CI for regressions.
  Triggers on: "merge dependency PRs", "clean up dependencies", "handle renovate PRs",
  "merge depfu PRs", "merge dependency bumps".
---

# Merge Dependency PRs

Safely process and merge automated dependency bump PRs from any bot (Dependabot, Renovate, Depfu, etc.), document blocker reasons in PR comments for future re-evaluation, and verify that merges do not cause base branch regressions.

## Step 0 — Determine Scope & Baseline CI

**Default:** target the current repository.

```bash
gh repo view --json nameWithOwner -q .nameWithOwner
```

Check the default branch baseline status before merging any PRs:

```bash
gh run list --repo <owner/repo> --branch <default-branch> --limit 5
```

Note whether main/master CI is currently green or red so post-merge regressions can be distinguished.

See `references/scope.md` for multi-repo scoping rules.

## Step 1 — List Dependency Bump PRs

Identify PRs authored by dependency bots or labeled as dependencies:

```bash
# Dependabot
gh pr list --repo <owner/repo> --author app/dependabot --state open \
  --json number,title,headRefName,statusCheckRollup,mergeable,baseRefName

# Renovate
gh pr list --repo <owner/repo> --author app/renovate --state open \
  --json number,title,headRefName,statusCheckRollup,mergeable,baseRefName

# By common labels/metadata fallback:
gh pr list --repo <owner/repo> --label "dependencies" --state open \
  --json number,title,headRefName,statusCheckRollup,mergeable,baseRefName,author
```

Classify PRs into:
- **Green**: checks passed, mergeable, no blocking reviews.
- **Failing / Pending**: tests failed or checks still in progress.
- **Blocked**: merge conflicts, peer dependency locks, or breaking API changes.

## Step 2 — Merge Green PRs in Safe Sequence

Merge oldest green PRs first to minimize rebasing overhead:

```bash
gh pr merge <number> --repo <owner/repo> --merge
# Use --admin only if explicitly allowed or authorized by repo policy
```

Prompt the bot to rebase or update open dependent PRs:
- **Dependabot**: `gh pr comment <number> --repo <owner/repo> --body "@dependabot rebase"`
- **Renovate**: `gh pr comment <number> --repo <owner/repo> --body "renovate: rebase"` (or trigger via UI/label if configured)

## Step 3 — Triage Blockers & Track Decisions in PR Comments

Every unmerged or blocked PR **must have its blocker documented directly on the PR** so that future runs know whether and when to re-evaluate it.

### Comment Template for Blockers
```bash
gh pr comment <number> --repo <owner/repo> --body "$(cat <<'EOF'
### ⏸️ Dependency Merge Evaluation

- **Status**: Blocked / Skipped
- **Reason**: <Clear description of failure or breaking change>
- **Known blocker / prerequisite**: <e.g., Blocked on upstream PR #123, awaits React 19 migration, or pending peer dependency package X@v2>
- **Re-evaluation criteria**: <e.g., Re-check once package Y is updated, or when test suite is migrated>
EOF
)"
```

Check existing comments before posting to avoid duplicate spam (`gh pr view <number> --json comments`).

See `references/triage-and-comments.md` for evaluating breaking changes, trivial fixes, and comment guidelines.

## Step 4 — Post-Merge Regression Watch

Immediately after merging PRs, monitor the default branch CI runs to ensure the merge did not introduce regressions:

```bash
# Watch the latest workflow run on base branch
gh run list --repo <owner/repo> --branch <default-branch> --limit 3
gh run watch <run-id> --repo <owner/repo> --exit-status
```

If CI goes from **green to red**:
1. Check the failing job logs (`gh run view <run-id> --log-failed`).
2. Identify which dependency PR introduced the failure.
3. Alert the user immediately with the offending PR and failure context.
4. Stop merging further PRs until the regression is addressed.

See `references/regression-watch.md` for watch timeouts and rollback protocols.

## Step 5 — Final Summary Report

Output a clear summary:

```
## Dependency PR Automation Summary

### ✅ Merged & Verified (N PRs)
- #101 bump vite from 5.1.0 to 5.2.0 (CI verified green on main)
- #102 bump typescript from 5.3.3 to 5.4.2

### ⏸️ Blocked / Documented (N PRs)
| PR | Bot | Package | Reason | Prerequisite / Re-evaluation |
|----|-----|---------|--------|------------------------------|
| #103 | renovate | eslint 8→9 | Config format changed to flat config | Blocked on eslint-plugin-foo v3 release |
| #104 | dependabot | prisma 5→6 | Breaking client generation API | Re-evaluate after migration task #88 |

### 🔍 Base Branch Status
- Base branch CI: ✅ Green (Run #456 passed after merges)
```
