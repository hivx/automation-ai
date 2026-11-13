# Parallel wave (`/team:run --all`)

A wave moves every feature that can move now, one agent per feature, at the same time. `team.py wave` decides who runs; the team-leader only dispatches and reads the results.

## Why agents, not skills
Forked skills run one at a time (`background: false`, ADJ-13). To run several roles at once, the team-leader calls the Agent tool once per wave item, all in ONE message, and each agent reads and follows the skill file itself. A wave of one item still goes through the Skill tool as in the normal run loop.

## Loop
1. `python3 "<kit>/scripts/team.py" wave --json` (Bash). `dispatch` is what runs now; `held` lists the rest with a reason (gate, question, human-only skill, headcount in use, files shared with a build in this wave).
2. `dispatch` is empty → print the `held` lines and stop with the 4-line stop message.
3. For each item: one reason line in `docs/team/journal/<ID>.md` (Write, `output_language`). Write `.team/current.json` once: {feature: first ID, stage: "wave", wave: [IDs], started_at}. Hooks read each agent's feature from its own transcript, so current.json is only a pointer.
4. Role budget: count each item against its own feature's `limits.max_agents_per_feature[size]`, as in the normal loop.
5. Send ONE message with one Agent call per item: `subagent_type: team:<role>` from the item, and this handoff (≤ 10 lines):
   ```
   Run skill <skill> for <ID>: read <kit>/skills/<skill>/SKILL.md and follow it with $ARGUMENTS = "<args>" (add --decide in decide mode)
   <kit> = contents of .team/plugin_root; ${CLAUDE_SKILL_DIR} = <kit>/skills/<skill>
   Input files: docs/team/features/<ID>/
   Parallel wave: other agents work on other features now; write only <ID>'s files; current.json may name another feature, use <ID>
   devs=<n> reviewers=<n>            (build items only, from the wave output)
   Done when: the skill's Verification list holds
   Report: ≤ 10 lines, first line is the status
   ```
6. Read each return by its first line, as in team-leader step 9. A stop in one feature never cancels the others. Journal after each handoff; `bash "<kit>/scripts/log-run.sh" --feature <ID> --skill <skill> --result <result>` (always pass `--feature` in a wave).
7. Rerun `team.py wave --json`. A feature with no progress since its dispatch (same stage and, for a build, same `tasks_done`) is held for the rest of this run (report it; never redispatch the same skill). Loop to step 2.

## Headcount
- `limits.headcount.<role>` in `.team/config.json` caps how many agents of one role run at once, team-wide (a missing key means 1). The config template ships `max_parallel_dev: 4`, reviewer 4, architect 1 and 2 for the other roles; a project onboarded earlier keeps its own values.
- dev uses `limits.headcount.dev`, else `limits.max_parallel_dev`; reviewer defaults to the dev value. When several features build at once, `team.py wave` splits the dev and reviewer headcount between them (`devs=`, `reviewers=`), and tech-lead's build loop uses that share.
- Two builds whose `tasks.md` `files:` overlap never run in the same wave; the later one waits.
- Cost grows with the number of agents running at once; `limits.feature_budget_usd` still applies per feature.

## Permissions
An agent dispatched this way does not get the skill's `allowed-tools`. `templates/project/claude/settings.json.tmpl` carries the extra allow entries (`cat`, `ls`, `git branch/rev-parse/merge/show/ls-tree/fetch/rebase/push`, `touch`/`rm` of `.team/active-build-*`); `/team:onboard` merges them. A project onboarded before v0.5.0 adds them to `.claude/settings.json` by hand. `role-policy.sh` still enforces each role's limits.
