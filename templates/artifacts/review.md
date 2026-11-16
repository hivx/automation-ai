Feature: <ID>
Stage: build
Author-agent: reviewer
Date: <YYYY-MM-DD>
Approved-by:
<!-- Gate: the approver fills in the line above as `Approved-by: <name> <YYYY-MM-DD>`. Leave it empty when there is no gate. -->

# Review NN — <ID> checkpoint <T<a>, T<b> [risk], F<k>, …>

- Diff: <`REVIEWED..team/<ID>` (every task and fix merged since the last review)>
- Open findings of the last review: <F-n ADDRESSED / NOT ADDRESSED, or none>
- Round: <1..max_rework>
- Verdict: <approve | request-changes | design-defect>

## Findings (blocker/major only)
| severity | STD | file:line | description | fix |
|---|---|---|---|---|
| blocker | STD-TEST-4 | <file:line> | <...> | <...> |

minor | — | — | <n> small points: <...> | dev's call

## Review checklist (10)
<1–10: pass / fail (STD code)>
