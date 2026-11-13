---
name: retro
description: Use when a retrospective is due, after a feature with a lot of rework, when feedback crosses its threshold twice, or when the scorecard shows an anomaly, to find the team's bottlenecks with evidence and propose agent/skill fixes awaiting the human's approval.
argument-hint: "[--since <YYYY-MM-DD>] [--decide]"
disable-model-invocation: true
context: fork
agent: team:coach
background: false
allowed-tools: Bash(python3 *) Bash(cat *) Bash(jq *) Bash(ls *)
---

# Evidence-based retrospective

## Overview
This skill finds at most three bottlenecks of the TEAM — agents, skills, configuration — backed by metrics and journal entries, diagnoses each against 5 causes (prompt · model/effort · input · profile/config · task size), and writes a safe fix proposal: a complete overlay + eval + canary + rollback plan, waiting for the human's approval. It runs in the `coach` context (fork): Bash is read-only, it calls no other role, and it never applies a change itself. coach DESIGNS the eval but cannot run it; the human or the kit maintainer runs `evals/run-eval.sh`.

Every finding has a source (a jsonl line, a journal line, `file:line`); without a source, drop it. The report must tell "checked and clean" apart from "could not check". Never blame an agent: the target is always one of the 5 causes. Example: reviewer hitting `maxTurns` on two features is traced to `design.md` missing its touchpoints (input), not to the reviewer's prompt.

`$ARGUMENTS`: `--since <YYYY-MM-DD>` (default: since the previous retro, or 14 days); `--decide` for scheduled runs with nobody watching. `<kit>` = the content of `.team/plugin_root`.

## When to use (and when not)
Use when:
- A retro is due (the `weekly-retro` batch), or at the end of a release milestone.
- A feature exceeded `limits.max_rework`; `feedback.jsonl` crossed its threshold twice; `measure.py` reports an anomaly.
- The canary of an applied proposal needs evaluating (keep / rollback / replace / remove).

Do not use when:
- You are looking for defects in the kit itself (bypassable hooks, mismatched names) → `/team:audit-kit`.
- You want an agent/skill fixed immediately → there is no shortcut: propose here, the human approves.
- No run has happened since the start date → do the work first.

## Discover the stack first
1. Read `.team/config.json`: `limits.max_agents_per_feature`, `limits.max_rework`, `limits.max_temp_skills`, `models`, `memory.*`.
2. Metric sources: `docs/team/metrics/runs.jsonl`, `feedback.jsonl`, `scorecard.json`, `sessions.jsonl`; journals `docs/team/journal/*.md`; earlier retros and proposals in `docs/team/retro/`, `docs/team/proposals/`; `docs/team/skills-registry.md`.
3. `python3 "<kit>/scripts/measure.py" --help`: the metrics available. The scorecard `result` field is guessed from the text of the last message (K-18) → metrics based on it are labelled "low confidence". Tokens exist only when run with `--logs`; otherwise write "not measured".

## Inputs and preconditions
- At least one line in `runs.jsonl` or `feedback.jsonl` after the start date. None → `NEEDS_CONTEXT` (missing metrics); never write an empty retro.
- Check: `python3 "<kit>/scripts/team.py" status` (which features fall in the period, and their sizes).

## Process
1. **Record position and skeleton.** Write `.team/current.json` {feature: "retro", stage: "retro", agent: "coach", started_at}. Write the skeleton of `docs/team/retro/<date>.md` from `<kit>/templates/artifacts/retro.md` immediately; already present (a re-run) → read it, reconcile it with the current metrics (the new metrics win), and continue from the first empty section. Write prose in `output_language` with the template from the matching language folder (handbook: Artifact language).
2. **List the sources.** For each source: the number of lines in the period, which features. A missing source → a line "not checked: missing <source>" and a narrower conclusion.
3. **Quantify.** `python3 "<kit>/scripts/measure.py" --since <date>`; paste the output: efficiency scores, trends, anomalies, attention ranking. Refresh `scorecard.json` when needed: `python3 "<kit>/scripts/team.py" scorecard`.
4. **Follow up the previous retro.** For each earlier proposal in `docs/team/proposals/*/`: approved or not (`Approved-by:`), canary run or not (journals of size S jobs), result keep/rollback/replace/remove — with a source; nothing found → "no evidence found" (which is different from "not done").
5. **Qualitative pass.** Read the journals of the features in the period; tie each candidate bottleneck to a metric line + a journal line. Findings from Explore or another agent count as unchecked: reopen the original source before relying on them.
6. **Minimum-sample rule (decision point, K-38).** Propose only for ≥ 2 occurrences across ≥ 2 features, or a `measure.py` trend/anomaly over ≥ 3 runs of the same subject and size. Anything less — including a single breach of a config cap — goes under `## Watch list`, with no proposal file. Each proposal records the number of features, the number of runs, and the confidence.
7. **Pick ≤ 3 bottlenecks.** Each gets two decisions: this time (propose / defer — watch / accept, recorded so the next retro does not raise it again) and prevention (which of the 5 causes).
8. **Diagnose the 5 causes.** A table where each cell cites a source or says "unclear". Input and task size are often the real cause; do not default to the prompt.
9. **Propose.** Write `docs/team/proposals/<date>/<agent-or-skill>.md` from `<kit>/templates/artifacts/proposal.md`: the evidence, the 5-cause table, the COMPLETE content of the overlay file (first line `# Overlay from retro <date>: <reason>`, plus the version), a fix form that matches the failure kind (a rationalization table for a skipped step, a template field for a missing part, a formula for a wrong shape, a rule tied to an observable condition), the eval, the canary, the rollback. The overlay body is AI-facing, so write it in English whatever `output_language` is. Eval and canary details: `${CLAUDE_SKILL_DIR}/references/proposal-eval.md`.
10. **An eval that discriminates.** ≥ 3 scenarios in the format of `evals/<skill>/scenarios.md`; at least one check that the current version FAILS and the proposed version passes; one control scenario that does not change; a check that passes on both versions is marked "does not discriminate". State who runs it (`evals/run-eval.sh`, the human/the kit maintainer).
11. **Cross-check the configuration.** Over-calling: the number of ROLES team-leader called itself per feature (including fork skills; not counting dev/reviewer called by tech-lead, K-15) against `max_agents_per_feature[size]`. A level-1 STD rule violated ≥ 2 times → propose raising its level.
12. **Project context.** `python3 "<kit>/scripts/check-claude-md.py"` (read-only); paste the summary line. A project fact the team rediscovered or got wrong in ≥ 2 features (the same Grep hunt in journals, the same convention flagged in `review-NN`, a rework caused by a trap) is an "input" cause whose fix is a CLAUDE.md line, not an overlay: write the exact line (add / fix / remove, section, source) under `## CLAUDE.md` in the retro; writer applies it at the next `/team:asbuilt`. A problem from the check (a stale path, over budget) goes there too.
13. **Review the registry.** From `skills-registry.md`: a `temp` entry unused for > 30 days → propose `retired`; a stable `temp` → `project` (the human approves); the number of `temp` entries against `max_temp_skills`. coach does not write the registry: this is a proposal for team-leader.
14. **Assumptions (`--decide`).** Record every assumption (the period chosen, the features counted, the confidence labels) under `## Assumptions`.
15. **Finish** `docs/team/retro/<date>.md`; memory: dated conclusions, no sensitive data; return to team-leader in ≤ 10 lines, first line `coach -> team-leader | retro <date> | <N> proposals, <M> watched`.

## Outputs
- `docs/team/retro/<date>.md`; `docs/team/proposals/<date>/*.md`; coach's memory.
- Example return message:
  ```
  coach -> team-leader | retro 2026-11-16 | 1 proposal, 2 watched
  measure.py --since 2026-11-09: 14 runs; anomaly: reviewer turns 2.6 MAD (size M)
  Bottleneck: reviewer hit maxTurns 3/5 times on FEAT-021, FEAT-024 (journal FEAT-021 line 4)
  Cause: input (design.md missing touchpoints) — not the prompt
  Proposal: proposals/2026-11-16/designer.md (overlay v2, 3 scenarios, 1 check fails on the current version; canary 3 size S jobs)
  Watched: analyst slow once (FEAT-024); max_agents S exceeded once (FEAT-022)
  Previous retro: config-max-agents, no Approved-by found. Next: the human reads retro/2026-11-16.md
  ```

## Common rationalizations
| Thought | Correct action |
|---|---|
| "One slow feature is enough for a proposal" | ≥ 2 occurrences or a trend; fewer → watch list (K-38). |
| "Edit the agent file directly, it is faster" | Propose an overlay; the human approves. |
| "The eval only needs the happy path" | ≥ 3 scenarios, a check the current version fails, and a control. |
| "No tokens/logs, so skip it" | Write "not measured" and narrow the conclusion. |
| "The old proposal was surely applied" | Look for `Approved-by` and the canary; none → "no evidence found". |
| "The cause is the prompt" | Fill all 5 cells with sources; input and size are frequent culprits. |
| "Add a MUST to the skill and we are done" | Choose the fix form by the failure kind. |
| "The scorecard result is the truth" | `result` is guessed from text; label the confidence. |
| "Run the eval to be sure" | coach cannot run it; write the scenarios and say who runs them. |

## Red flags
- A proposal without the number of features, the number of runs, and the confidence.
- An evidence cell with no path or source line number.
- A proposal with < 3 eval scenarios, or no check that the current version fails.
- An overlay missing the `# Overlay from retro <date>: <reason>` line or the version.
- coach writing outside `docs/team/retro/**`, `docs/team/proposals/**`, `.team/current.json`, `scorecard.json`, memory.
- More than 3 bottlenecks; no follow-up section for the previous retro.
- A retro without the pasted `measure.py` output.

## Verification
- [ ] The output of `measure.py --since …` is pasted.
- [ ] `ls docs/team/proposals/<date>/` matches the list of proposals in the retro.
- [ ] Every proposal has the overlay line, a sourced 5-cause table, ≥ 3 eval scenarios, a canary, a rollback.
- [ ] The previous-retro follow-up table and the over-calling table (counted per K-15) are in the retro.
- [ ] The source table shows which sources were checked and which were missing.
- [ ] `## CLAUDE.md` holds the `check-claude-md.py` summary line and a source for every line it asks to add, fix or remove.

## See also
- `${CLAUDE_SKILL_DIR}/references/proposal-eval.md` — the discriminating eval template, the canary, the keep/rollback/replace/remove criteria. Open it at steps 9–10.
- Agent `coach`; `<kit>/templates/artifacts/{retro,proposal}.md`; `scripts/measure.py`.
- `/team:audit-kit` (kit defects); `workflows/retro.md`, `workflows/batch/weekly-retro.md`; `docs/07-improvement.md`.
