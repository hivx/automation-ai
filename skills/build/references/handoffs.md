# Handoff templates in the build loop

## Dev status (first line of the return message)
| Status | Meaning | What the tech-lead does |
|---|---|---|
| DONE | Done, with red then green, lint clean | Check the evidence → merge with the round's other tasks; the round's checkpoint tests and reviews them together |
| DONE_WITH_CONCERNS | Done, but with a concern | Concern about correctness/scope → resolve it before review |
| NEEDS_CONTEXT | Missing information to do it right | Add it, call again (never resend the old message) |
| BLOCKED | Several attempts and still not passing | Change one thing; after max_attempts → stop |
| DESIGN_CONFLICT | Would have to modify outside the touchpoints / change a contract | Local (no criterion, outside contract, schema, ADR or outside file) → decide, journal line, call again; else one report per round to the team-leader |

## Shares
- Dev share: the `devs=` line of the team-leader's handoff when several features build at once (`team.py wave` splits the team-wide headcount), else `limits.headcount.dev`, else `limits.max_parallel_dev`.
- Reviewer share: `reviewers=`, else `limits.headcount.reviewer`, else the dev share.

## Calling the dev (first time)
```
Task FEAT-012 T3 — Reject expired OTP codes
Criterion: AC-2 (a code older than 5 minutes returns 401)
Touchpoints: src/auth/otp.py, tests/auth/test_otp.py — modify ONLY inside the touchpoints
Design: design.md §7 "OTP expiry" only (Grep the heading, Read that section; not the whole file)
Baseline: 1 red before this feature — test_legacy_import (not yours)
Shared constraints: plan.md §"Shared constraints" only
Test: cmd.test_one with {file}=tests/auth/test_otp.py
Branch: team/FEAT-012-task-3 (created from team/FEAT-012)
Recurring findings (check your diff before DONE): STD-TEST-8 — seed non-default values so a hard-coded constant fails (review-02, review-05)
Report: the return message only, ≤ 10 lines, status first, RED and GREEN lines verbatim; details in the commit body, never a file (ADJ-41)
```

## Calling the reviewer — the round's checkpoint (one call)
The only review call in the loop (ADJ-42): after the round's merges and its single green `cmd.test`, sent in the next dispatch round beside the devs.
```
Checkpoint review FEAT-012 T1, T2 [risk], T4, F1 — grade against the Review checklist (10)
Range: 4c1d2e0..team/FEAT-012 (4c1d2e0 = last `reviewed:` line; run git log / git diff --stat / git diff yourself)
Per task: T1 AC-1 (RED "…", GREEN "…"); T2 AC-3, AC-4 (RED "…", GREEN "…"); T4 AC-6 (RED "…", GREEN "…")
Open findings to mark ADDRESSED / NOT ADDRESSED: review-02 F-1 report.py:41, F-2 test_report.py:88 (fixed by F1)
cmd.test after the round's merges: exit 0, "Ran 57 tests … OK"
Design: design.md §4 "Export", §8 "Test plan" only
Return: verdict + findings (each naming its task) + "cannot verify from the diff"
```
Due when ≥ 3 merged tasks are unreviewed, a merged `[risk]` task is unreviewed (its dependents wait for it), or nothing is left to dispatch. When it returns, journal line `reviewed: <sha of team/FEAT-012> (T1, T2, T4, F1) <verdict>`; the next range starts at that sha.

## Rework round
```
Fix FEAT-012 F1 (review-02), round 2/3
Findings (verbatim): docs/team/features/FEAT-012/review-02.md (every blocker/major, all tasks)
Branch: team/FEAT-012-fix-1, created from team/FEAT-012, in your own worktree (never point git at another worktree)
Fix report: finding → change → covering test → command + output
```
One dev per checkpoint covers every blocker/major of that review; the fix merges like a task in the next round.
- Fix changes only tests → the tech-lead checks the new test is red on the old code and green now; that closes those findings.
- Fix changes production code → the next checkpoint's range contains it; that call marks the old findings `ADDRESSED`/`NOT ADDRESSED`. No separate re-review call.

## Tests in the loop (ADJ-40)
Measured on one shared Frappe site (`erp_ai`, kit 0.6.2–0.6.4): a module test ran in about 11 s when the site was free, yet devs spent 70–90% of their time running or waiting for tests, queued behind 112 full suites of 3–20 minutes, one after every merge. So:
- **Dev:** `cmd.test_one` on the task's `test:` file: RED once (for the right reason), GREEN once after the last change, then the other test files of the touched module once. Rerun only when code or test changed since the last run; copy the summary line and the failing assertion the first time.
- **Merges:** the round's tasks and fixes merge one after another with no test in between (ADJ-42); the dev already ran their tests.
- **Once per round,** after its last merge: the full `cmd.test` (holding `@shared-state` when `test.shared_state` is true). Green (nothing red outside `baseline:`) → journal line `tested: <sha of team/<ID>> <summary line>`, then tick every task merged in the round, except `[risk]` tasks, which wait for their checkpoint review. A green `tested:` line stays valid for that sha: verify and pr reuse it instead of running the suite again (ADJ-43).
- **Red:** for each new red test, check out the round's merges oldest first in the feature worktree and run `cmd.test_one` on its file; the first red merge broke it. That task stays unticked; one dev on `team/<ID>-fix-K` (from `team/<ID>`) gets the red lines and merges first in the next round; tick the other tasks.
- **Evidence:** a missing GREEN comes from the round's `cmd.test`; a missing RED goes back in a rework call. Never call a dev only to rerun tests.
- **Waiting:** one foreground call per run (Bash `timeout` up to 600000 ms). A longer run goes to the background and is waited for in blocking calls of ≤ 10 minutes, never in a loop of short checks: each check is a turn that rereads the whole context.

## State after a compaction (no progress lines in tasks.md)
- Open tasks: `grep -n "^- \[ \]" docs/team/features/<ID>/tasks.md`.
- Rounds and verdicts: the last 20 lines of `docs/team/journal/<ID>.md`.
- Task and fix branches still open: `git branch --list "team/<ID>-task-*" "team/<ID>-fix-*"`; REVIEWED: the sha of the last `reviewed:` journal line; open findings: that line's verdict and its `review-NN.md`.
