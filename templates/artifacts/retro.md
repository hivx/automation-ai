Feature: <ID>
Stage: retro
Author-agent: coach
Date: <YYYY-MM-DD>
Approved-by:
<!-- Gate: the approver fills in the line above as `Approved-by: <name> <YYYY-MM-DD>`. Leave it empty when there is no gate. -->

# Retro <YYYY-MM-DD>

- Period: <from> → <to>; features: <list>
- Command: `measure.py --since <date>` (output below)

## Attention ranking
<table from measure.py>

## Bottlenecks (≤ 3)
| # | Subject | Evidence (metrics + journal lines) |
|---|---|---|

## Five-cause diagnosis
| Bottleneck | prompt | model/effort | input | profile/config | task size | Conclusion |
|---|---|---|---|---|---|---|

## Proposals
- `docs/team/proposals/<date>/<agent-or-skill>.md` — <summary>; awaiting the human's approval

## Excess agent calls
<agents per feature compared with max_agents_per_feature>
