# CLAUDE.md — repo of the `automation-ai` kit (plugin `team`)

This is the repo of the KIT, not a project that uses the kit. Specification: `SPEC.md` (do not edit). Approved deviations from SPEC: `docs/00-overview.md`, section "Approved adjustments (relative to SPEC)".

## Checks before reporting done
- `scripts/validate.sh` — must end with `0 fail`. From P4 on, use `scripts/validate.sh --strict`.
- `claude plugin validate .` — plugin manifest + marketplace.
- Paste the real output into the report. Never say "done" without output.
- The owner's requests are logged in section 9 of `GUIDE-VI.md`; every session reads that section before starting work.

## Rules without exceptions
1. A process change is ONE change everywhere at once: docs + skill/agent + hook/template. Never let them drift apart.
2. Never hard-code stack commands (test, build, lint...) in agents/, skills/, hooks/, scripts/. Reference only the `cmd.*` slots of `.team/profile.json`.
3. Names must match everywhere: docs ↔ agents ↔ skills ↔ templates ↔ scripts. When you rename, grep and fix every occurrence.
4. Three language zones. Zone 1, AI-facing (agents, skills, references, handbook, workflows, templates, scripts, docs/, evals/, this file, README.md): English. Zone 2, owner-facing: Vietnamese, only in `GUIDE-VI.md`. Zone 3, artifacts written inside a project: prose follows `config.output_language`. The anchors listed in `scripts/anchors.txt` are never translated in any zone. Identifiers are always English: file/directory names, JSON keys, skill/agent names, STD codes, branches, scripts, CLI flags, frontmatter keys. Check: `python3 scripts/check-lang.py`.
5. Use only bash, python3 (stdlib), jq, git, gh (optional). No new dependencies.
6. Quality bar (P7): always-loaded skills ≤ 400 words, 4 sections (Overview, Process, Common rationalizations, Verification); other skills 1,200–2,500 words, 10 sections (Overview, When to use (and when not), Discover the stack first, Inputs and preconditions, Process, Outputs, Common rationalizations, Red flags, Verification, See also); agents 600–1,200 words, 10 sections (1. Identity … 10. When to stop and escalate). Configuration: `scripts/skill-budgets.txt`, `skill-sections.txt`, `agent-sections.txt`; measurement: `scripts/kit-metrics.py`; items below the bar live in `scripts/quality-backlog.txt` (it may only shrink). Move long material into `references/`.
7. No `@file` in skills/agents. Inside the plugin, point to files with `${CLAUDE_PLUGIN_ROOT}`.
8. A skill description starts with "Use when", is < 500 characters, and does not summarize the process.
9. Do not write an MCP server, and do not create any plugin other than `team`.
10. Never write a piece of knowledge twice: skills/rules/agents are the source of truth for the AI; `docs/` holds only the overview, installation, the map from tasks to skills, and the design rationale.

## Layout
- `.claude-plugin/` manifest · `agents/` 13 roles · `skills/<name>/SKILL.md` 26 skills · `workflows/` 17 playbooks + `batch/`
- `hooks/hooks.json` · `scripts/` · `handbook/` · `profiles/` · `templates/{artifacts,project,schemas}/` · `evals/<skill>/` · `docs/`

## Add a role (agent)
1. Create `agents/<role>.md`: frontmatter `name` = file name, `description` ("Delegate when…"), `tools`, `model`, `effort`, `maxTurns`; body follows the 10 sections of `scripts/agent-sections.txt` (with an example return message and a 4-line stop message).
2. Plugin agents ignore `hooks`, `permissionMode`, `mcpServers`: put path/command limits in the role-policy table of the hook.
3. Update `docs/02-team.md`, `handbook/who-calls-whom.md`, the sample `models` in config, and the related playbooks.
4. Add the role's Vietnamese one-liner to `scripts/vi-strings.json` (the same applies to every new skill); a missing line fails validate.
5. Run `scripts/validate.sh`.

## Add a stage
1. Create the skill `skills/<stage>/SKILL.md` and the artifact template in `templates/artifacts/`; add the skill's Vietnamese one-liner to `scripts/vi-strings.json`.
2. Add the state rule to `scripts/team.py`; add the gate (if any) to `templates/project/team/config.json`.
3. Update `docs/01-process.md`, the playbook in `workflows/`, `docs/guides/want-x-type-y.md`.
4. Run `scripts/validate.sh`.

## Try the kit on a sample project
```
cd /path/to/sample-project
claude --plugin-dir /path/to/automation-ai
```
In that session type `/team:takeover`. Never run the kit inside this repo.
