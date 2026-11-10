Feature: <ID>
Stage: any
Author-agent: team-leader
Date: <YYYY-MM-DD>
Approved-by:
<!-- Gate: the approver fills in the line above as `Approved-by: <name> <YYYY-MM-DD>`. Leave it empty when there is no gate. -->

# Project temp skills and agents

Active cap (`temp` skills + agents): `limits.max_temp_skills`. `temp` unused for 30 days → `retired`; stable and approved by the human → `project`; `project` used in ≥ 2 projects → propose moving it into the kit.
team-leader updates `last used` and `runs` in the same journal write when handing off work that uses the skill/agent; retro reviews them and proposes status changes.

| name | kind skill/agent | status temp/project/retired | need (evidence) | created | last used | runs | model (agent) | test cases |
|---|---|---|---|---|---|---|---|---|
| <name> | skill | temp | <one sentence> (<journal/review that led to it>) | <YYYY-MM-DD> | <YYYY-MM-DD> | 0 | — | .claude/skills/<name>/references/tests.md |
