---
name: using-team
description: Use when starting any non-trivial work in a project that has the team, before acting or asking a clarifying question: check for a matching skill and playbook.
---

# Use the right skill before doing it yourself

## Overview
The team works from `/team:*` skills and playbooks, not from memory. This skill is preloaded for team-leader and tech-lead; **other subagents do not rediscover skills**, they use only the skill they were given.

## Process
1. Before any non-trivial work, even before Explore, classify it:
   a question → answer it yourself (progress → `/team:status`), no intake, no agent; a change → `/team:intake` (trivial → playbook quick, one dev); repo without a profile → `/team:takeover`; spec needed → `/team:analyze`; change to an approved spec → `/team:analyze --amend`; spec/design exists → `/team:plan`; tasks exist → `/team:build`.
2. List the temp skills in `.claude/skills/` (see `docs/team/skills-registry.md`). Priority: the human's words > kit process skills > temp skills > default behavior.
3. If `<kit>/workflows/` has a playbook for this kind of work (`<kit>` = contents of `.team/plugin_root`) → follow its chain; skills govern the detailed steps. If they disagree → follow the skill and report it with `/team:feedback`.
4. Several skills match → run them one after another and record the whole chain; never blend two processes.
5. Write one journal line in `docs/team/journal/<ID>.md` (Write) BEFORE editing the first artifact: which skill/playbook you chose and why.
6. No skill matches → write "no matching skill" + the closest skill you ruled out + the reason; if the work will recur → propose `/team:make-skill`.

## Common rationalizations
| Thought | Correct action |
|---|---|
| "Let me read the repo for context first" | Skills say how to explore; check them first, then Explore. |
| "I remember this skill" | Skills change; read the current version. |
| "Do it now, journal later" | Write the line before the first edit; "later" means never. |
| "Two skills look alike, merge them" | Run one, then chain the other. |
| "A question, so open an intake to be safe" | Answer it yourself; intake is only for a change the human asked for. |
| "I'm a subagent, so I should survey every skill" | Use the skill you were given; discovery is team-leader's job. |

## Verification
- The journal has a line naming `/team:<skill>` or a playbook, placed before the first artifact edit.
- The skill named exists (`skills/<name>/` or `.claude/skills/<name>/`).
- "No matching skill" always comes with the closest skill ruled out and the reason.
