Feature: <ID>
Stage: plan
Author-agent: tech-lead
Date: <YYYY-MM-DD>
Approved-by:
<!-- Gate: the approver fills in the line above as `Approved-by: <name> <YYYY-MM-DD>`. Leave it empty when there is no gate. -->

# Plan <ID>

- Feature branch: `team/<ID>` from `<base_branch>`
- Tasks: <n>; max parallel: <limits.max_parallel_dev>

## Design (size M, no design.md; ≤ 40 lines)
- Contracts and schema changes: <endpoint / field / migration, exact names>
- Touchpoints: <file — what changes>
- Test per criterion: <AC-n → test file>

## Order
1. <task group, reason for the order>

## Parallel groups
- <T2, T3> (no shared files)

## Risks
| Risk | Signal | Response |
|---|---|---|

## Walking skeleton (size L)
<what T1 runs end to end>
