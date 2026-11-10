# Batch: build-all-tasks

## When it applies
- The feature has `tasks.md` and G3 is approved (or disabled).
- You want every task built after hours, unattended.

## Default size
M or L (size S is faster by hand).

## Chain
`decide` mode is mandatory. Do not use `--bare` (hooks must run, ADJ-03).
1. `/team:build <ID> --decide` → tech-lead → dev, reviewer for each unticked task.
2. Tasks run out or a stop point is hit → record the result.

```bash
claude -p "/team:build FEAT-012 --decide" \
  --agent team:team-leader --permission-mode dontAsk \
  --allowedTools "$(jq -r '["Read","Grep","Glob","Edit","Write","Agent","Skill"] + (.permissions.allow // []) | join(",")' .claude/settings.json)" \
  --max-turns 200 --max-budget-usd 20 --output-format json \
  > docs/team/metrics/batch-build-FEAT-012.json
```
`--allowedTools` comes from the `permissions.allow` that onboard wrote (it includes the `cmd.*` slots): in an untrusted directory (CI, a new machine) `-p` ignores `permissions.allow`, so it must be passed again as a flag (K-06). Full GitHub Actions template: `templates/project/github/workflows/team-feature.yml`.

## Gates
No gate is passed. From G4 on, it waits for the human.

## Stop points
- Every stop point of `/team:build`; `--max-turns` or `--max-budget-usd` runs out.

## Done criteria
The next morning the human reads: `/team:status`, `tasks.md` (ticked tasks), `review-NN.md`, `docs/team/journal/<ID>.md`, and the result JSON (`subtype`, `total_cost_usd`).

## Common mistakes
- Running before the plan is approved.
- A budget so low it stops mid-task.

## Related playbooks
`new-feature`, `batch/verify-all.md`.
