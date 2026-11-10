# First day on an existing project

Goal: before the team changes a single line of code, you and the team both know what the project does, how far along it is, and what the next piece of work is.

## Before you start
- Install the plugin (`docs/06-install.md`).
- Work on a clean branch. takeover does not modify the project's files; it only writes into `docs/team/`.

## Step 1 — `/team:takeover`
- The team scans in tiers: T0 metadata → T1 documentation → T2 sampled cross-check → T3 only when needed (or `--full`).
- Results in `docs/team/`:
  - `assessment.md` — the three answers + a stack-health appendix (do build/test run, lint, coverage, outdated/CVE dependencies, leaked secrets, flaky tests).
  - `ai-readiness.md` — existing CLAUDE.md, `.claude/`, plugins, MCP, AGENTS.md: keep / cut / rewrite; verdict: ready / adjust profile / clean first.
  - `profile-proposal.md` — the proposed profile, with evidence for every slot.
  - `debt.md` — technical debt: blocking / should do / later.
  - `open-questions.md` — at most 10 questions.

## Step 2 — Read and approve (gate G0)
1. Read the "scanned / not scanned / confidence" section first.
2. Check `profile-proposal.md`, especially `cmd.test_one`, `protected_paths`, `allowed_new_file_roots`.
3. Answer `open-questions.md` directly in the file.
4. Add `Approved-by: <name> <YYYY-MM-DD>` at the top of `ai-readiness.md`.

## Step 3 — `/team:onboard`
- Writes `.team/profile.json`, `.team/config.json`, `.claude/settings.json` (permissions, protected branches, team-leader as the main-session agent), `.claude/rules/`, the `team` block in `CLAUDE.md`.
- Prints the install commands for the recommended plugins; you decide whether to install them.
- Commit these files.

## Step 4 — The first piece of work
- Pick something small (size S) to gauge the team: a defect from `debt.md` or `open-questions.md`.
- `/team:intake --type bug "<description>"`, then follow it with `/team:status`.
- At the end of the day: read `docs/team/journal/`. Where the team was slow or wrong → `/team:feedback`.
