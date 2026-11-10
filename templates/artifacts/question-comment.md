Feature: <ID>
Stage: analyze
Author-agent: team-leader
Date: <YYYY-MM-DD>
Approved-by:
<!-- Gate: the approver fills in the line above as `Approved-by: <name> <YYYY-MM-DD>`. Leave it empty when there is no gate. -->

**The `team` crew needs your answers before continuing `<ID>`** (ask mode, round <n>/2)

1. <question>
   - a) <option> — consequence: <...>
   - b) <option> — consequence: <...>
   - Recommendation: **b** because <...>
2. <question>
   - a) <...>
   - b) <...>
   - Recommendation: **a** because <...>

Reply with one comment, one line per question, for example:
```
A1: option b
A2: option a — add a note if needed
```
The `team:needs-answer` label is removed once the team has all the answers.
