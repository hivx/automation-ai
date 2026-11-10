---
name: clean
description: Use when a behavior-preserving cleanup of exactly one kind of debt is needed: dead code, naming, structure, unused dependencies, orphan tests, simplification, deprecating an old API, or adding logs/metrics.
argument-hint: "<dead-code|naming|structure|deps|tests|simplify|deprecate|observe> [<path>] [--decide]"
context: fork
agent: team:maintainer
background: false
allowed-tools: Bash(python3 *) Bash(cat *) Bash(git *)
---

# Cleanup without behavior change

## Overview
This skill does exactly ONE kind of cleanup and proves behavior is unchanged with two runs of `cmd.test` — before and after — with the same test count, the same test names, the same results. It runs in the `maintainer` context (fork). The "unchanged" evidence is worth something only where tests cover the code: an area no test touches proves nothing, so stop, or first write characterization tests in a separate commit. For example, removing `src/util/legacy_fmt.py` is a valid `dead-code` run only when grep for its name and string forms comes back empty and the before/after test-name lists are identical.

Before deleting or rewriting a piece of code, you must be able to say why it exists (`git log -L`, `git blame`). If you cannot explain it → do not touch it; record it in `debt.md` (Chesterton's fence). Changing an assertion to make a test green means behavior changed — revert and escalate.

`$ARGUMENTS`: the kind, the path scope, `--decide` (maintainer never asks the human; an unclear point → `NEEDS_ANSWER` back to team-leader). `<kit>` = the content of `.team/plugin_root`.

## When to use (and when not)
Use when:
- Playbook `refactor` after `/team:design --short` (G2b approved), or batch `clean-sweep`.
- A debt item in `docs/team/debt.md` comes up: dead code, names off `naming.*`, files misplaced per `structure.*`, unused dependencies, orphan tests.
- An internal API needs deprecating (its replacement already exists), or a running path needs logs/metrics.

Do not use when:
- There is a bug to fix → `bug-fix`; mixing it in breaks the before == after evidence.
- A data schema change → playbook `data-migration` (expand → migrate → contract).
- Replacing a framework, splitting a large module → `change-request`/`new-feature` with a full design.
- Two kinds at once → two runs, two PRs.

## Discover the stack first
1. Read `.team/profile.json`: `cmd.test`, `cmd.test_one`, `cmd.lint`, `cmd.typecheck`, `cmd.build`, `cmd.install`, `naming.*`, `structure.*`, `test.skip_markers`, `protected_paths`.
2. Read `.team/config.json`: `base_branch`.
3. Read `docs/team/features/<ID>/design.md` (the "How to prove behavior is unchanged" section) and the debt item in `docs/team/debt.md`.

## Inputs and preconditions
- The `<ID>` (refactor), exactly ONE kind, a path scope.
- Check: `python3 "<kit>/scripts/team.py" status <ID>` reports `designed` and G2b approved (the refactor playbook always has G2b on). Batch `clean-sweep` has no design → the scope must be one specific `debt.md` item.
- Branch `team/<ID>` is not checked out in another worktree; if it is → `NEEDS_CONTEXT`.
- Expected scope > 500 changed lines → split into several runs, or stop and ask team-leader for a tool-driven approach (codemod).

## Process
1. **Record position.** Write `.team/current.json` {feature: <ID>, stage: "clean", agent: "maintainer", started_at}.
2. **Branch.** In your own worktree: `git switch -c team/<ID> <base_branch>` (or `git switch team/<ID>` if it already exists).
3. **Baseline.** `cmd.test` BEFORE: save the test count AND the list of names, the exit code, `git rev-parse HEAD`. With a `cmd.build` → save the warning count. No test covers the scope (Grep the module name in the test directory) → decision point: if the design allows it, add characterization tests in a SEPARATE commit before the baseline; otherwise stop.
4. **Chesterton's fence.** For every piece you will delete or rewrite: one line "exists because …" from `git log -L`/`git blame`. Cannot explain it → record it in `debt.md` and skip that piece.
5. **Do exactly the kind** (details per kind: `${CLAUDE_SKILL_DIR}/references/kinds.md`):
   - `dead-code`: Grep the name AND its string forms, entry points in `structure.config`, exports, dynamic calls. Public (exported, mentioned in the README) → do not delete, switch to `deprecate`.
   - `naming`: one identifier family per commit, per `naming.*`; afterwards grep for the old name = 0 results (except CHANGELOG).
   - `structure`: moves only; `git diff -M --stat` shows renames ≥ 90% similar; new directories under `allowed_new_file_roots`.
   - `deps`: grep for the package's imports = 0 → edit the manifest → `cmd.install` so the tool regenerates the lockfile (STD-DEP-2); never hand-edit the lockfile; manifest in `protected_paths` → stop.
   - `tests`: delete an orphan test only when its target code is gone or its assertion duplicates a differently named test (cite both).
   - `simplify`: one simplification at a time → `cmd.test_one` on the covering test → the next one. Never remove error handling (that is behavior).
   - `deprecate`: the replacement must work first; mark the old one with status, replacement, removal deadline; full removal is a later run, once grep for call sites = 0.
   - `observe`: write 2–4 operational questions first; structured logs, bounded labels, no sensitive data (STD-SEC-6); tests stay unchanged.
6. **After.** `cmd.test` AFTER: compare the name list with the baseline (empty diff). The only exception: kind `tests` — record "before N, after N−k, deleted: <names>". `cmd.lint`, `cmd.typecheck` exit code 0. Different from the baseline → STOP; never "adjust it to match".
7. **Forbidden-change check.** `git diff --name-only <base_branch>` ∩ `protected_paths` = empty; grep the diff for new `test.skip_markers` = empty; test files change only in kind `tests` or through symbol renames.
8. **Commit** with `/team:commit` (`refactor(<scope>): … (<ID>)`). After the commit: `git switch --detach` to release branch `team/<ID>` so qa can check it out.
9. **Mark done for `team.py`.** Write `docs/team/features/<ID>/tasks.md` in the MAIN tree (the root path = the first line of `git worktree list`): `- [x] T1 — clean <kind> (<scope>)`. The refactor chain has no plan; this line makes the feature `built` so `/team:verify` can run (ADJ-26). Write prose in `output_language` with the template from the matching language folder (handbook: Artifact language); the task line itself stays as shown.
10. **Debt.** Update `docs/team/debt.md`: the item paid, what remains, anything newly found.
11. **Return** to team-leader in ≤ 10 lines, first line `maintainer -> team-leader | <ID> | DONE (<kind>)` (or `BLOCKED`, `NEEDS_ANSWER`).

## Outputs
- A commit on `team/<ID>`; `docs/team/features/<ID>/tasks.md` (T1 ticked); `docs/team/debt.md`.
- Example return message:
  ```
  maintainer -> team-leader | REF-007 | DONE (dead-code)
  Branch team/REF-007, commit 3f2a9c1 (branch released)
  Deleted: src/util/legacy_fmt.py (grep "legacy_fmt" 0 results outside CHANGELOG; existed for an old export, removed in v2.0)
  cmd.test before: 142 passed @a1b2c3d; after: 142 passed @3f2a9c1; name lists identical
  lint exit 0, typecheck exit 0; protected_paths: untouched; new skip markers: 0
  Remaining debt: src/report.py two duplicate functions (debt.md #12)
  Next: /team:verify REF-007
  ```

## Common rationalizations
| Thought | Correct action |
|---|---|
| "Grep finds no caller" | Also check strings, config, exports; public → `deprecate`. |
| "Green tests mean behavior is unchanged" | Only where tests cover the code; uncovered → characterization tests first, or stop. |
| "I only need to adjust one assertion" | Behavior has changed; revert and escalate. |
| "Drop the error handling to tidy up" | The error path is behavior; forbidden. |
| "The lockfile is stale, edit it by hand" | `cmd.install` (STD-DEP-2). |
| "While I'm here, fix this bug" | `debt.md` + a separate bug-fix. |
| "Rename things the way I like" | Only per `naming.*`. |
| "Same test count is enough" | Compare test names, not just the count. |
| "Since I'm deprecating, migrate the callers too" | Migrating callers is a separate run. |

## Red flags
- The two `cmd.test` outputs differ in count or names with no "deleted" list.
- A diff mixing renames with logic changes.
- Test files edited in kind `simplify`/`naming` beyond symbol renames.
- The lockfile changed but the report has no `cmd.install` line.
- A diff > 500 lines.
- "Dead" code deleted without a pasted empty-grep command.
- No `tasks.md` T1 after finishing (feature stuck at `designed`).

## Verification
- [ ] Both `cmd.test` outputs (count + names) with before/after SHAs; the name diff is empty, or matches the deleted list for kind `tests`.
- [ ] The exit codes of `cmd.lint`, `cmd.typecheck` are pasted.
- [ ] The kind-specific evidence (empty grep, rename similarity, `cmd.install` output).
- [ ] `git diff --name-only` ∩ `protected_paths` and the skip-marker grep are pasted (even when empty).
- [ ] `team.py status <ID>` reports `built` after step 9.

## See also
- `${CLAUDE_SKILL_DIR}/references/kinds.md` — the evidence and traps of each kind. Open it at step 5.
- Agent `maintainer`; `workflows/refactor.md`, `workflows/batch/clean-sweep.md`.
- `/team:design --short` (before), `/team:verify` (after), `/team:commit`, `/team:pr`.
- `handbook/STD.md`: STD-TEST-5, STD-DEP-2, STD-STRUCT-1, STD-NAME-1, STD-DESIGN-3, STD-SEC-6, STD-OPS-5.
