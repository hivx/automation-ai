# Eval results

How to run: `evals/run-eval.sh <skill> <n> --project <sample project>`; configuration in `evals/config.json` (model sonnet for the main session, `--max-turns 40`, `--max-budget-usd 2.0`; subagents use the model in their frontmatter). Sample project: a copy of `sample-existing` after P6 (FEAT-001 verified, waiting for G4). Cost is the `total_cost_usd` that Claude Code prints.

## Round 0 — v0.1.0 (2026-11-09, Claude Code 2.1.319)

| Skill / scenario | Mode | Result | Turns | Cost | Notes |
|---|---|---|---|---|---|
| verify s1 | baseline (without `skills/verify`) | 3/4 — FAIL `^Verdict:` | 7 | $0.89 | Has `acceptance.md` and `Ran N tests` output, but no `Verdict:` line → `team.py` does not recognize the verified stage. |
| verify s1 | with-skill | **4/4** | 0* | $0.69 | `Verdict: accepted`, real command output, no code edits. |
| using-team s1 | baseline (without `skills/using-team`) | 2/3 — FAIL grep OUTPUT | 15 | $0.34 | Creates the FEAT-002 intake.md and hands straight to dev; no review. |
| using-team s1 | with-skill | 2/3 — FAIL grep OUTPUT | 2 | $0.31 | Same as baseline. The two modes cannot be told apart. |

\* `num_turns` of the main session; the work runs in a forked subagent, so it is not counted here.

Conclusions:
- `verify`: the skill makes a measurable difference (the machine-readable `Verdict:` line).
- `using-team` s1: **inconclusive.** The OUTPUT grep check is too narrow (both modes name FEAT-002 but neither writes `/team:intake`); the `unchanged inventory` check is weak because dev commits in a worktree. The team-leader agent still carries the using-team rules in its own body, so the baseline is nearly identical. Rewrite the scenario in the next round (K-33).
- Both modes of using-team let dev do a size S task with no reviewer → K-34.

The first run (same day) was discarded: the project copy sat inside the plugin folder, so every write was refused in with-skill mode (K-20). `run-eval.sh` was fixed and the run repeated; the table above is the repeated run.

The other scenarios (analyze, build, commit, pr, takeover, make-skill; s2–s3 of verify and using-team) have not been run; see their commands with `--dry-run`.

## Round 1 — P7 (2026-11-09, Claude Code 2.1.319)

BEFORE = `pre-p7-round1` (= v0.1.0) run through `EVAL_KIT=<worktree of the tag>`; AFTER = the current tree. Same sample project, same scenarios, same `run-eval.sh`, with-skill mode; only the kit differs.

| Scenario | BEFORE | AFTER | Cost B → A | Real difference |
|---|---|---|---|---|
| using-team s1 (3 original checks) | 3/3 | 3/3 | $0.36 → $1.57 | — |
| using-team s1 (+2 new checks, re-scored on the same working directory) | 3/5 — FAIL `spec.md`, FAIL `review-*.md` | **5/5** | — | BEFORE: team-leader hands straight to dev, skips analyze and the reviewer, then reads the diff itself (against the contract). AFTER: analyze → `/team:build` (tech-lead → dev + reviewer), `review-01.md`, the journal counts "2/3 roles". The higher cost is the review that v0.1.0 skipped (K-34, K-15). |
| verify s1 | 4/4 (80 lines, 8 table rows) | 4/4 (72 lines, 6 table rows) | $0.94 → $0.87 | Equivalent; AFTER is 8% cheaper. |
| analyze s1 | 4/4 (115 lines) | 4/4 (88 lines) | $0.68 → $0.83 | Equivalent; the AFTER spec is shorter, with the same number of criteria. |

Honest notes:
- The two new using-team s1 checks were added AFTER the run and re-scored on the saved working directories of both runs; the original checks could not tell the two versions apart (K-33). From the next round on, the scenario uses 5 checks.
- No eval got worse by its checks; the higher using-team cost is explained (a more correct process), not a regression.
- `num_turns` of the main session is 0–2 because the work runs in a forked subagent; do not use it for comparison.

## Round 2 — P7 round 2 (2026-11-10, Claude Code 2.1.319)

BEFORE = `pre-p7-round2` (= v0.2.1) through `EVAL_KIT=<worktree of the tag>`; AFTER = the current tree (v0.3.0). Same sample project (`eval-project`: FEAT-001 accepted, waiting for G4), same `run-eval.sh`, with-skill mode. Scenarios fixed BEFORE the run: make-skill s1 (discriminating checks), asbuilt s1 (new).

| Scenario | BEFORE | AFTER | Cost B → A | Notes |
|---|---|---|---|---|
| using-team s1 (5 checks) | 5/5 | run 1: 2/5 → fix K-70 → run 2: 3/5 → fix K-73 → run 3: **5/5** | $1.71 → $0.14 / $0.17 / $1.76 | The two relevant files (intake, team-leader) were IDENTICAL in both versions at run 1: the difference is run-to-run variance, which exposed two real kit bugs. Run 1: intake could only be invoked by the human (`disable-model-invocation`) while using-team pointed to it → team-leader stopped and made the human type the command (K-70). Run 2: intake ran, then stopped and printed `/team:analyze` because "print the next command" was ambiguous (K-73). Run 3: intake → analyze → build (dev + reviewer), as in BEFORE. |
| verify s1 (4 checks) | 4/4 | **4/4** | $0.90 → $1.05 | Equivalent. |
| make-skill s1 (6 checks) | 0/6 | 0/6 | $0.33 → $0.16 | Inconclusive. BEFORE: every write to `.claude/skills/**` was refused by Claude Code under `-p` (K-72; 4 forms of `--allowedTools` tried, all refused). AFTER: refuses CORRECTLY per the new contract — the need has no evidence (a single CSV export, no recurring task); writes no file. The "create the skill" branch can only be tested in an interactive session. |
| asbuilt s1 (7 checks, re-scored) | 6/7 | **7/7** | $0.23 → $0.30 | The CHANGELOG check first pointed by mistake at `CHANGELOG.md` in the root (the project uses `docs/CHANGELOG.md`), and the "What changed" heading check (then in its Vietnamese form) was added AFTER the run; both working directories were re-scored. BEFORE: `pr-body.md` had 3/4 of the headings that `/team:pr` greps (missing "What changed"), and no post-G4 debt section. AFTER: 4/4 headings, the post-G4 debt section has 3/3 closed, and a 17-row table compares each criterion/touchpoint. |

Honest notes:
- No eval got worse after the fixes; the bad runs (using-team runs 1 and 2) have a cause, a fix (K-70, K-73) and a rerun.
- The using-team AFTER run 3 cost ≈ BEFORE: same chain of roles.
- make-skill needs a scenario with real evidence (a recurring task) and an interactive session; recorded in the next round's backlog.
