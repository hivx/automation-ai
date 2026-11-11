# Temp agent template

A temp agent follows the same 10-section contract as the kit's agents (`<kit>/scripts/agent-sections.txt`), with a recommended body of 400–1,200 words. It is AI-facing, so it is written in English with the headings below, and its description starts with "Delegate when". It is a working contract, not a persona.

```markdown
---
name: <name>
description: Delegate when <situation>. (starts with "Delegate when", ≤ 300 characters, says WHEN to delegate)
tools: <minimal, bare tool names; no AskUserQuestion; Agent only when the body restricts it to Explore>
model: <haiku|sonnet|opus|fable — by the shape of the work (SPEC-OVERRIDES.md entry 2); the reason goes in the registry>
effort: <low|medium|high>
maxTurns: <n>
skills:
  - team:handbook   # local install: team-handbook
---

<!-- team: temp, created <YYYY-MM-DD>, need: <one-sentence need>, evidence: <source>, why-agent: <own context|tools|model: ...> -->

## 1. Identity
<who it is, who it reports to (team-leader), whom it may call (Explore only, or nobody); it does not ask the human — questions go back as NEEDS_ANSWER>

## 2. Inputs you must receive
<exactly what the caller must hand over: IDs, files, criteria; missing → ≤ 5 lines, NEEDS_CONTEXT, stop>

## 3. Discover the stack first
<profile slots to read; never guess commands>

## 4. Procedure
1. <step — tool — profile slot — checkpoint>

## 5. Outputs
<paths>
Example return message (≤ 10 lines, first line `<name> -> team-leader | <ID> | <STATUS>`):

## 6. Done criteria
<observable; paste the real command + output>

## 7. Never
- <≥ 4 lines, each with an STD code>

## 8. Common rationalizations
| Thought | Correct action |
|---|---|
| "<rationalization>" | <correct action> |  (≥ 6 rows)

## 9. Red flags
- <≥ 3 lines>

## 10. When to stop and escalate
<conditions; the 4-line stop message in a code block: STOP: … / Work: … / Who does what: … / Resume: …>
```

Test cases: `docs/team/agents/<name>.tests.md` (NEVER inside `.claude/agents/` — any `.md` there may be loaded as an agent).

Machine limits for temp agents: the role-policy hook applies the `_temp` role to every agent carrying the `team: temp` marker — it may write (protect.sh still blocks the forbidden zones), Bash is read-only + basic git + the `cmd.*` slots, and it may call Explore only. Never use the frontmatter keys `permissionMode`, `hooks`, `mcpServers` (project agents honour them, and they could override the kit's machine rules).
