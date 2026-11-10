# As-Built writing rules

## Reading the diff by design section
1. Get the file list from `diff.patch`: Grep `^diff --git a/` → one line per file.
2. For each touchpoint in `design.md` section 7: is the file in the diff?
   - Yes, and the kind of change matches ("new"/"edit") → read that file's hunks.
   - No → a row "differs: not touched (design planned an edit)"; look for the reason in `tasks.md`.
3. A file in the diff that is not among the touchpoints → its own row "outside touchpoints", citing the `review-NN.md` that accepted it (reviewer scores item 2 of the checklist).
4. For design sections 2–6 (data, API, flow, permissions, migration): find the hunk that proves each point (field name, error code, permission check, migration file). Record the `file:line` of the first `+` line in the hunk.

## Table-row template
| Design section | Reality | file:line | Reason |
|---|---|---|---|
| 3. API — `POST /otp/verify` returns 409 when expired | differs: returns 422 | src/auth/otp.py:41 | review-02: STD-ERR-3, use the project's shared error code |
| 6. Migration 0007 | as designed | migrations/0007_otp.py:1 | — |
| (outside touchpoints) src/auth/__init__.py | export edited | src/auth/__init__.py:3 | accepted by review-01 (needed for the import) |

## Sourced sentences
- Each release-notes sentence ends with its source in parentheses while drafting (`(AC-2)`, `(src/x.py)`); the final user-facing version may drop the parentheses, but the source must remain in the As-Built.
- Keep names, numbers, units, commands, paths and conditions exactly as in the source; never promise more than the evidence ("always", "in every case" only when acceptance has the matching boundary/error path).
- No source → do not write it; if the reader needs it, put it under "Needs a human read".

## CHANGELOG groups (Keep a Changelog)
| Group | When |
|---|---|
| Added | a new feature/command/field the user can see |
| Changed | existing behavior changed (including breaking — say "breaking" and point to the migration guide) |
| Deprecated | still usable, will be removed; give the deadline and the replacement |
| Removed | already removed |
| Fixed | a bug fixed (bug-fix, hotfix) |
| Security | a vulnerability fixed; never describe how to exploit it |

Each line: one sentence, present tense, ending `(<ID>)`. No line for an internal change nobody sees (pure refactor → group Changed only when build/install behavior changed; otherwise omit).

## Audience
| `--audience` | Write about | Avoid |
|---|---|---|
| user | what they can now do, changes they see, what they must do | file names, tasks, STD |
| dev | API contract, configuration, migration, how to upgrade | marketing language |
| client | benefit, scope, conditions, milestones | internal detail; content that needs a human approver → "Needs a human read" |
