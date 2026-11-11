# 08 — Working channels

Source of truth: `SPEC.md` §11. Adjustments: ADJ-01, ADJ-03.

| Channel | Asks the human through | Mode | Notes |
|---|---|---|---|
| CLI / Desktop / IDE | `AskUserQuestion` in the main session (team-leader) | `ask` or `decide` | The everyday main channel |
| GitHub Actions | Issue comment + label `team:needs-answer` | `ask` or `decide` | Uses `anthropics/claude-code-action@v1` |
| Scheduled tasks | Does not ask | `decide` only | retro, clean-sweep, post-deploy smoke |
| Headless `claude -p` | Does not ask | `decide` only | See below |
| Projects (cloud) | Like the CLI | either | Runs several features in parallel |

## GitHub Actions
- Label `team:intake` on an issue → intake; `team:run` → continue to the next gate.
- Approve a gate with the comment `@claude approve Gn`.
- Questions are posted as comments following the template `templates/artifacts/question-comment.md`; the job stops with `WAITING_FOR_ANSWER`.
- Sample workflows: `templates/project/github/workflows/team-ci.yml`, `team-feature.yml`.

## Headless
Command for work that edits files (hooks needed):
```
claude -p "<command /team:...>" \
  --permission-mode dontAsk \
  --allowedTools "$(jq -r '["Read","Grep","Glob","Edit","Write","Agent","Skill"] + (.permissions.allow // []) | join(",")' .claude/settings.json)" \
  --max-turns <n> --max-budget-usd <usd> --output-format json
```
- `--allowedTools` is mandatory: in a directory that is not yet trusted (a CI runner, a new machine), `-p` ignores the project's `permissions.allow` (K-06). The list is taken from the `permissions.allow` that onboard wrote, so stack commands never have to be copied by hand.
- Do NOT use `--bare` for work that edits files: `--bare` turns off every hook, including the plugin's hooks, so the machine rules do not run (ADJ-03).
- `--bare` is only for read-only reports such as `/team:status`; in that case load the plugin with `--plugin-dir` and set `ANTHROPIC_API_KEY`.
- Many features at once: `claude -p "/team:run --all"` with the same flags; raise `--max-turns`/`--max-budget-usd` with the headcount.
- `decide` mode is mandatory. Read the result from the JSON output and check it against `templates/schemas/stage-result.json`.

## Scheduled tasks
Batch playbooks in `workflows/batch/`: `build-all-tasks`, `verify-all`, `weekly-retro`, `clean-sweep`. They run in `decide` mode; on reaching an enabled gate they stop and report.
