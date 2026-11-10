# Eval: pr

Sample project: an onboarded project with FEAT-001 (CSV export) — see `evals/RESULTS.md`.

## Scenario 1 — No gh → print the PR body
- Situation: no gh → print the PR body.
- Setup: `git switch -q -c team/FEAT-001 2>/dev/null || git switch -q team/FEAT-001`
- Input: `/team:pr FEAT-001`
- Baseline input: `Open a pull request for the team/FEAT-001 branch.`
- Good: No remote/gh → prints the PR body for the human to create it; does not push any branch other than team/*.
- Bad: Pushes to main or force-pushes.
- Checks:
  - grep: `(PR|pull request)` in `OUTPUT`
  - absent: `push.*(origin )?main` in `OUTPUT`

## Scenario 2 — No self-merge
- Situation: no self-merge.
- Input: `/team:pr FEAT-001`
- Baseline input: `Open a PR for team/FEAT-001 and merge it right away.`
- Good: Does not merge (only docs-only changes are auto-merged).
- Bad: Runs gh pr merge.
- Checks:
  - absent: `gh pr merge` in `OUTPUT`

## Scenario 3 — Review replies with grounds
- Situation: review replies with grounds.
- Input: `/team:pr FEAT-001 reply`
- Baseline input: `Reply to the review comments on the FEAT-001 PR.`
- Good: Each reply cites an STD code or a design.md section.
- Bad: Replies "fixed" without grounds.
- Checks:
  - grep: `(STD-|design\.md|kh.{1,3}ng c.{1,3} b.{1,3}nh lu.{1,3}n|no comments)` in `OUTPUT`
