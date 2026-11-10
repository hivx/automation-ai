---
name: release
description: Use when a feature is accepted, G4 is approved and the As-Built exists, and it needs to be merged, tagged, deployed to staging for UAT, then to prod once the human has approved G5.
argument-hint: "<ID> [staging|prod]"
disable-model-invocation: true
allowed-tools: Bash(python3 *) Bash(cat *) Bash(gh pr checks *) Bash(gh pr view *) Bash(git tag *) Bash(git log *)
---

# Release with human approval

## Overview
This skill takes an accepted feature to staging, then to prod — and never to prod without the human's approval line. It runs in the main session: team-leader checks the preconditions, picks the version, and holds the gates; devops (Agent `team:devops`) does the infrastructure-touching part: merge, tag, run the deploy and smoke commands. The kit never deploys prod on its own (SPEC §1): prod runs only after `Approved-by-prod:`, using exactly the command/pipeline recorded and tested in `docs/team/ci.md` (ADJ-24).

Three non-negotiables: the rollback plan exists BEFORE the deploy (STD-OPS-1); a red smoke means stop and propose rollback, never "keep it for now"; G5 is always a human. For example, a staging run whose smoke prints one failed check ends this skill with a rollback proposal and a message to the human, not with a second deploy attempt.

`$ARGUMENTS`: the `<ID>`; `staging` (default) or `prod`. `<kit>` = the content of `.team/plugin_root`.

## When to use (and when not)
Use when:
- `team.py status <ID>` reports `verified`, G4 is approved, `asbuilt.md` exists, and the PR is open (`/team:pr`).
- UAT on staging is done and the human has added `Approved-by-prod:` → `/team:release <ID> prod`.
- Playbook `release` (a version bundling several features) or `hotfix` (the prod part always needs a human).

Do not use when:
- There is no As-Built or CHANGELOG entry yet → `/team:asbuilt`.
- CI is red on the PR → `/team:ci fix`; never release on red CI.
- You want to change the deploy command or write a rollback script → `/team:ci deploy-script` (separate PR, reviewed).

## Discover the stack first
1. Read `.team/profile.json`: `deploy.staging`, `deploy.smoke`, `deploy.prod_requires_reviewer`, `ci.provider`, `protected_paths`.
2. Read `.team/config.json`: `base_branch`, `protected_branches`, `gates.G5_prod`, `approvers.G5_prod`.
3. Read the `## Deploy` section of `docs/team/ci.md`: how prod is reached (a CI job with an environment that requires a reviewer, or a command) and the line `rollback: <verified command>`. The profile has no slot for prod deploy or rollback (SPEC §8); those two commands live only in `docs/team/ci.md` (ADJ-24).
4. `deploy.staging` empty, or no rollback line in `docs/team/ci.md` → STOP, next command: `/team:ci deploy-script`. Never invent a deploy command.

## Inputs and preconditions
Run and paste each command; if one condition fails → stop, print what is missing and the command that fixes it:
- `python3 "<kit>/scripts/team.py" status <ID>` → `verified`; G4 approved (or off).
- `gh pr checks <PR number>` → every check green.
- `docs/team/features/<ID>/asbuilt.md` exists; `CHANGELOG.md` has a line with `(<ID>)` under `## [Unreleased]`.
- Post-G4 debt (K-35): the `## Post-G4 debt` section of `asbuilt.md` is closed, or the items marked "left for /team:release to check" are rerun here (devops runs the commands qa left) and are green.
- `git diff --name-only <base_branch>...team/<ID>` touches no `protected_paths` without a human approval.
- `prod`: the additional conditions in step 8.

## Process
1. **Record position and reason.** Write `.team/current.json` {feature, stage: "release", agent: "devops", started_at}; one journal sentence: why devops is being called and with what goal.
2. **Pick the version (decision point).** `git tag --sort=-v:refname | head -n 5` + the groups in the feature's CHANGELOG entry: any Removed or "breaking" → bump major; any Added → minor; only Fixed/Security → patch. If the project has another convention (recorded in `profile.notes` or visible in CHANGELOG history), follow it. Record the chosen tag and the reason in the journal.
3. **Rollback plan before deploy.** Write the `## Rollback` section in `asbuilt.md` (team-leader may write `docs/team/**`): trigger conditions (red smoke; an NFR from the spec violated), the command (copied from `docs/team/ci.md`), the data part (cite the migration up/down/up line in `acceptance.md`), and the expected duration. Write prose in `output_language` with the template from the matching language folder (handbook: Artifact language). No tested rollback command → do not continue.
4. **Hand off `deploy-staging` to devops** (Agent `team:devops`), handoff message ≤ 10 lines: ID, PR, chosen tag, the `deploy.staging`/`deploy.smoke` commands, the `asbuilt.md` file. devops does:
   1. Merge the PR once it has its approvals under the branch-protection rules — no forced merge, no admin rights.
   2. Rename `## [Unreleased]` to `## [<version>] - <YYYY-MM-DD>` in CHANGELOG (on the merged branch), create the tag, push only the tag (STD-GIT-3).
   3. Record the version currently running on staging BEFORE the deploy (the rollback target).
   4. `deploy.staging` → `deploy.smoke`; paste the exit codes and output.
5. **Read devops' result.** Green smoke → step 6. Red smoke → devops PROPOSES a rollback to the version recorded in step 4.3; team-leader informs the human and writes the journal; stop. Never redeploy to "try once more".
6. **UAT stop point.** Print for the human the UAT list = the criteria in `spec.md` + the "What to do" part of the release notes, and the next command. The state stops here; the skill ends.
7. **Prod: preconditions.** The first 20 lines of `asbuilt.md` contain `Approved-by-prod: <name> <YYYY-MM-DD>` (with a date). If `approvers.G5_prod` is non-empty → the name must be in that list. Missing → STOP and print the G5 approval instructions. There is no "urgent" exception — hotfix included.
8. **Prod: recheck before touching anything.** `gh pr checks` is still green on the tagged commit; the `## Rollback` section exists; if `deploy.prod_requires_reviewer` is true → prod must be reached through a CI job with an environment that requires a reviewer, or by the human running the command; devops only triggers, never operates by hand on prod data or infrastructure (STD-OPS-7).
9. **Hand off `deploy-prod` to devops**: trigger exactly the pipeline/command in `docs/team/ci.md` → `deploy.smoke` on prod; paste the exit code. If the design has a log/metric for the new path (STD-OPS-5) → paste one line proving the feature is running.
10. **Red prod smoke** → devops proposes a rollback immediately (command from `## Rollback`); the human decides and runs it under the prod rules. The journal records the incident; open `docs/team/defects.md` if needed. Stop.
11. **Green** → devops adds the line `Released: <tag> <YYYY-MM-DD>` to `asbuilt.md` (the template reserves the spot). Check: `team.py status <ID>` reports `released`; `git tag -l <tag>` lists it.
12. **Journal and metrics.** One journal line: tag, staging/prod, smoke, duration; `bash "<kit>/scripts/log-run.sh" --skill release --result <released|staging|stopped>`.

## Outputs
- A version tag; `CHANGELOG.md` with the version section; the `## Rollback` section and the `Released:` line in `docs/team/features/<ID>/asbuilt.md`; journal.
- Message to the human (staging done):
  ```
  release FEAT-014 | staging green
  Tag: v1.5.0 (minor: Added 1 in CHANGELOG). PR #87 merged, CI green.
  deploy.staging exit 0; deploy.smoke exit 0 ("12 checks ok")
  Rollback: to v1.4.2 with the command in docs/team/ci.md (verified 2026-11-02)
  UAT: AC-1..AC-5 in spec.md + OTP_TTL config change
  Next: add `Approved-by-prod: <name> <date>` to asbuilt.md, then /team:release FEAT-014 prod
  ```

## Common rationalizations
| Thought | Correct action |
|---|---|
| "It's urgent, go to prod first and approve later" | Stop and wait for a dated `Approved-by-prod:`; urgency is the human's call, not the team's. |
| "Staging is green, so prod is surely fine" | Prod smoke still runs and its exit code is pasted. |
| "The smoke is only slightly red, keep it" | Stop, propose rollback, inform the human. |
| "We'll figure out rollback later" | No tested rollback command, no deploy. |
| "Force the merge to make the deadline" | Follow branch protection; missing approvals means wait. |
| "Skip UAT this time" | The human decides that, not the team. |
| "I'll roll back prod myself, it's faster" | devops proposes; the human decides and runs it (STD-OPS-7). |
| "Just guess the version number" | Follow the latest tag + the CHANGELOG groups. |
| "Everyone knows the prod deploy command" | Only the command/pipeline recorded in `docs/team/ci.md`; if absent, `/team:ci deploy-script`. |

## Red flags
- A tag created before CI was green.
- A prod deploy while the `asbuilt.md` header has no dated `Approved-by-prod:`.
- CHANGELOG still shows `[Unreleased]` for a feature that already has a tag.
- "Smoke ok" without an exit code and output.
- A `Released:` line exists but `git tag -l <tag>` is empty.
- `--force`, a merge using admin rights, a push to a protected branch.
- A deploy command that does not come from `deploy.*` or `docs/team/ci.md`.
- No `## Rollback` section before the first deploy.

## Verification
- [ ] The output of `team.py status <ID>` and `gh pr checks` is pasted before the deploy.
- [ ] The exit codes of `deploy.staging` and `deploy.smoke` (and the prod smoke when going to prod) are pasted.
- [ ] Prod: the `Approved-by-prod:` line is quoted from the first 20 lines of `asbuilt.md`.
- [ ] `git tag -l <tag>` and the version line in CHANGELOG are pasted.
- [ ] The `## Rollback` section has the command, the trigger conditions, and the data part.
- [ ] After prod: `grep '^Released:' asbuilt.md` and `team.py status <ID>` reporting `released`.

## See also
- Agent `devops`; `/team:ci deploy-script` (writes deploy/rollback/smoke commands), `/team:asbuilt` (before), `/team:status`.
- `workflows/release.md`, `workflows/hotfix.md`; `docs/team/ci.md` (Deploy section).
- `handbook/STD.md`: STD-OPS-1, STD-OPS-4, STD-OPS-5, STD-OPS-7, STD-CI-6, STD-GIT-3.
