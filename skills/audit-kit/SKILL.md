---
name: audit-kit
description: Use when the `team` kit running in this project needs an audit of itself: a hook that can be bypassed, permissions broader than the contract, contradictory instructions, mismatched names, unused skills, or agents hitting their turn limit.
argument-hint: "[--since <YYYY-MM-DD>]"
disable-model-invocation: true
context: fork
agent: team:coach
background: false
allowed-tools: Bash(python3 *) Bash(cat *) Bash(jq *) Bash(ls *)
---

# Audit the kit

## Overview
This skill looks for defects in the KIT — agents, skills, hooks, scripts, templates — not in the project, and records each defect with its evidence in `docs/team/kit-issues.md` so the human can report it to the `automation-ai` repo. It runs in the `coach` context (fork): Bash is read-only, it calls no other role, and it never edits a kit file. One defect found is one row; fixing it is the kit maintainer's job, not the auditor's.

Point of view: machine rules (hooks, permissions, scripts) are the law. Any place where a machine rule can be bypassed, fails open, or says one thing and does another is a heavier defect than wrong prose. "0 issues" only means something when every check states the scope it covered; a check that could not run is written as "skipped: <reason>", never left silent. Example: a hook that exits 1 on malformed JSON lets the write through, so it is a major defect even if every document says the path is protected.

`$ARGUMENTS`: `--since <YYYY-MM-DD>` for the metric-based checks (default 30 days). `<kit>` = the content of `.team/plugin_root`.

## When to use (and when not)
Use when:
- On a regular cadence (the same rhythm as retro), or after upgrading the kit version.
- A hook blocked something by mistake or let something through once; an agent broke a rule and nothing stopped it.
- `/team:retro` found that the cause sits in the kit (prompt, hook, template) rather than in the project.

Do not use when:
- You are looking for the project's technical debt → `debt.md`, `/team:clean`.
- You want to propose a change to an agent/skill from effectiveness metrics → `/team:retro` (proposal with eval and canary).
- You want the kit defect fixed right now → not here; report it to the kit repo and let the maintainer fix it.

## Discover the stack first
1. Read `.team/plugin_root` → `<kit>`; take the `realpath` of `<kit>` and of the project root (step 2 needs both).
2. Read `<kit>/hooks/hooks.json`, `<kit>/hooks/role-policy.json`, `<kit>/templates/schemas/profile.schema.json`.
3. Glob `<kit>/agents/*.md`, `<kit>/skills/*/SKILL.md`, `.claude/skills/*/SKILL.md`, `.claude/agents/*.md`; Read `docs/team/skills-registry.md`.
4. Metrics: `docs/team/metrics/runs.jsonl` (present or not, and how many lines since the start date).
5. Known issues: `<kit>/docs/kit-issues.md` when it is readable (used for de-duplication in step 8).

## Inputs and preconditions
- The kit is readable at `<kit>`; if not → `BLOCKED`, naming the path that failed.
- No `runs.jsonl`: STILL run the static checks; the metric-based checks are recorded as "skipped: no data". Missing metrics are not a reason to stop (unlike retro, which needs them).
- Where to write (K-44): `<kit>` equals the project root, or the project root lies inside `<kit>` (you are running inside the kit repo itself) → do NOT write `docs/team/kit-issues.md`; print the rows in the return message, using the columns of `docs/kit-issues.md`, and say "copy into docs/kit-issues.md".

## Process
1. **Record position.** Write `.team/current.json` {feature: "audit-kit", stage: "audit", agent: "coach", started_at}. Checkpoint: the file exists before any check runs, so a stopped run still shows where it was.
2. **Decide where to write** using the K-44 condition above; state the decision (file or return message, and the two `realpath` values) at the top of the report.
2a. **Skeleton first, then write as you go (K-74).** Write `docs/team/kit-issues.md` from the template immediately: the scope table lists all of S1–S14 and D1–D3 with status "not run yet". After every group of 3–4 checks, Edit in the issue rows and update the scope table. Seventeen checks do not fit one 40-turn run: if turns run out midway, the file still holds every result so far; on a re-run → read the scope table and continue with the checks still "not run yet". Each check gets a few commands at most; when you need to try several command forms, combine them in one command instead of one command per form. Write prose in `output_language` with the template from the matching language folder (handbook: Artifact language).
3. **Static checks S1–S14** following `${CLAUDE_SKILL_DIR}/references/checks.md`, one after another. For each check: the command run or file read → the result → a scope line (`checked: N files / skipped: reason`). Exit condition: every static check has a scope line, even when it found nothing.
4. **Machine rules first.** For hooks (S2, S3, S4): read the script's code, not only the documentation. A hook that "exists" but whose matcher misses a tool, or that fails open on error, is a defect even when the docs say the action is blocked. Quote the exit code path you found (`file:line`).
5. **Write lists per role (S5).** Compare three places for each role: `role-policy.json`, the "writes only …" sentence in the agent file, and SPEC §3 plus the ADJ entries. Any mismatch → one row, with the three quotations pasted side by side.
6. **Metric-based checks D1–D3** when `runs.jsonl` exists: read it with `jq`; state exactly which data is missing (a skill that never logs metrics ≠ a skill that is never used; `result` is guessed from text). Without the file, each D check gets "skipped: no data" in the scope table.
7. **Assign a level.** blocker = the process gets stuck, or a result is wrong and nobody notices; major = a machine rule can be bypassed, or permissions are broader than the contract; minor = mismatched names, documentation, descriptions. Every level comes with a one-sentence reason.
8. **De-duplicate.** Compare with `<kit>/docs/kit-issues.md`: a duplicate → status "known (K-xx)" plus the new evidence (it may have regressed); a new finding → "new".
9. **Evidence on every row.** `file:line`, or the command plus its output. No evidence → do not write that row; mention it as an unconfirmed lead in the return message instead.
10. **Write.** Write `docs/team/kit-issues.md` from `<kit>/templates/artifacts/kit-issues.md` (its issue table columns — ID, level, status, location, symptom with evidence, proposal — and its scope table), or print the rows in the return message when K-44 applies.
11. **Final check.** `git status --short`: only `docs/team/kit-issues.md`, `.team/current.json` (and coach's memory) have changed. The count of rows per level in the return message equals the count in the file.
12. **Return** to team-leader in ≤ 10 lines, first line `coach -> team-leader | audit-kit <date> | <N> issues`.

## Outputs
- `docs/team/kit-issues.md` (or the rows inside the return message when running inside the kit repo).
- Example return message:
  ```
  coach -> team-leader | audit-kit 2026-11-16 | 5 issues (0 blocker, 2 major, 3 minor)
  File: docs/team/kit-issues.md (14 static checks; 3 metric checks: 2 run, 1 skipped — no skill data)
  Major: A-01 role-policy allows `uniq IN OUT` (teamlib.py:398, new); A-02 clean-sweep missing cmd.* in --allowedTools (known K-06)
  Minor: A-03 skill `foo` description is 540 chars; A-04 coach write list differs across three places (known K-43); A-05 docs mention a skill command with no folder under skills/
  Scope: 13 agents, 26 skills, 2 temp skills, 9 hooks
  Human action: report A-01, A-05 to the automation-ai repo
  ```

## Common rationalizations
| Thought | Correct action |
|---|---|
| "No runs.jsonl, so skip the audit" | Run the static checks; mark the metric checks "no data" in the scope table. |
| "The hook exists, so the rule is enforced" | Read the matcher, the exit codes and the error path of the script; quote `file:line`. |
| "This is a project bug, record it anyway" | Kit defects only; project defects go through team-leader into `debt.md`. |
| "Found a hook bug, fix it now" | coach does not edit kit files (SPEC §3); write the row and the proposal column. |
| "jq returned nothing, so 0 unused skills" | Empty data is not clean data; write the scope and "no data". |
| "This was reported last time, skip it" | Write "known (K-xx)" with the new evidence; a repeat may be a regression. |
| "Run validate.sh, it is faster" | That script writes files; use read-only commands only. |
| "Write kit-issues right here in the kit repo" | K-44: print the rows in the return message for the human to copy. |
| "Write the report once at the end" | Skeleton first, write after every group; when turns run out the results are still there (K-74). |

## Red flags
- An issue row without `file:line` or a command plus its output.
- A level with no reason, or a level outside blocker/major/minor.
- A row that is about the project's code.
- "0 issues" with no scope table.
- coach writing a file outside its write list, or running a script that writes.
- Writing `docs/team/kit-issues.md` while running inside the kit repo.

## Verification
- [ ] Every check S1–S14 and D1–D3 has a command plus result, or "skipped: reason".
- [ ] Every issue row has `file:line` or a command plus its output.
- [ ] The write target (file or return message) is stated and matches the K-44 condition.
- [ ] The number of issues per level in the return message equals the number of rows in the file.
- [ ] `git status --short` shows only files inside coach's write zone.

## See also
- `${CLAUDE_SKILL_DIR}/references/checks.md` — the 14 static checks, the 3 metric checks, and how to de-duplicate. Open it at steps 3 and 6.
- Agent `coach`; `<kit>/templates/artifacts/kit-issues.md`.
- `/team:retro` (change proposals with eval); `handbook/tool-selection.md` (what must be a machine rule).
- `handbook/STD.md`: STD-SEC-1, STD-SEC-5, STD-SEC-8.
