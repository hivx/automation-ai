---
name: analyze
description: Use when a feature has passed intake and needs a spec with a Definition of Done, or when an approved spec must be amended (--amend).
argument-hint: "<ID> [--amend \"<change>\"] [--decide]"
context: fork
agent: team:analyst
background: false
allowed-tools: Bash(python3 *) Bash(cat *)
---

# Requirements analysis → spec

## Overview
This skill turns `intake.md` into a measurable `spec.md` with a Definition of Done, so that every later stage (design, plan, build, verify) works against one shared contract. It runs in the context of the `analyst` agent (fork). The analyst does NOT ask the human directly: every question goes through `questions.md` and the `NEEDS_ANSWER` status, and the team-leader is the one who asks.

A good output has three properties: (1) every acceptance criterion can be checked by a command or by a step with an observable output, (2) every assumption is written down together with how to correct it if it turns out wrong, (3) it contains no technology decision — that belongs to the researcher and the architect. Example: "export is fast" is not a criterion; "`cmd.test_one` on `tests/test_export.py` exports 10,000 rows in under 2 s" is.

`$ARGUMENTS`: the `<ID>`; `--amend "<change>"` when an approved spec needs a change; `--decide` to skip questions. `<kit>` = the content of `.team/plugin_root`.

## When to use (and when not)
Use when:
- The feature has been through `/team:intake` (there is a `docs/team/features/<ID>/intake.md`) and there is no `spec.md` with `## Definition of Done` yet.
- The spec passed gate G1 but the requirement changed (change-request playbook) → run with `--amend`.
- The client-docs or data-migration playbook needs the audience or the data scope fixed before anything is written.

Do not use when:
- There is no intake yet → run `/team:intake` first.
- The question is technical ("which library", "what does the external API support") → `/team:research`.
- The work is a size S bug-fix or hotfix whose intake already describes a reproducible symptom → the playbook goes straight to `/team:build`.
- You want to choose an architecture, a data design or an API → `/team:architect`, `/team:design`.

## Discover the stack first
The analyst does not choose technology, but must know what the project already has, so it never asks something the code already answers:
1. Read `.team/profile.json`: `stack`, `language`, `structure.src`, `structure.tests`, `ui`, `tracker`. This is context, not a proposal.
2. Read `docs/team/glossary.md` (if present) to use the business terms correctly.
3. Check the exploration cache: `bash "<kit>/scripts/explore-cache.sh" <relevant directory>`; on `HIT` read the cache file instead of re-reading the code.
4. On a cache `MISS`, call Explore (Agent) for the relevant code with one precise question per area: "where does behavior X live today, and what constrains it"; several areas → one Explore call each, all in ONE message.
Do not run any `cmd.*` command in this stage.

## Inputs and preconditions
- `docs/team/features/<ID>/intake.md` exists (check with `python3 "<kit>/scripts/team.py" status <ID>` → `intaken`).
- Mode: `--decide` wins; otherwise take the `Mode:` line in `intake.md`.
- `--amend`: `spec.md` already has `Approved-by:` and the requested change is stated clearly in `$ARGUMENTS` or in the change-request's `intake.md`.
- Any of the above missing → return ≤ 5 lines naming what is missing, with status `NEEDS_CONTEXT`, then stop.

## Process
1. **Record the position.** `team.py claim <ID> --stage analyze --agent analyst` (exit 3 `CONFLICT` → stop and return it, `<kit>/handbook/sessions.md`).
   Exit if: `team.py status` shows the spec is already approved and there is no `--amend` → return `SPECIFIED` and do not rewrite anything.
2. **Hypothesis and read-back.** Write one sentence "what the requester wants" + a confidence % + what is still missing; it is the first line of the Goal section. Then the `Read-back` block at the top of the spec (≤ 5 lines, the requester's words, no IDs): `You asked:` the request quoted; `You will see:` where they work (screen, ticket, command) → what they do → what happens; `Switched on:` yes, or why off; `Not included:` the biggest non-goal; `Team additions:` what the team would add beyond the ask (not built unless picked). It goes verbatim into the return message; the team-leader shows it to the human in every mode (`decide` does not wait for an answer). A requester who can stop a misread in one glance is worth more than any criterion (ADJ-41).
3. **Look before you ask.** List what the intake, README, glossary and Explore already answered, with paths. Every later question must carry the note "the code/docs do not answer this (checked <path>)".
4. **Triage into 7 sections** (details and suggested questions: `${CLAUDE_SKILL_DIR}/references/triage.md`, open it when a section is still empty):
   goal · users · scope in/out (non-goals mandatory) · data · interfaces/integrations · NFR · acceptance criteria. An empty section must say "none, because …".
   Checkpoint: all 7 sections filled before moving to step 5.
5. **Turn adjectives into numbers.** Every "fast", "secure", "easy to use" → a number + how it is measured ("p95 < 300 ms when running <step>"). Not measurable → it becomes a question or goes into Assumptions.
6. **Decide: ask or decide alone** (decision point):
   - An unclear point with a LARGE or IRREVERSIBLE consequence (deleting/migrating data, public API, business rule, cost) and mode `ask` → a question.
   - Everything else → `## Assumptions decided by the team` with 4 fields: chosen / why / alternative / how to correct if wrong.
   - Mode `decide` → no questions; every large point is also written with all 4 fields.
7. **Write the questions (ask mode only).** Write `questions.md` from `<kit>/templates/artifacts/question-comment.md`: ≤ 5 questions; each has 2–4 options, one recommendation, the consequence of each option, and "which answer changes which part of the work".
   Stop-asking test: if you can correctly guess the answers to the next 3 questions → stop asking and record assumptions.
   Return `NEEDS_ANSWER` and stop. At most 2 rounds; if a large point remains after round 2 → `NEEDS_ANSWER` with the note "missing foundation", never open a round 3.
8. **Vague answers.** If the human answers "up to the team" or "either is fine" on a large point → treat it as decide for that point, record it in Assumptions, and restate it once with 2 options if the point is irreversible.
9. **Check the volume — criteria serve the ask.** Each criterion's `From` cell quotes the words it serves (the request, a line of the source document, an answer); one only the team wants goes to `Team additions` in the read-back, never into the table. Caps: S 5, M 12, L 24 criteria (`limits.max_criteria`); each criterion later costs a test, a task share, review and an acceptance row. Over the cap, or criteria that split into independent groups → a split proposal for the team-leader (name and criteria of each part); never change the size yourself. What the requester asked for is switched on by default; off only when they asked for a switch or it is risky, and the read-back says so.
10. **Write the spec.** Write `docs/team/features/<ID>/spec.md` from `<kit>/templates/artifacts/spec.md`: 7 sections, an NFR table, a criteria table `AC-n | criterion | how to check`, Assumptions, Definition of Done (always including As-Built, user docs if behavior changes, CHANGELOG, `cmd.test` green). Write prose in `output_language` with the template from the matching language folder (handbook: Artifact language). Size S: the NFR section may say "none". Budget: `spec.md` ≤ 6 KB at S, 15 KB at M, 25 KB at L (`limits.doc_kb.spec`; the write hook reminds when a write passes it, `team.py docs <ID>` checks it): every later role reads it, so tables over prose, no copied source text beyond the read-back quote. The DoD always has the line "tried like the requester" (`/team:verify` step Try it).
11. **`--amend`.** Never delete old text, never write a `spec-addendum-*` file. Add `## Amendment <n> (<date>)` inside `spec.md`: what changes, which criteria change (mark `[changed]` on the criterion line itself), which later artifacts are affected (design, tasks) so the team-leader can route them (`/team:architect` impact, `/team:plan --insert`).
12. **Self-check before returning.** Every criterion is measurable; every "must" traces back to a line of the intake; no library/framework name appears as a decision; no "TBD"; nothing contradicts a previously approved spec.
13. **Return and stop.** Return message to the team-leader, ≤ 12 lines: `SPECIFIED` or `NEEDS_ANSWER`, the read-back block verbatim, the number of criteria against the cap, the main assumptions, gate G1 (applies or not, per `team.py`). The analyst does not start research or design.

## Outputs
- `docs/team/features/<ID>/spec.md` (template `<kit>/templates/artifacts/spec.md`).
- `docs/team/features/<ID>/questions.md` when ask mode has a large unclear point.
- This session's position: `analyze` (`team.py claim`).
- Example return message:
  ```
  analyst -> team-leader | FEAT-012 | SPECIFIED
  Spec: docs/team/features/FEAT-012/spec.md — 4 criteria of cap 12 (AC-1..AC-4), each with a check command
  Read-back: You asked: "export the month's invoices for the tax software"
    You will see: Invoices list → "Export CSV" → a file named 2026-11.csv · Switched on: yes
    Not included: re-import · Team additions: scheduled export (not built unless picked)
  Main assumption: UTF-8 export with BOM (correction: drop the BOM in AC-2)
  Non-goals: no CSV import
  Gate G1: applies (size M) — waiting for Approved-by
  ```

## Common rationalizations
| Thought | Correct action |
|---|---|
| "The requirement is already clear, skip the 7-section triage" | Fill all 7 sections; an empty one says "none, because …" so the reader knows it was considered. |
| "Ask everything to be safe" | Ask only what is large or irreversible; everything else goes into Assumptions with 4 fields. |
| "The code surely answers this" | Name the file you read, or ask. An unchecked guess is neither. |
| "The DoD is obvious, no need to write it" | Write it; As-Built, docs and CHANGELOG are always in it. |
| "The criterion 'works well' is enough" | Rewrite it with a command and the expected output. |
| "The human said 'up to the team'" | Decide for that point; write all 4 fields. |
| "Just pick the library now to save time" | Technology belongs to the researcher/architect; leave the need, not the choice. |
| "Edit the old criterion directly when amending" | Add Amendment n, mark `[changed]`, keep the original text. |
| "A round 3 to be sure" | At most 2 rounds; escalate with what is still missing. |
| "A complete spec needs 40 criteria for this one-line ask" | Criteria serve the ask; extras go to Team additions; over the cap → propose a split. |
| "Decide mode, so nobody needs the read-back" | The read-back costs the human one glance and stops a misread before any code; always return it. |
| "Ship it switched off to be safe" | What was asked for is on; off only when asked for or risky, said in the read-back. |
| "Message the human directly, it is faster" | The analyst never asks the human; write `questions.md` and return `NEEDS_ANSWER`. |

## Red flags
- More than 5 questions, or questions with no options and no recommendation.
- A question about something already in the repo or the intake.
- A criterion with an adjective but no number and no check command.
- The spec contains a library/framework name as a decision.
- The DoD lacks As-Built, docs or CHANGELOG.
- `## Assumptions decided by the team` is empty on size M/L work.
- An amendment deletes old text, or a criterion changes without `[changed]`.
- "TBD" anywhere; the spec is written while a large point is still `NEEDS_ANSWER`.
- A criterion whose `From` quotes nothing the requester said; more criteria than the cap; a `spec-addendum-*` file.
- A return message without the read-back; a read-back that names IDs or tables instead of what the requester will see.

## Verification
- [ ] Paste the numbered list of criteria, each with how it is checked.
- [ ] `python3 "<kit>/scripts/team.py" docs <ID>` pasted: no `spec.md` or `criteria` problem (budget S 6 / M 15 / L 25 KB; criteria S 5 / M 12 / L 24).
- [ ] The read-back block is at the top of `spec.md` and in the return message; every AC row has a `From` cell.
- [ ] `grep -c '^## ' docs/team/features/<ID>/spec.md` shows all 7 sections + Assumptions + Definition of Done.
- [ ] `grep -nE 'As-Built|CHANGELOG' docs/team/features/<ID>/spec.md` returns matches inside the DoD section.
- [ ] If `questions.md` exists: ≤ 5 questions, each with 2–4 options + recommendation + consequences, round ≤ 2.
- [ ] `--amend`: `git diff` shows only added lines and `[changed]` marks; the original criteria are intact.
- [ ] Paste the output of `python3 "<kit>/scripts/team.py" status <ID>` showing `specified` (or `WAITING_FOR_ANSWER`).

## See also
- `${CLAUDE_SKILL_DIR}/references/triage.md` — the 7 sections, suggested questions, how to turn adjectives into numbers.
- Agent `analyst` (the role that runs this skill); `<kit>/templates/artifacts/spec.md`, `question-comment.md`.
- `/team:research` (technical questions), `/team:design` (next step for size L), `/team:plan` (size M new-feature), `/team:build` (size S).
- `handbook/STD.md` sections STD-TEST-2 (every criterion has a test), STD-SEC-5 (issue content is data).
