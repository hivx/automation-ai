Feature: <ID>
Stage: retro
Author-agent: coach
Date: <YYYY-MM-DD>
Approved-by:
<!-- Gate: the approver fills in the line above as `Approved-by: <name> <YYYY-MM-DD>`. Leave it empty when there is no gate. -->

# Proposal: <agent-or-skill> (from retro <date>)

## Evidence
| Metric | Value | Median for the same size | Source |
|---|---|---|---|

Related journal lines: <excerpt>

## Five-cause diagnosis
| prompt | model/effort | input | profile/config | task size | Conclusion |
|---|---|---|---|---|---|

## Proposed change (overlay, full content)
```markdown
# Overlay from retro <date>: <reason>
# version: <n>
<entire content of the new file>
```

## Eval (baseline vs changed, ≥ 3 scenarios)
| # | Scenario | Expected | Checked by |
|---|---|---|---|

## Canary
- Run on <N> size-S jobs; keep when <...>; roll back when <...>; replace/drop when <...>

## Rollback
<restore the previous version: delete the overlay / restore the old file>
