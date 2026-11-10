# Playbook: integration

## When it applies
- Connecting to an external API, service or system.
- Authentication, rate limits, webhooks or data sync are involved.

## Default size
M (L when several systems are involved).

## Chain
0. `/team:intake` → team-leader → `intake.md`.
1. `/team:research` → researcher → `research.md`: API, authentication, limits, sandbox environment.
2. `/team:architect` (impact) → architect → `arch-impact.md`.
3. `/team:design` → designer → `design.md`: contract, retry, idempotency, timeout.
4. `/team:plan` → tech-lead → `tasks.md`.
5. `/team:build` → tech-lead → dev, reviewer.
6. `/team:verify` → qa → `acceptance.md`: runs against the external party's sandbox.
7. `/team:release` → devops.

## Gates
G2, G3, G4, G5 (+ G1 when there is a new spec).

## Stop points
- No sandbox account or secret yet: stop, tell the human.

## Done criteria
- Checks against the sandbox pass; retry and timeout have tests; no secret lives in the repo.

## Common mistakes
- Tests that call the real API directly.
- Retries that are not idempotent.

## Related playbooks
`new-feature`, `data-migration`.
