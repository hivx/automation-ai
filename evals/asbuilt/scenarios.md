# Eval: asbuilt

Sample project: an onboarded project with FEAT-001 (CSV export) already at `Verdict: accepted`, waiting for G4 — see `evals/RESULTS.md`. Setup adds the G4 approval line. The sample project keeps its CHANGELOG at `docs/CHANGELOG.md` (created by T1). Run of 2026-11-10: the CHANGELOG check first pointed by mistake at `CHANGELOG.md` in the root, and the `## What changed` heading check (then in its Vietnamese form) was added AFTER the run; both versions were re-scored on the saved working directories.

## Scenario 1 — Feature accepted and G4 approved
- Situation: FEAT-001 has passed acceptance; the human approves G4.
- Setup: `sed -i '0,/^Approved-by:$/s//Approved-by: Lan 2026-11-10/' docs/team/features/FEAT-001/acceptance.md`
- Input: `/team:asbuilt FEAT-001`
- Baseline input: `Write the As-Built, the CHANGELOG entry and the PR body for FEAT-001.`
- Good: `asbuilt.md` compares each section against the diff, the CHANGELOG has a `(FEAT-001)` line under `[Unreleased]`, `pr-body.md` has the four headings that `/team:pr` greps, and the post-G4 debt items from qa are closed.
- Bad: The As-Built copies the design; the CHANGELOG gets turned into a version number; pr-body lacks "How verified"; code is edited.
- Checks:
  - exists: `docs/team/features/FEAT-001/asbuilt.md`
  - grep: `FEAT-001` in `docs/CHANGELOG.md`
  - grep: `Unreleased` in `docs/CHANGELOG.md`
  - grep: `^## What changed` in `docs/team/features/FEAT-001/pr-body.md`
  - grep: `^## How verified` in `docs/team/features/FEAT-001/pr-body.md`
  - grep: `^## Why` in `docs/team/features/FEAT-001/pr-body.md`
  - absent: `^Released:` in `docs/team/features/FEAT-001/asbuilt.md`
  - unchanged: `inventory/`
