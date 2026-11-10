# Playbook: new-feature

## When it applies
- The human asks for new behavior in a running system.
- It is not a bug fix and does not change an approved spec.

## Default size
From intake (S, M or L).

## Chain
0. `/team:intake` → team-leader → `intake.md` (already run).
1. `/team:analyze` → analyst → `spec.md` (size S: short version, no G1).
2. [`/team:research` → researcher → `research.md`: when the spec still has technical questions.]
3. [`/team:architect` → architect → `arch-impact.md`: size L only.]
4. `/team:design` → designer → `design.md` (skipped at size S).
5. `/team:plan` → tech-lead → `plan.md`, `tasks.md` (skipped at size S).
6. `/team:build` → tech-lead → dev, reviewer (size S: 1 dev).
7. `/team:verify` → qa → `acceptance.md` (size S: automated checks, no separate qa call).
8. `/team:asbuilt` → writer → `asbuilt.md`.
9. `/team:pr` → tech-lead → PR.
10. `/team:release` → devops.

## Gates
G1, G3, G4 (+ G2 at size L, G5 when going to prod). Size S skips G1 and G3.

## Stop points
- An enabled gate is not approved; analyst returns `NEEDS_ANSWER`; reviewer reports design-defect.

## Done criteria
- `acceptance.md` is accepted; As-Built and CHANGELOG exist; the PR is open or merged.

## Common mistakes
- Sizing a schema/API change as S.
- Bundling several capabilities into one feature.
- Skipping As-Built because "it matches the design".

## Related playbooks
`change-request` (change to an approved spec), `integration`, `bug-fix`.
