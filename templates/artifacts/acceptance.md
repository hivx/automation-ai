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

## Try it
<!-- On a running instance, done the way the requester will do it (verify step "Try it"). Fails → Verdict: rework. -->
- Instance: <site / URL / command>, commit <sha>, feature switched on: <yes / how>
- Walk-through: <what was done → what happened (output, record created, screenshot path)>
- For you (≤ 3 steps): 1. <…> 2. <…> 3. <…>

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
