# Eval: analyze

Sample project: an onboarded project with FEAT-001 (CSV export) — see `evals/RESULTS.md`.

## Scenario 1 — Size S spec in decide mode
- Situation: size S spec in decide mode.
- Setup: `rm -f docs/team/features/FEAT-001/spec.md docs/team/features/FEAT-001/questions.md`
- Input: `/team:analyze FEAT-001 --decide`
- Baseline input: `Write a spec with a Definition of Done for docs/team/features/FEAT-001/intake.md, deciding open points yourself.`
- Good: `spec.md` has 7 sections, `## Assumptions decided by the team`, `## Definition of Done`, and measurable criteria.
- Bad: The spec has no DoD, criteria like "works well", or it picks a library.
- Checks:
  - exists: `docs/team/features/FEAT-001/spec.md`
  - grep: `^## Definition of Done` in `docs/team/features/FEAT-001/spec.md`
  - grep: `^## Assumptions decided by the team` in `docs/team/features/FEAT-001/spec.md`
  - unchanged: `inventory`

## Scenario 2 — Ask mode with a major unclear point
- Situation: ask mode with a major unclear point.
- Setup: `rm -f docs/team/features/FEAT-001/spec.md; sed -E -i 's/(Mode|Ch[^:]*): decide.*/\1: ask/' docs/team/features/FEAT-001/intake.md`
- Input: `/team:analyze FEAT-001`
- Baseline input: `Write a spec for docs/team/features/FEAT-001/intake.md; ask if anything major is unclear.`
- Good: Either a spec with a full DoD, or a `questions.md` with ≤ 5 questions, each with options + a recommendation, and status NEEDS_ANSWER; no question the code already answers.
- Bad: Asks > 5 questions, or asks something the README/code already states clearly (the CSV header).
- Checks:
  - absent: `(header|ti.{1,3}u .{1,3} c.{1,3}t).*\?` in `docs/team/features/FEAT-001/questions.md`

## Scenario 3 — Amend an approved spec
- Situation: amend an approved spec.
- Setup: `printf '\n' >> docs/team/features/FEAT-001/spec.md`
- Input: `/team:analyze FEAT-001 --amend "Add a currency column"`
- Baseline input: `Edit the spec docs/team/features/FEAT-001/spec.md: add a currency column.`
- Good: Adds `## Amendment 1` and marks [changed]; the old criteria are still there.
- Bad: Edits the old criteria in place, no amendment section.
- Checks:
  - grep: `^## Amendment` in `docs/team/features/FEAT-001/spec.md`
  - grep: `\[changed\]` in `docs/team/features/FEAT-001/spec.md`
