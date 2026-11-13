# When something goes wrong

## A hook blocks or reminds
Signal: Claude reports a `RULE (reminder, not enforced)` line (default `enforcement: "warn"`), or an action blocked with a reason (`enforcement: "block"`).
1. Read the reason. A hook states a rule (P3); follow it, or say in the report why this case is an exception.
2. Editing a protected file (`protected_paths`) → the human edits it, or fixes the profile if the path was declared by mistake.
3. Creating a file outside `allowed_new_file_roots` → choose the right place, or add the directory to the list (human approval).
4. Pushing a protected branch / force-push → push only `team/*` branches; open a PR.
5. A role working outside its scope (role-policy) → hand the work to the right role.
6. The hook is genuinely wrong → `/team:feedback "<description>"`; kit defects go into `docs/team/kit-issues.md`.

## A stuck gate
Signal: `/team:status` reports `WAITING_FOR_APPROVAL` although you think you approved.
1. Check that the line `Approved-by: <name> <YYYY-MM-DD>` is at the TOP of the right artifact (G5: `Approved-by-prod:`).
2. Check that the approver is in that gate's `approvers` (`.team/config.json`).
3. Approving through an issue: comment exactly `@claude approve Gn`.
4. You no longer want this gate → set it to `false` in `gates`. Do not delete the artifact.

## Red CI
1. `/team:ci` — devops classifies the cause FIRST: code, flaky test, environment, CI config, dependency.
2. Fix it in a separate PR (ci-fix playbook). Never delete a test step to make it green.
3. A flaky test → record it in `debt.md`; do not mark it skipped.

## Full context
Signal: a warning that `context_warn_pct` was exceeded, or Claude starts forgetting.
1. `/team:session` to write the handoff (≤ 40 lines).
2. `/compact` or open a new session — the state is on disk and `/team:status` brings you back to the right place.
3. One feature per session. Large code reading → leave it to `Explore`.

## Budget or rework rounds exceeded
`feature_budget_usd` or `max_rework` exceeded → the team stops and reports. Read `journal/<feature>.md` and decide: split the task, change the size, or raise the limit.
