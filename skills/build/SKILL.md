---
name: build
description: Use when a plan is approved (or the work is size S, a bug-fix or a hotfix) and a dev must write tests and code, a reviewer must grade them, and each task must be merged into the feature branch.
argument-hint: "<ID> [--task T<N>] [--decide]"
context: fork
agent: team:tech-lead
background: false
allowed-tools: Bash(python3 *) Bash(cat *) Bash(git *) Bash(touch .team/active-build) Bash(rm .team/active-build)
---

# The build loop: dev → reviewer → fix → merge

## Overview
This skill runs a feature's build loop until every task in `tasks.md` is ticked: the dev (own worktree) writes a failing test first, then the code; the reviewer (fresh context, read-only) grades it against the Review checklist (10); the dev fixes blockers/majors; the tech-lead merges the task branch into `team/<ID>` and runs `cmd.test`. The skill runs in the `tech-lead` context (fork); the tech-lead calls only `team:dev`, `team:reviewer` and Explore.

One rule never changes with size: **size S still goes through this skill with 1 dev + 1 reviewer** (K-34). Nobody says "done" without the output of a real command. `.team/active-build` is created at the start and removed on EVERY exit; the `stop-check.sh` hook reads it to run lint/test when the dev and the tech-lead stop. Example: a one-line hotfix still produces a red-then-green `cmd.test_one` output, a `review-01.md` and a merge commit on `team/<ID>`.

`$ARGUMENTS`: the `<ID>`; `--task T<N>` to run a single task; `--decide`. `<kit>` = the content of `.team/plugin_root`.

## When to use (and when not)
Use when:
- A plan exists and G3 has passed (or does not apply, per `team.py`).
- Size S, bug-fix or hotfix with a `spec.md` (or an intake describing the bug) but no `tasks.md` yet → create a one-task `tasks.md`, then run.
- qa returned `rework` → rerun exactly the failing task with `--task T<N>`.

Do not use when:
- A gate before build is still waiting for approval → stop and print the gate.
- The work is a cleanup that does not change behavior → `/team:clean`.
- The work is fixing CI → `/team:ci`.

## Discover the stack first
1. Read `.team/profile.json`: `cmd.test_one`, `cmd.test`, `cmd.lint`, `cmd.typecheck`, `naming.test_file`, `naming.branch`, `structure.allowed_new_file_roots`, `protected_paths`. `cmd.test_one` missing → stop and report (never guess the command).
2. Read `.team/config.json`: `base_branch`, `limits.max_parallel_dev`, `limits.max_rework`, `limits.max_attempts`, `limits.max_agents_per_feature`.
3. Resume from disk: if `.team/active-build` already exists → read `tasks.md` and `git log --oneline <base_branch>..team/<ID>` BEFORE anything else; ticked tasks are never redone.

## Inputs and preconditions
- `python3 "<kit>/scripts/team.py" status <ID>`: no `WAITING_FOR_APPROVAL` for a gate before build.
- `tasks.md` with lines `- [ ] T<N> — … — files: … — test: … — depends: …`; size S without one → Write a single task from `spec.md` (files = the touchpoints in the spec/intake, test = a test file named per `naming.test_file`).
- `design.md` (size M/L) for the reviewer to compare against.
- Branch `team/<ID>` exists (create it from `base_branch` if missing).

## Process
1. **Switch the build on.** `touch .team/active-build`; Write `.team/current.json` {feature, stage: "build", agent: "tech-lead", started_at}.
2. **Check before calling anyone (preflight).** Tabulate every pair of tasks that touch a shared file or interface; tasks that contradict themselves (their test does not match their touchpoints); tasks that require something the Review checklist treats as a defect. Any problem → `DESIGN_CONFLICT` to the team-leader, and no dev is called yet.
3. **Pick a wave.** Every unticked task whose `depends:` are all ticked, up to `limits.max_parallel_dev`, with no two sharing a file or interface (the preflight table). Migrations and shared state go alone. One ready task → a wave of one. Write the wave into `tasks.md` progress (`wave N: T2, T3`).
4. **Record BASE.** `git rev-parse team/<ID>` → write `BASE=<sha>` into each wave task's progress line in `tasks.md` (Edit). The reviewer's diff is always `BASE..<task branch head>`, never `HEAD~1`.
5. **Call the devs** — every task of the wave in ONE message: one Agent `team:dev` call per task, each in its own worktree, so they run at the same time; never one after another when the wave has two or more tasks. Each call gets a handoff message ≤ 10 lines: task code; criteria (quoted); touchpoints; `cmd.test_one` with `{file}` set to the test file; branch `team/<ID>-task-N` created from `team/<ID>`; the sentence "only modify inside the touchpoints"; where to write the detailed report. Message templates: `${CLAUDE_SKILL_DIR}/references/handoffs.md`.
6. **Read each dev's status** (steps 6–11 run per task; a stop in one task does not cancel the others already running) — the first line of the return message is one of `DONE`, `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, `BLOCKED`, `DESIGN_CONFLICT` (decision point):
   - `DONE`: check there is a RED output for the right reason (missing behavior, not an import/syntax error) and a GREEN one after; check the full `cmd.test` is there; anything missing → back to the dev (counts as one attempt).
   - `DONE_WITH_CONCERNS`: a concern about correctness or scope → resolve it before review; any other concern → note it for the review.
   - `NEEDS_CONTEXT`: add the context and call again; never resend the old message unchanged.
   - `BLOCKED`: change one thing (add context, split the task, report that the plan is wrong); after `limits.max_attempts` → stop.
   - `DESIGN_CONFLICT`: stop and report to the team-leader.
7. **Review package.** Write `docs/team/features/<ID>/review-pkg-T<N>.md`: the list of commits, `git diff --stat` and `git diff BASE..team/<ID>-task-N`. The reviewer reads one file.
8. **Call the reviewers** (Agent `team:reviewer`), one per task that is ready for review, all in ONE message: the review package path, `design.md`, the task criteria, the sentence "grade against the Review checklist (10)". Do not include the dev's explanations; never say "don't flag X".
9. **Read the verdict** — `approve` / `request-changes` / `design-defect`, with a list of "cannot verify from the diff":
   - `design-defect` → stop and report to the team-leader.
   - "Cannot verify" items → the tech-lead (who holds the context of several tasks) resolves them before ticking; if something is really missing → treat it as a failed review.
10. **Rework round** (`request-changes`): send the dev the blocker/major findings verbatim + the review path; a new dev sits in a new worktree and must `git switch team/<ID>-task-N` inside its own worktree (K-14). The fix report must contain: finding → change → covering test → command + output. Call the reviewer again in **scoped re-review** mode: only the fix diff (`FIX_BASE..HEAD`), each old finding marked `ADDRESSED` / `NOT ADDRESSED`; out-of-scope notes go to `deferred` and do not extend the round.
11. **Break the loop.** Count the rounds; > `limits.max_rework`, or the same defect in two rounds → stop; write a ruling for each open finding (reviewer wrong / real but deferred / blocking) and escalate to the team-leader. The last round before the cap may use a fresh dev with the old report as input.
12. **Merge and tick** (`approve`): merges are serial, one task at a time in task order; merge `team/<ID>-task-N` into `team/<ID>` (git), run `cmd.test` on `team/<ID>` after each merge. Red → find out whether the merge or an earlier task caused it before doing anything else; do not tick. Green → tick the task (`- [x] T<N>`), Write `review-NN.md` from `<kit>/templates/artifacts/review.md` (verdict, findings, number of rounds, diff command, `deferred` section), and write one journal line. Write prose in `output_language` with the template from the matching language folder (handbook: Artifact language).
13. **Loop** back to step 3 for the next wave once every task of this wave is ticked or stopped.
14. **All tasks done.** Run `git diff <base_branch>...team/<ID>` and write its output to `docs/team/features/<ID>/diff.patch` with Write (for the writer). Record the number of roles used (distinct roles, not counting re-calls within rework rounds) against `limits.max_agents_per_feature`.
15. **Every exit** (done, stopped, error): `rm .team/active-build`.

## Outputs
- Commits on `team/<ID>`; `docs/team/features/<ID>/tasks.md` ticked; a `review-NN.md` per task; `diff.patch`.
- One journal line per dev/reviewer call (the reason before the call, the result after), prose in `output_language`.
- Return message to the team-leader, ≤ 10 lines:
  ```
  tech-lead -> team-leader | FEAT-012 | DONE
  Tasks ticked: T1..T4 (review-01..04 approve). Roles used: dev, reviewer (cap M: 6)
  Rework: T3 two rounds (max_rework=3), round 2 clean
  cmd.test on team/FEAT-012: exit 0, "Ran 42 tests … OK"
  Deferred (minor): review-03 STD-NAME-2
  Files: docs/team/features/FEAT-012/{tasks,review-01..04,diff.patch}
  Next: /team:verify FEAT-012
  ```

## Common rationalizations
| Thought | Correct action |
|---|---|
| "Size S, a one-line fix, no reviewer needed" | Still call `team:reviewer` (K-34). |
| "The dev says the tests are green" | You need the pasted red-then-green output; missing → send it back. |
| "Red because of an import error is still red" | Red must come from missing behavior; send the dev back to fix the test. |
| "A flaky red test, unrelated, merge anyway" | Stop: reproduce it, record it in `debt.md` (STD-TEST-7); do not merge. |
| "Three lines to fix, I will do it myself" | Send it to the dev; the tech-lead writes only `docs/team/**`. |
| "One more rework round and it is done" | Over `max_rework`, or the same defect twice: stop and escalate. |
| "The reviewer is nitpicking, drop that finding" | Rule on it only at the cap, in writing; never drop it silently. |
| "HEAD~1 is the task's diff" | Use the recorded `BASE..task branch head`. |
| "I remember what task 3 did" | Reread the task line and `git log`; the tick on disk is the truth. |
| "Call qa now while we are at it" | The tech-lead calls only dev, reviewer and Explore. |
| "Safer to run the devs one by one" | Ready, file-disjoint tasks form one wave; call all of them in one message, up to `max_parallel_dev`. |

## Red flags
- A test is green on its first run, or there is no red output.
- The dev's return message has no command, or says "should work".
- The diff touches files outside the touchpoints, or `.team/profile.json`/`config.json`.
- Two running tasks touch the same file.
- A wave of two or more ready tasks was dispatched one dev at a time.
- A `review-NN.md` says approve without a diff command or a tier-1 verdict.
- The same finding appears in two consecutive rounds.
- A task is ticked without a merge commit on `team/<ID>`; `.team/active-build` remains after stopping.
- Size S has only a dev call and no reviewer.

## Verification
- [ ] Each task: the red output (name of the failing assertion) and the green output of `cmd.test_one` are pasted.
- [ ] `cmd.test` on `team/<ID>` after the last merge: exit 0, output pasted.
- [ ] `git log --oneline <base_branch>..team/<ID>` is pasted; each commit has the form `type(scope): description (<ID>)`.
- [ ] `git diff --name-only` of each task is a subset of its touchpoints.
- [ ] Each task has a `review-NN.md` with verdict, diff command and round count; rework rounds have ADDRESSED/NOT ADDRESSED.
- [ ] `tasks.md` progress lists each wave; a wave of two or more tasks shows its dev calls sent together.
- [ ] `ls .team/active-build` reports no such file; `diff.patch` exists and is not empty.

## See also
- `${CLAUDE_SKILL_DIR}/references/handoffs.md` — handoff templates for the dev, the reviewer and rework rounds; the status table.
- Agents `tech-lead`, `dev`, `reviewer`; `<kit>/templates/artifacts/review.md`, `tasks.md`.
- `/team:plan` (before), `/team:verify` (after), `/team:commit` (used by the dev).
- `handbook/STD.md`: Review checklist (10), STD-TEST-1/4/5, STD-DESIGN-1, STD-GIT-3/4.
