---
name: feedback
description: Use when the human or a role wants to record feedback on one of the team's agents or skills: good, slow, wrong, hard to use.
argument-hint: "<agent|skill> <1-5> \"<comment>\" [<ID>]"
allowed-tools: Bash(jq *) Bash(cat *) Bash(date *) Bash(mkdir *) Bash(tail *)
---

# Record feedback

## Overview
Write one structured feedback line about an agent or skill so coach can measure it. `$ARGUMENTS`: the subject (`agent:<name>` or `skill:<name>`), a score 1–5, a comment, a feature ID (optional).

## Process
1. Check that the subject exists in the kit's `agents/`/`skills/` or the project's `.claude/`; if not → report it, stop.
2. Take `feature`, `stage` from `.team/current.json` when not passed.
3. Read `docs/team/metrics/feedback.jsonl` (it may not exist yet), then Write the file back with one new JSON line at the end:
   `{"ts": "<ISO>", "from": "<human|role>", "about": "<agent|skill>:<name>", "feature": "<ID>", "stage": "<stage>", "score": <1-5>, "note": "<comment>"}`.
4. Check that the last line is valid: `tail -n 1 docs/team/metrics/feedback.jsonl | jq .`.
5. Score ≤ 2 → remind: two scores past the threshold for the same subject trigger `/team:retro`.

## Common rationalizations
| Thought | Correct action |
|---|---|
| "Fix the agent right away based on the feedback" | Only record it; coach diagnoses, the human approves. |
| "Append quickly with `jq >>`" | Use Write; headless mode refuses redirection. |
| "Rewrite the whole file to clean it up" | Keep every old line, add exactly one. |
| "Skip the score, it's hard to pick" | A score 1–5 is mandatory. |
| "Just write 'slow'" | Name the concrete task, feature and stage. |
| "The feedback is about the project, not the team" | Only agents/skills; project defects go in `debt.md`. |

## Verification
- `jq` parses the last line — paste the output.
- The file's line count grew by exactly 1 (`wc -l` before/after).
