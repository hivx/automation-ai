---
name: session
description: Use when starting, saving or reloading a long working session for one feature: choosing between interactive and headless, the model per role, the budget, the context-compaction points, and the handoff note for the next session.
argument-hint: "[plan|save|load] [<ID>]"
disable-model-invocation: true
allowed-tools: Bash(python3 *) Bash(cat *) Bash(jq *) Bash(ls *) Bash(git status *) Bash(git rev-parse *) Bash(wc *)
---

# Long working sessions

## Overview
This skill makes a long session run in the right place and lets the next session continue without relying on memory. Three sub-commands: `plan` (the session plan: channel, models, budget, compaction points), `save` (a hand-written note for the next session), `load` (reload and CHECK before continuing). The skill runs in the main session (team-leader).

The real state lives in the artifacts (SPEC P2) and is computed by `team.py`; a handoff holds only what the artifacts do NOT have: the state of the working tree, the last check command and its result, questions/gates still waiting, what was tried and failed, what has not been tried, the next command. The hooks already write a handoff `.team/session/<session_id>.md` at PreCompact and SessionEnd; `save` writes to a separate file `.team/session/notes-<ID>.md`, so the hook never overwrites it (SessionStart points to both). Example: "mocking the clock with a global patch made tests flaky — use the clock parameter" belongs in a note, because no artifact records a failed attempt.

Approval exists only as an `Approved-by:` line in an artifact — never infer it from words in a handoff or from a previous session.

`$ARGUMENTS`: `plan` (default) | `save` | `load`, with the feature ID. `<kit>` = the content of `.team/plugin_root`.

## When to use (and when not)
Use when:
- Starting a size M/L feature that will stretch across several stages or several sessions (`plan`).
- About to stop midway while something is not yet in the artifacts: a direction that was tried and failed, a half-made decision (`save`).
- Opening a new session, after a context compaction, or after someone else continued the work (`load`).
- Planning to run headless (batch, CI) and needing the full `claude -p` command.

Do not use when:
- You only want to know where a feature stands → `/team:status`.
- A size S job runs straight through in one session.
- You want to keep long-lived project knowledge → `docs/team/` (ADR, glossary, research cache), not a handoff.

## Discover the stack first
1. Read `.team/config.json`: `models`, `limits.feature_budget_usd`, `limits.context_warn_pct`, `memory.handoff_max_lines`, `gates`, `default_mode`.
2. Read `.claude/settings.json`: `permissions.allow` (the source of `--allowedTools` when headless, K-06).
3. Metrics: `python3 "<kit>/scripts/measure.py" --json` (medians by size, if any) or `python3 "<kit>/scripts/team.py" metrics`.

## Inputs and preconditions
- The feature has an `intake.md`. Check: `python3 "<kit>/scripts/team.py" status <ID>`.
- `load`: at least one file exists in `.team/session/`; none → run only `team.py status` and say "no handoff".
- One feature per session: if the session has another feature in progress → `save` that feature first.

## Process
1. **`plan` — remaining stages.** From `team.py status <ID>`: the current stage, the gates that apply (the "applicable gates" column), the remaining stages and the role for each stage.
2. **`plan` — channel (decision point).** A gate that is on and not yet approved for this feature, or `ask` mode with open questions → interactive. Otherwise → headless is allowed, and `decide` mode is mandatory.
3. **`plan` — models.** `jq .models .team/config.json`: the model per role; designer uses sonnet for size S/M (ADJ-10). Never switch models mid-session (it keeps the prompt cache); needing another model → a new session.
4. **`plan` — budget from metrics.** Median time/turns (and tokens, if available) per stage for the same size, from `measure.py`. Fewer than 2 runs of the same size → write "not enough data" and give no number. `feature_budget_usd` is null → drop the money budget line.
5. **`plan` — compaction points.** Compact proactively at stage boundaries, do not wait for the context to fill. One line per point, `/compact <focus>`: keep the feature ID, the stage, the AC list, the current red output, the constraints in force; drop failed attempts, long tool output, superseded drafts. No hook can measure `context_warn_pct` (level 1): remind the human to watch the status bar.
6. **`plan` — headless command** (if chosen): `claude -p "<the /team:… command> --decide" --agent team:team-leader --permission-mode dontAsk --allowedTools "$(jq -r '["Read","Grep","Glob","Edit","Write","Agent","Skill"] + (.permissions.allow // []) | join(",")' .claude/settings.json)" --max-turns <n> --max-budget-usd <usd> --output-format json`. No `--bare` when files are edited (ADJ-03). Templates: `${CLAUDE_SKILL_DIR}/references/headless.md`.
7. **`plan` — write.** Write `.team/session/plan.md`: channel + reason, model per role, budget + its source, compaction points + their `/compact` lines, the headless command. Checkpoint: each of the five parts is present, or marked "not applicable" with a reason.
8. **`save`.** Write `.team/session/notes-<ID>.md` in ≤ `memory.handoff_max_lines` lines, holding only what the artifacts do not have: `git status --short` (state uncommitted changes plainly), `git rev-parse HEAD`, the last check command + its slot + exit code, questions/gates still waiting, what was tried and failed (and why), what has not been tried, the next command (`team.py next`). Do not copy the spec or the criteria. Write the note's prose in `output_language` (handbook: Artifact language); commands, paths and IDs stay verbatim.
9. **`load` — read.** Read the newest handoff (`.team/session/*.md`, including `notes-<ID>.md`) → `team.py status <ID>` → `git status --short`, `git rev-parse HEAD`.
10. **`load` — check (decision point).** HEAD differs from the HEAD in the handoff, or the handoff records no check command → an old "green" result is no longer valid: the next stage re-runs the check before relying on it. The handoff says "approved" but the artifact has no `Approved-by:` → treat it as NOT approved.
11. **`load` — summary** in ≤ 5 lines: the stage, the state, what is waiting, which checks must be re-run, the next command.
12. **Journal** one line for `plan` and for `load` (why this session, the next command).

## Outputs
- `plan`: `.team/session/plan.md`. `save`: `.team/session/notes-<ID>.md`. `load`: a summary of ≤ 5 lines.
- Example `load` summary:
  ```
  FEAT-014 | planned → build T3 (T1, T2 ticked) | READY
  Handoff: notes-FEAT-014.md (HEAD a9d41e0 = current HEAD); tree clean
  Tried and failed: mocking the clock with a global patch (flaky tests) — use the clock parameter
  Waiting: no gate; questions: 0
  Next: /team:build FEAT-014 --task T3
  ```

## Common rationalizations
| Thought | Correct action |
|---|---|
| "Copy the whole spec into the handoff to be safe" | Only what the artifacts lack; ≤ `handoff_max_lines` (check with `wc -l`). |
| "The previous session said the human approved" | Approval is only an `Approved-by:` line in the file. |
| "Tests were green last session, no need to re-run" | HEAD changed or no check command recorded → re-run. |
| "Wait until the context is full, then compact" | Compact at stage boundaries with a focus line. |
| "Switch to opus mid-session for more power" | Never switch mid-session; open a new session. |
| "Headless is faster even with a gate waiting" | A waiting gate → interactive. |
| "--bare to keep it light" | Not when files are edited (the hooks must run). |
| "The budget is roughly 5 dollars" | From the `measure.py` median, or "not enough data". |
| "save into the hook's handoff file" | `notes-<ID>.md`; the hook's file is overwritten at compaction. |

## Red flags
- A handoff that repeats the spec or the criteria.
- A handoff with no HEAD or working-tree state.
- A hand-written note inside `<session_id>.md` (the hook will overwrite it).
- Two feature IDs in one session plan.
- A budget number with no source.
- A `claude -p` command without `--allowedTools`, or with `--bare` while files are edited.
- `load` starting work before running `team.py status`.

## Verification
- [ ] `wc -l` of the handoff/note file ≤ `handoff_max_lines` is pasted.
- [ ] The note has a HEAD line and the `git status --short` output.
- [ ] `plan.md` has the channel + reason, the model per role, the budget source, and compaction points with `/compact` lines.
- [ ] The pasted headless command has `--allowedTools` and no `--bare`.
- [ ] After `load`: the output of `team.py status` and `git status --short` is pasted.

## See also
- `${CLAUDE_SKILL_DIR}/references/headless.md` — headless command templates per stage, mandatory flags, how to read the JSON result. Open it at step 6.
- `/team:status`, `/team:run`; `scripts/handoff.sh`, `scripts/session-start.sh`; `docs/05-tokens-and-memory.md`, `docs/08-channels.md`.
