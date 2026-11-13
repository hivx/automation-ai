# Playbook: quick

## When it applies
- A trivial change: a text or label, a config value, one obvious line; the diff fits in one sentence.
- At most 2 files; no schema, API, contract, migration, security or `protected_paths` change; production is not broken.
- Not for a question: a question is answered by team-leader directly, with no intake and no agent.

## Default size
S (always).

## Chain
0. `/team:intake` → team-leader → `intake.md` (`Playbook: quick`) and a one-line `tasks.md` (`- [ ] T1 — … — files: … — test: … — depends: —`).
1. team-leader calls ONE `team:dev` (Agent, own worktree): branch `team/<ID>` from `base_branch`; a failing test first when behavior changes; `cmd.test_one`, then the tests of the touched module; commit. No tech-lead, reviewer, qa or writer.
2. dev returns `DONE` with the RED/GREEN lines → team-leader ticks T1 and reports the branch and the commit; the human merges it or asks for `/team:pr`.

## Gates
None (G5 only if it is released to prod).

## Stop points
- dev finds the change is bigger than the limits above (more files, a contract, a migration) → stop and re-run intake as `bug-fix` or `new-feature`.
- dev returns `BLOCKED` or `DESIGN_CONFLICT` → report to the human.

## Done criteria
- T1 ticked; the commit is on `team/<ID>`; dev's test output is pasted in the report.

## Common mistakes
- Calling the whole chain (tech-lead, reviewer, qa, writer) for a one-line change.
- Using quick for a change that touches a contract or data, to skip review.
- Opening intake for a question.

## Related playbooks
`bug-fix`, `docs-only`, `new-feature` (size S).
