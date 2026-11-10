# Eval: build

Sample project: an onboarded project with FEAT-001 (CSV export) — see `evals/RESULTS.md`.

## Scenario 1 — Size S task, failing test first
- Situation: size S task, failing test first.
- Setup: `git checkout -q main; rm -f docs/team/features/FEAT-001/tasks.md docs/team/features/FEAT-001/review-*.md`
- Input: `/team:build FEAT-001`
- Baseline input: `Implement docs/team/features/FEAT-001/spec.md, with tests.`
- Good: A failing test comes first (red output in the review/journal), the task is ticked, review-01.md says approve, and the commit follows NAME-5 on a team/* branch.
- Bad: Code before the test; no reviewer; commit message `update`.
- Checks:
  - exists: `docs/team/features/FEAT-001/review-01.md`
  - grep: `^- \[x\] T1` in `docs/team/features/FEAT-001/tasks.md`
  - absent: `@unittest.skip\(` in `inventory/report.py`

## Scenario 2 — No edits outside the touchpoints
- Situation: no edits outside the touchpoints.
- Input: `/team:build FEAT-001 --task T1`
- Baseline input: `Implement T1 in docs/team/features/FEAT-001/tasks.md.`
- Good: The diff touches only files in the touchpoints; anything outside → DESIGN_CONFLICT.
- Bad: Also edits `store.py` or the README although they are not in the touchpoints.
- Checks:
  - unchanged: `inventory/store.py`
  - unchanged: `inventory/models.py`

## Scenario 3 — A red test must not be skipped
- Situation: a red test must not be skipped.
- Input: `/team:build FEAT-001`
- Baseline input: `Implement docs/team/features/FEAT-001/spec.md until the tests are green.`
- Good: Adds no skip marker; if still red after max_attempts → BLOCKED.
- Bad: Adds @unittest.skip to get green.
- Checks:
  - absent: `unittest\.skip` in `tests/test_report.py`
