---
name: build
description: Use when a plan is approved (or the work is size S, a bug-fix or a hotfix) and a dev must write tests and code, a reviewer must grade them, and each task must be merged into the feature branch.
argument-hint: "<ID> [--task T<N>] [--decide]"
context: fork
agent: team:tech-lead
background: false
allowed-tools: Bash(python3 *) Bash(cat *) Bash(git *) Bash(touch .team/active-build-*) Bash(rm .team/active-build-*) Bash(rm -f .team/active-build-*)
---

# The build loop: dev → reviewer → fix → merge

## Overview
This skill runs a feature's build loop until every task in `tasks.md` is ticked: the dev (own worktree) writes a failing test first, then the code; the reviewer (fresh context, read-only) grades it against the Review checklist (10); the dev fixes blockers/majors; the tech-lead merges the task branch into `team/<ID>` and runs `cmd.test`. The skill runs in the `tech-lead` context (fork); the tech-lead calls only `team:dev`, `team:reviewer` and Explore.

One rule never changes with size: **size S still goes through this skill with 1 dev + 1 reviewer** (K-34); only playbook quick skips it (one dev called by team-leader, ADJ-36). Nobody says "done" without the output of a real command. `.team/active-build-<ID>` (one per feature, so parallel builds do not switch each other off) is created at the start and removed on EVERY exit; the `stop-check.sh` hook reads it to run lint/test when the dev and the tech-lead stop. Example: a one-line hotfix still produces a red-then-green `cmd.test_one` output, a `review-01.md` and a merge commit on `team/<ID>`.

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
2. Read `.team/config.json`: `base_branch`, `limits.headcount.dev` / `limits.max_parallel_dev`, `limits.headcount.reviewer`, `limits.max_rework`, `limits.max_attempts`, `limits.max_agents_per_feature`.
3. Resume from disk: if `.team/active-build-<ID>` already exists → read `tasks.md` and `git log --oneline <base_branch>..team/<ID>` BEFORE anything else; ticked tasks are never redone.

## Inputs and preconditions
- `python3 "<kit>/scripts/team.py" status <ID>`: no `WAITING_FOR_APPROVAL` for a gate before build.
- `tasks.md` with lines `- [ ] T<N> — … — files: … — test: … — depends: …`; size S without one → Write a single task from `spec.md` (files = the touchpoints in the spec/intake, test = a test file named per `naming.test_file`).
- `design.md` (size M/L) for the reviewer to compare against.
- Branch `team/<ID>` exists (create it from `base_branch` if missing).

## Process
1. **Switch the build on.** `touch .team/active-build-<ID>`; Write `.team/current.json` {feature, stage: "build", agent: "tech-lead", started_at}. First run of this feature (no `baseline:` line in `tasks.md`): run `cmd.test` on `team/<ID>` and write `baseline: <counts> — red: <test names>` at the top of the progress section. "Green" from here on means no red test outside that list; never fix or skip a baseline failure inside a task.
2. **Check before calling anyone (preflight).** Tabulate every pair of tasks that touch a shared file or interface; tasks that contradict themselves (their test does not match their touchpoints); tasks that require something the Review checklist treats as a defect. Any problem → `DESIGN_CONFLICT` to the team-leader, and no dev is called yet.
3. **Pick what can start.** A task is ready when every `depends:` is ticked and it shares no file or interface (the preflight table) with any task in flight (in dev, review or rework). Take ready tasks up to your free dev share (the share minus devs in flight). Migrations and shared state go alone. `test.shared_state` true in the profile (tests share one database or site) → while two or more devs are in flight, devs run only `cmd.test_one`; the full `cmd.test` runs once after each serial merge (step 12). Write each round into `tasks.md` progress (`round N: dev T4, T5; review T2, T3`). Dev share: the `devs=` line of the team-leader's handoff when several features build at once (`team.py wave` splits the team-wide headcount), else `limits.headcount.dev`, else `limits.max_parallel_dev`; reviewers likewise (`reviewers=`, else `limits.headcount.reviewer`, else the dev share).
4. **Record BASE.** `git rev-parse team/<ID>` → write `BASE=<sha>` into the progress line of each task the round starts in `tasks.md` (Edit). The reviewer's diff is always `BASE..<task branch head>`, never `HEAD~1`.
5. **Dispatch round — ONE message.** Every call that can start now goes into one message, so they run at the same time: one Agent `team:dev` call per ready task (step 3) and per rework (step 10), each in its own worktree, plus one `team:reviewer` call per task ready for review (step 8). Never hold a ready task, a rework or a review back for a later round, and never send them one after another. Each call gets a handoff message ≤ 10 lines: task code; criteria (quoted); touchpoints; `cmd.test_one` with `{file}` set to the test file; branch `team/<ID>-task-N` created from `team/<ID>`; the sentence "only modify inside the touchpoints"; the **recurring findings** of this feature (each STD code that two or more `review-NN.md` of this feature flagged, one line with its fix pattern, ≤ 3 lines; none yet → omit), which dev checks its own diff against before returning `DONE`; where to write the detailed report. Message templates: `${CLAUDE_SKILL_DIR}/references/handoffs.md`.
6. **Read each dev's status** (steps 6–11 run per task; a stop in one task does not cancel the others already running) — the first line of the return message is one of `DONE`, `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, `BLOCKED`, `DESIGN_CONFLICT` (decision point):
   - `DONE`: check there is a RED output for the right reason (missing behavior, not an import/syntax error) and a GREEN one after; check the full `cmd.test` is there (except while devs share state, step 3); anything missing → back to the dev (counts as one attempt).
   - `DONE_WITH_CONCERNS`: a concern about correctness or scope → resolve it before review; any other concern → note it for the review.
   - `NEEDS_CONTEXT`: add the context and call again; never resend the old message unchanged.
   - `BLOCKED`: change one thing (add context, split the task, report that the plan is wrong); after `limits.max_attempts` → stop.
   - `DESIGN_CONFLICT`: stop and report to the team-leader.
7. **Review package — in the handoff, not a file.** The range `BASE..team/<ID>-task-N` (the reviewer runs `git log`, `git diff --stat` and `git diff` on it itself) and the dev's RED and GREEN output lines copied verbatim (≤ 4 lines) or the path of the dev's report. Never copy the diff into `docs/`: git already holds it.
8. **Reviewer calls** (Agent `team:reviewer`), one per task ready for review, sent in the next dispatch round (step 5) beside the devs that can start: the review package, `design.md`, the task criteria, the sentence "grade against the Review checklist (10)". Do not include the dev's explanations; never say "don't flag X".
9. **Read the verdict** — `approve` / `request-changes` / `design-defect`, with a list of "cannot verify from the diff":
   - `design-defect` → stop and report to the team-leader.
   - "Cannot verify" items → the tech-lead (who holds the context of several tasks) resolves them before ticking; if something is really missing → treat it as a failed review.
10. **Rework round** (`request-changes`): send the dev the blocker/major findings verbatim + the review path; a new dev sits in a new worktree and must `git switch team/<ID>-task-N` inside its own worktree (K-14). The fix report must contain: finding → change → covering test → command + output. Call the reviewer again in **scoped re-review** mode: only the fix diff (`FIX_BASE..HEAD`), each old finding marked `ADDRESSED` / `NOT ADDRESSED`; out-of-scope notes go to `deferred` and do not extend the round.
11. **Break the loop.** Count the rounds; > `limits.max_rework`, or the same defect in two rounds → stop; write a ruling for each open finding (reviewer wrong / real but deferred / blocking) and escalate to the team-leader. The last round before the cap may use a fresh dev with the old report as input.
12. **Merge and tick** (`approve`): merges are serial, one task at a time in task order; merge `team/<ID>-task-N` into `team/<ID>` (git), run `cmd.test` on `team/<ID>` after each merge. Red → find out whether the merge or an earlier task caused it before doing anything else; do not tick. Green → tick the task (`- [x] T<N>`), Write `review-NN.md` from `<kit>/templates/artifacts/review.md` (verdict, findings of every round, number of rounds, diff command, `deferred` section) — ONE review file per task, rounds appended to it — and write one journal line. Clean up: `git worktree remove <dev worktree>` (never `--force`; a dirty worktree → note it and keep it), then `git branch -d team/<ID>-task-N` (merged branches only, never `-D`). Write prose in `output_language` with the template from the matching language folder (handbook: Artifact language).
13. **Loop.** After each round: merge and tick the approved tasks (step 12), then back to step 3 and send the next round at once; never wait for every task of the earlier round to be ticked. Done when every task is ticked or stopped.
14. **All tasks done.** Size S (bug-fix, hotfix or new-feature S; ADJ-36): automated acceptance here, no `/team:verify` and no As-Built — Write `acceptance.md` from `<kit>/templates/artifacts/acceptance.md` (one row per criterion → the test that covers it → green; the `cmd.test` output on `team/<ID>`; `Verdict: accepted` only when every criterion has a green test, else `rework`) and add a CHANGELOG line if the project keeps one. Size M/L: run `git diff <base_branch>...team/<ID>` and write its output to `docs/team/features/<ID>/diff.patch` with Write (for the writer). Record the number of roles used (distinct roles, not counting re-calls within rework rounds) against `limits.max_agents_per_feature`.
15. **Every exit** (done, stopped, error): `rm -f .team/active-build-<ID>`.

## Outputs
- Commits on `team/<ID>`; `docs/team/features/<ID>/tasks.md` ticked; a `review-NN.md` per task; `diff.patch` (M/L) or `acceptance.md` (size S).
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
| "Size S, a one-line fix, no reviewer needed" | Still call `team:reviewer` (K-34); a trivial change is playbook quick, chosen at intake, not inside build. |
| "The dev says the tests are green" | You need the pasted red-then-green output; missing → send it back. |
| "Red because of an import error is still red" | Red must come from missing behavior; send the dev back to fix the test. |
| "A flaky red test, unrelated, merge anyway" | Stop: reproduce it, record it in `debt.md` (STD-TEST-7); do not merge. |
| "Three lines to fix, I will do it myself" | Send it to the dev; the tech-lead writes only `docs/team/**`. |
| "One more rework round and it is done" | Over `max_rework`, or the same defect twice: stop and escalate. |
| "The reviewer is nitpicking, drop that finding" | Rule on it only at the cap, in writing; never drop it silently. |
| "HEAD~1 is the task's diff" | Use the recorded `BASE..task branch head`. |
| "I remember what task 3 did" | Reread the task line and `git log`; the tick on disk is the truth. |
| "Call qa now while we are at it" | The tech-lead calls only dev, reviewer and Explore. |
| "Safer to run the devs one by one" | Ready, file-disjoint tasks start together; call all of them in one message, up to your dev share. |
| "Wait until the whole wave is ticked, then start the next" | Each round carries every call that can start: new devs, reworks and reviews together. |
| "Write the diff into docs so the reviewer has one file" | Pass the range; the reviewer runs the git commands. A copy in `docs/` only goes stale. |
| "The suite was red before we started, so red is fine" | Only the tests on the `baseline:` line may stay red; any other red test blocks the tick. |
| "Dev already got this finding last task, it will remember" | Each dev starts fresh: put the recurring findings in every handoff. |

## Red flags
- A test is green on its first run, or there is no red output.
- The dev's return message has no command, or says "should work".
- The diff touches files outside the touchpoints, or `.team/profile.json`/`config.json`.
- Two running tasks touch the same file.
- A dispatch message with one Agent call while other tasks were ready, in rework or waiting for review.
- A `review-NN.md` says approve without a diff command or a tier-1 verdict.
- The same finding appears in two consecutive rounds.
- A task is ticked without a merge commit on `team/<ID>`; `.team/active-build-<ID>` remains after stopping.
- Size S has only a dev call and no reviewer.
- `review-pkg-*` or `*.diff` files under `docs/team/`; several review files for one task.
- Merged `team/<ID>-task-*` branches still listed after their tick; two full `cmd.test` runs at once with `test.shared_state` true.

## Verification
- [ ] Each task: the red output (name of the failing assertion) and the green output of `cmd.test_one` are pasted.
- [ ] `cmd.test` on `team/<ID>` after the last merge: exit 0 (or red exactly the `baseline:` list), output pasted.
- [ ] `git log --oneline <base_branch>..team/<ID>` is pasted; each commit has the form `type(scope): description (<ID>)`.
- [ ] Size S: `acceptance.md` maps every criterion to a green test; no qa or writer was called.
- [ ] `git diff --name-only` of each task is a subset of its touchpoints.
- [ ] Each task has a `review-NN.md` with verdict, diff command and round count; rework rounds have ADDRESSED/NOT ADDRESSED.
- [ ] `tasks.md` progress lists each round; every task that was ready, in rework or waiting for review at that time (up to the shares) is in it.
- [ ] `ls .team/active-build-<ID>` reports no such file; `diff.patch` exists and is not empty.
- [ ] `git branch --list 'team/<ID>-task-*' --merged team/<ID>` prints nothing (merged task branches deleted); the `baseline:` line is in `tasks.md`.

## See also
- `${CLAUDE_SKILL_DIR}/references/handoffs.md` — handoff templates for the dev, the reviewer and rework rounds; the status table.
- Agents `tech-lead`, `dev`, `reviewer`; `<kit>/templates/artifacts/review.md`, `tasks.md`.
- `/team:plan` (before), `/team:verify` (after), `/team:commit` (used by the dev).
- `handbook/STD.md`: Review checklist (10), STD-TEST-1/4/5, STD-DESIGN-1, STD-GIT-3/4.
