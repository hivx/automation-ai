# Sample sessions (condensed from a real run)

The three sessions below come from the end-to-end run of 2026-11-09 (Claude Code 2.1.319) on the sample project `sample-existing`: a 3-module Python library `inventory`, 24 commits, a README that promises `to_csv` although the code does not have it, one skipped test, an old 120-line CLAUDE.md. Only commands, decisions and verdicts are kept; tool-call details are dropped. Costs are the figures Claude Code printed. The run predates P9, so its artifacts were written in Vietnamese; the excerpts are shown in English.

## 1. First day on an existing project (takeover → G0 → onboard)

```
human> /team:takeover
team-leader: T0 detect-stack.sh --deep (24 commits, 3 authors, 1 skip marker, 1 TODO)
             T1 README, CLAUDE.md, Makefile, .env.example (4 documents)
             T2 direct reading, < 30 files (11 tracked files)
             T3 not run: the contradictions were explained at T2
  → docs/team/assessment.md      Does: a 3-module inventory library.
                                 How far: README promises to_csv — the code does not have it (grep: 0);
                                          test_remove_unknown_sku is skipped ("flaky on CI", the repo has no CI).
                                 Next: rewrite CLAUDE.md; implement to_csv or drop it from the README; ...
  → ai-readiness.md  Verdict: clean-first — CLAUDE.md describes a Django app that does not exist → Rewrite
  → profile-proposal.md  cmd.test = make test; cmd.test_one = python3 -m unittest {file}; cmd.lint = make lint
  (35 turns, $0.27; no source file was modified)
human> (adds "Approved-by: Miyano 2026-11-09" to ai-readiness.md)
human> /team:onboard
team-leader: profile + config (check-profile: valid); CLAUDE.md: 16-line block inserted, the old 120 lines kept;
             .claude/settings.json (agent team:team-leader), settings.local.json (Read kit), 4 rules;
             make lint → 0; make test → "Ran 4 tests … OK (skipped=1)"
             Manual work: rewrite CLAUDE.md; fill in approvers; install security-guidance (command printed only)
  (57 turns, $0.38)
```

## 2. A size S feature (intake → run → verify, stops at G4)

```
human> /team:intake "Implement the feature the README promises" --size S --decide
team-leader: FEAT-001 · playbook new-feature · size S · decide
             reason: README.md line 8 promises to_csv, grep "csv" in inventory/ = 0      ($0.19)
human> /team:run FEAT-001 --until-blocked
  analyst  → spec.md: 5 criteria AC-1..AC-5, each with a check command; DoD includes CHANGELOG   (SPECIFIED)
  tech-lead → tasks.md: T1 to_csv + test + README + CHANGELOG
    dev (worktree)   failing test first → to_csv → make test green → commit "feat(report): add to_csv (FEAT-001)"
    reviewer         request-changes: a tiny negative price prints "-0.00" (major)
    dev (rework)     "fix(report): normalise negative zero in to_csv (FEAT-001)"
    reviewer         approve → review-01.md; merged into team/FEAT-001; make test: 11 tests OK (skipped=1)
  qa       → acceptance.md: "Ran 8 tests … OK"; make test "Ran 11 tests"; make lint 0
             Verdict: accepted
team-leader: stop — WAITING_FOR_APPROVAL G4_uat (docs/team/features/FEAT-001/acceptance.md)
```

Journal `docs/team/journal/FEAT-001.md`:
```
- 2026-11-09 intake → team-leader | new-feature, S, decide | intake.md | — | good | README promises to_csv but the code lacks it; size S forced by the human
- 2026-11-09 build → tech-lead | skill team:build (playbook new-feature, S) | tasks.md 1 task | — | good | no design.md because size S
- 2026-11-09 verify → qa | done | acceptance.md | — | good | accepted; stopped at G4
```

Kit defects exposed in this session (fixed in v0.1.0): status stuck at `planned` because of the bold `- [x] **T1**` (K-11); team-leader stopped at G1 although size S skips G1 (K-02); writing the journal with `printf` was refused (K-12). See `docs/kit-issues.md`.

## 3. Looking back (retro)

```
human> /team:retro --decide
coach: measure.py --since 2026-11-09 → attention rank 1: team:tech-lead (420 s, 46 turns, size S)
       Bottleneck: FEAT-001 size S called 5 roles / 8 turns > cap max_agents_per_feature.S = 3;
                   the journal wrongly says "agents 3 within the limit"
       Diagnosis: config (cap 3 < the minimum chain of 5 roles) + prompt (team-leader has no way to count)
  → docs/team/retro/2026-11-09.md
  → docs/team/proposals/2026-11-09/team-leader.md: overlay rule "agent budget", 5-scenario eval,
    canary on 3 size-S jobs, rollback; waiting for human approval
  (the kit's agents/ and skills/ unchanged — checked with sha256)
```
