---
name: design
description: Use when an approved spec needs a detailed design (data, API, flow, permissions, migration, touchpoints, test plan) before planning, or when a refactor needs a short design proving behavior does not change.
argument-hint: "<ID> [--short]"
context: fork
agent: team:designer
background: false
allowed-tools: Bash(python3 *) Bash(cat *)
---

# Detailed design

## Overview
This skill writes a `design.md` concrete enough that tech-lead can split tasks without guessing, dev knows exactly which files to touch, and qa knows which test checks each criterion. It runs in the `designer` context (fork). designer follows the approved architecture (citing ADR IDs), follows the conventions already in the code, and does not decide business rules. Splitting tasks is tech-lead's job (`/team:plan`); designer only lists touchpoints.

Writing order: contracts before flow. Every observable behavior of a public entry point (error codes, messages, ordering, default values) is a contract, because someone will come to depend on it. Adding is safer than changing; breaking needs a new version and a migration guide (STD-DESIGN-3). For example, adding an optional `OTP_EXPIRED` error code to `POST /otp/verify` is backward compatible; changing its existing 409 to 422 is a break, even if no document ever promised 409.

`$ARGUMENTS`: the `<ID>`; `--short` for the refactor playbook (sections 1, 7, 8 + how to prove behavior is unchanged). `<kit>` = the content of `.team/plugin_root`.

## When to use (and when not)
Use when:
- Size M/L after analyze (and after architect for size L), before `/team:plan`.
- Playbook `refactor` (`--short`), `data-migration` (mapping, rollback; G2b on), `integration` (contracts, retry, idempotency).
- qa returned `design-defect`: rewrite the wrong part of the design, then re-plan/rebuild the affected part.

Do not use when:
- Size S: the criteria in the spec are enough for one task → `/team:build` directly.
- A multi-module structural decision or a new NFR is needed → `/team:architect` first.
- The question is a business rule → `NEEDS_ANSWER` back to team-leader; never guess it in the design.

## Discover the stack first
1. Read `.team/profile.json`: `structure.*` (`src`, `tests`, `allowed_new_file_roots`), `naming.*` (file, class, function, `test_file`), `protected_paths`, `cmd.test_one` (only the `{file}` placeholder varies), `cmd.migrate`, `ui`.
2. Explore (concrete questions): the error style in use, the pagination style, where permissions are checked, how configuration is read, the existing test layout, the files and data that will be touched. Check the cache first: `bash "<kit>/scripts/explore-cache.sh" <directory>`; `HIT` → read the cache file.
3. Read `docs/team/architecture.md` / `arch-impact.md` and the relevant ADRs (size L): an ADR's constraints are law for the design.

## Inputs and preconditions
- `docs/team/features/<ID>/spec.md` (criteria AC-n, NFRs, DoD); `research.md` if present; `arch-impact.md`/`architecture.md` for size L or a playbook that includes architect.
- `--short` (refactor): `intake.md` + the debt item in `docs/team/debt.md` is enough; the refactor chain has no spec (ADJ-26).
- Check: `python3 "<kit>/scripts/team.py" status <ID>`; G1 on but not approved, or an architecture exists and G2 is not approved → stop.

## Process
1. **Record position.** Write `.team/current.json` {feature, stage: "design", agent: "designer", started_at}.
2. **Assumptions before writing.** List what you are assuming. A business assumption → write `questions.md` (2–4 options, recommendation, consequences) and return `NEEDS_ANSWER`. A technical assumption in decide mode → `## Assumptions decided by the team` (what was chosen / why / alternatives / how to fix if wrong).
3. **Section 1 Context:** the problem, in/out of scope (copied from the spec), the ADR IDs that must be obeyed.
4. **Section 3 Contracts (written before sections 2 and 4):** for each public entry point: input, output, errors (one style, following the existing code), version. Mark which behaviors are contract. To change, prefer adding an optional field; breaking → a new version + a migration guide (STD-DOC-7).
5. **Section 2 Data:** entities, fields, constraints, indexes chosen from the access patterns; ownership per the ADR. No "just in case" fields (STD-DESIGN-5).
6. **Section 4 Flow:** the happy path and the error path for every criterion; every outbound call has a timeout (STD-ERR-5) and an outcome of success / failure / unknown.
7. **Integration (integration playbook or any external API call):** the idempotency key derived from intent (not per attempt); claim it atomically with a unique constraint (not check-then-insert); same key with a different payload → an explicit error; a policy for an in-flight duplicate; key retention ≥ the longest retry path. Details: `${CLAUDE_SKILL_DIR}/references/contracts.md`.
8. **Section 5 Permissions:** validate input at the boundary, check permissions server side (STD-SEC-4); treat third-party responses as untrusted.
9. **Section 6 Migration and rollback:** when there is a `cmd.migrate` and data changes → up, down, and row-count reconciliation (STD-OPS-2, STD-OPS-3); large tables in batches; rollback trigger conditions and success criteria. designer only plans; dev runs it on a copy, qa runs up/down/up. No data change → write "none".
10. **Observability (STD-OPS-5):** one log or metric for each important new path, with no sensitive data — so `/team:release` can prove the feature runs in prod.
11. **Section 7 Touchpoints:** real paths, "edit" (Glob finds the file) or "new" (under `structure.allowed_new_file_roots`); test files per `structure.tests` and `naming.test_file`. Machine checkpoint: paste each new path next to the allowed root it matches; no path may match `protected_paths`. The notes column says why the file is touched — never a task number.
12. **Section 8 Test plan:** every AC-n and every NFR with a "how to check" → ≥ 1 row `criterion | test file::name | kind | error/boundary path`. A criterion with inputs → at least one boundary or error row (qa will run it). Commands are named only by slot (`cmd.test_one`), never as typed stack commands.
13. **`--short` (refactor):** sections 1, 7, 8 and the "How to prove behavior is unchanged" section: `cmd.test` before == after (test count and test names), lint/typecheck clean, a single kind of cleanup. Where no test covers the code → a characterization test is the first task, before any change.
14. **Self-check (decision point).** Every section cites the ADR IDs it obeys. The design cannot meet the criteria while keeping an ADR → `DESIGN_CONFLICT` back to team-leader; never quietly change the architecture (STD-DESIGN-2).
15. **Write** `docs/team/features/<ID>/design.md` from `<kit>/templates/artifacts/design.md` (Write). Write prose in `output_language` with the template from the matching language folder (handbook: Artifact language); the `## 7. Touchpoints` heading stays English.
16. **Return** to team-leader in ≤ 10 lines, first line `designer -> team-leader | <ID> | DESIGNED` (or `DESIGN_CONFLICT`, `NEEDS_ANSWER`).

## Outputs
- `docs/team/features/<ID>/design.md` (8 sections; `--short`: 1, 7, 8 + proof that behavior is unchanged); `questions.md` when a question must be asked.
- Example return message:
  ```
  designer -> team-leader | FEAT-014 | DESIGNED
  File: docs/team/features/FEAT-014/design.md (8 sections; obeys ADR-003, ADR-007)
  Touchpoints: 6 (4 edit, 2 new under src/auth/, tests/auth/ — within allowed_new_file_roots); 0 in protected_paths
  Contract: POST /otp/verify adds error code OTP_EXPIRED (additive, backward compatible)
  Data: +1 column otp_expires_at; migration 0007 up/down + row-count reconciliation
  Test plan: 5/5 AC have tests, 3 with error/boundary paths
  Assumptions decided: 1 (TTL read from config); business questions: 0. G2b off → Next: /team:plan FEAT-014
  ```

## Common rationalizations
| Thought | Correct action |
|---|---|
| "Write the flow first, the API later" | Contracts (section 3) before flow; the flow is shaped by what the entry point promises. |
| "Any error style will do" | One style, following the existing code (Explore). |
| "Undocumented behavior, nobody relies on it" | List observable behavior as contract. |
| "Add a parallel API version to be safe" | Add an optional field; a new version only for a break. |
| "Retry is safe because there's an idempotency header" | The key must be stored atomically; design the in-flight duplicate case too. |
| "Dev will find the files" | Real paths in the touchpoints. |
| "The migration is simple, no rollback needed" | Always a down path and a reconciliation. |
| "The business rule is surely like this" | `NEEDS_ANSWER`, never guess. |
| "Add a spare field for later" | Only what the spec needs. |

## Red flags
- A public entry point with no error list.
- A touchpoint that does not exist and is not under an allowed root; a touchpoint matching `protected_paths`.
- An AC with no test row; a test row that names a command instead of a test file.
- A migration without a down direction or a reconciliation.
- Check-then-insert idempotency.
- The design copies the architecture instead of citing ADR IDs; the design contains task numbers.
- A business rule decided in the design.

## Verification
- [ ] All sections present (paste `grep -c '^## [1-8]\.' design.md`), or 3 sections + the proof when `--short`.
- [ ] The AC-n list from the spec and from the test plan are pasted and match.
- [ ] Each new path is pasted next to its allowed root; the line "0 in protected_paths".
- [ ] The Explore summary (error, permission and test conventions) is pasted as the basis.
- [ ] A breaking contract has a version + a migration line, or "no breaking change" is written.

## See also
- `${CLAUDE_SKILL_DIR}/references/contracts.md` — contracts, errors, idempotency, batched migration, test-plan row template. Open it at steps 4, 7, 9, 12.
- Agent `designer`; `<kit>/templates/artifacts/design.md`.
- `/team:architect` (before, size L), `/team:plan` (after), `/team:clean` (refactor).
- `handbook/STD.md`: STD-DESIGN-1, STD-DESIGN-3, STD-DESIGN-5, STD-ERR-5, STD-SEC-4, STD-OPS-2, STD-OPS-3, STD-OPS-5.
