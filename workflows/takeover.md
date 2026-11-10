# Playbook: takeover

## When it applies
- The repo has code the team has never worked on (no `.team/profile.json` yet).
- The human asks "what does this project do, how far along is it, what comes next".
- The project changes owner or is handed over from another team.

## Default size
Not applicable (read-only, no code changes).

## Chain
1. `/team:takeover` → team-leader (+Explore, researcher) → scan T0 metadata → T1 docs → T2 sampled cross-check → [T3 deep read: only when T2 finds a contradiction, an undocumented module, or `--full`].
2. Report answering the 3 questions → `docs/team/assessment.md`, `ai-readiness.md`, `profile-proposal.md`, `debt.md`, `open-questions.md`.
3. The human approves `ai-readiness.md` (G0).
4. `/team:onboard` → team-leader → `.team/`, `.claude/`, the `CLAUDE.md` block, `docs/team/onboarding.md`.

## Gates
- G0: the human adds `Approved-by:` to `docs/team/ai-readiness.md`.

## Stop points
- After step 2: wait for G0.
- A scan tier exceeds its budget without an answer: stop, record "not scanned" and the confidence level.

## Done criteria
- All 5 reports have scanned / not scanned / confidence sections.
- G0 is approved; onboard prints the created / skipped / manual-work table.
- No project file was modified before onboard.

## Common mistakes
- Reading the whole repo deeply from the start (skipping T0–T2).
- Trusting the README without checking it against the code.
- Running onboard before G0 is approved.

## Related playbooks
`new-project` (empty repo), `new-feature` (the first work after onboard), `refactor` (debt in `debt.md`).
