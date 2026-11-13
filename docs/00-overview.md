# 00 — Overview

## What it is, who it is for
`automation-ai` is the `team` plugin for Claude Code. Install it into any project and it gives Claude Code an IT team with clear roles, a 9-stage process, approval gates and machine-enforced rules.

For:
- Team leads who want to hand over raw requests and only approve documents at the gates.
- Developers who want Claude to work with discipline: tests first, separate review, acceptance on real output.
- Whoever takes over a legacy project and needs to learn quickly where it stands.

It is not: a process for one specific stack; a store of the project's business knowledge; a tool that deploys to production on its own; a place to write MCP servers or new plugins.

## Seven principles
| # | Principle | Meaning |
|---|---|---|
| P1 | An agent is a person | Every role has a contract; there is no "does everything" agent. |
| P2 | State lives on disk | The current position is computed from the artifacts in `docs/team/`. |
| P3 | Machine before LLM | Anything that must not go wrong is checked by a hook, a permission or a script. Hooks remind by default and stop the tool only with `enforcement: "block"` (ADJ-34). |
| P4 | Platform independent | Commands and project structure live in `.team/profile.json`. |
| P5 | Call the right person, when needed | Every call has a one-sentence reason in the journal. |
| P6 | Measure before you fix | Scorecard + journal; every change has an eval, a canary and a rollback. |
| P7 | The human decides | Gates are configuration; an enabled gate is never bypassed. |

## The takeover idea: three questions
`/team:takeover` answers only three questions and changes nothing:
1. What does the project **do**?
2. How **far along** is it?
3. What is the **next piece of work**?

It scans in 4 tiers; a later tier runs only when the earlier one could not answer: T0 metadata (directory tree, manifests, git log) → T1 documentation → T2 documentation checked against the code, by sampling → T3 deep reading module by module. The report states what was scanned, what was not, and the confidence level. The human approves `ai-readiness.md` (gate G0) before running `/team:onboard`.

## Where things are
| You want to know | Look at |
|---|---|
| The full specification | `SPEC.md` |
| Process, gates, work size | `docs/01-process.md` |
| The roles and who calls whom | `docs/02-team.md` |
| The engineering handbook | `handbook/STD.md` (summary: `docs/03-handbook.md`) |
| The profile slots | `docs/04-profile.md` |
| Tokens, memory | `docs/05-tokens-and-memory.md` |
| Install, uninstall | `docs/06-install.md` |
| Self-improvement | `docs/07-improvement.md` |
| Channels (CLI, GitHub, headless) | `docs/08-channels.md` |
| Known kit issues, backlog | [`docs/kit-issues.md`](kit-issues.md) |
| Quality audit of skills/agents | [`docs/research/kit-audit-round1.md`](research/kit-audit-round1.md), [`kit-audit-round2.md`](research/kit-audit-round2.md) |
| Language switch (P9): measured context effect | [`docs/research/language-switch.md`](research/language-switch.md); owner guide [`GUIDE-VI.md`](../GUIDE-VI.md); [`SPEC-OVERRIDES.md`](../SPEC-OVERRIDES.md) |
| Original requirements and acceptance | [`docs/requirements/ban-hieu-yeu-cau.md`](requirements/ban-hieu-yeu-cau.md), raw inputs before amendments ([understanding document v1](requirements/raw/automation-ai_ban-hieu-yeu-cau.md), [prompt chain P0–P6](requirements/raw/automation-ai_prompts.md)), [`docs/acceptance/acceptance-2026-11-10.md`](acceptance/acceptance-2026-11-10.md) ([traceability matrix](acceptance/traceability-2026-11-10.md), [requirements register](acceptance/requirements-register.md), [measured quality](acceptance/measured-quality.md), [SPEC vs requirements](acceptance/spec-vs-requirements.md)); these files stay in Vietnamese as historical records |
| Reference kits, comparison | [`docs/research/reference-kits.md`](research/reference-kits.md) |
| Credits | [`docs/credits.md`](credits.md) |
| Start in 5 minutes | [`docs/guides/5-minute-start.md`](guides/5-minute-start.md) |
| Want X, type Y | [`docs/guides/want-x-type-y.md`](guides/want-x-type-y.md) |
| Choose a playbook | [`docs/guides/decision-tree.md`](guides/decision-tree.md) |
| Sample sessions | [`docs/guides/sample-sessions.md`](guides/sample-sessions.md) |
| Read `/team:status`, who is waiting for whom | [`docs/guides/who-is-waiting-for-what.md`](guides/who-is-waiting-for-what.md) |
| When something goes wrong | [`docs/guides/incidents.md`](guides/incidents.md) |
| First day on an existing project | [`docs/guides/first-day-on-existing-project.md`](guides/first-day-on-existing-project.md) |

In a project where the kit is installed: configuration lives in `.team/`, artifacts in `docs/team/`, path-scoped rules in `.claude/rules/`.

## Approved adjustments (relative to SPEC)
SPEC is kept verbatim. The points below were approved by the owner on 2026-11-09, after checking them against the official Claude Code 2.1.319 docs (ADJ-30 was added in P9). Where they differ from SPEC, they win.

| Code | Adjustment | Reason (docs) |
|---|---|---|
| ADJ-01 | `team-leader` runs as the main-session agent: `/team:onboard` writes `"agent": "team:team-leader"` into `.claude/settings.json`. Only the main session asks the human. `analyst` and the other roles return their questions as a file + status `NEEDS_ANSWER`. | Subagents never have `AskUserQuestion`. |
| ADJ-02 | Per-role limits (paths that may be written, Bash commands that may run, agents that may be called) are enforced by the plugin's PreToolUse hook, which reads `agent_type` and the role-policy table. An agent's `tools` field lists tool names only. | `tools` does not accept path limits; plugin agents ignore `hooks`, `permissionMode`, `mcpServers`. |
| ADJ-03 | Headless runs that edit files do NOT use `--bare`. `--bare` is only for read-only reports (status, metrics). | `--bare` turns off every hook, including the plugin's hooks. |
| ADJ-04 | Call depth: main session (team-leader) → tech-lead → dev/reviewer → Explore = 3 levels, exactly the default of `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`. Do not lower this value. | Nested subagents go at most 3 levels deep by default. |
| ADJ-05 | The plugin entry in `marketplace.json` has no `version`; only `plugin.json` carries it. | If both carry it, `plugin.json` wins and validate warns. |
| ADJ-06 | `effort` accepts `low|medium|high|xhigh|max`; SessionStart gets an extra `fork` matcher. | Current docs. |
| ADJ-07 | `TaskCreate/TaskUpdate` removed from team-leader's tools; `tasks.md` is the state. | These two tools are only on by default on older models. |
| ADJ-08 | A local install (`install-local.sh`, `npx skills`) has no namespace: commands are `/team-<name>` (ADJ-22). Hooks are wired into `.claude/settings.json` (P5). `npx skills` installs skills only. | `${CLAUDE_PLUGIN_ROOT}` and `hooks/hooks.json` only take effect inside a plugin. |
| ADJ-09 | Gates apply by work size: size S skips G1 by design; the refactor playbook turns on G2b. | The simplest reading of SPEC §4. |
| ADJ-10 | `designer` defaults to opus; team-leader passes `model: sonnet` when calling it for size S/M work. | An agent file has only one `model`. |
| ADJ-11 | Tools added relative to SPEC §3: `Write` for tech-lead and qa (they must create `plan.md`, `tasks.md`, `review-NN.md`, `acceptance.md`); `Skill` for every role (temp skills, `/team:commit`); `AskUserQuestion` removed from analyst (ADJ-01). | Edit cannot create a new file; without `Skill` a subagent cannot call a skill. |
| ADJ-12 | The `handbook` skill does not use `` !`cat` ``; its step 1 is a Read of `${CLAUDE_PLUGIN_ROOT}/handbook/STD-short.md` (fallback `<kit>`). | Experiment: when preloaded into a subagent, a `!` command goes through the permission check and the subagent does NOT start in `dontAsk` mode, even with `Bash(cat *)` allowed. |
| ADJ-13 | A skill that forks to a role names it with the plugin prefix: `agent: team:<role>`; it sets `background: false` so that `/team:run` runs sequentially. | Experiment: a bare name (`analyst`) is ignored and the skill runs on the general agent. Forked skills run in the background by default. |
| ADJ-14 | `make-skill` and `make-agent` are callable by Claude (no `disable-model-invocation`): team-leader creates temp skills when needed (SPEC §9). `pr` and `audit-kit` fork to tech-lead and coach. | The P4 prompt both listed these two skills as "human-only" and said team-leader calls them; team-leader has read-only Bash, so it cannot open a PR itself. |
| ADJ-15 | Skills do not use `` !`command` ``; the precondition is a step that runs `python3 "$(cat .team/plugin_root)/scripts/team.py" status` through Bash. | Same reason as ADJ-12: a `!` command goes through the permission check and can stop the skill from starting. |
| ADJ-16 | The `data-migration` playbook turns on G2b (approval of `design.md`), like `refactor`. | SPEC is silent; risk of data loss. |
| ADJ-17 | The `role-policy.sh` hook + `hooks/role-policy.json` enforce ADJ-02. When `.team/current.json` has `stage: onboard`, team-leader may also write `CLAUDE.md`, `.claude/rules/`, `.github/`, `.gitignore`. | Onboard runs in the main session (team-leader). |
| ADJ-18 | `scripts/render.py` builds project files from templates (replaces `{{…}}`, expands lists, merges without overwriting); `scripts/teamlib.py` holds the shared hook logic. | Avoids having the LLM fill in settings JSON by hand. |
| ADJ-19 | `Read(//<kit>/**)` is written to `.claude/settings.local.json`, not to the shared settings. | The kit path differs between machines; the P4 dry run showed this permission is needed. |
| ADJ-20 | `stop-check.sh` also runs on the SubagentStop of `team:dev`, `team:maintainer`, `team:researcher`. | The build loop runs inside a subagent; the main session's Stop alone comes too late. |
| ADJ-21 | STD-GIT-3 at machine level: only `team/*` or tags may be pushed; `--force-with-lease` is blocked too; Edit/Write on `.claude/settings*.json` is blocked. | Simplest and safest. |
| ADJ-22 | Local install: `install-local.sh` drops the `team:` prefix from agent names, renames skills to `team-<name>` (avoids clashing with `/status`, `/run`, `/verify`…), merges the hooks into `.claude/settings.json`; role-policy accepts the unprefixed names as well. | There is no plugin namespace in a local install. |
| ADJ-23 | coach writes: `docs/team/retro/**`, `docs/team/proposals/**`, `docs/team/kit-issues.md` (audit-kit), `docs/team/metrics/scorecard.json` (only through `team.py scorecard`), `.team/current.json`, its own memory — one list in `agents/coach.md` = `hooks/role-policy.json`. | SPEC §3 names only retro/proposals, but audit-kit must write kit-issues and every stage writes `current.json` (K-43). |
| ADJ-24 | There is no deploy slot for prod or rollback (SPEC §8 has only `deploy.staging`, `deploy.smoke`, `deploy.prod_requires_reviewer`): the checked prod and rollback commands live in `docs/team/ci.md` under `## Deploy`, written by `/team:ci deploy-script` through a PR. devops triggers exactly that command/pipeline, and only after `Approved-by-prod:`; a CI job with an environment that requires a reviewer is preferred (STD-OPS-7). | SPEC §13 forbids inventing slots; new slots are proposed in the report. |
| ADJ-25 | researcher may write any file in its own worktree `.claude/worktrees/<n>/` (POC), but not the main tree (`worktree_write` in role-policy). | SPEC §3 "POC in worktree" cannot work when role-policy only allows `docs/team/**`. |
| ADJ-26 | `team.py`: playbooks without analyze (bug-fix, hotfix, refactor, dependency-upgrade, spike, ci-fix, docs-only) do not need `spec.md`; bug-fix, hotfix, refactor do not need `plan.md`; refactor counts as `built` when `/team:clean` writes `tasks.md` (T1 ticked). | The SPEC §5 chain of these playbooks has no such step; the status used to get stuck (K-47). |
| ADJ-27 | analyst, architect, designer, writer have the `Bash` tool, only to run read-only commands (`team.py status`, `explore-cache.sh`, `git log`); role-policy keeps `bash: read-only`. | These roles' skills need to check status; eval analyze s1 (2026-11-09) showed analyst skipping the step because it had no Bash (K-52). |
| ADJ-28 | `intake` is callable by Claude (`disable-model-invocation` removed): when the human types a raw request, team-leader runs `/team:intake` itself. | SPEC §3: team-leader does intake; `using-team` used to point at a skill only the human could call (K-70). |
| ADJ-29 | (superseded by ADJ-36 in v0.6.2) Size S still gets acceptance through `/team:verify` (qa, a shortened check), not "automated verify without a separate qa"; qa counts toward the 3-role cap of size S (analyst, tech-lead, qa). | SPEC §4 says "verify (automated, no separate qa)"; the kit keeps an independent acceptor because size S work can be wrong too (K-15, K-78). |
| ADJ-36 | Right-size the team (v0.6.2, owner decision 2026-11-13; supersedes ADJ-29). A question, explanation or status check → team-leader answers, no intake, no agent. New playbook `quick` (trivial change, ≤ 2 files, no schema/API/security) → one dev called by team-leader, done when T1 is ticked. Size S → build (tech-lead, 1 dev + 1 reviewer) writes `acceptance.md` itself (automated acceptance, SPEC §4 "no separate qa"), no As-Built, `/team:pr` writes a short body. | erp_ai: a size S bug took 6 agents and 20.5 min for a 51 s fix; the owner asked that only the needed roles run. |
| ADJ-35 | Only `/team:release` stays human-only (v0.6.1, owner decision 2026-11-13). takeover, onboard, run, retro, audit-kit, session and ci lose `disable-model-invocation`: team-leader runs takeover/onboard when a project has no profile, ci when CI is red, retro when feedback crosses its threshold, `run` for its own loop. Gates still stop the work (G0 before onboard, G5 before prod). `validate.sh` `HUMAN_ONLY_SKILLS="release"`. | The owner had to type `/team:onboard` himself in erp_ai; SPEC only requires a human for prod (§8 stage 8 "G5 ALWAYS HUMAN"). |
| ADJ-34 | Hooks remind, they do not block (v0.6.0, owner decision 2026-11-13): config `enforcement` = `warn` (default, also when missing) → protect, check-git and role-policy hand the rule to Claude as additionalContext and let the tool run; stop-check skips its lint/test pass and reminds about `## Sources`. `enforcement: "block"` restores exit 2. See SPEC-OVERRIDES.md entry 5. | The owner: skills and rules are working rules; blocking stopped the team-leader on read-only work again and again (K-96). |
| ADJ-33 | Run independent work at the same time (v0.6.0, owner request): build dispatches in rounds, one message per round with every call that can start (new devs, reworks, reviews), never waiting for a whole wave; one Explore call per independent question in one message; a request with independent items gets one intake each and runs as a wave. Config template defaults: `max_parallel_dev` 4, `headcount` reviewer 4, architect 1, the other roles 2. See SPEC-OVERRIDES.md entry 4. | `erp_ai`: 496 of 522 dispatch messages carried one Agent call; the SPEC default of 2 devs capped plans 5–7 tasks wide (K-92..K-94). |
| ADJ-32 | CLAUDE.md describes the project (v0.6.0): a project block `<!-- project:start -->…<!-- project:end -->` (≤ 150 lines; template `templates/artifacts/claude-md.md`) above the team block (≤ 25 lines). `/team:onboard` writes it and adopts an old CLAUDE.md into it; `/team:asbuilt` (writer) keeps it true after each feature; `/team:retro` reports drift; `scripts/check-claude-md.py` checks markers, budgets, placeholders and stale paths. See SPEC-OVERRIDES.md entry 3. | A CLAUDE.md that only introduced the team never described the project and never changed after onboard. |
| ADJ-31 | Parallel waves across features (v0.5.0): `/team:run --all` dispatches `team.py wave` items as Agent calls in one message (each agent follows the skill file); per-feature build flag `.team/active-build-<ID>`; hooks read a subagent's feature from its transcript, so `.team/current.json` is only a pointer. Headcount per role in `limits.headcount`. | Forked skills run one at a time (ADJ-13); one shared current.json and one build flag let parallel features overwrite each other. |
| ADJ-30 | Language zones (P9): AI-facing text English; owner-facing Vietnamese only in GUIDE-VI.md; artifact prose follows config.output_language (vi default); anchors English (scripts/anchors.txt). See SPEC-OVERRIDES.md entry 1. | Decision of the owner in P9; overrides SPEC §0. |
