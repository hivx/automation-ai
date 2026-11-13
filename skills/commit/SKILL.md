---
name: commit
description: Use when a dev or maintainer has a green change and needs to commit it to the team's standard.
argument-hint: "[<ID>] [--task T<N>]"
allowed-tools: Bash(git status *) Bash(git diff *) Bash(git add *) Bash(git commit *) Bash(git restore *) Bash(git log *)
---

# Committing to the team's standard

## Overview
This skill turns a change that is already green into one or a few small commits, each with one intent, in the format `type(scope): description (<ID>)` (STD-NAME-5), containing only files within the touchpoints. Its users are the dev or the maintainer, running it directly in their own worktree (no fork). A commit is a save point: each commit must be revertible on its own while the project still builds and passes its tests (STD-GIT-2).

The `check-git.sh` hook flags `--no-verify`, `-n`, force-push and a badly formatted message (a reminder by default, a stop with `enforcement: block`); this skill does what the hook cannot: choose the files, separate the intents, write a meaningful message, and scan the staged part for secrets. Example: a task that adds expiry checking and also renames a helper ends up as two commits — `fix(otp): reject expired codes (FEAT-012)` and `refactor(otp): rename check helper (FEAT-012)`.

`$ARGUMENTS`: the `<ID>`, `--task T<N>`. The touchpoints come from the handoff message or from the task line in `docs/team/features/<ID>/tasks.md`.

## When to use (and when not)
Use when:
- The dev has just got `cmd.test_one` green and `cmd.lint` clean for the current task.
- The maintainer finished one kind of cleanup and has `cmd.test` output that is identical before and after.
- A rework round after review: a NEW commit for the fix (never amend a commit already sent for review).

Do not use when:
- Tests are still red, or have not been rerun since the last edit → rerun them first.
- The change touches files outside the touchpoints → stop, `DESIGN_CONFLICT`.
- You want to push the branch or open a PR → `/team:pr` (tech-lead).
- The lockfile needs to change → only through `cmd.install` in a dependency task (STD-DEP-2).

## Discover the stack first
1. Read `.team/profile.json`: `cmd.test_one`, `cmd.lint`, `cmd.typecheck`, `test.skip_markers`, `protected_paths`, `naming.branch`.
2. `git branch --show-current` must be the task branch `team/<ID>-…` (your own worktree, K-14). Wrong branch → stop and report.
3. The list of commit types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `ci`, `perf`, `build`.

## Inputs and preconditions
- Green `cmd.test_one` output and clean `cmd.lint` output produced AFTER the last file edit. Any edit since → rerun.
- The task's touchpoints (a list of paths).
- A working tree without an unfinished merge conflict.

## Process
1. **See the whole picture.** `git status --short` and `git diff` (Bash). Write down the list of changed files.
2. **Filter by touchpoints.** A file outside the touchpoints → keep it out of the commit (`git restore --staged <file>` if already staged); record it in the report under "Seen but not touched" and return `DESIGN_CONFLICT` if that change is needed for the task. Files in `protected_paths`, `.env*`, lockfiles, `.team/profile.json`, build output → never committed.
3. **Clean the diff.** Remove debug logging, commented-out code, temp files, new TODOs without a task code (STD-STYLE-5). Code orphaned by the change → list it in the report; never silently delete anything outside the touchpoints.
4. **Split by intent (decision point).** One intent per commit: the test + code of one behavior → `feat`/`fix`; a pure rename or reformat → a separate `refactor`/`chore`; docs → `docs`. Formatting forced by the formatter on a touchpoint file goes with that file's commit; formatting that spread to other files → revert it.
5. **Stage deliberately.** `git add <specific path>` for each intent; no `git add -A`, no `git add .`.
6. **Review what is staged.** `git diff --staged --name-only` (compare with the touchpoints) and `git diff --staged` (reread every line). For every hunk you must be able to answer three questions: which criterion (`AC-n`) does this hunk serve? which test would fail if the hunk were removed? does the hunk change a contract (signature, field name, format) that the plan does not record? A hunk that cannot answer the first question → take it out of the commit; a yes to the third → `DESIGN_CONFLICT`.
7. **Scan the staged part.**
   - Test skip markers: search `git diff --staged` for every string in `test.skip_markers`; any hit → stop (blocker STD-TEST-4).
   - Secrets: search for the patterns in `${CLAUDE_SKILL_DIR}/references/secret-patterns.md`; any hit → stop and report to the human through the tech-lead (STD-SEC-1, STD-SEC-8). Record the location, never copy the value.
8. **Atomicity test.** "If this commit alone were reverted, would the project still build and pass its tests?" No → merge or re-split.
9. **Size.** > 300 changed lines or > 3 files on a size S task → record a `DONE_WITH_CONCERNS` concern suggesting the tech-lead split the task; never change the scope yourself.
10. **Write the message.** No `Co-Authored-By:` trailer and no "Generated with" line (STD-GIT-8; the hook flags them). First line: `type(scope): description (<ID>)`, imperative, standing on its own, ≤ 72 characters where possible. Body (for a non-trivial change): WHY, constraints, the `AC-n` criteria covered. First lines like "fix", "update", "misc", "phase 1" are forbidden. Examples: `${CLAUDE_SKILL_DIR}/references/messages.md`.
11. **Commit.** `git commit` (NO `--no-verify`, no `-n`).
    If the project's commit hook reports an error (decision point):
    - Format/lint error on a touchpoint file → fix it, rerun `cmd.lint`, stage again, make a NEW commit.
    - Test error → back to dev work: run `cmd.test_one`, fix, rerun; never commit while red.
    - Error on a file outside the touchpoints (the hook scans the whole repo) → do not fix that file; record it in the report and return `DONE_WITH_CONCERNS` for the tech-lead to decide.
    - The hook cannot run (missing tool) → record the error verbatim, return `BLOCKED`; never bypass the hook.
    The kit's `check-git.sh` hook flags `--no-verify`/`-n`; its message is a rule, not a suggestion, even when it only reminds.
12. **Save point when red.** After a slice where `cmd.test_one` turns red for no clear reason: do not pile more edits on top. Go back to the last green commit for your own files (`git restore <file>` on touchpoint files), find the cause, then redo it in small steps. Never use `reset --hard` (it loses other people's work, and it is not in this skill's permissions).
13. **Never rewrite shared history.** No `--amend`, no `reset --hard`, no rebase of commits the reviewer has already seen; rework rounds use new commits.
14. **Check after committing.** `git log -1 --stat` for each commit; `git status --short` clean for the task's files.
15. **Report.** Return ≤ 10 lines to the caller: status, commits (sha + first line), files, the test command run with its output, "Seen but not touched", concerns.

## Outputs
- One or a few commits on the task branch `team/<ID>-…`.
- Example return message:
  ```
  dev -> tech-lead | FEAT-012 T3 | DONE
  Commit: a1b2c3d fix(otp): reject expired code (FEAT-012)
  Files: src/auth/otp.py, tests/auth/test_otp.py (exactly the touchpoints)
  Test: <cmd.test_one tests/auth/test_otp.py> → 6 passed; lint: exit 0
  Staged scan: skip markers 0, secrets 0
  Seen but not touched: src/auth/session.py:88 swallows an error (recorded as debt, not fixed)
  ```

## Common rationalizations
| Thought | Correct action |
|---|---|
| "One task, so one commit for everything" | Split by intent: test + code of one behavior; rename/reformat separately. |
| "The commit hook is slow, `--no-verify`" | Never; fix what the hook reports. |
| "I will write the message later" | Write the first line in the right format now. |
| "That extra file is only a small edit" | Take it out of the commit and report `DESIGN_CONFLICT`. |
| "Tests were green before the last edit" | Rerun `cmd.test_one` and `cmd.lint` after it. |
| "Amend the commit already sent for review" | A new commit (STD-GIT-4). |
| "Commented-out code as a reminder" | Delete it; STD-STYLE-5. |
| "The lockfile changed, commit it too" | The lockfile is protected; only via `cmd.install` in a dependency task. |
| "`git add -A` is faster" | Add exactly the paths in the touchpoints. |
| "The formatter also touched other files, leave it" | Keep only the changes on touchpoint files; revert the rest. |
| "The hook fails on someone else's file, disable it once" | Never disable it; report `DONE_WITH_CONCERNS` to the tech-lead. |
| "It is red, a few more edits will surely make it green" | Go back to the green save point and find the cause first. |

## Red flags
- `git add -A` or `git add .` in the command history.
- A message without `(<ID>)`, or with a type not on the list.
- A commit containing files outside the touchpoints, `.env*`, lockfiles, `.team/profile.json`, build output.
- `--no-verify`, `-n`, `--amend`, `reset --hard` in any command.
- A test and an unrelated refactor in the same commit.
- No test output after the last edit.
- A change of > 300 lines without a message body.

## Verification
- [ ] `git status --short` before and after is pasted; after, it is clean for the task's files.
- [ ] `git diff --staged --name-only` is a subset of the touchpoints.
- [ ] Output of `cmd.test_one` and `cmd.lint` (and `cmd.typecheck` if present) produced after the last edit.
- [ ] The (empty) result of the skip-marker and secret scans on the staged part is pasted.
- [ ] If the commit hook reported an error: the error output and the new commit after the fix are pasted (no `--no-verify`).
- [ ] `git log -1 --stat` for each commit; the first line matches `^(feat|fix|refactor|test|docs|chore|ci|perf|build)(\(.+\))?: .+ \((FEAT|BUG|CHG)-[0-9]+\)$`.

## See also
- `${CLAUDE_SKILL_DIR}/references/messages.md` — good/bad message examples, splitting commits.
- `${CLAUDE_SKILL_DIR}/references/secret-patterns.md` — patterns for scanning the staged part for secrets.
- Agents `dev`, `maintainer`; skill `/team:build` (the loop that calls commit), `/team:pr`.
- `handbook/STD.md`: STD-NAME-5, STD-GIT-2/4/5, STD-STYLE-5, STD-SEC-1, STD-DEP-2.
