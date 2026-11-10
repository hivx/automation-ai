# Playbook: change-request

## When it applies
- A feature has a `spec.md` approved at G1 and the human wants to change the requirements.
- Scope or acceptance criteria change midway.

## Default size
M.

## Chain
0. `/team:intake` → team-leader → `intake.md` (already run, pointing to the original feature).
1. `/team:analyze --amend` → analyst → `spec.md` with `## Amendment <n>`.
2. `/team:architect` (impact mode) → architect → `arch-impact.md`.
3. `/team:plan --insert` → tech-lead → `tasks.md` gains new tasks, affected tasks are marked.
4. `/team:build` → tech-lead → dev, reviewer.
5. `/team:verify` → qa → `acceptance.md` (re-runs the old criteria too).
6. `/team:asbuilt`, `/team:pr`, `/team:release` as in new-feature.

## Gates
G1 (re-approve the amended spec), G2, G3, G4; G5 when going to prod.

## Stop points
- The amendment contradicts the approved architecture.
- A merged task is invalidated by the change.

## Done criteria
- The spec has an approved amendment; old and new criteria all pass in `acceptance.md`.

## Common mistakes
- Editing `spec.md` directly without recording an amendment.
- Forgetting to re-run the old criteria.

## Related playbooks
`new-feature`, `refactor`.
