# 07 — Self-improvement

Source of truth: `SPEC.md` §9 (Journal & self-improvement, Temp skills). Related skills: `/team:retro`, `/team:feedback`, `/team:audit-kit`, `/team:make-skill`, `/team:make-agent`.

## Journal (qualitative)
`docs/team/journal/<feature>.md`. After each handoff, team-leader or tech-lead writes 3–5 lines:
- who it was handed to, and what;
- the result, time taken / number of rounds;
- a remark on the agent/skill: good / slow / wrong + a first guess at the cause;
- an improvement idea.

Template: `templates/artifacts/journal-entry.md`. Cap: `journal.max_lines_per_entry` in the config.

## Scorecard (quantitative)
Per agent/skill: number of calls, turns, time, rework/rejections, STD violations caused, tokens (from Claude Code's local logs), number of times the human had to step in. Compared with the median of work of the same size. The SubagentStop hook writes to `docs/team/metrics/`.

`scripts/measure.py` runs periodically, without an LLM: efficiency score, trends, anomalies, an attention ranking → handed to coach and the journal. Human feedback: `docs/team/metrics/feedback.jsonl`; an alert after 2 threshold breaches. Over-calling indicator: agents called per feature versus `max_agents_per_feature`.

## The coach loop
1. Read the scorecard + journal → find the bottlenecks.
2. Diagnose among 5 causes, with evidence: prompt · model/effort · input (a defect from an earlier stage) · profile/config · task size.
3. Write a proposal in `docs/team/proposals/`: a diff in overlay form (`# Overlay from retro <date>: <reason>`, versioned) + a before/after eval.
4. The human approves → canary on N size-S pieces of work.
5. Keep / roll back / replace / drop.

coach never applies a change itself and never edits the kit's originals.

## Temp skills and agents
Create them only when needed; nothing is pre-created at install time.
1. At intake/plan, team-leader sees that a task needs expertise the kit does not have, or that it will recur.
2. Check what already exists: the kit, the project's `.claude/skills/`, plugins.
3. Hand off `/team:make-skill` (researcher first gathers examples and in-repo docs if needed).
4. The skill lives in `.claude/skills/<name>/`: purpose, when to use, inputs/outputs, steps, tools, reference examples, done criteria, 1–2 test cases; label `temp`; recorded in `docs/team/skills-registry.md`.
5. Hand it to a subagent as "use /<name> for step X"; use it right away; record it in the journal.
6. Follow-up: `temp` → `project` (stable, approved by the human) → proposed for the kit (≥ 2 projects) or `retired` (unused for 30 days). There is a cap on the number of active temp skills.

`/team:make-agent` follows the same lifecycle. Defects of the kit itself go into `docs/team/kit-issues.md`.

## Measurement scripts
| Job | Command |
|---|---|
| Record one agent run | automatic: SubagentStop hook → `scripts/scorecard.sh` |
| Record the result of one stage | `scripts/log-run.sh --skill <x> --result <y>` (called by the `run` skill) |
| Aggregate per agent/skill/size | `python3 scripts/team.py metrics`; write `docs/team/metrics/scorecard.json` with `team.py scorecard` |
| Efficiency score, trends, anomalies, ranking | `python3 scripts/measure.py [--since <date>] [--logs ~/.claude/projects/<slug>/] [--json]` |

The efficiency-score weights sit at the top of `scripts/measure.py` (`WEIGHTS`). Tests: `scripts/tests/test_measure.py`.
