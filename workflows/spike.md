# Playbook: spike

## When it applies
- It is unknown whether it can be done, which approach is better, or what it costs.
- A quick trial is needed before committing to a feature.

## Default size
S.

## Chain
0. `/team:intake` → team-leader → `intake.md` (the question to answer, the time box).
1. `/team:research` → researcher → `research.md`; a POC in a worktree if needed, deleted afterwards.
2. Save to the cache → `docs/team/research/<topic>@<version>.md`.
3. [ADR proposal → draft in `research.md`: when the result leads to an architecture decision.]

## Gates
None.

## Stop points
- The time box runs out without an answer: report the partial result.

## Done criteria
- The question has an answer with sources and a confidence level; no POC code remains on the working branch.

## Common mistakes
- Turning the POC into production code.
- A spike without a clear question.

## Related playbooks
`new-feature`, `dependency-upgrade`.
