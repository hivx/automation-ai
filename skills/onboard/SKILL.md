---
name: onboard
description: Use when takeover's G0 has been approved, or an empty repo needs the team configured for the first time (--new), to install the profile, config, settings, rules, CI and the docs/team skeleton for the project.
argument-hint: "[--new] [--accept-clean-first]"
allowed-tools: Read Glob Bash(jq *) Bash(cat *) Bash(ls *) Bash(mkdir *) Bash(cp *) Bash(python3 *) Bash(git status *) Bash(echo *) Bash(awk *) Bash(wc *)
---

# Bring the team into the project

## Overview
This skill turns the project into a place where the team can work: `.team/profile.json`, `.team/config.json`, `CLAUDE.md` (a project block that describes THIS project, plus a short team block), `.claude/settings.json` + `settings.local.json`, path-scoped rules, CI, and the `docs/team/` skeleton. It runs in the main session (team-leader) under the permission exception of the `onboard` stage (it may write `CLAUDE.md`, `.gitignore`, `.claude/rules/**`, `.github/**`, profile/config; `cp` only from `<kit>/templates/`). The exception opens when `.team/current.json` has `stage: onboard` and MUST be closed (`stage: idle`) on every exit, including an early stop.

Three rules: merge, never overwrite (settings are merged as JSON, CLAUDE.md gets its two blocks, an existing rule is skipped); print plugin install commands, never install them (SPEC §8); re-running onboard must report "skipped (already present)" for every file — if it does not, onboard has a defect. Example: a project that already has `.claude/settings.json` with its own `permissions.allow` keeps every entry; onboard only adds what is missing and lists any risky leftover as work for the human.

`$ARGUMENTS`: empty (a project with code, after G0) | `--new` (empty repo) | `--accept-clean-first` (the human has confirmed running even though the AI-readiness verdict is `clean-first`). `<kit>` = the content of `.team/plugin_root`. `R` = `python3 "<kit>/scripts/render.py"`.

## When to use (and when not)
Use when:
- `docs/team/ai-readiness.md` has `Approved-by:` (G0 approved) after `/team:takeover`.
- An empty repo is starting a new project (`--new`, playbook `new-project`).
- Upgrading the kit version: re-run it to add the missing parts (everything already present is kept).

Do not use when:
- A project with code has not been taken over yet → `/team:takeover` first.
- You want to change one command in the profile → the human edits `profile.json` (or re-runs onboard with a new proposal); agents do not edit the profile outside onboard.
- You want to install plugins → onboard only prints the commands.

## Discover the stack first
1. Read `docs/team/profile-proposal.md` (a proposal per slot, with evidence) and `docs/team/ai-readiness.md` (the `Verdict:` line); `--new`: ask the human for the stack (the main session may use AskUserQuestion), then choose `<kit>/profiles/<stack>.json`.
2. Read the existing `.claude/settings.json`, `.claude/settings.local.json`, `CLAUDE.md`, `.gitignore` — to know what will be merged and what will be kept.
3. Read `<kit>/.claude-plugin/plugin.json`: the kit version (recorded in `onboarding.md`).
4. The profile's `plugins.required`/`recommended`; the current `enabledPlugins` (plugins that overlap with `team`: superpowers, commit-commands, pr-review-toolkit).

## Inputs and preconditions
- Without `--new`: the first 20 lines of `docs/team/ai-readiness.md` contain `Approved-by: <name> <YYYY-MM-DD>`. Missing → stop and print the approval command.
- K-09: `Verdict: clean-first` → STOP before any write: list the clean-up work that ai-readiness names, ask the human for a separate confirmation (AskUserQuestion), or re-run with `--accept-clean-first`. `adjust-profile` → use `profile-proposal.md` together with the edits made in the G0 approval.
- First run in this repo (no `.team/plugin_root`): Write `.team/plugin_root` with one line, the kit root = `${CLAUDE_SKILL_DIR}` without its last two parts (`/skills/onboard`). The SessionStart hook only refreshes the file once `.team/` exists; it never creates `.team/` in a repo nobody took over. (`--new` runs without takeover.)
- Check: `python3 "<kit>/scripts/team.py" status`.

## Process
Details of every file and how it is merged: `${CLAUDE_SKILL_DIR}/references/files.md`.
1. **Open the exception.** Write `.team/current.json` {stage: "onboard"}. From here on, every exit (including errors) ends with step 13.
2. **Plan before writing.** Print a table: target file | write mode (create / merge JSON / insert block / skip because present) | template source. This is also the skeleton of the table in `onboarding.md`. Checkpoint: every file of steps 3–10 appears in the table before anything is written.
3. **Profile.** From `profile-proposal.md` (or `<kit>/profiles/<stack>.json`) → Write `.team/profile.json`. Check: `python3 "<kit>/scripts/check-profile.py" "<kit>/templates/schemas/profile.schema.json" .team/profile.json` — `cmd.test_one` and `cmd.format` must contain `{file}` (K-01). Red → fix the proposal or stop; never write a wrong profile.
4. **Config.** `<kit>/templates/project/team/config.json` → `.team/config.json` (already present: keep it, add only the missing keys); a project with code keeps G0 on. The template sets `output_language` to `vi` (the prose language of artifacts the team writes); keep an existing value, and tell the human they can change it to `en`. Check with `check-profile.py` against `config.schema.json`.
5. **CLAUDE.md — about the project, not about the team.** (a) Team block: `R --template "<kit>/templates/project/CLAUDE.md.tmpl" --insert-block CLAUDE.md` (creates the file when missing; ≤ 25 lines, at the end). (b) Project block `<!-- project:start -->…<!-- project:end -->`, placed above the team block: present → keep it (re-run = skipped). Missing → Edit it in from `<kit>/templates/artifacts/claude-md.md` (language folder per `output_language`), every `<fill:` replaced with a fact from `assessment.md`, `profile-proposal.md`, the profile's `cmd.*` and `structure.*`; `--new` → from the chosen stack and the human's answers. An old CLAUDE.md (text outside the team block) is adopted into the project block and the keep / cut / rewrite of its ai-readiness row is applied; every cut or corrected line gets one row in `onboarding.md` (what, why, evidence) — never drop a line without a reason. Machine check: `python3 "<kit>/scripts/check-claude-md.py"` → 0 problems.
6. **Settings.** `R --json --template "<kit>/templates/project/claude/settings.json.tmpl" --merge-into .claude/settings.json`; likewise `settings.local.json.tmpl` → `.claude/settings.local.json` (`Read(//<kit>/**)` is machine-specific, ADJ-19). Existing values win → review them: a leftover `Bash(*)`, `defaultMode: bypassPermissions`, or an `"agent"` other than `team:team-leader` → record it under "work the human must do by hand"; never report success silently. Overlapping plugins → print the `skillOverrides` entries to add.
7. **Rules.** Each `<kit>/templates/project/claude/rules/<x>.md.tmpl` → `R --template … --out .claude/rules/<x>.md` (already present → skip).
8. **CI.** `ci.provider` = `github` → render `<kit>/templates/project/github/workflows/*.yml` into `.github/workflows/`, copy the PR/issue templates and CODEOWNERS with `cp` from `<kit>/templates/` (no overwrite); `gitlab` → a skeleton `.gitlab-ci.yml`; `none` → skip. Record as manual work: the `ANTHROPIC_API_KEY` secret, and that the CI runner needs `--allowedTools` (already in the templates, K-06).
9. **`docs/team/` skeleton**: `features/`, `adr/`, `research/`, `explore/`, `journal/`, `metrics/`, `retro/`, `proposals/`, `agents/`; `skills-registry.md`, `kit-issues.md` from their templates.
10. **`.gitignore`.** Merge the missing lines from `<kit>/templates/project/gitignore.tmpl` (it includes `.claude/worktrees/`, `.team/current.json`, `.team/session/`).
11. **Plugins: print only.** `claude plugin install <name>@<marketplace>` for each `plugins.required` (with a blocking warning) and `recommended`. Do not install.
12. **One trial run.** `git status --short` first; `cmd.install`, `cmd.lint`, `cmd.test` (Bash) — record the command, exit code, output (record red too); `git status --short` after: a changed lockfile or protected file → report it, do not commit it. Check `grep -c '{{' CLAUDE.md .claude/settings.json .claude/rules/*.md` = 0 (no empty placeholder left behind).
13. **Close the exception.** Write `.team/current.json` {stage: "idle"}. Do this step on EVERY exit.
14. **Report.** Write `docs/team/onboarding.md` (template `<kit>/templates/artifacts/onboarding.md`): the step-2 table with the real status, the kit version, the trial-run table, uninstalled plugins, manual work. Write prose in `output_language` with the template from the matching language folder (handbook: Artifact language). One journal line.

## Outputs
- `.team/profile.json`, `.team/config.json`, `CLAUDE.md` (project block + team block), `.claude/settings.json`, `.claude/settings.local.json`, `.claude/rules/*.md`, `.github/**` (if github), the `docs/team/` skeleton, `docs/team/onboarding.md`.
- Message to the human:
  ```
  onboard | done (kit team 0.3.0)
  Created 11, merged 2 (settings.json, .gitignore), skipped 3 (already present); CLAUDE.md: project 64/150, team 17/25, 0 problems
  check-profile: profile OK, config OK (output_language: vi — change to en in .team/config.json if wanted)
  Trial run: cmd.install exit 0; cmd.lint exit 0; cmd.test exit 1 (2 failed — pre-existing, recorded in debt)
  Plugins not installed: pyright-lsp (recommended) — command in onboarding.md
  Manual work: add the ANTHROPIC_API_KEY secret; remove the existing "Bash(*)" from settings.json
  Next: commit the files above, then /team:intake "<request>"
  ```

## Common rationalizations
| Thought | Correct action |
|---|---|
| "G0 is surely fine" | No `Approved-by:` → stop, close the exception. |
| "clean-first, but it was approved, just run it" | A separate confirmation (K-09) or `--accept-clean-first`. |
| "Overwrite settings/CLAUDE.md, it is cleaner" | Merge JSON, insert the blocks; report the old values that were kept. |
| "CLAUDE.md is where the team introduces itself" | CLAUDE.md describes the project; the team block is ≤ 25 lines at the end. A file with only the team block is unfinished. |
| "Install the missing plugins right away" | Print the commands only. |
| "cmd.install changed the lockfile, commit it" | Report it; lockfiles are in the forbidden zone. |
| "Count the block's lines by eye" | `awk … | wc -l` (K-08). |
| "It failed midway, leave stage onboard as is" | Always write `stage: idle` on exit. |
| "Tests are red, no need to record them" | Record the red output verbatim in `onboarding.md`. |
| "Copy the template files from another project, it is faster" | `cp` only from `<kit>/templates/` (the hook flags other sources, K-26). |

## Red flags
- `.team/current.json` still has `stage: onboard` after the run.
- A `{{` left in a rendered file.
- `git diff CLAUDE.md` touches lines outside the two blocks (other than an old CLAUDE.md adopted with a reason row per change).
- CLAUDE.md holds only the team block, or a `<fill:` is left in the project block.
- Something was written into `~/.claude/`; a plugin was installed.
- `onboarding.md` has no exit codes for the trial run.
- `Bash(*)` or `bypassPermissions` still in settings with no warning.
- Re-running onboard produces new "created" files (onboard is not idempotent).

## Verification
- [ ] The `check-profile.py` output for both profile and config is pasted.
- [ ] The `check-claude-md.py` output (0 problems, project and team line counts) is pasted; `git diff CLAUDE.md` stays inside the two blocks.
- [ ] `grep -c '{{'` on the rendered files = 0; `jq '.agent, .permissions.deny' .claude/settings.json` is pasted.
- [ ] `cat .team/current.json` shows `idle`.
- [ ] The trial-run table in `onboarding.md` has exit codes; `git status --short` before/after `cmd.install` is pasted.

## See also
- `${CLAUDE_SKILL_DIR}/references/files.md` — every target file, its template source, and how it is merged. Open it at steps 2–10.
- `/team:takeover` (before), `/team:intake` (after); `scripts/render.py --help`, `scripts/check-profile.py --help`.
- `docs/04-profile.md`, `docs/06-install.md`; `hooks/role-policy.json` (the `onboard` exception).
