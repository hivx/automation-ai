Feature: <ID>
Stage: analyze
Author-agent: analyst
Date: <YYYY-MM-DD>
Approved-by:
<!-- Gate: the approver fills in the line above as `Approved-by: <name> <YYYY-MM-DD>`. Leave it empty when there is no gate. -->

# Spec <ID> — <title>

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
| ID | Criterion (measurable) | How to check |
|---|---|---|
| AC-1 | <...> | <command or step with output> |

## Assumptions decided by the team
- <assumption> — because <reason>; if wrong, <how to fix>

## Definition of Done
- [ ] Every AC passes, output pasted into acceptance.md
- [ ] As-Built written (asbuilt.md) — after G4, `/team:asbuilt`
- [ ] README/user docs updated if behavior changed — after G4, `/team:asbuilt`
- [ ] CHANGELOG entry — after G4, `/team:asbuilt`
- [ ] CI green

## Amendment <n> (<YYYY-MM-DD>)
<only with --amend: what changed; criteria marked [changed]>
