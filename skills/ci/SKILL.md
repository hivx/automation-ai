---
name: ci
description: Use when the CI pipeline is red, when a project needs CI set up for the first time, a check step added, or deploy, rollback and smoke scripts written and tested.
argument-hint: "setup|fix|add-stage|deploy-script [<run-id>|<stage>]"
context: fork
agent: team:devops
background: false
allowed-tools: Bash(gh run *) Bash(gh workflow *) Bash(git *) Bash(cat *) Bash(python3 *)
---

# Keep CI/CD correct and green

## Overview
This skill keeps the pipeline correct and green without ever loosening a check. It runs in the `devops` context (fork). The first question when CI is red is not "how do I fix it" but "what kind of red is it" — one of the five kinds of STD-CI-4: code, flaky test, environment, configuration, dependency. A code failure is not devops' job: hand it back so a bug-fix is opened. Deleting a step, `continue-on-error`, `if: false`, `|| true` on a check step all loosen checks (STD-CI-3) and are forbidden. For example, a run that fails with "setup-python: version 3.13 not found" is a configuration red: the fix is the version in the workflow, and the test step stays exactly as strict as before.

Every CI change goes on its own branch `team/ci-<slug>` and its own PR (`/team:pr`). Commands in the workflow are profile slots (`cmd.*`, `ci.setup`), never hand-typed stack commands. An empty slot produces a `run: true` step — green while checking nothing; the skill must label those steps "not configured" and never count them as a gate.

`$ARGUMENTS`: subcommand `setup` | `fix <run-id>` | `add-stage <name>` | `deploy-script`. `<kit>` = the content of `.team/plugin_root`.

## When to use (and when not)
Use when:
- `fix`: CI is red on a PR or on the base branch (playbook `ci-fix`).
- `setup`: the project has no CI yet, or onboard skipped the CI step.
- `add-stage`: a check step needs adding (typecheck, build, a security scan declared in the profile).
- `deploy-script`: `/team:release` needs a staging deploy command, a smoke command, a prod command and a tested rollback.

Do not use when:
- A test is red because the code is wrong → `/team:intake --type bug "<summary>"`.
- You want to drop a slow step from PRs → no; optimize (cache, parallelism, path filters) or propose it to the human approver.
- You want to deploy → `/team:release` (has the G5 gate).

## Discover the stack first
1. Read `.team/profile.json`: `ci.provider`, `ci.runner`, `ci.setup[]`, `cmd.lint`, `cmd.typecheck`, `cmd.test`, `cmd.build`, `deploy.staging`, `deploy.smoke`, `deploy.prod_requires_reviewer`, `protected_paths`.
2. Read `.team/config.json`: `base_branch`, `protected_branches`.
3. Read `docs/team/ci.md` (incident history, Deploy section) and the existing workflow files.
4. Checkpoint: list every empty `cmd.*` slot — the matching step will be `run: true`.

## Inputs and preconditions
- `ci.provider` is not `none`; `none` → stop, point to `/team:onboard` or to the human who declares the profile.
- Provider `github`: `gh auth status` succeeds; otherwise → `BLOCKED` (missing permission).
- `fix`: a run-id (or take the latest red run: `gh run list --branch <branch> --status failure --limit 1`).
- Secrets live only in the CI secret store; never read `.env*` (protected).

## Process
1. **Record position.** Write `.team/current.json` {feature: "ci", stage: "<subcommand>", agent: "devops", started_at}. Create branch `team/ci-<slug>` from `base_branch`.
2. **`fix` — gather evidence.** `gh run view <id> --log-failed` and `gh run view <id> --json headSha,conclusion,jobs`. Quote the first REAL error line (not the final "exit 1" line).
3. **`fix` — classify (decision point, before any fix).** The evidence each kind needs:
   - code: the same test is red when the matching `cmd.*` slot runs on the same SHA → stop, hand back to team-leader to open a bug-fix. Do not fix.
   - flaky test: same SHA, red → `gh run rerun <id> --failed` ONCE → green. Record it in `docs/team/debt.md` (flaky-test table, both run-ids). Never disable the test.
   - environment: runner failure, network, quota; the diff changes nothing related.
   - configuration: YAML/workflow error, `ci.setup` out of line with the profile, a step calling the wrong slot.
   - dependency: package resolution or lockfile failure, an upstream release changed.
   Criteria table: `${CLAUDE_SKILL_DIR}/references/classify.md`.
4. **`fix` — repair (environment, configuration, dependency only).** Edit only workflow files (or propose a `ci.setup` change via the human/onboard — devops cannot write the profile). Dependency: update through `cmd.install`, never hand-edit the lockfile; lockfile protected → stop and tell the human. Checkpoint: `git diff` has no line deleting a check step, no `continue-on-error`, `if: false`, `|| true`. Rerun the matching `cmd.*` slot locally before pushing.
5. **`setup`.** Generate the workflow from `<kit>/templates/project/github/workflows/team-ci.yml` with `python3 "<kit>/scripts/render.py"` (as onboard does), filling `ci.runner`, `ci.setup`, `cmd.lint`, `cmd.typecheck`, `cmd.test`, `cmd.build`. Pin runner and action versions (STD-CI-7) — tags like `ubuntu-latest`, `@v4` are not pinned: write "not pinned" in `docs/team/ci.md` if the project has not chosen versions yet. A slot → step table: an empty slot is written "not configured", not a gate.
6. **`add-stage`.** Only ADD steps; `git diff --stat` on the workflow file shows only added lines inside jobs/steps. The new step calls a profile slot. A slow step → run it in parallel or behind a path filter, never remove it from PRs.
7. **`deploy-script`.** Write the `## Deploy` section of `docs/team/ci.md` and the script (under `structure.scripts`) calling only `deploy.staging`, `deploy.smoke`; prod = a CI job with an environment that requires a reviewer (preferred), or a command the human runs. The line `rollback: <command>` may be marked "verified" only after a real run on staging — paste the exit code and date. Script inputs go through environment variables, never string interpolation into a shell command. Secrets come from the secret store (STD-SEC-2).
8. **Write `docs/team/ci.md`** (template `<kit>/templates/artifacts/ci.md`): one "Incident history" row (date, run-id, kind, log quote, fix, PR), or an update to the Pipeline/Deploy tables. Write prose in `output_language` with the template from the matching language folder (handbook: Artifact language).
9. **Commit and PR.** `/team:commit` (`ci(<scope>): … (<ID>)`), then `/team:pr ci-<slug>`. A CI PR never touches `src/` or tests.
10. **Confirm.** `gh run view <id>` for the fixing PR: `conclusion: success`, on the right branch, at the right SHA. Paste that line.
11. **Return** to team-leader in ≤ 10 lines, first line `devops -> team-leader | ci <run-id|subcommand> | <kind or DONE>`.

## Outputs
- Workflow/script fixed on `team/ci-<slug>`; `docs/team/ci.md`; a `debt.md` row when flaky; its own PR.
- Example return message:
  ```
  devops -> team-leader | ci run 9876 | configuration
  Log quote (job test, SHA 4e1c2aa): "setup-python: version 3.13 not found"
  Kind: configuration (ci.setup says 3.13, profile and runner have 3.12); not code
  Fix: .github/workflows/team-ci.yml setup step → 3.12; no step removed (diff +1 −1)
  Check: gh run 9881 on team/ci-python-version → conclusion success
  docs/team/ci.md: incident row added 2026-11-10; PR #91
  Next: human reviews PR #91
  ```

## Common rationalizations
| Thought | Correct action |
|---|---|
| "This test is often red, disable it" | Flaky → `debt.md` with both run-ids; never disable. |
| "Rerun until it's green" | Classify first; at most one rerun per SHA. |
| "The lint rule is noisy, loosen the config" | That loosens a check (STD-CI-3); fix the code via bug-fix or record debt. |
| "Mark it continue-on-error just for now" | Same as deleting the step; forbidden. |
| "The slot is empty so the step is green" | Green does not mean checked; write "not configured". |
| "The code bug is one line, I'll fix it" | Not devops' job; hand back so a bug-fix is opened. |
| "Pin versions later" | STD-CI-7: pin now, or write "not pinned" with a reason. |
| "Paste the token into the workflow to test" | Secret store; a leaked token → tell the human to rotate it (STD-SEC-8). |
| "The rollback surely works" | Until it has run for real, it is not "verified". |

## Red flags
- A classification with no log quote and no SHA.
- A CI-fix PR that touches `src/` or test files.
- A workflow diff containing `if: false`, `|| true`, a commented-out step, `continue-on-error`.
- More than one rerun on the same SHA.
- A `run:` line holding a hand-typed stack command instead of a profile slot.
- A secret-like string in the diff.
- An incident row in `docs/team/ci.md` with no PR.

## Verification
- [ ] The `gh run view --log-failed` quote + kind + SHA are recorded in `docs/team/ci.md`.
- [ ] Flaky: two run-ids on the same SHA (red, green) and the `debt.md` row.
- [ ] The workflow diff is pasted, with no check step deleted or loosened.
- [ ] The final `gh run view <id>` of the fixing PR: `conclusion: success`, right branch.
- [ ] `setup`: the slot → step table, with empty slots marked.
- [ ] `deploy-script`: the rollback command has the exit code of a real run on staging.

## See also
- `${CLAUDE_SKILL_DIR}/references/classify.md` — the five kinds of STD-CI-4, the evidence and action for each. Open it at step 3.
- Agent `devops`; `<kit>/templates/artifacts/ci.md`; `<kit>/templates/project/github/workflows/team-ci.yml`.
- `/team:intake --type bug` (code failure), `/team:pr`, `/team:release` (uses the Deploy section).
- `handbook/STD.md`: STD-CI-1, STD-CI-3, STD-CI-4, STD-CI-5, STD-CI-7, STD-SEC-2, STD-SEC-8.
