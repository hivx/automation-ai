# Batch: verify-all

## When it applies
- Some features are in the built state without acceptance yet.
- After a dependency upgrade, you want acceptance re-run for every open feature.

## Default size
Not applicable.

## Chain
`decide` mode is mandatory; no `--bare`.
1. `python3 "$(cat .team/plugin_root)/scripts/team.py" status` lists the built features.
2. For each feature: `/team:verify <ID> --decide` → qa → `acceptance.md`.

```bash
claude -p "/team:verify FEAT-012 --decide" \
  --agent team:team-leader --permission-mode dontAsk \
  --allowedTools "$(jq -r '["Read","Grep","Glob","Write","Agent","Skill"] + (.permissions.allow // []) | join(",")' .claude/settings.json)" \
  --max-turns 80 --max-budget-usd 8 --output-format json
```

## Gates
Writes `acceptance.md` but does NOT approve G4; the human approves.

## Stop points
- The environment cannot run; the budget runs out.

## Done criteria
The next morning: every feature has an `acceptance.md` with a verdict; `/team:status` lists the G4 gates waiting for the human.

## Common mistakes
- Treating accepted as G4 approved.

## Related playbooks
`batch/build-all-tasks.md`, `release`.
