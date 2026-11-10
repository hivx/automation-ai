---
name: asbuilt
description: Use when a feature is accepted and G4 is approved and it needs an As-Built, release notes, a CHANGELOG entry, README or user-doc updates, and the PR body before release.
argument-hint: "<ID> [--audience user|dev|client]"
context: fork
agent: team:writer
background: false
allowed-tools: Bash(python3 *) Bash(cat *)
---

# Record what was delivered

## Overview
This skill records what WAS delivered — not what was planned — for the right reader. It runs in the `writer` context (fork), after qa has written `Verdict: accepted` and the human has approved G4. It produces four things: `asbuilt.md`, which compares every design section with the real code; release notes for the named audience; a CHANGELOG entry under `## [Unreleased]`; and `pr-body.md`, which `/team:pr` uses verbatim.

The rule: every sentence you write must trace back to a line in `acceptance.md` (AC-n) or a hunk in `diff.patch`. No source, no sentence. For example, "OTP codes now expire after the configured TTL (AC-2)" is allowed only because AC-2 exists and was run; "OTP is now more secure" is not, because nothing measured it. The As-Built is also where the "after G4" part of the DoD, whose owner qa recorded, gets closed (K-35).

`$ARGUMENTS`: the `<ID>`, optional `--audience` (default `user`). `<kit>` = the content of `.team/plugin_root`.

## When to use (and when not)
Use when:
- `team.py status <ID>` reports `verified` and G4 is approved (or G4 is off).
- `/team:release` reports a missing As-Built, CHANGELOG entry, or user doc.
- After a rework round that was accepted again: rewrite the As-Built for the new commit, because the old table points at lines that moved.

Do not use when:
- Not accepted yet → `/team:verify`. An As-Built written before acceptance is a guess.
- The work is documentation only (playbook `docs-only`, `client-docs`): team-leader hands it straight to writer per the playbook; there is no diff to compare against.
- You want to change code so it matches the docs → that is rework, not As-Built.

## Discover the stack first
1. Read `.team/profile.json`: `structure.docs` (where user docs live), `cmd.*` (every command shown to readers is copied from here, never typed from memory), `protected_paths`.
2. Read `.team/config.json`: `base_branch`, `gates.G4_uat`.
3. The project's PR template: `.github/PULL_REQUEST_TEMPLATE.md` (if present) — `pr-body.md` fills exactly its sections; if absent use `<kit>/templates/project/github/PULL_REQUEST_TEMPLATE.md`.
4. The existing CHANGELOG format: Read the first 30 lines of `CHANGELOG.md` (Keep a Changelog or a house style). Follow what exists; if there is no file, create one in Keep a Changelog format. A root `CHANGELOG.md` is always created (K-05).

## Inputs and preconditions
- `docs/team/features/<ID>/spec.md`, `design.md` (size M/L), `acceptance.md`, `review-NN.md`, `tasks.md`.
- `docs/team/features/<ID>/diff.patch` — written by `/team:build` in its last step (Write). Missing or empty → return `NEEDS_CONTEXT` with "need diff.patch from /team:build".
- Check: `python3 "<kit>/scripts/team.py" status <ID>` reports `verified`; `grep -E '^Verdict: accepted$' acceptance.md` matches exactly one line. Either fails → stop and hand back.
- G4 on: the first 20 lines of `acceptance.md` contain `Approved-by: <name> <YYYY-MM-DD>`. Absent → stop; do not write an As-Built for a version the human has not taken delivery of.

## Process
1. **Record position.** Write `.team/current.json` {feature, stage: "asbuilt", agent: "writer", started_at}.
2. **Collect qa's post-G4 debt.** Grep `acceptance.md` for the lines marked "owner: writer, after G4" and the check commands qa left with them. Each line becomes one job for this run. Checkpoint: write down how many jobs you collected; at the end, the number closed must equal it.
3. **Design ↔ reality table.** For every section of `design.md` (8 sections) and every touchpoint row: Grep the path in `diff.patch`, read the changed hunk, then write one row `section | as designed / differs: … | file:line | reason`. Take reasons only from `review-NN.md`, notes in `tasks.md`, and `DESIGN_CONFLICT` lines; if there is none, write "reason: not recorded" — never invent one. A file in the diff that is not among the touchpoints → its own row, citing the `review-NN` that accepted it. Size S has no `design.md`: compare against the criteria in `spec.md`. How to read the diff and the row template: `${CLAUDE_SKILL_DIR}/references/writing-rules.md`. Exit condition: rows = design sections + touchpoints (+ out-of-touchpoints files).
4. **Decision point — behavior outside the spec.** The diff contains behavior that is in neither `spec.md` nor `acceptance.md` (a new endpoint, a new config flag, a changed default) → STOP and hand back to team-leader (it needs analyst `--amend` or a human decision). Do not describe it as a feature.
5. **Release notes** for the reader named in `--audience`: what changed, who is affected, what they must do (config change, migration window, new API version — taken from design sections 3 and 6). Each sentence cites AC-n or a file. Internal terms (task, review, STD) belong in the As-Built only, never in the release notes.
6. **CHANGELOG.** Edit `CHANGELOG.md`: add lines under `## [Unreleased]` in the groups Added / Changed / Deprecated / Removed / Fixed / Security; one user-visible change per line, ending with the feature ID `(<ID>)`. A breaking change → group Changed/Removed with a pointer to the migration guide. Do NOT turn `[Unreleased]` into a version number — that belongs to `/team:release`.
7. **User docs.** Grep the README and `structure.docs` for the command names, flags and behavior that just changed; edit exactly those passages, in the present tense ("command X outputs Y"), never as a change history. Commands shown to readers are copied from the `cmd.*` values. If the README is already correct → write "README: unchanged (grep `<string>` matches the AC-n behavior)".
8. **pr-body.md.** Write `docs/team/features/<ID>/pr-body.md` following the PR template: `## Feature` (ID, paths of design/asbuilt/acceptance, Verdict), `## Why` (cite the spec), `## What changed` (behavior + main files; where it differs from design, cite the As-Built), `## How verified` (commands + exit codes copied from `acceptance.md`, no new claims), then the template's Review checklist. `/team:pr` greps exactly these four headings, so they stay English whatever `output_language` is.
9. **Close the post-G4 debt.** For each job from step 2: do it, then rerun the check command qa left (read-only commands only, such as `grep`); record the result in the `## Post-G4 debt` section of `asbuilt.md`. A check that needs to run code → write "left for /team:release to check".
10. **Write `asbuilt.md`** from `<kit>/templates/artifacts/asbuilt.md` (Write): the step-3 table under `## Differences from design`, the release notes, the CHANGELOG entry you added, the post-G4 debt section, and an empty `## Rollback` section for `/team:release`. Write prose in `output_language` with the template from the matching language folder (handbook: Artifact language). Keep a placeholder for `Approved-by-prod:` within the first 20 lines; do NOT fill it in yourself, and do not write `Released:` (devops writes it after prod).
11. **Final check.** `git status --short`: only `docs/**`, `CHANGELOG.md`, `README.md` changed (writer's role-policy). Grep `pr-body.md` for the four headings; grep CHANGELOG for `(<ID>)`.
12. **Return** to team-leader in ≤ 10 lines, first line `writer -> team-leader | <ID> | ASBUILT` (or `NEEDS_CONTEXT`, `NEEDS_ANSWER`).

## Outputs
- `docs/team/features/<ID>/asbuilt.md`, `docs/team/features/<ID>/pr-body.md`.
- `CHANGELOG.md` (entry under `[Unreleased]`); `README.md` or files under `structure.docs` when behavior changed.
- Example return message:
  ```
  writer -> team-leader | FEAT-014 | ASBUILT
  Files: docs/team/features/FEAT-014/{asbuilt,pr-body}.md, CHANGELOG.md, docs/auth.md
  Design comparison: 8 sections + 6 touchpoints; 1 differs (section 3: error 409→422, src/auth/otp.py:41, reason review-02)
  CHANGELOG: Added 1, Changed 1 under [Unreleased] (FEAT-014)
  Post-G4 debt from acceptance: 2/2 closed (CHANGELOG, docs/auth.md)
  Needs a human read: release notes "What to do" (OTP_TTL config change)
  Next: /team:pr FEAT-014
  ```

## Common rationalizations
| Thought | Correct action |
|---|---|
| "The code matches the design, one row is enough" | One row per design section and per touchpoint, each with `file:line`; a short table hides the one difference reviewers need. |
| "The deviation was probably for performance" | Take reasons only from `review-NN`, `tasks.md`; otherwise write "not recorded". |
| "Technical release notes are quicker" | Write for the `--audience` reader; technical detail goes in the As-Built. |
| "Mention the upcoming feature too, for completeness" | Only what is in the diff and in acceptance; future work is a promise nobody verified. |
| "The README is surely still right" | Grep the changed behavior string and paste the grep result as evidence. |
| "I'll type the install command from memory" | Copy the `cmd.*` value from the profile. |
| "Turn `[Unreleased]` into 1.4.0 while I'm here" | That belongs to `/team:release` (devops), which picks the version from tags. |
| "Add `Approved-by-prod:` to complete the paperwork" | Only the human fills it (G5 is always a human). |
| "The diff has a new endpoint, describe it as a feature" | Behavior outside the spec → stop and hand back to team-leader. |

## Red flags
- The design ↔ reality table has fewer rows than design sections plus touchpoints.
- A "differs" row without `file:line` or a diff hunk as its basis.
- A release-notes sentence that traces to no AC-n and no file.
- A CHANGELOG line without the feature ID; `[Unreleased]` already renamed to a version number.
- The README mentions a command that is not in `cmd.*`.
- `pr-body.md` lacks one of the four headings; "How verified" contains a command that is not in `acceptance.md`.
- writer wrote `Released:` or `Approved-by-prod:`; a file was written outside `docs/**`, `CHANGELOG.md`, `README.md`.

## Verification
- [ ] Paste `grep -E '^Verdict: accepted$' acceptance.md` (one line) and the G4 `Approved-by:` line (when G4 is on).
- [ ] Design ↔ reality table: row count = design sections + touchpoints; every "differs" row quotes its diff hunk.
- [ ] The `CHANGELOG.md` diff under `## [Unreleased]` is pasted and contains `(<ID>)`.
- [ ] Every qa line marked "owner: writer, after G4" has a closing result in `## Post-G4 debt`.
- [ ] `grep -cE '^## (Feature|Why|What changed|How verified)$' pr-body.md` = 4 is pasted.
- [ ] `git status --short` shows only files inside writer's write zone.

## See also
- `${CLAUDE_SKILL_DIR}/references/writing-rules.md` — reading the diff by design section, the table-row template, CHANGELOG groups, the sourced-sentence rule. Open it at steps 3 and 5.
- Agent `writer`; `<kit>/templates/artifacts/asbuilt.md`; PR template `<kit>/templates/project/github/PULL_REQUEST_TEMPLATE.md`.
- `/team:verify` (before), `/team:pr` (uses `pr-body.md`), `/team:release` (turns `[Unreleased]` into a version, rechecks the post-G4 debt).
- `handbook/STD.md`: STD-DOC-1, STD-DOC-2, STD-DOC-3, STD-SEC-6, STD-GIT-7.
