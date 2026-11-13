---
name: make-agent
description: Use when team-leader sees project-specific expertise large enough to need its own context, tool set or model, that no kit role can take on and that a temp skill would not cover.
argument-hint: "<name> \"<one-sentence need>\" [--evidence <journal|review|task>]"
allowed-tools: Bash(ls *) Bash(cat *) Bash(date *)
---

# Create a project temp agent

## Overview
This skill creates a temp agent in `.claude/agents/<name>.md` that follows the team's 10-section contract exactly — only when a temp skill is not enough because the work needs its own context, its own tool set or its own model (`handbook/tool-selection.md`, the "agent" row). A good example: a UI specialist that must have the design system preloaded and use the Playwright MCP that no role has. A bad example: a two-minute job, or a repeated step (that is a skill).

A temp agent is a worker with a contract: what it does, what it does not do, inputs, outputs, done criteria, tools, turn limit — not a persona. It does not ask the human (subagents have no `AskUserQuestion`), it does not call other roles (Explore only), and only team-leader calls it. The role-policy hook applies the default `_temp` limits to every agent carrying the `team: temp` marker; the frontmatter `tools` list is the other hard limit, so keep it minimal. Like every agent file, it is AI-facing and written in English: the 10 English section headings and a description that starts with "Delegate when".

The skill runs in the main session (team-leader may write `.claude/agents/**`, `docs/team/**`). `$ARGUMENTS`: the name (kebab-case, English), the need, the evidence. `<kit>` = the content of `.team/plugin_root`.

## When to use (and when not)
Use when:
- The work needs a tool that no role has (an MCP server already installed for the project, a special measuring tool).
- The work needs a large preloaded context (a design system, a protocol specification) that would flood the context of an existing role if loaded there.
- The work needs a different model from the role doing it because the cost of a mistake differs (for example, checking a legal contract needs opus while writer uses sonnet).

Do not use when:
- A temp skill is enough → `/team:make-skill`.
- One of the 13 roles can take it on (even with a temp skill added).
- The work is a one-off, or you only want "an agent to keep things tidy".
- tech-lead would need to call the agent: the hook lets tech-lead call only dev, reviewer and Explore — a temp agent is called by team-leader.

## Discover the stack first
1. Read `<kit>/handbook/tool-selection.md` from the first row: stop at the first row that matches; only the "agent" row is valid here.
2. Read the descriptions of the 13 roles in `<kit>/agents/*.md` and of `.claude/agents/*.md`; installed plugin agents.
3. Read `.team/config.json`: `limits.max_temp_skills` (shared by temp skills and temp agents), `models`.
4. Read `docs/team/skills-registry.md`: the number of active `temp` entries.
5. The tools it needs must really exist: an MCP server must already be installed for the project; if not → print the install command for the human, do not add an `mcpServers` configuration.

## Inputs and preconditions
- A one-sentence need + evidence + the reason a skill is not enough (context / tools / model — name which one and why).
- The temp cap is not reached; at the cap → refuse and propose `retired`.
- The name does not clash with any role, project agent or plugin agent.
- Interactive session: writing into `.claude/agents/` always needs the human's approval, and headless mode cannot grant it in advance (K-72). Headless → print the file content in the return message, status `NEEDS_ANSWER`.

## Process
1. **Check the reason for an agent.** Walk `tool-selection.md` from top to bottom; record the row where you stopped. Not the agent row → refuse and point the way (hook, script, rule, skill). Checkpoint: the stopping row is quoted in your notes.
2. **Match capabilities.** For each role that might take it on: quote its description line and say why it is not enough. A role is enough (even with a temp skill) → refuse and suggest `/team:make-skill`.
3. **Collect samples.** Agent → Explore: sample files, conventions, profile slots. External docs needed → researcher through team-leader.
4. **Choose the model by the shape of the work** (`SPEC-OVERRIDES.md` entry 2): haiku for mechanical work, sonnet for reading, analysis and documentation, opus for carrying out one concrete job whose mistakes are expensive, fable only for coordinating many tasks. Record the reason in the registry.
5. **Choose minimal tools.** No `AskUserQuestion`; `Agent` only when the body says explicitly that it calls Explore only; MCP tools by their full names. Never use `permissionMode`, `hooks` or `mcpServers` in the frontmatter.
6. **Write** `.claude/agents/<name>.md` from `${CLAUDE_SKILL_DIR}/references/agent-template.md`, in English: the description starts with "Delegate when", ≤ 300 characters; `skills` preloads the handbook (`team:handbook`; local install `team-handbook`); the 10 sections of `<kit>/scripts/agent-sections.txt`, with an example return message (first line `<name> -> team-leader | <ID> | <STATUS>`) and a 4-line stop message.
7. **Marker line** at the top of the body: `<!-- team: temp, created <YYYY-MM-DD>, need: <need>, evidence: <source>, why-agent: <…> -->`. The `team: temp` marker is what the hook uses to apply the `_temp` limits — without it the agent runs with no role limits.
8. **Test cases.** Write `docs/team/agents/<name>.tests.md` (NOT in `.claude/agents/`, where any `.md` may be loaded as an agent): 1–2 cases whose input is a handoff message of ≤ 10 lines, the expected result, and a check that tells right from wrong (for example, the first line of the return message has the right format).
9. **Machine checks.** `grep -c '^## [0-9]' .claude/agents/<name>.md` = 10; `wc -w` on the body; no forbidden key in the frontmatter. Paste the output.
10. **Register.** Edit `docs/team/skills-registry.md`: kind `agent`, status `temp`, need + evidence, model + reason, path to the test cases. Write the row's prose in `output_language` with the template from the matching language folder (handbook: Artifact language).
11. **Who calls it.** Record in the registry: "caller: team-leader". If tech-lead needs it during build → team-leader calls it between tasks, or proposes promoting it to a kit role (the human approves).
12. **Try it once** with case 1 on exactly the chosen model: the first line of the return message must have the right format; the agent can quote a line of the handbook (evidence that the handbook was loaded). Record the result in the journal; `runs` +1.

## Outputs
- `.claude/agents/<name>.md`; `docs/team/agents/<name>.tests.md`; a new row in `docs/team/skills-registry.md`; a journal line.
- Message to the human:
  ```
  make-agent ui-specialist | created (temp)
  Reason for an agent: own tool (Playwright MCP installed) + design-system context of 9,000 words; tool-selection stopped at the "agent" row
  Roles compared: dev (no Playwright, build context), qa (acceptance only) — not enough
  Files: ui-specialist.md in .claude/agents/ (10 sections, 780 words, sonnet); test cases in docs/team/agents/ (2 cases)
  Limits: role-policy _temp (read-only Bash + git + cmd.*, Explore only); no permissionMode/hooks keys
  Trial of case 1: first line "ui-specialist -> team-leader | FEAT-009 | DONE"; quoted handbook STD-TEST-1
  Next: team-leader hands FEAT-009 the UI check step, with the reason in the journal
  ```

## Common rationalizations
| Thought | Correct action |
|---|---|
| "A dedicated agent is tidier than a skill" | Walk all of `tool-selection.md`; an agent only when its own context/tools/model is needed, with evidence. |
| "Give it plenty of tools so it can manage" | Minimal tools; `tools` is a hard limit. |
| "Let the agent ask the human, it is faster" | No `AskUserQuestion`; `NEEDS_ANSWER` goes back to the caller. |
| "This agent can call dev and reviewer too" | Subagents do not call each other; Explore only. |
| "permissionMode: bypassPermissions so it is never asked" | Never; it removes the machine rules (P3). |
| "opus to be safe" | Choose by the cost of a mistake; record the reason in the registry. |
| "It does not need the handbook" | Preloading is mandatory; prove it with one trial run. |
| "Keep the test cases next to the agent, it is handy" | Put them in `docs/team/agents/`, never in `.claude/agents/`. |
| "tech-lead calls this agent during build" | role-policy flags it; team-leader calls it, or proposes promoting it to a role. |

## Red flags
- A description that does not start with "Delegate when", or is > 300 characters.
- `tools` contains `Agent` while the body does not restrict it to Explore; it contains `AskUserQuestion`.
- The frontmatter has `permissionMode`, `hooks` or `mcpServers`.
- No example return message or 4-line stop message; no `team: temp` marker.
- An agent for a one-off job; no registry row of kind `agent`.
- The test-case file sits in `.claude/agents/`.

## Verification
- [ ] The frontmatter is pasted: `name` = the file name, description "Delegate when", minimal `tools`, no forbidden keys.
- [ ] `grep -c '^## [0-9]'` = 10 and `wc -w` on the body are pasted.
- [ ] The marker line has `team: temp`, `evidence:`, `why-agent:`.
- [ ] `grep '<name>' docs/team/skills-registry.md`: kind agent, model + reason, caller.
- [ ] One trial of case 1: the first line of the return message has the right format, and the agent quoted the handbook.

## See also
- `${CLAUDE_SKILL_DIR}/references/agent-template.md` — the 10-section template, the `_temp` machine limits, where the test cases go. Open it at steps 6 and 8.
- `/team:make-skill`; `handbook/tool-selection.md`, `handbook/who-calls-whom.md`.
- `hooks/role-policy.json` (the `_temp` role); `<kit>/templates/artifacts/skills-registry.md`.
