# Eval: make-skill

Sample project: an onboarded project with FEAT-001 (CSV export) — see `evals/RESULTS.md`.

## Scenario 1 — A real need exists
- Situation: a real need exists.
- Input: `/team:make-skill csv-format "The project's CSV format, reused by every export"`
- Baseline input: `Create a skill for the project's CSV format.`
- Good: `.claude/skills/csv-format/SKILL.md` has the 8 sections of SPEC §9 and the temp line with evidence; `references/tests.md` has a refusal/edge case and near-miss phrases that should not trigger; the registry has a row.
- Bad: The skill has no test cases and is not registered; the test cases only check "the file exists".
- Checks:
  - exists: `.claude/skills/csv-format/SKILL.md`
  - grep: `team: temp` in `.claude/skills/csv-format/SKILL.md`
  - grep: `evidence:` in `.claude/skills/csv-format/SKILL.md`
  - grep: `^## (Test cases|Done criteria|Ca th|Ti.{1,3}u ch.{1,3} xong)` in `.claude/skills/csv-format/SKILL.md`
  - grep: `(should not|near.miss|similar|refus|reject|kh.{1,3}ng n.{1,3}n|g.{1,3}n gi.{1,3}ng|t.{1,3} ch.{1,3}i)` in `.claude/skills/csv-format/references/tests.md`
  - grep: `csv-format` in `docs/team/skills-registry.md`

## Scenario 2 — Duplicates an existing skill
- Situation: duplicates an existing skill.
- Input: `/team:make-skill verify-again "Run feature acceptance with real commands"`
- Baseline input: `Create a skill for feature acceptance.`
- Good: Refuses: it duplicates `/team:verify`.
- Bad: Creates the duplicate skill.
- Checks:
  - grep: `(duplicate|overlap|verify|refus|reject|decline|tr.{1,3}ng|t.{1,3} ch.{1,3}i)` in `OUTPUT`
  - absent: `verify-again` in `docs/team/skills-registry.md`

## Scenario 3 — No need stated
- Situation: no need stated.
- Input: `/team:make-skill misc`
- Baseline input: `Create a few spare skills for later.`
- Good: Refuses because there is no one-sentence need.
- Bad: Creates a skill in advance.
- Checks:
  - grep: `(need|refus|reject|decline|evidence|nhu c|t.{1,3} ch.{1,3}i)` in `OUTPUT`
