# Eval: using-team

Sample project: an onboarded project with FEAT-001 (CSV export) — see `evals/RESULTS.md`.

## Scenario 1 — Raw request with no command
- Situation: raw request with no command.
- Setup: `sed -i '0,/^Approved-by:$/s//Approved-by: Eval 2026-11-09/' docs/team/features/FEAT-001/acceptance.md`
- Input: `Add a function that returns the total quantity (sum of qty) in the store, with a test.`
- Baseline input: `Add a function that returns the total quantity (sum of qty) in the store, with a test.`
- Good: team-leader recognizes this as new work, goes through `/team:intake` (playbook new-feature), writes the journal; does not edit code itself.
- Bad: Edits `inventory/store.py` directly without intake, no journal.
- Checks:
  - grep: `(FEAT-00[2-9]|/team:intake|intake)` in `OUTPUT`
  - unchanged: `inventory`
  - exists: `docs/team/features/FEAT-00[2-9]/intake.md`
  - exists: `docs/team/features/FEAT-00[2-9]/spec.md`
  - exists: `docs/team/features/FEAT-00[2-9]/review-*.md`

## Scenario 2 — Status question
- Situation: status question.
- Input: `What is the team working on, and who is waiting for whom?`
- Baseline input: `What is the team working on, and who is waiting for whom?`
- Good: Uses `/team:status` (team.py), prints the exact table and waiting lines; does not infer.
- Bad: Reads the artifacts itself and summarizes them, skipping the script.
- Checks:
  - grep: `FEAT-001` in `OUTPUT`
  - grep: `(team\.py|/team:status|Ti.{1,3}p theo|next)` in `OUTPUT`

## Scenario 3 — Bug report
- Situation: bug report.
- Input: `Store.remove raises a confusing KeyError when the SKU does not exist — please fix it.`
- Baseline input: `Store.remove raises a confusing KeyError when the SKU does not exist — please fix it.`
- Good: Goes through intake with `--type bug` (playbook bug-fix), ID BUG-NNN; does not edit code before there is a failing test.
- Bad: Edits `store.py` right away, without a failing test first.
- Checks:
  - grep: `(BUG-0|bug-fix)` in `OUTPUT`
  - unchanged: `inventory`
