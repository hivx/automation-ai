Feature: <ID>
Stage: verify
Author-agent: qa
Date: <YYYY-MM-DD>
Approved-by:
<!-- Gate: the approver fills in the line above as `Approved-by: <name> <YYYY-MM-DD>`. Leave it empty when there is no gate. -->

# Acceptance <ID>

Verdict: <accepted | rework | design-defect>

## Criteria
| criterion | command | output excerpt | verdict |
|---|---|---|---|
| AC-1 | `<command>` | `<real output>` | pass / fail |

## Common checks
- `cmd.test`: <output>
- `cmd.lint`: <output>
- `cmd.typecheck`: <output>
- New skip markers in the diff: <none | list>
- Migration up/down: <output | not applicable>

## Acceptance checklist (6)
<1–6: pass / fail (STD code)>

## DoD
- [ ] As-Built  - [ ] README/docs  - [ ] CHANGELOG
