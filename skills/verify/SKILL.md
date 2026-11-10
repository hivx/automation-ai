---
name: verify
description: Use when every task of a feature is ticked and each criterion needs independent acceptance with real commands before release.
argument-hint: "<ID>"
context: fork
agent: team:qa
background: false
allowed-tools: Bash(python3 *) Bash(cat *) Bash(git *)
---

# Acceptance with real commands

## Overview
This skill delivers the verdict `accepted` / `rework` / `design-defect` for a built feature by RE-RUNNING every criterion on exactly the commit that will go into the PR and pasting the real output. It runs in the `qa` context (fork). qa does not modify code, does not modify tests, and does not trust the dev's description or an old CI result: the only evidence is the output of a command qa has just run, tied to one commit.

The `Verdict:` line is machine-read (`team.py` relies on it to know the feature is `verified`); a malformed line means the feature cannot pass (K-18). Example: `Verdict: accepted` on its own line is valid; `**Verdict:** Accepted` or `Verdict = accepted` is not.

`$ARGUMENTS`: the `<ID>`. `<kit>` = the content of `.team/plugin_root`.

## When to use (and when not)
Use when:
- `team.py status <ID>` reports `built` (every task is ticked).
- After rework, to run acceptance again.
- The dependency-upgrade, data-migration or refactor playbook needs a full check before the PR.

Do not use when:
- Some task is still unticked → `/team:build`.
- You want a per-task code quality review → that is the reviewer inside `/team:build`.
- You need a release → `/team:asbuilt`, `/team:pr`, `/team:release` after G4 is approved.

## Discover the stack first
1. Read `.team/profile.json`: `cmd.test`, `cmd.test_one`, `cmd.lint`, `cmd.typecheck`, `cmd.build`, `cmd.migrate`, `test.skip_markers`, `protected_paths`, `ui`.
2. Read `.team/config.json`: `base_branch`.
3. The command that checks each criterion comes from the "how to check" column in `spec.md` and the test plan in `design.md`; if another command is needed, use only a `cmd.*` slot or a data-reading command. Never write a new check script.

## Inputs and preconditions
- `docs/team/features/<ID>/spec.md` (criteria + DoD), `design.md` (test plan, size M/L), `tasks.md` fully ticked.
- `python3 "<kit>/scripts/team.py" status <ID>` reports `built`; otherwise hand it back and stop.
- Branch `team/<ID>` can be checked out, with a clean tree.

## Process
1. **Record the position.** Write `.team/current.json` {feature, stage: "verify", agent: "qa", started_at}.
2. **Pin the commit.** `git switch team/<ID>`; `git status --porcelain` must be empty (dirty tree → stop and report); `git rev-parse HEAD` → write it at the top of `acceptance.md`. All evidence must be produced AFTER this command, on this commit. If the branch moves mid-way (a new commit appears), record the new commit and rerun every criterion — evidence from the old commit is no longer valid.
3. **Reread the requirements.** Reread every criterion and the DoD in `spec.md` and make a list; never infer them from green tests.
4. **A gate for each criterion** — identify the command → run it fresh → read the full output, the exit code, the error count → compare with the criterion → only then write the conclusion. Each row: `criterion | command | exit code | output (excerpt) | covering test | conclusion`. Details and the "what a claim needs" table: `${CLAUDE_SKILL_DIR}/references/evidence.md`.
5. **Regression evidence (bug-fix).** A "bug is fixed" criterion needs a reproducing test: its RED output before the fix must be in the dev report or a `review-NN.md`; if absent → `rework` with the request "paste the red output of the reproducing test". qa never reverts code itself to try it.
6. **Beyond the happy path.** A criterion with inputs → run at least one command for an error path or a boundary value named in the test plan. Only happy-path evidence → record a gap.
7. **Test quality.** For each criterion, find the test that covers it (file::name) and read it: does the assertion state the criterion exactly (expected value hard-coded, not computed by the very code under test; not only checking a mock)? No covering test → `rework` (STD-TEST-2); a test that can never fail → `rework` (STD-TEST-5).
8. **General checks.** `cmd.test`, `cmd.lint`, `cmd.typecheck` (if present), `cmd.build` (if present): paste the exit code and error count. Odd warnings in the output (deprecations, errors printed while the exit code is 0) are a note in the general-checks table; an error swallowed while the exit code stays 0 is `rework` (STD-ERR-1).
9. **Skip markers and weakened assertions.** Grep `git diff <base_branch>...team/<ID>` for every string in `test.skip_markers`, and for assertion lines that were deleted or loosened (STD-TEST-4, STD-TEST-5). Paste the result, even when it is empty.
10. **Migration** (if `cmd.migrate` exists and the diff contains a migration): write the expected figures first, run up → down → up, reconcile the counts (STD-OPS-2, STD-OPS-3).
11. **UI** (`ui: true`): Playwright MCP if available; if not → that criterion is `NOT VERIFIABLE` and you return `NEEDS_ANSWER` so the team-leader asks the human for screenshots (qa never asks the human directly).
12. **Failures before conclusions (decision point).** A red command → classify it: wrong test / wrong code / environment / flaky.
    - Flaky: record 3 runs; flaky = `rework` + a line in `debt.md`, never `accepted`.
    - Environment cannot run it: no conclusion; return `BLOCKED` with the command and the error.
    - A failure that already exists on `base_branch`: name it, never hide it.
13. **DoD.** Grade the build part of the DoD (tests, code, docs changed within tasks). As-Built, CHANGELOG and user docs are written in `/team:asbuilt` AFTER G4: their absence is NOT a reason for `rework` — write "owner: writer, after G4" and the check command so `/team:release` checks it again. An existing README that describes the behavior just run WRONGLY → `rework`. Compare `git diff --name-only` with `protected_paths` (STD-SEC-1).
14. **Verdict** per `${CLAUDE_SKILL_DIR}/references/evidence.md`:
    - `accepted`: every criterion passes, the build part of the DoD is complete, Acceptance checklist 6/6, no `NOT VERIFIABLE` item.
    - `rework`: code/tests/docs are lacking but the design is right; every failing criterion has a reproduce command and an owning task (T<N>).
    - `design-defect`: the code matches the design but the design/spec cannot satisfy the criterion (contradictory criteria, impossible NFR).
15. **Write** `docs/team/features/<ID>/acceptance.md` from `<kit>/templates/artifacts/acceptance.md` (Write): commit, criteria table, general checks, the 6-item checklist, DoD, a `NOT VERIFIABLE` section if any, and a last line of the exact form `Verdict: accepted` (or `rework`, `design-defect`). Write prose in `output_language` with the template from the matching language folder (handbook: Artifact language).
16. **Return** to the team-leader in ≤ 10 lines; record metrics if asked to (`bash "<kit>/scripts/log-run.sh" --skill verify --result <verdict>`).

## Outputs
- `docs/team/features/<ID>/acceptance.md` (template `<kit>/templates/artifacts/acceptance.md`).
- `.team/current.json` {stage: "verify"}.
- Example return message:
  ```
  qa -> team-leader | FEAT-012 | rework
  Commit checked: a9d41e0 (team/FEAT-012). File: docs/team/features/FEAT-012/acceptance.md
  Passed 3/4 criteria; AC-2 failed: <cmd.test_one tests/auth/test_otp.py> → exit 1, "AssertionError: 200 != 401" (task T3)
  cmd.test exit 0; cmd.lint exit 0; new skip markers: 0
  DoD missing: CHANGELOG (STD-DOC-3). Checklist 6: 4 pass, 2 fail
  Next: /team:build FEAT-012 --task T3, then /team:verify FEAT-012
  ```

## Common rationalizations
| Thought | Correct action |
|---|---|
| "The dev says it already passed" | Run it yourself and paste the output. |
| "CI is green" | CI ran on another commit at another time; run it on the HEAD under acceptance. |
| "Lint passes, so the build is fine" | Run `cmd.build` (or typecheck) separately. |
| "This criterion obviously passes" | Run one command that hits exactly that behavior; paste it. |
| "I ran it earlier in this session" | Rerun it on the recorded commit. |
| "The down migration is rarely used" | Up → down → up, then reconcile. |
| "No command can check this criterion" | Write `NOT VERIFIABLE`, return `NEEDS_ANSWER`; never accept by reading. |
| "The README is only slightly off" | `rework` (STD-DOC-2). |
| "The test is flaky, rerun until green" | Flaky = rework + `debt.md`. |
| "The code matches the design but the result is wrong" | `design-defect`, not rework. |
| "Fix the assertion to get it done" | qa never modifies code or tests; write `rework`. |
| "The output in the dev's message is enough" | Only output qa just ran, on the recorded commit. |
| "The happy path passes, that is enough" | Also run the boundary/error path named in the test plan; if missing, record a gap. |

## Red flags
- The words "probably", "seems", "looks like" in `acceptance.md`.
- Pasted output without a command or an exit code; two criteria with identical output.
- Output produced before the commit recorded at the top; `acceptance.md` without a commit.
- The number of criteria in `acceptance.md` differs from `spec.md`.
- `accepted` while a failing row remains, a `NOT VERIFIABLE` remains, or there is a new skip marker.
- The migration was run in the up direction only.
- The verdict line is not exactly of the form `Verdict: <value>`.
- `rework` without a reproduce command and an owning task for each failing criterion.
- qa wrote files other than `acceptance.md` and its own memory.
- Figures (timings, coverage ratios) that cannot be traced to a command that was run.

## Verification
- [ ] `git rev-parse HEAD` of `team/<ID>` is at the top of `acceptance.md`.
- [ ] One row per criterion with command, exit code, output; the row count equals the criteria count in the spec.
- [ ] Output of `cmd.test`, `cmd.lint`, `cmd.typecheck` (if present) with error counts.
- [ ] The grep result for skip markers and deleted assertions in the diff is pasted (even if empty).
- [ ] A criterion → covering test table.
- [ ] `grep -E '^Verdict: (accepted|rework|design-defect)$' acceptance.md` returns exactly one line; `team.py status <ID>` agrees.

## See also
- `${CLAUDE_SKILL_DIR}/references/evidence.md` — the claim/evidence table, verdict decisions, failure classification.
- Agent `qa`; `<kit>/templates/artifacts/acceptance.md`.
- `/team:build --task T<N>` (rework), `/team:design` (design-defect), `/team:asbuilt` (after G4).
- `handbook/STD.md`: Acceptance checklist (6), STD-TEST-2/4/5/7, STD-OPS-2/3, STD-DOC-1/2/3.
