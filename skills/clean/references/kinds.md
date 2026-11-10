# Each cleanup kind: evidence and traps

| Kind | Required evidence | Common traps |
|---|---|---|
| dead-code | grep for the name + string forms (dynamic registration, reflection), grep for entry points in `structure.config`, the export list — all empty; one "exists because" line | code called only through config or a plugin; a public API (must be deprecated) |
| naming | old → new name list; grep for the old name after the rename = 0 (except CHANGELOG); one identifier family per commit | renaming inside user-facing strings (that is behavior); names in stored data |
| structure | `git diff -M --stat`: renames ≥ 90% similar; imports updated; new directories under `allowed_new_file_roots` | a "while I'm here" logic fix in the moved file |
| deps | grep imports = 0; manifest changed; `cmd.install` output; `cmd.build` + `cmd.test` afterwards | a package used only at build/test time; a package that pulls in a plugin; manifest in `protected_paths` |
| tests | target code is gone, or the assertion duplicates another test (cite both `file::name`) | a test that "looks" orphaned but covers the only error path |
| simplify | for each step: `cmd.test_one` on the covering test before the next step | removing error handling, merging two branches with a small difference, reordering something with side effects |
| deprecate | the replacement works (tested); the deprecation mark names the replacement + removal deadline; grep call sites before full removal | removing it while call sites remain; deprecating a schema (goes to data-migration) |
| observe | 2–4 operational questions; structured logs, bounded labels, no sensitive data; tests unchanged | logging PII, unbounded labels (user id as a metric label), logging in a hot loop |

## Characterization tests
When the area to clean has no covering test and the design allows it:
1. A separate commit, BEFORE the baseline: tests that record the CURRENT behavior (odd behavior included) — no code changes.
2. Run the new tests: they must be green on the old code.
3. The baseline (step 3) runs after this commit.
Never write characterization tests in the same commit as the change.

## When to stop
- `cmd.test` after differs from before (count, names, results).
- The scope exceeds 500 lines.
- The target is a public API or stored data.
- A `protected_paths` change would be needed (manifest, lockfile, prod config).
- Chesterton's fence cannot be explained for an important piece of code.
