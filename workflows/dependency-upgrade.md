# Playbook: dependency-upgrade

## When it applies
- Upgrading a library, framework or runtime version.
- There is a vulnerability alert or a version nearing end of support.

## Default size
M.

## Chain
0. `/team:intake` → team-leader → `intake.md`.
1. `/team:research` → researcher → `research.md`: changelog, breaking changes, migration path, official sources.
2. `/team:plan` → tech-lead → `plan.md`, `tasks.md` (one task per breaking change).
3. `/team:build` → tech-lead → dev, reviewer; the lockfile changes only through `cmd.install`.
4. `/team:verify` (full) → qa → `acceptance.md`: `cmd.test`, `cmd.lint`, `cmd.typecheck`, `cmd.build`.
5. `/team:pr` → tech-lead → a separate PR for the upgrade.

## Gates
G3, G4.

## Stop points
- A breaking change requires changing the project's public API: stop, tell the human.

## Done criteria
- Every breaking change in `research.md` has a ticked task; full verify is green.

## Common mistakes
- Upgrading several major libraries in one PR.
- Editing the lockfile by hand.

## Related playbooks
`spike`, `refactor`.
