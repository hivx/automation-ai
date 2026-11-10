# Playbook: data-migration

## When it applies
- Moving, transforming or loading data between schemas/systems.
- There is a risk of losing or corrupting data.

## Default size
M (L when several systems are involved).

## Chain
0. `/team:intake` → team-leader → `intake.md`.
1. `/team:analyze` → analyst → `spec.md`: data scope, volumes, reconciliation rules.
2. `/team:design` → designer → `design.md`: field mapping, migration, rollback.
3. `/team:plan` → tech-lead → `tasks.md`.
4. `/team:build` → dev: trial runs on a COPY of the data (`cmd.migrate`), never touching real data.
5. `/team:verify` → qa → `acceptance.md`: count reconciliation; migration up/down.
6. `/team:release` → devops → runs in the agreed time window, with a rollback plan.

## Gates
G1, G2b (enabled for this playbook), G3, G4, G5.

## Stop points
- Reconciliation does not match; no tested rollback; no agreed time window yet.

## Done criteria
- Reconciliation matches on the copy and on real data; rollback has been rehearsed.

## Common mistakes
- Trial runs on real data.
- A migration with no down direction.

## Related playbooks
`release`, `integration`.
