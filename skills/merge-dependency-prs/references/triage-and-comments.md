# PR Comment Tracking & Blocker Triage

Tracking blocker decisions directly on PR comments ensures full traceability across automated agent runs and human reviewers.

## Why Comment on the PR?

1. **Persistent Memory Across Agent Sessions**: Future agent runs inspect PR comments to avoid re-evaluating known blocked PRs repeatedly.
2. **Prerequisite Awareness**: Captures explicit dependencies (e.g., "PR #55 must be merged before PR #58 can update peer dependencies").
3. **Transparent Handoff to Humans**: Reviewers see immediately why a bot PR was held back without having to dig through CI logs.

## Decision Guidelines

### Trivial Fixes vs Non-Trivial Blockers

- **Trivial (Fix & Merge)**:
  - Simple type imports or minor export name updates.
  - Minor 1-3 line configuration changes conforming to upstream deprecations.
  - Updating a lockfile hash or lockfile sync inconsistency.

- **Non-Trivial (Block & Document)**:
  - Major architectural / framework breaking changes (e.g. Next.js major bump, Webpack to Vite).
  - Unmet peer dependencies across the ecosystem.
  - Test suites failing due to behavioral changes in business logic.
  - Broken third-party typings without clear resolution.

### PR Approval Requirements

Repositories that enforce required reviews before merging do not block automated dependency merges:
- If a PR is green but has `reviewDecision: "REVIEW_REQUIRED"`, the agent is authorized to submit an approving review.
- Do not mark the PR as blocked or post a blocker comment solely because review approval is pending.
- Run `gh pr review <number> --repo <owner/repo> --approve --body "Approved dependency bump"` and proceed to merge.

## Comment Idempotency & Re-Evaluation Checks

Before adding a comment:
```bash
# Check existing comments by the agent or bots
gh pr view <number> --repo <owner/repo> --json comments --jq '.comments[].body'
```

If a prior blocker comment exists:
- Verify whether the stated **re-evaluation criteria** have been met (e.g., prerequisite PR merged, upstream fix released).
- If not met, do not post duplicate comments. Record the PR as still blocked in the final summary.
- If criteria **are** now met, re-trigger CI or rebase the PR to evaluate whether it can now be safely merged.
