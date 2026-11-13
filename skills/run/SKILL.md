---
name: run
description: Use when the human wants the team to move a feature on to the next stage or gate, or to keep running until it is blocked.
argument-hint: "[<ID>] [--until-blocked] | --all"
allowed-tools: Bash(python3 *) Bash(cat *)
---

# Move a feature forward

## Overview
Run the feature's next stage according to its playbook and gates. `$ARGUMENTS`: a feature ID (default from `.team/current.json`), `--until-blocked` to loop until blocked; `--all` to move every ready feature at once, in parallel waves capped by `limits.headcount` (follow `${CLAUDE_SKILL_DIR}/references/parallel-wave.md` instead of the steps below). Never pass a gate.

## Process
1. Check that `docs/team/features/<ID>/intake.md` exists; if not → print `/team:intake`, stop.
2. Bash: `python3 "<kit>/scripts/team.py" next <ID>` and `status <ID>` (`<kit>` = the path read from `.team/plugin_root`, typed literally).
3. Gates: ONLY from the `team.py` output (already adjusted for size: S skips G1, G3; refactor/data-migration enable G2b). Do not read `gates` in config yourself. `WAITING_FOR_*` → stop and print what the human must do.
4. The next command is `/team:release` (human-only: merge, tag, deploy) → print the command, stop.
5. Write a one-sentence reason in the journal (Write; prose in `output_language`), then call the next skill (Skill). Size S still goes through `/team:build` so a reviewer runs.
6. After the skill: rerun `team.py status <ID>`. Progress = the stage changed, or `tasks_done` grew (a build that ran out of turns resumes from `tasks.md`; call `/team:build` again). Neither → stop and report (do not rerun the same skill).
7. Log metrics: `bash "<kit>/scripts/log-run.sh" --feature <ID> --skill <skill> --result <result>`.
8. `--until-blocked` → back to step 2; otherwise → stop.

## Common rationalizations
| Thought | Correct action |
|---|---|
| "The gate will surely be approved" | Stop at the gate. |
| "Config enables G1, so we must wait" | Trust `team.py`; size S has no G1. |
| "Size S, call dev directly to save time" | Still `/team:build` (dev + reviewer). |
| "Status didn't change, rerun build" | Stop and report; an artifact may be malformed. |
| "Another feature waits on a gate, so stop everything" | A gate blocks only its own feature. |
| "Skip log-run to go faster" | Metrics are the input to retro. |
| "`--all`: call the skills one by one" | One message, one Agent call per wave item. |

## Verification
- The `team.py status <ID>` output (`--all`: `team.py wave`) is pasted after each stage or wave.
- Every skill called has a journal line.
- Every stop uses the 4-line stop message: `STOP: <reason>` / `Work: <item>` / `Who does what: <who>` / `Resume: <command>`.
