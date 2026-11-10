# Playbook: docs-only

## When it applies
- Only technical docs, README or comments change; no running code changes.

## Default size
S.

## Chain
0. `/team:intake` → team-leader → `intake.md`.
1. writer (team-leader calls it through Agent) → `docs/**`, `README.md`.
2. `/team:pr` → tech-lead → PR; enable auto-merge on green CI (`gh pr merge --auto`), still under the branch protection rules.

## Gates
None.

## Stop points
- The diff touches files outside `docs/**` and `README.md`: switch to another playbook.

## Done criteria
- The PR contains only docs; CI is green; the content matches the current code.

## Common mistakes
- Sneaking code changes into a docs PR.
- Docs describing behavior that does not exist yet.

## Related playbooks
`client-docs`.
