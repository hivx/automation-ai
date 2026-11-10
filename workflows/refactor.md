# Playbook: refactor

## When it applies
- Structure, names, dead code or unneeded dependencies need cleaning up WITHOUT changing behavior.
- A debt item in `docs/team/debt.md` is next in line.

## Default size
M.

## Chain
0. `/team:intake` → team-leader → `intake.md`.
1. `/team:design` (short version) → designer → `design.md`: scope, touchpoints, how to prove behavior is unchanged.
2. `/team:clean <kind>` → maintainer → commits; one kind of cleanup per run.
3. `/team:verify` → qa → `acceptance.md`: `cmd.test` output before == after.
4. `/team:pr` → tech-lead → PR.

## Gates
G2b is ON for this playbook (the human approves `design.md`); G4 if enabled.

## Stop points
- Test output differs before and after.
- The cleanup forces a behavior change: split it into `new-feature` or `change-request`.

## Done criteria
- Two identical `cmd.test` outputs (before/after) are pasted; lint/typecheck is clean; one kind per PR.

## Common mistakes
- Mixing bug fixes into the refactor.
- Cleaning the whole repo in one PR.

## Related playbooks
`bug-fix`, `dependency-upgrade`.
