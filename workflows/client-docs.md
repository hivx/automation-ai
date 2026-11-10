# Playbook: client-docs

## When it applies
- Docs for clients or end users: guides, introductions, release notes.
- The readers are not developers.

## Default size
S (M when there are several documents).

## Chain
0. `/team:intake` → team-leader → `intake.md`.
1. `/team:analyze` → analyst → `spec.md`: audience, scope, level of detail, format.
2. writer (team-leader calls it through Agent) → documents in `docs/**`.
3. The human approves the content (a content review, not a code review).
4. `/team:pr` → tech-lead → PR.

## Gates
G1 (audience and scope); content approval at step 3.

## Stop points
- The audience is unclear; the content needs business knowledge the team does not have.

## Done criteria
- The human approved the content; every step in the docs matches real behavior.

## Common mistakes
- Writing for developers instead of the stated audience.
- Outdated screenshots.

## Related playbooks
`docs-only`, `release`.
