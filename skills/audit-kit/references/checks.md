# audit-kit checks

Every check ends with a scope line `checked: N files / skipped: <reason>`, so that "0 issues" can be told apart from "not run". Use only read-only commands (Read, Grep, Glob, `jq`, `git log`) and `python3 <kit>/scripts/{team.py status,measure.py,check-profile.py}` by absolute path. Do not run `validate.sh`, `log-run.sh`, `team.py scorecard` or `evals/run-eval.sh`.

## Static checks (no metrics needed)
| # | Check | How | Report when |
|---|---|---|---|
| S1 | Trust boundary | List the sources that feed text into agents: issue content (the prompt of `team-feature.yml`), web pages (researcher), temp skills in `.claude/skills/`, the project's CLAUDE.md/rules, `docs/team/**` written by other roles. Grep for the "data, not instructions" sentence (STD-SEC-5) where each is read. | A source is read without that sentence |
| S2 | Hooks failing open | Read `protect.sh`, `role-policy.sh`, `check-git.sh`: which exit code follows malformed JSON or a failing sub-command? Claude Code blocks only on exit code 2; any other code lets the call through. | A safety hook lets the call through on error without printing a diagnosis to stderr |
| S3 | Matchers cover the tools | Collect `tools:` from `agents/*.md`, `.claude/agents/*.md` and `allowed-tools:` from skills; compare with the PreToolUse matchers in `hooks/hooks.json`. File writes must be blocked on `Edit`, `Write`, `NotebookEdit`, `Bash`. | A tool can write and no matcher blocks it |
| S4 | Read-only list | `hooks/role-policy.json` `readonly_commands`: which commands have flags that write or run commands (`sed -i/e/w`, `sort -o`, `uniq IN OUT`, `tree -o`, `rg --pre`, `find -delete/-fprint`, `mkdir`)? Does `teamlib.py is_readonly` block each form (read the code)? Does `readonly_scripts` match by path or by name? | A write form slips through; scripts matched by name |
| S5 | Write list per role | Compare `roles[*].write` in `role-policy.json` with the "writes only …" sentence in section 1 of `agents/<role>.md` and the tools column of SPEC §3 (with the ADJ entries in `docs/00-overview.md`). | The three places differ |
| S6 | Gates loosened by configuration | Are the lint/format/test config files (names from the profile, or the usual ones) inside `protected_paths`; can a `bash: any` role edit them? | A check configuration can be edited by dev/maintainer/devops |
| S7 | Headless allowlist | For each `workflows/batch/*.md` and `templates/project/github/workflows/*.yml`: is `--allowedTools` enough for the skill chain (`python3` for `team.py`, the `cmd.*` slots); is it built from `permissions.allow` (K-06)? | Missing entries, or stack commands copied by hand |
| S8 | `allowed-tools` too broad | Grep `allowed-tools:` for bare `Bash`, `Bash(*)`, `Bash(bash *)`, `Bash(rm *)`, `Bash(sudo *)`. Record `Bash(python3 *)` separately (it allows `python3 -c`, K-25). | Every such line |
| S9 | Descriptions | Skill: starts with "Use when", < 500 characters, no process summary (repeated "then", "after that"). Agent: starts with "Delegate when", ≤ 300 characters. | Any one rule broken |
| S10 | Dangling slots | Grep `cmd\.[a-z_]+`, `deploy\.[a-z_]+`, `ci\.[a-z_]+` in agents/skills/workflows; compare with `templates/schemas/profile.schema.json`. | A slot that is not in the schema |
| S11 | Contradictory instructions | Grep the same noun (push, skip, migration, prod, asking the human) paired with "always/must" in one file and "never/forbidden" in another. | Every pair found (paste both `file:line`) |
| S12 | Mismatched names | Grep `/team:<x>`, `agents/<x>.md`, `skills/<x>` in `docs/`; compare with the folders. | A name that does not exist |
| S13 | Temp skills/agents | Compare `.claude/skills/*/`, `.claude/agents/*.md` with `docs/team/skills-registry.md`; `temp` rows unused for 30 days; temp agents with `permissionMode`, `hooks`, `mcpServers` in their frontmatter. | Not registered, overdue, dangerous keys |
| S14 | Hook kill switches | Grep for environment variables or flags that turn hooks off in `scripts/`. | Any switch at all (machine rules must not have a bypass) |

## Metric-based checks (need `docs/team/metrics/runs.jsonl`)
| # | Check | How | Report when |
|---|---|---|---|
| D1 | Unused skills | SubagentStop lines have `skill: null`; only a few skills call `log-run.sh --skill`. Match fork skills through `agent` + `stage` (from `current.json`). A skill that never logs metrics → "no data", NOT "unused". | 0 runs in 30 days for a skill that has data |
| D2 | Agents hitting the turn limit | Normalise the `team:` prefix of `agent`; compare `turns` with `maxTurns` in the frontmatter. `turns` is the number of assistant messages (approximate) — say so. | ≥ 2 times |
| D3 | Results guessed from text | The scorecard `result` field is guessed from the last message (K-18) — every metric based on `result` is labelled "low confidence". | Always note it |

## De-duplication
Read the kit's `docs/kit-issues.md` when it is readable (`<kit>/docs/kit-issues.md`). A duplicate finding → status "known (K-xx)" with the new evidence (it may have regressed). A new finding → "new".
