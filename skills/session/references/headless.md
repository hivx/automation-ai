# Running headless

## Mandatory flags
| Flag | Why |
|---|---|
| `--agent team:team-leader` | team-leader is the only entry point, even when nobody is watching (ADJ-01) |
| `--permission-mode dontAsk` | nobody is there to answer permission dialogs |
| `--allowedTools "<from permissions.allow>"` | an untrusted folder (CI, a new machine) ignores the project's `permissions.allow` (K-06) |
| `--max-turns`, `--max-budget-usd` | hard caps; hitting a cap stops the run, it does not continue |
| `--output-format json` | to read `subtype`, `total_cost_usd`, `result` |
| a command with `--decide` | the human cannot be asked; big questions → `WAITING_FOR_ANSWER` |
Do not use `--bare` when files are edited: it turns off every hook, including the plugin's hooks (ADJ-03). `--bare` is only for read-only reports such as `/team:status`.

The `--allowedTools` list:
```
jq -r '["Read","Grep","Glob","Edit","Write","Agent","Skill"] + (.permissions.allow // []) | join(",")' .claude/settings.json
```
Stages that do not edit code (verify, retro): drop `Edit` from the first array.

## Templates per stage
| Job | Command | Suggested cap |
|---|---|---|
| Build every task | `/team:build <ID> --decide` | the `measure.py` median × 1.5; no data → start low, read the JSON, then raise it |
| Acceptance | `/team:verify <ID>` | same as above |
| Periodic retro | `/team:retro --decide` | same as above |
| Clean one kind of debt | `/team:clean <kind> --decide` | same as above |

## Reading the result
- `subtype: success` + `team.py status <ID>` to learn the real stage (do not trust the text in `result`).
- A `subtype` reporting turns/budget exhausted → the job is unfinished; `/team:session load` in the next session.
- A state waiting for the human (`WAITING_FOR_APPROVAL`, `WAITING_FOR_ANSWER`) is a normal ending, not an error.
- Record `total_cost_usd` in the feature's journal.
