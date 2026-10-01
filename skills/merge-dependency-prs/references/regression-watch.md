# Regression Watch & Post-Merge Verification

## Why Watch the Base Branch?

Individual PR checks run against a merge-commit snapshot at a specific point in time. When multiple dependency PRs are merged in sequence, or when interactions between packages only show up after being joined on the main branch, CI can transition from green to red.

## Step-by-Step Watch Procedure

1. **Get the latest commit on the base branch after your merge(s)**:
   ```bash
   LATEST_SHA=$(gh api repos/<owner/repo>/commits/<default-branch> --jq .sha)
   ```

2. **Identify triggering workflow runs for that commit**:
   ```bash
   gh run list --repo <owner/repo> --commit "$LATEST_SHA" --json databaseId,name,status,conclusion
   ```

3. **Watch the workflow execution**:
   ```bash
   # Wait for completion and check exit status
   gh run watch <run-id> --repo <owner/repo> --exit-status
   ```

4. **Diagnose Regressions**:
   If the run fails:
   ```bash
   gh run view <run-id> --repo <owner/repo> --log-failed
   ```

   - **Immediate Action**: Halt any further merging.
   - **Isolate**: Match the failure in the logs against the dependencies updated in the recent merge batch.
   - **Report / Rollback**: Note the exact commit and PR number that introduced the breakage. If configured or authorized, revert the breaking merge commit or notify the team with reproducible failure details.
