# Scan tier budgets

| Tier | Reads | Budget | Answers | Stops when |
|---|---|---|---|---|
| T0 | Directory tree, manifests, `git log --stat`, tags, open issues/PRs, CHANGELOG (names and figures only) | ≈ 0 content tokens; ≤ 10 commands | How far has it got (first pass) | Enough to know the stack, commit cadence, hot spots |
| T1 | README, `docs/`, ADRs, CLAUDE.md, specs/plans | ≤ 15 documents; table of contents first | What does it do (in the documents' words) | The main features are described |
| T2 | Main modules + hot spots: feature ↔ code/test, TODO/FIXME, skipped tests, unmerged branches, unapplied migrations | ≤ 10 modules, through Explore | How far has it got (really), what comes next | No new contradiction |
| T3 | Deep read of each module | Only on a T2 contradiction, an undocumented module, or `--full` | Clear up the contradiction | The contradiction is explained |

## Small repo
A repo with < 30 tracked files: T2 may read files directly instead of using Explore; record "read directly, < 30 files" in the Scanned table. T3 still runs only on a contradiction or with `--full`.

## AI-readiness — what to examine
- The existing CLAUDE.md: line count, content, staleness, contradictions with the code.
- `.claude/`, plugins, MCP, AGENTS.md: keep / cut / rewrite.
- Conclude with one of three: `ready` / `adjust-profile` / `clean-first`.

## Health appendix in assessment.md
Can build/test run (proposed commands), lint, coverage if figures exist, outdated dependencies/CVEs, exposed secrets, flaky tests.
