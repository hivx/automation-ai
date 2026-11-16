Feature: <ID>
Stage: analyze
Author-agent: analyst
Date: <YYYY-MM-DD>
Approved-by:
<!-- Gate: the approver fills in the line above as `Approved-by: <name> <YYYY-MM-DD>`. Leave it empty when there is no gate. -->

# Spec <ID> — <title>

## Read-back
<!-- ≤ 5 lines in the requester's words, no IDs. The team-leader shows this block to the human in every mode. -->
- You asked: "<the request, quoted>"
- You will see: <where you work (screen, ticket, command) → what you do → what happens>
- Switched on: <yes / off because you asked for a switch, or because <risk>>
- Not included: <the biggest non-goal>
- Team additions (not built unless you pick them): <… or none>

## Goal
<why we do it; value for whom>

## Users
<who uses it, in which situation>

## Scope
- In: <...>
- Out: <...>

## Data
<entities, fields, volume; sensitive data>

## Interface / integration
<API, screens, external systems>

## NFR
| ID | Requirement | Measured by |
|---|---|---|
| NFR-1 | <...> | <...> |

## Acceptance criteria
<!-- Every criterion serves the ask: "From" quotes the request, a source line or an answer. Caps: S 5, M 12, L 24. -->
| ID | Criterion (measurable) | From | How to check |
|---|---|---|---|
| AC-1 | <...> | "<request words>" | <command or step with output> |

## Assumptions decided by the team
- <assumption> — because <reason>; if wrong, <how to fix>

## Definition of Done
- [ ] Every AC passes, output pasted into acceptance.md
- [ ] Tried like the requester: the feature is switched on and its main flow runs on a running instance (verify: Try it)
- [ ] As-Built written (asbuilt.md) — after G4, `/team:asbuilt`
- [ ] README/user docs updated if behavior changed — after G4, `/team:asbuilt`
- [ ] CHANGELOG entry — after G4, `/team:asbuilt`
- [ ] CI green

## Amendment <n> (<YYYY-MM-DD>)
<only with --amend, in this file (never a separate addendum file): what changed; criteria marked [changed]>
