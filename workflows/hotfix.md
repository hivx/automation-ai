# Playbook: hotfix

## When it applies
- Production is broken and users are affected now.
- The human asks to fix first and do the full work later.

## Default size
S.

## Chain
0. `/team:intake --type hotfix` → team-leader → `intake.md`.
1. `/team:build` → dev: branch `team/<ID>-hotfix` cut from the branch running in prod; minimal fix; a reproducing test if one can be written in a few minutes.
2. `/team:verify` (quick) → qa → `acceptance.md`: fix criteria + smoke test.
3. `/team:pr` → tech-lead → PR into the prod branch.
4. `/team:release` → devops → prod ONLY when `Approved-by-prod:` is present.
5. Open a full `bug-fix` right away (test, root cause) and record it in `defects.md`.

## Gates
G5 is always a human. Other gates follow config.

## Stop points
- `Approved-by-prod:` is not present yet.
- The fix needs more than one small change: stop, tell the human.

## Done criteria
- The prod smoke test is green; the follow-up `bug-fix` has been opened.

## Common mistakes
- Dropping the full bug-fix once prod is healthy again.
- Bundling other changes into the hotfix.

## Related playbooks
`bug-fix`, `release`, `ci-fix`.
