---
name: build
description: Use when a plan is approved (or the work is size S, a bug-fix or a hotfix) and a dev must write tests and code, a reviewer must grade them, and the tasks must be merged into the feature branch.
argument-hint: "<ID> [--task T<N>] [--decide]"
context: fork
agent: team:tech-lead
background: false
allowed-tools: Bash(python3 *) Bash(cat *) Bash(git *) Bash(touch .team/active-build-*) Bash(rm .team/active-build-*) Bash(rm -f .team/active-build-*)
---

# The build loop: devs → merge → one checkpoint (test + review) per round → fix

## Overview
This skill runs a feature's build loop until every task in `tasks.md` is ticked and every merged line is reviewed: devs (own worktrees) write a failing test first, then the code; after each round the tech-lead merges every finished task into `team/<ID>` and holds ONE checkpoint: the full `cmd.test` once, then one reviewer call (fresh context, read-only) over everything merged since the last review, sent beside the next round's devs; one dev fixes the blockers/majors. Tests and review are paid per round, never per task (ADJ-42). The skill runs in the `tech-lead` context (fork); the tech-lead calls only `team:dev`, `team:reviewer` and Explore.

One rule never changes with size: **size S still goes through this skill with 1 dev + 1 reviewer** (K-34); only playbook quick skips it (ADJ-36). Nobody says "done" without the output of a real command. `.team/active-build-<ID>` (one per feature) is created at the start and removed on EVERY exit; `stop-check.sh` reads it.

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
3. Resume from disk: if `.team/active-build-<ID>` already exists → read `tasks.md` and `git log --oneline <base_branch>..team/<ID>` BEFORE anything else; ticked tasks are never redone; production code merged after the last `reviewed:` journal line gets its checkpoint first.

## Inputs and preconditions
- `python3 "<kit>/scripts/team.py" status <ID>`: no `WAITING_FOR_APPROVAL` for a gate before build.
- `tasks.md` with lines `- [ ] T<N> — … — files: … — test: … — depends: …`; size S without one → Write a single task from `spec.md` (files = the touchpoints in the spec/intake, test = a test file named per `naming.test_file`).
- `design.md` (or `plan.md` § Design) for the reviewer.
- Branch `team/<ID>` exists (create it from `base_branch` if missing).

## Process
1. **Switch the build on.** `touch .team/active-build-<ID>`; `team.py claim <ID> --stage build --agent tech-lead` (`CONFLICT` → stop, return it). Merges run in the feature worktree (`git worktree add .claude/worktrees/<ID> team/<ID>`, once), never by switching the main tree (`<kit>/handbook/sessions.md`). First run of this feature (no `baseline:` line in `tasks.md`): run `cmd.test` on `team/<ID>` and write one line `baseline: <counts> — red: <test names>` under the task list. "Green" from here on means no red test outside that list; never fix or skip a baseline failure inside a task.
2. **Preflight, before calling anyone.** Tabulate every pair of tasks sharing a file or interface; tasks whose test does not match their touchpoints; tasks that require what the Review checklist treats as a defect. A problem you cannot decide under step 6 → `DESIGN_CONFLICT` to the team-leader, no dev called yet.
3. **Pick what can start.** A task is ready when every `depends:` is ticked, it shares no file or interface (the preflight table) with any task in flight (in dev, review or rework), and `team.py claim <ID> --task T<N> --files <its files>` exits 0 (exit 4 `BUSY` → the task waits for a later round). Take ready tasks up to your free dev share. Migrations and shared state go alone. Devs run `cmd.test_one` only; the full `cmd.test` runs once per round (step 12), holding `@shared-state` when `test.shared_state` is true. One journal line per round (`round N: dev T4, T5; checkpoint T1–T3`). `tasks.md` holds only task lines, ticks and the `baseline:` line. Dev and reviewer shares: `${CLAUDE_SKILL_DIR}/references/handoffs.md` § Shares.
4. **No bookkeeping.** REVIEWED = the sha of the last `reviewed:` journal line, else the fork point from `base_branch`; a review range is `REVIEWED..team/<ID>`, never `HEAD~1`. Hold the loop state in your context: never re-Read `tasks.md`, the journal or kit files during the loop (after a compaction: handoffs.md § State after a compaction).
5. **Dispatch round — ONE message.** Every call that can start now goes into one message, so they run at the same time: one Agent `team:dev` call per ready task (step 3) and per rework (step 10), each in its own worktree, plus the checkpoint's `team:reviewer` call when one is due (step 8). Never hold a ready task, a fix or a due review back. Each call gets a handoff ≤ 10 lines from the templates in `${CLAUDE_SKILL_DIR}/references/handoffs.md` (≤ 2 design headings, never "read design.md"), with the **recurring findings**: blocker/major STD codes flagged by ≥ 2 reviews of this feature, ≤ 3 lines with the fix.
6. **Read each dev's status** (per task; a stop in one task does not cancel the others) — the return message's first line is one of `DONE`, `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, `BLOCKED`, `DESIGN_CONFLICT` (decision point):
   - `DONE`: check a RED for the right reason (missing behavior, not an import/syntax error), then a GREEN; a missing RED → back to the dev (one attempt), a missing GREEN comes from the round's `cmd.test`.
   - `DONE_WITH_CONCERNS`: a concern about correctness or scope → resolve it before review; any other concern → note it for the review.
   - `NEEDS_CONTEXT`: add the context and call again; never resend the old message unchanged.
   - `BLOCKED`: change one thing (add context, split the task, report that the plan is wrong); after `limits.max_attempts` → stop.
   - `DESIGN_CONFLICT`: decide it yourself when it changes no criterion, no contract used outside the feature, no schema, no ADR and no file outside the feature's touchpoints (helper or test names, internal signatures, fixtures, which touchpoint holds a helper): one journal line, then call the dev again with the decision. Otherwise collect every open conflict of the round into ONE report to the team-leader, so one designer call answers them all.
7. **Review package — in the handoff, not a file.** The range `REVIEWED..team/<ID>` (the reviewer runs `git log`/`git diff` itself), each task's criteria and the dev's RED and GREEN lines verbatim (≤ 4 lines per task), the open findings of the last checkpoint. Never copy the diff into `docs/`.
8. **One checkpoint per round: test, then review.** After the round's merges (step 12) run the full `cmd.test` once. Green → a review is due when ≥ 3 merged tasks are unreviewed, a merged `[risk]` task is unreviewed, or nothing is left to dispatch. ONE reviewer call (Agent `team:reviewer`) covers the whole range, `[risk]` tasks included, in the next dispatch round beside the devs: the package, the design headings, "grade against the Review checklist (10)". No dev explanations; never say "don't flag X". When it returns: journal line `reviewed: <sha> (T…) <verdict>`. Never review a task alone; never test between merges.
9. **Read the verdict** — `approve` / `request-changes` / `design-defect`, with a list of "cannot verify from the diff":
   - `design-defect` → stop and report to the team-leader.
   - "Cannot verify" items → the tech-lead resolves them; something really missing → a failed review.
10. **Rework** (`request-changes`): ONE dev in a new worktree (K-14) on `team/<ID>-fix-K`, from `team/<ID>`, gets every blocker/major verbatim + the review path, in the next round; the fix merges like a task. Fix report: finding → change → covering test → command + output. A tests-only fix: the new test red on the old code, green now, closes its findings. A production fix: the next checkpoint covers it and marks the old findings; no separate re-review; new notes → `deferred`.
11. **Break the loop.** Count the rounds; > `limits.max_rework`, or the same defect in two rounds → stop; write a ruling for each open finding (reviewer wrong / real but deferred / blocking) and escalate to the team-leader.
12. **Merge, test once, tick.** Merge every task or fix whose `DONE` evidence checks out, `[risk]` included, serially in task order in the feature worktree, no test in between; then the checkpoint's single `cmd.test` (step 8; journal `tested: <sha> <summary>`). Green → tick the round's merged tasks (`- [x] T<N>`), one journal line; a `[risk]` task is ticked only when a checkpoint leaves no blocker/major on it, so tasks that depend on it wait for that review. Red → find the merge that broke it (`${CLAUDE_SKILL_DIR}/references/handoffs.md` § Tests in the loop). After each review call, Write `review-NN.md` from `<kit>/templates/artifacts/review.md` (tasks covered, verdict, findings per round, diff command, `deferred`; ≤ 6 KB) — ONE file per review call, rounds appended. Clean up: `team.py release <ID> --task T<N>`; `git worktree remove <dev worktree>` (never `--force`; dirty → note it, keep it), then `git branch -d team/<ID>-task-N` (merged only, never `-D`). Prose in `output_language` (handbook: Artifact language).
13. **Loop.** After each round: merge and tick (step 12), then back to step 3 and send the next round at once. Done when every task is ticked or stopped, no blocker/major is open, and no production code was merged after the last `reviewed:` sha.
14. **All tasks done.** Size S (ADJ-36): acceptance here, no `/team:verify`, no As-Built — Write `acceptance.md` from `<kit>/templates/artifacts/acceptance.md` (criterion → covering test → green; `cmd.test` output; the Try it row: the main flow run once on the running app as the requester would, `/team:verify` § Try it; `Verdict: accepted` only when all pass, else `rework`); a CHANGELOG line if the project keeps one. No `diff.patch`: the writer runs `git diff` itself (ADJ-41). Commit `docs/team/**` once, now or at a stop, never per tick. Record the roles used against `limits.max_agents_per_feature`.
15. **Every exit** (done, stopped, error): `rm -f .team/active-build-<ID>`; `team.py release <ID> --files`.

## Outputs
- Commits on `team/<ID>`; `docs/team/features/<ID>/tasks.md` ticked; a `review-NN.md` per review call; `acceptance.md` (size S). No other file in the feature folder (`team.py docs <ID>`).
- One journal line per round, prose in `output_language`.
- Return message to the team-leader, ≤ 10 lines:
  ```
  tech-lead -> team-leader | FEAT-012 | DONE
  Tasks ticked: T1..T4; review-01 T1–T3 (T2 [risk]) request-changes, review-02 T4 + F1 approve. Roles: dev, reviewer (cap M: 6)
  Rounds: 3, one cmd.test each; rework: F1 (2 findings), one round
  cmd.test on team/FEAT-012: exit 0, "Ran 42 tests … OK"
  Deferred (minor): review-03 STD-NAME-2
  Files: docs/team/features/FEAT-012/{tasks,review-01..02}
  Next: /team:verify FEAT-012
  ```

## Common rationalizations
| Thought | Correct action |
|---|---|
| "Size S, a one-line fix, no reviewer needed" | Still call `team:reviewer` (K-34); trivial work is playbook quick, chosen at intake. |
| "The dev says the tests are green" | You need the pasted red-then-green output; missing → send it back. |
| "Red because of an import error is still red" | Red must come from missing behavior; send the dev back to fix the test. |
| "A flaky red test, unrelated, merge anyway" | Stop: reproduce it, record it in `debt.md` (STD-TEST-7); do not merge. |
| "Three lines to fix, I will do it myself" | Send it to the dev; the tech-lead writes only `docs/team/**`. |
| "Review the `[risk]` task alone, before its merge" | It joins the round's checkpoint; its dependents wait for that review. |
| "A local naming question, ask the designer" | Decide it, one journal line; only criteria, contracts, schema, ADRs or outside files go up, all in one report. |
| "One more rework round and it is done" | Over `max_rework`, or the same defect twice: stop and escalate. |
| "The reviewer is nitpicking, drop that finding" | Rule on it only at the cap, in writing. |
| "Run the task's tests after each merge, to be safe" | The dev ran them; one `cmd.test` after the round's merges covers all, a red one is traced to its merge. |
| "The suite was red before we started, so red is fine" | Only the tests on the `baseline:` line may stay red; any other red test blocks the tick. |
| "Dev already got this finding last task, it will remember" | Each dev starts fresh: put the recurring findings in every handoff. |

## Red flags
- A test is green on its first run, or there is no red output.
- The dev's return message has no command, or "should work".
- The diff touches files outside the touchpoints, or `.team/profile.json`/`config.json`.
- Two running tasks touch the same file, in this session or another (`team.py sessions`); `git switch` in the main tree.
- A dispatch message with one Agent call while other tasks were ready, in rework or waiting for review.
- A task reviewed alone, or a review call outside a checkpoint; one designer call per open point.
- A `review-NN.md` says approve without a diff command or a tier-1 verdict.
- A task is ticked without a merge commit on `team/<ID>`; `.team/active-build-<ID>` remains after stopping.
- Size S has only a dev call and no reviewer.
- `review-pkg-*` or `*.diff` files under `docs/team/`; a task started while a `[risk]` task it depends on is unreviewed.
- Merged `team/<ID>-task-*` branches still listed after their tick; two full `cmd.test` runs at once with `test.shared_state` true, or two in one round; a test run between merges; a dev called only to rerun tests.

## Verification
- [ ] Each task: the red output (name of the failing assertion) and the green output of `cmd.test_one` are pasted.
- [ ] `cmd.test` on `team/<ID>` after the last merge: exit 0 (or red exactly the `baseline:` list), output pasted.
- [ ] `git log --oneline <base_branch>..team/<ID>` is pasted; each commit has the form `type(scope): description (<ID>)`.
- [ ] Size S: `acceptance.md` maps every criterion to a green test; no qa or writer was called.
- [ ] `git diff --name-only` of each task is a subset of its touchpoints.
- [ ] Every ticked task is named in a `review-NN.md` (verdict, diff command, ADDRESSED/NOT ADDRESSED); no blocker/major open; `git diff --stat <last reviewed: sha>..team/<ID>` lists no production file.
- [ ] One journal line per round, naming every task started, in rework or in review; `tasks.md` has no progress lines.
- [ ] `ls .team/active-build-<ID>` reports no such file; `team.py docs <ID>` reports 0 problems.
- [ ] `git branch --list 'team/<ID>-task-*' --merged team/<ID>` prints nothing (merged task branches deleted); the `baseline:` line is in `tasks.md`.

## See also
- `${CLAUDE_SKILL_DIR}/references/handoffs.md` — handoff templates for the dev, the reviewer and rework rounds; the status table; tests in the loop.
- Agents `tech-lead`, `dev`, `reviewer`; `<kit>/templates/artifacts/review.md`, `tasks.md`.
- `/team:plan` (before), `/team:verify` (after), `/team:commit` (used by the dev).
- `handbook/STD.md`: Review checklist (10), STD-TEST-1/4/5, STD-DESIGN-1, STD-GIT-3/4.
