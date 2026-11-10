# Playbook: new-project

## When it applies
- The repo is empty or holds only a README.
- The human describes a system to be built from scratch.

## Default size
L.

## Chain
1. `/team:onboard --new` → team-leader → `.team/`, `.claude/`, `docs/team/`.
2. `/team:intake --size L` → team-leader → `intake.md`.
3. `/team:analyze` → analyst → `spec.md` (with DoD, NFRs).
4. `/team:research` → researcher → `research.md`.
5. `/team:architect` → architect → `docs/team/architecture.md`, `docs/team/adr/ADR-NNN.md`.
6. `/team:design` → designer → `design.md`.
7. `/team:plan` → tech-lead → `plan.md`, `tasks.md`; task 1 is the walking skeleton.
8. `/team:build` → tech-lead → dev, reviewer → commits, `review-NN.md`.
9. `/team:verify` → qa → `acceptance.md`.
10. `/team:asbuilt` → writer → `asbuilt.md`, CHANGELOG.
11. `/team:pr` → tech-lead → PR.
12. `/team:release` → devops → staging, then prod once `Approved-by-prod:` is present.

## Gates
G1 (spec), G2 (architecture), G2b if enabled, G3 (plan), G4 (acceptance), G5 (prod) — approved by the humans listed in `approvers` in config.

## Stop points
- Every enabled gate.
- The walking skeleton does not run end to end: stop before task 2.

## Done criteria
- The walking skeleton runs end to end; every criterion in `acceptance.md` passes; CI is green; the staging smoke test is green.

## Common mistakes
- Skipping the walking skeleton and building one layer at a time.
- Choosing technology before the NFRs exist.
- Architecting for needs that do not exist yet.

## Related playbooks
`new-feature`, `integration`, `release`.
