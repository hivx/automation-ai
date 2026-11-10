# Playbook: retro

## When it applies
- On a schedule (see `batch/weekly-retro.md`), or after a feature with a lot of rework.
- Feedback crossed the threshold twice; the scorecard shows an anomaly.

## Default size
Not applicable.

## Chain
1. `/team:retro` → coach: `measure.py` → journal → bottlenecks → diagnosis across the 5 causes.
2. coach → `docs/team/proposals/<date>/<agent-or-skill>.md`: overlay + before/after eval.
3. The human approves the proposal.
4. Canary on N size-S jobs; coach compares against the baseline.
5. Keep / roll back / replace / drop — the human decides.

## Gates
The human approves each proposal before the canary and before keeping it.

## Stop points
- Missing metrics; the canary is worse than the baseline.

## Done criteria
- `docs/team/retro/<date>.md` exists; every proposal has evidence, an eval, a canary and a rollback; the human's decision is recorded.

## Common mistakes
- Changing an agent the first time it looks slow.
- No baseline to compare against.

## Related playbooks
`batch/weekly-retro.md`.
