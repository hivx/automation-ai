# Handoff templates in the build loop

## Dev status (first line of the return message)
| Status | Meaning | What the tech-lead does |
|---|---|---|
| DONE | Done, with red then green, lint clean | Check the evidence → review package (in the reviewer handoff) |
| DONE_WITH_CONCERNS | Done, but with a concern | Concern about correctness/scope → resolve it before review |
| NEEDS_CONTEXT | Missing information to do it right | Add it, call again (never resend the old message) |
| BLOCKED | Several attempts and still not passing | Change one thing; after max_attempts → stop |
| DESIGN_CONFLICT | Would have to modify outside the touchpoints / change a contract | Stop, report to the team-leader |

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
Detailed report: docs/team/features/FEAT-012/dev-T3.md; return message ≤ 10 lines, first line is the status
```

## Calling the reviewer
```
Review FEAT-012 T3 — grade against the Review checklist (10)
Range: $(git merge-base team/FEAT-012 team/FEAT-012-task-3)..team/FEAT-012-task-3 (run git log / git diff --stat / git diff on it yourself)
Dev evidence: RED "FAILED test_expired_code - AssertionError: 200 != 401"; GREEN "3 passed"; module tests "11 passed"
Design: docs/team/features/FEAT-012/design.md §7 "OTP expiry", §8 "Test plan" only
Task criterion: AC-2
Return: verdict + findings `severity | STD | file:line | description | fix` + a "cannot verify from the diff" section
```

## Rework round
```
Fix FEAT-012 T3 round 2/3
Findings (verbatim): docs/team/features/FEAT-012/review-03.md#round-1
In your worktree: git switch team/FEAT-012-task-3 (never point git at another worktree)
Fix report: finding → change → covering test → command + output
```
Scoped re-review: the reviewer receives `FIX_BASE..HEAD` and the list of old findings; it returns `ADDRESSED`/`NOT ADDRESSED` for each item.

## State after a compaction (no progress lines in tasks.md)
- Open tasks: `grep -n "^- \[ \]" docs/team/features/<ID>/tasks.md`.
- Rounds and verdicts: the last 20 lines of `docs/team/journal/<ID>.md`.
- Task branches still open: `git branch --list "team/<ID>-task-*"`; BASE of one: `git merge-base team/<ID> team/<ID>-task-N`.
