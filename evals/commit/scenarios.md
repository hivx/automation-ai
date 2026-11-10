# Eval: commit

Sample project: an onboarded project with FEAT-001 (CSV export) — see `evals/RESULTS.md`.

## Scenario 1 — Commit in the right format
- Situation: commit in the right format.
- Setup: `git switch -q -c team/FEAT-009-x; echo 'def f():\n    return 1' >> inventory/report.py`
- Input: `/team:commit FEAT-009`
- Baseline input: `Commit the current changes.`
- Good: Message `type(scope): description (FEAT-009)`; no --no-verify.
- Bad: Message `update`.
- Checks:
  - grep: `^(feat|fix|refactor|docs|test|chore|ci|build|perf)(\(.+\))?: .+ \(FEAT-009\)$` in `OUTPUT`

## Scenario 2 — Remove a debug log
- Situation: remove a debug log.
- Setup: `git switch -q -c team/FEAT-009-y; printf 'print("DEBUG")\n' >> inventory/report.py`
- Input: `/team:commit FEAT-009`
- Baseline input: `Commit the current changes.`
- Good: Deletes the debug print line before committing (STD-STYLE-5), or refuses to commit.
- Bad: Commits the debug line as is.
- Checks:
  - absent: `print\("DEBUG"\)` in `inventory/report.py`

## Scenario 3 — File outside the touchpoints
- Situation: file outside the touchpoints.
- Setup: `git switch -q -c team/FEAT-009-z; echo '# x' >> inventory/store.py; echo '# y' >> README.md`
- Input: `/team:commit FEAT-009 --task T1 (touchpoints: inventory/store.py)`
- Baseline input: `Commit the changes for a task that touches only inventory/store.py.`
- Good: Commits only store.py; leaves README out and reports DESIGN_CONFLICT.
- Bad: Commits README too.
- Checks:
  - grep: `(DESIGN_CONFLICT|README)` in `OUTPUT`
