# Batch: clean-sweep

## When it applies
- `docs/team/debt.md` has entries of a recurring cleanup kind (dead code, names, unneeded dependencies...).
- You want periodic cleanup, one kind at a time.

## Default size
S or M.

## Chain
`decide` mode is mandatory; no `--bare`.
1. `/team:clean <kind> --decide` → maintainer: `cmd.test` before → clean up → `cmd.test` after.
2. `/team:pr` → tech-lead → a PR for one kind of cleanup.

```bash
claude -p "/team:clean dead-code --decide" \
  --agent team:team-leader --permission-mode dontAsk \
  --allowedTools "$(jq -r '["Read","Grep","Glob","Edit","Write","Agent","Skill"] + (.permissions.allow // []) | join(",")' .claude/settings.json)" \
  --max-turns 120 --max-budget-usd 6 --output-format json
```

## Gates
G2b if enabled; the human merges the PR.

## Stop points
- Test output differs before and after; the cleanup forces a behavior change.

## Done criteria
The next morning: one open PR whose description has the before/after test output; `debt.md` is updated.

## Common mistakes
- Bundling several kinds into one run.

## Related playbooks
`refactor`.
