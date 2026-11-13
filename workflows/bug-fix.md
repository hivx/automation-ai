# Playbook: bug-fix

## When it applies
- Behavior differs from the spec or the docs; it is reproducible.
- It is not urgent enough to fix directly on prod.

## Default size
S.

## Chain
0. `/team:intake --type bug` → team-leader → `intake.md`, a new entry in `docs/team/defects.md`.
1. `/team:build` → tech-lead → dev (1 task): write a failing test that reproduces the bug FIRST, paste the red output → fix → `cmd.test_one` green → reviewer. Size S: tech-lead writes `acceptance.md` at the end of build (automated acceptance, no qa call).
2. Size M: `/team:verify` → qa → `acceptance.md`.
3. `/team:pr` → tech-lead → PR (size S: no As-Built; pr writes a short body).

## Gates
G4 if enabled; G5 when releasing to prod.

## Stop points
- The bug cannot be reproduced: stop, ask for more data.
- The fix needs a design change: switch to `change-request`.

## Done criteria
- The reproducing test has red output before and green after; `cmd.test` is green; `defects.md` is updated.

## Common mistakes
- Fixing first, writing the test afterwards.
- A test that checks the symptom, not the cause.
- Fixing other things "while I'm here".

## Related playbooks
`hotfix`, `change-request`.
