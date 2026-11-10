---
name: architect
description: Use when size-L work or a new project needs a system architecture, when a change touching several modules, contracts or NFRs needs an impact assessment, or when a design.md needs a three-sentence review of architectural fit.
argument-hint: "<ID> [system|impact|review]"
context: fork
agent: team:architect
background: false
allowed-tools: Bash(python3 *) Bash(cat *) Bash(ls *)
---

# Architecture and ADRs

## Overview
This skill settles the structural decisions that independently built parts could make differently and collide over — then records each decision as an ADR with a checkable constraint. It runs in the `architect` context (fork). architect does not write code, does not decide business rules, and does not go down to field or endpoint detail (that is designer's job).

The central test: a decision belongs at the architecture level only when (1) two parts built separately could choose differently and conflict, (2) the choice is not obvious, (3) there is a real trade-off. Missing one → write "left to the designer". This test guards against both under-design and over-design (STD-DESIGN-5). For example, "only billing writes the `invoices` table" passes all three when billing and notify both touch invoices; "use `created_at` rather than `createdAt`" fails the second, because `naming.*` already answers it.

Three modes: `system` (no architecture yet), `impact` (a running system), `review` (three sentences on one `design.md`). `$ARGUMENTS`: the `<ID>` and the mode. `<kit>` = the content of `.team/plugin_root`.

## When to use (and when not)
Use when:
- Size L (mandatory), playbook `new-project`, `integration`, a `change-request` touching several modules.
- A new NFR (performance, availability, security) that the existing architecture does not answer.
- team-leader needs an independent review of a `design.md` (`review`).

Do not use when:
- Size S, or size M contained in one module with no contract change → `/team:design` directly.
- The question is "which library supports X" → `/team:research` first; architect has no WebFetch.
- You want to change a business rule → analyst (`--amend`).

## Discover the stack first
1. Read `.team/profile.json`: `structure.*` (module roots), `structure.config`, `ci.*`, `deploy.*` (the operational envelope: environments, deploy units).
2. Read `docs/team/architecture.md`, Glob `docs/team/adr/ADR-*.md` (an `accepted` ADR is a binding constraint, read-only), `docs/team/assessment.md` (conventions measured from the code at takeover).
3. Explore: the real module boundaries, dependency direction, deploy units (build/CI config files). Containers come from how the system is actually deployed, not from logical grouping.
4. The project already has ADRs elsewhere (found by takeover T1) → read them as constraints and cite them in Context; do not renumber them, do not start a second numbering sequence.

## Inputs and preconditions
- `docs/team/features/<ID>/spec.md` with an NFR table (IDs NFR-n); `research.md` if present; `design.md` for `review`.
- Check: `python3 "<kit>/scripts/team.py" status <ID>`; G1 on but not approved → stop.
- Pick the mode: no `docs/team/architecture.md` yet → `system`; it exists → `impact`; called on a `design.md` → `review`. The assigned mode does not match the artifacts → `NEEDS_CONTEXT`.

## Process
1. **Record position.** Write `.team/current.json` {feature, stage: "architect", agent: "architect", started_at}.
2. **Read everything, inherit silently.** Spec (NFRs, scope), research, the architecture and accepted ADRs. Do not re-decide what an ADR has settled; to change it → a new superseding ADR (STD-DESIGN-2) and one line in `## Decision` of `arch-impact.md`.
3. **Reality first (running system).** Explore with concrete questions: which module owns which data, who calls whom, which deploy units exist. Paste the Explore summary as your basis. Ratify what the code already does before proposing anything new.
4. **Candidate decision list** from the spec + NFRs. Each candidate goes through the three-condition test (Overview). Passes → ADR. Fails → `## Left to the designer` with the reason. Details and examples: `${CLAUDE_SKILL_DIR}/references/decision-test.md`.
5. **NFR sweep.** Every NFR-n → a solution + ADR, or "dropped: reason". An NFR without a row is a defect.
6. **Dimension sweep.** Environments and deploy, data ownership (one owner per entity), state write paths, error/log/config conventions, authentication/authorization. Each dimension: "decided" / "left to the designer" / "open question". A whole dimension left silent is a finding.
7. **Technology.** Every library, service and version name must have a source in `research.md`. Missing → return `NEEDS_CONTEXT` with "need researcher: <question>" (team-leader calls researcher). Prefer technology the project already uses (STD-DEP-3).
8. **Write the artifacts.** Write prose in `output_language` with the template from the matching language folder (handbook: Artifact language).
   - `system`: Write `docs/team/architecture.md` from `<kit>/templates/artifacts/architecture.md` (context, components, data flow, NFR → solution, boundaries and dependencies, risks, Mermaid diagram). AND Write a short `docs/team/features/<ID>/arch-impact.md` (section `## System mode`: point to `architecture.md`, list the new ADRs). `team.py` reads the feature's G2 gate from `arch-impact.md`; without that file the feature is stuck at G2 (K-46).
   - `impact`: Write `docs/team/features/<ID>/arch-impact.md` from `<kit>/templates/artifacts/arch-impact.md`: modules touched, contracts changed (backward compatible or new version), NFRs affected, decisions, left to the designer, risks.
9. **Dependency diagram.** Mermaid, one direction, no cycles (STD-DESIGN-6); every edge labeled with its protocol; external systems shown explicitly.
10. **ADR.** The next number from Glob `docs/team/adr/ADR-*.md`. Write from `<kit>/templates/artifacts/adr.md`: context, decision, `## Constraints` (rules reviewer can check on a diff), options considered, consequences. Status `proposed`; it becomes `accepted` when G2 is approved. Never delete an ADR; superseding = a new ADR + editing only the status line of the old one.
11. **Self-challenge.** Try to construct two tasks that both obey every ADR and still conflict (two owners writing one table, two error styles). If you find one → tighten that ADR's constraint. Record "tried: …" in `## Risks`.
12. **`review` mode.** Exactly three sentences, each citing an ADR/NFR ID or a file: does it fit the architecture; the biggest risk; what must change. First line `REVIEW: ok` or `REVIEW: fix`. Do not rewrite the design.
13. **Return** to team-leader in ≤ 10 lines, first line `architect -> team-leader | <ID> | ARCHITECTED (<mode>)` (or `REVIEW: ok|fix`, `NEEDS_CONTEXT`, `NEEDS_ANSWER`).

## Outputs
- `system`: `docs/team/architecture.md` + `docs/team/features/<ID>/arch-impact.md`; `impact`: `arch-impact.md`; any mode with a decision: `docs/team/adr/ADR-NNN.md`.
- Example return message:
  ```
  architect -> team-leader | FEAT-030 | ARCHITECTED (impact)
  Files: docs/team/features/FEAT-030/arch-impact.md; new ADR: ADR-007 (email send queue); ADR-004 superseded
  Modules touched: 3 (billing, notify, api); contract: event invoice.paid v2, backward compatible
  NFR: 4/4 have a solution; NFR-3 (p95 < 300 ms) relies on research.md option B
  Left to the designer: payload format, retry interval
  Biggest risk: two consumers writing invoices → ADR-007 Constraint: only billing writes
  Gate: G2 awaiting Approved-by in arch-impact.md. Next: approve, then /team:design FEAT-030
  ```

## Common rationalizations
| Thought | Correct action |
|---|---|
| "It's obvious, no ADR needed" | Run the three-condition test; if it passes, write the ADR. |
| "Design for future scale" | Only the NFRs in the spec (STD-DESIGN-5); a speculative cache or queue is over-design. |
| "Use the standard architecture to be safe" | Ratify what the code already does; a change needs a reason traced to an NFR. |
| "I know the latest version of this library" | A source in `research.md`, or `NEEDS_CONTEXT`. |
| "The old ADR is wrong, just edit its content" | A new superseding ADR; the old one changes only its status line. |
| "Deployment is devops' problem" | The dimension sweep must record decided / left to the designer / open question. |
| "System mode only needs architecture.md" | Add the feature's `arch-impact.md` to carry the G2 gate. |
| "A thorough review must be long" | Exactly three sentences, with ADR/NFR IDs. |
| "I'll settle the business rule to finish" | `NEEDS_ANSWER` via team-leader. |

## Red flags
- An NFR in the spec has no row in the NFR → solution table.
- An ADR without options considered or without `## Constraints`.
- The Mermaid diagram has a dependency cycle.
- A technology name with no source in `research.md`.
- `system` mode without the feature's `arch-impact.md`.
- The content of an accepted ADR was edited.
- architect wrote design-level detail (field lists, endpoints, function names).

## Verification
- [ ] The NFR-n list from the spec and from the solution table are pasted and match.
- [ ] The Glob of new ADRs is pasted; each ADR has Context, Decision, Constraints, Options, Consequences.
- [ ] The Explore summary (modules, dependencies, deploy units) is pasted as the basis.
- [ ] `team.py status <ID>` after writing reports `architected` and waiting on G2 in `arch-impact.md` (when G2 is on).
- [ ] `review`: three sentences, each with an ADR/NFR ID or a file.

## See also
- `${CLAUDE_SKILL_DIR}/references/decision-test.md` — the threshold test, pass/fail examples, the list of dimensions to sweep. Open it at steps 4 and 6.
- Agent `architect`; `<kit>/templates/artifacts/{architecture,arch-impact,adr}.md`.
- `/team:research` (technology facts), `/team:design` (next step), `/team:analyze --amend` (business rules).
- `handbook/STD.md`: STD-DESIGN-2, STD-DESIGN-5, STD-DESIGN-6, STD-DOC-4, STD-DEP-3.
