---
name: plan
description: Use when a feature has an approved spec and design and must be split into 2–5 minute tasks with touchpoints, or when a change-request needs new tasks inserted (--insert).
argument-hint: "<ID> [--insert]"
context: fork
agent: team:tech-lead
background: false
allowed-tools: Bash(python3 *) Bash(cat *) Bash(git branch *)
---

# Planning → plan.md + tasks.md

## Overview
This skill splits a feature into 2–5 minute tasks, each with concrete file paths, a test file, criteria and dependencies, so that a dev who sees only one task line can still do it right without asking back. It runs in the `tech-lead` context (fork). A plan is a set of DECISIONS (files, signatures, test names, order), not a pre-written program.

A good plan: every touchpoint in `design.md` belongs to at least one task; every criterion in `spec.md` is covered by at least one task; no two parallel tasks touch the same file; size L has a walking skeleton as its first task. Example: "T2 — Reject expired OTP codes — files: src/auth/otp.py — test: tests/auth/test_otp.py — depends: T1" is a task; "do the auth part" is not.

`$ARGUMENTS`: the `<ID>`; `--insert` when a change-request adds tasks to a plan already in progress. `<kit>` = the content of `.team/plugin_root`.

## When to use (and when not)
Use when:
- The spec and (size M/L) the design are approved under the gates that `team.py` reports as applicable.
- The dependency-upgrade playbook after research: each breaking change becomes a task.
- A change-request already has an Amendment and an arch-impact → `--insert`.

Do not use when:
- Size S, bug-fix, hotfix: `/team:build` creates a one-task `tasks.md` from `spec.md` itself.
- The design still lacks touchpoints or a test plan → return `DESIGN_CONFLICT`; do not design it yourself.
- `tasks.md` already holds unticked tasks of ANOTHER piece of work → stop and escalate (never overwrite).

## Discover the stack first
1. Read `.team/profile.json`: `structure.src`, `structure.tests`, `naming.test_file`, `structure.allowed_new_file_roots`, `cmd.test_one`. Test file names in tasks follow `naming.test_file`; new files go only under the allowed roots.
2. Read `.team/config.json`: `limits.max_parallel_dev`, `limits.max_rework`, `base_branch`.
3. Check that "modify" touchpoints really exist (Glob) and that "new" touchpoints sit under the allowed roots. Any mismatch → `DESIGN_CONFLICT`.
4. Run no `cmd.*`; planning only reads and writes two files.

## Inputs and preconditions
- `docs/team/features/<ID>/spec.md` has `## Definition of Done`.
- `design.md` (size M/L), `arch-impact.md` or `docs/team/architecture.md` (size L).
- `python3 "<kit>/scripts/team.py" status <ID>`: the previous gate has passed (no `WAITING_FOR_APPROVAL`). Still waiting on a gate → hand it back and stop.
- `--insert`: the spec has a latest `## Amendment <n>` that has not been planned yet.

## Process
1. **Record the position.** Write `.team/current.json` {feature, stage: "plan", agent: "tech-lead", started_at}.
2. **File map first, tasks second.** List every file that will be created or modified and its responsibility (from the design's touchpoints). Tasks are derived from this map, never the other way round. Checkpoint: every touchpoint appears in the map before any task is written.
3. **Shared constraints.** A `## Shared constraints` section in `plan.md`: copy the values VERBATIM from the spec/design (field names, formats, limits, versions). Every task inherits them; the dev never has to guess.
4. **Dependency graph.** Write `depends:` from data flow and contracts (what must exist first for the other task's test to run), not from gut feeling. Foundations first; high-risk parts early so they fail early.
5. **Vertical slices.** Each task (or small group) delivers one checkable behavior. Horizontal splits such as "the whole DB, then the whole API" are forbidden at size M/L.
6. **Walking skeleton (size L).** T1 runs end to end through every layer with a faked core; its evidence is one end-to-end test run with `cmd.test_one`. No other task starts before T1's review is `approve`.
7. **Write tasks.md.** Write it from `<kit>/templates/artifacts/tasks.md`, one line per task:
   `- [ ] T<N> — <name> — files: <paths> — test: <test file> — depends: <T… or —>`
   followed by sub-lines: criteria (quote `AC-n`), interface (`Receives:` / `Returns:` with exact names and signatures), and `Expect:` the output of `cmd.test_one`. Write prose in `output_language` with the template from the matching language folder (handbook: Artifact language).
   No bold around the task code (`team.py` counts tasks by `- [ ] T<N>`).
8. **Right-size each task.** Split when a reviewer could reject one part and accept the other; fold preparation and docs into the task that needs them. A task with > 5 files, or whose name contains "and" → reconsider it. Each task takes 2–5 minutes.
9. **Parallelism.** A "one file, one owner" table in `plan.md`. Two tasks sharing a file → chain them with `depends:`. Migrations and shared state are always sequential. At most `limits.max_parallel_dev` tasks at a time.
10. **Checkpoints.** After every 2–3 tasks and at the end: `cmd.test` green on `team/<ID>` and the main flow runs — write them in `plan.md`.
11. **Review focus.** ≤ 5 inputs or failure modes that the spec implies but no task tests yet; add the test to the owning task.
12. **`--insert`.** Add new tasks after the last ticked task; tasks affected by the Amendment get `[affected]` at the end of the line. Never renumber existing tasks.
13. **Branch.** `git branch --list team/<ID>`; if it does not exist → create it from `config.base_branch`.
14. **5-point self-review before returning** (details: `${CLAUDE_SKILL_DIR}/references/self-review.md`): spec coverage, no vague words ("TBD", "handle edge cases"), consistent names across tasks, review focus, proportion (the plan is not longer than the code it describes).
15. **Return and stop.** Return message ≤ 10 lines; the tech-lead does NOT start the build while G3 applies and is not yet approved.

## Outputs
- `docs/team/features/<ID>/plan.md` (template `<kit>/templates/artifacts/plan.md`): order, shared constraints, the one-file-one-owner table, checkpoints, risks, review focus.
- `docs/team/features/<ID>/tasks.md` (template `<kit>/templates/artifacts/tasks.md`).
- Branch `team/<ID>`; `.team/current.json` {stage: "plan"}.
- Example return message:
  ```
  tech-lead -> team-leader | FEAT-012 | planned
  Tasks: 6 (T1 walking skeleton), 2 parallel groups {T2,T3} {T5,T6}; no shared files
  Touchpoint → task: 9/9 covered; AC → task: 4/4
  Risk: T4 touches a migration, runs sequentially
  Gate G3: applies — waiting for Approved-by in plan.md
  ```

## Common rationalizations
| Thought | Correct action |
|---|---|
| "The tasks are obvious, just start" | Write tasks.md first; hidden dependencies show up only when you list them. |
| "Task: 'do the backend part'" | Split down to 2–5 minutes with a concrete file and test file. |
| "Two tasks share a file but they are quick" | Chain them with `depends:`; never run them in parallel. |
| "Size L, a walking skeleton is too much effort" | It is mandatory; it proves the riskiest integration first. |
| "Let the dev pick the test file" | Write `test:` now; the reviewer and qa need it too. |
| "Plan the happy path, edge cases later" | The review focus lists the edge cases, each with a test. |
| "The old tasks.md is stale, overwrite it" | An unticked task may be in progress; stop and escalate. |
| "That touchpoint is tiny, skip it" | The touchpoint → task table must cover all of them. |
| "Paste the code into the plan so the dev can copy it" | A plan holds signatures and test names, not a program. |
| "Bold the task code so it reads better" | `team.py` reads `- [ ] T<N>`; keep the exact form. |

## Red flags
- A task without `files:` or `test:`; a missing `depends:`.
- A touchpoint in `design.md` that belongs to no task.
- A task touching > 5 files, or a horizontal split by layer at size M/L.
- Size L without a walking skeleton; T1 without an end-to-end test.
- Two parallel tasks touching the same file.
- Function/field names that differ between tasks.
- A stack command hard-coded in the plan (it must be a `cmd.*` slot).

## Verification
- [ ] Paste the touchpoint → task table, with no empty row.
- [ ] Paste the AC → task table; every criterion has at least one task.
- [ ] `grep -cE '^- \[ \] T[0-9]+' docs/team/features/<ID>/tasks.md` equals the task count in the return message.
- [ ] Every task line has `files:`, `test:`, `depends:` (paste the empty output of the `grep -L`/awk check).
- [ ] `git branch --list team/<ID>` shows the branch.
- [ ] Paste the output of `team.py status <ID>` showing `planned` (or waiting for G3).

## See also
- `${CLAUDE_SKILL_DIR}/references/self-review.md` — the 5 self-review points, the interface block template.
- Agent `tech-lead`; `<kit>/templates/artifacts/plan.md`, `tasks.md`.
- `/team:design` (previous step), `/team:build` (next step), `/team:analyze --amend` (when the plan exposes a contradiction in the spec).
- `handbook/STD.md`: STD-DESIGN-1 (touchpoints), STD-GIT-1 (one task, one PR/commit), STD-TEST-2.
