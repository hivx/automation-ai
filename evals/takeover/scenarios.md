# Eval: takeover

Sample project: an onboarded project with FEAT-001 (CSV export) — see `evals/RESULTS.md`.

## Scenario 1 — Small project whose docs drift from the code
- Situation: small project whose docs drift from the code.
- Setup: `rm -rf docs .team .claude`
- Input: `/team:takeover`
- Baseline input: `Find out what this project does, how far along it is and what comes next; write a report and change nothing.`
- Good: 5 reports; T0 via detect-stack; finds the missing to_csv and the skipped test; T3 does not run; has the Scanned/Not scanned/Confidence table.
- Bad: Edits code; no tier table; does not notice the skipped test.
- Checks:
  - exists: `docs/team/assessment.md`
  - exists: `docs/team/ai-readiness.md`
  - exists: `docs/team/profile-proposal.md`
  - exists: `docs/team/debt.md`
  - exists: `docs/team/open-questions.md`
  - grep: `to_csv` in `docs/team/assessment.md`
  - grep: `skip` in `docs/team/assessment.md`
  - grep: `(Scanned|qu.{1,3}t ?[/|])` in `docs/team/assessment.md`
  - unchanged: `inventory`

## Scenario 2 — Outdated CLAUDE.md
- Situation: outdated CLAUDE.md.
- Setup: `rm -rf docs .team .claude`
- Input: `/team:takeover`
- Baseline input: `Assess how ready this repo is for AI.`
- Good: ai-readiness recommends rewriting CLAUDE.md (it describes a Django app that does not exist).
- Bad: Keeps CLAUDE.md.
- Checks:
  - grep: `(rewrite|Vi.{1,3}t l.{1,3}i)` in `docs/team/ai-readiness.md`
  - unchanged: `CLAUDE.md`

## Scenario 3 — Valid profile proposal
- Situation: valid profile proposal.
- Setup: `rm -rf docs .team .claude`
- Input: `/team:takeover`
- Baseline input: `Propose test/lint commands for this repo.`
- Good: `cmd.test_one` contains `{file}`; uses only slot names from the schema.
- Bad: A `{module}` placeholder, or a `cmd.test_all` slot.
- Checks:
  - grep: `cmd\.test_one.*\{file\}` in `docs/team/profile-proposal.md`
  - absent: `cmd\.test_all` in `docs/team/profile-proposal.md`
