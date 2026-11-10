# 02 — The team

Source of truth: `SPEC.md` §3 and the `agents/*.md` files. Adjustments: ADJ-01, ADJ-02, ADJ-04, ADJ-07, ADJ-10 in `docs/00-overview.md`.

## Thirteen roles
The table below is GENERATED from the frontmatter of `agents/*.md` by `scripts/gen-team-table.py`; do not edit it by hand. What each role does and does not do, its inputs and its outputs live in the agent file itself.

<!-- team-table:start -->
| Role | Delegate when | Tools | Model | Effort | maxTurns | Memory | Isolation | Preloaded skills |
|---|---|---|---|---|---|---|---|---|
| [team-leader](../agents/team-leader.md) | the user brings a new request, asks about progress or approves a gate, or when a playbook must be chosen, the work sized and the other roles coordinated. Runs as the main-session agent. | Read, Grep, Glob, Bash, Agent, AskUserQuestion, Write, Skill | sonnet | low | 30 | — | — | handbook, using-team |
| [tech-lead](../agents/tech-lead.md) | a feature has an approved spec/design and needs a plan, a task breakdown, coordination of dev and reviewer, branch merging or a PR. | Read, Grep, Glob, Bash, Agent, Edit, Write, Skill | sonnet | medium | 60 | — | — | handbook, using-team |
| [coach](../agents/coach.md) | a retro is due, the scorecard shows an anomaly, feedback crosses its threshold, or the kit needs an audit and evidence-backed proposals to fix an agent or skill. | Read, Grep, Glob, Bash, Write, Skill | opus | high | 40 | project | — | handbook |
| [analyst](../agents/analyst.md) | a raw request must become a spec with a Definition of Done, or when an approved spec must be amended (--amend mode). | Read, Grep, Glob, Bash, Agent, Write, Skill | opus | high | 40 | — | — | handbook |
| [researcher](../agents/researcher.md) | a spec still has technical questions that need official docs, when options must be compared, a dependency upgraded, an external API integrated, or a POC built. | Read, Grep, Glob, Bash, WebFetch, WebSearch, Agent, Write, Skill | opus | high | 50 | — | — | handbook |
| [architect](../agents/architect.md) | size-L work needs an architecture, when a change touches several modules or NFRs, when an ADR decision is needed, or when design.md needs the three-sentence review. | Read, Grep, Glob, Bash, Agent, Write, Skill | opus | high | 40 | — | — | handbook |
| [designer](../agents/designer.md) | an approved spec needs a detailed design before planning: data, API, flows, permissions, migrations, touchpoints and the test plan. | Read, Grep, Glob, Bash, Agent, Write, Skill | opus | high | 40 | — | — | handbook |
| [dev](../agents/dev.md) | tech-lead (or team-leader for size-S work) has one concrete task with touchpoints and criteria that needs tests and code written in a separate worktree. | Read, Edit, Write, Grep, Glob, Bash, Skill | sonnet | medium | 60 | — | worktree | handbook |
| [reviewer](../agents/reviewer.md) | a task has dev's commits and needs an independent review in a clean context before merging, scored against the Review checklist (10). | Read, Grep, Glob, Bash, Skill | opus | high | 25 | project | — | handbook |
| [qa](../agents/qa.md) | every task of a feature is ticked and each criterion needs independent acceptance with real commands, following the Acceptance checklist (6). | Read, Grep, Glob, Bash, Write, Skill | opus | high | 40 | project | — | handbook |
| [writer](../agents/writer.md) | a feature is accepted and needs As-Built, release notes, a CHANGELOG entry, a README update or the PR body; or when the work is documentation only (docs-only, client-docs). | Read, Grep, Glob, Bash, Write, Skill | sonnet | medium | 30 | — | — | handbook |
| [maintainer](../agents/maintainer.md) | cleanup must happen WITHOUT changing behavior: dead code, renames, structure, unused dependencies, orphan tests, simplification, deprecating old APIs, adding observability. | Read, Edit, Write, Grep, Glob, Bash, Skill | sonnet | medium | 60 | — | worktree | handbook |
| [devops](../agents/devops.md) | the CI pipeline is red, when CI/CD must be set up or fixed, deploy, rollback or smoke scripts written, or when releasing to staging or to prod with G5 approved. | Read, Edit, Write, Grep, Glob, Bash, Skill | sonnet | medium | 60 | — | — | handbook |
<!-- team-table:end -->

Temporary agents: `.claude/agents/<name>.md` in the project, created only when team-leader sees the need (`/team:make-agent`).

The `tools` field lists tool names only: the docs do not allow path/command limits there (experiment: `Bash(git status *)` still grants all of Bash). Each role's limits (for example, team-leader writes only `docs/team/**`) are written in the agent body and enforced by the role-policy hook (ADJ-02).

## Who calls whom
```
human <-> main session = team-leader       (the only place with AskUserQuestion)
          ├─► analyst, researcher, architect, designer, writer, maintainer, devops, coach, qa
          ├─► dev                            (size S single-task work only)
          └─► tech-lead ─► dev, reviewer
team-leader, tech-lead, analyst, researcher, architect, designer ─► Explore   (code reading only)
```
- Only team-leader and tech-lead call other roles. analyst, researcher, architect, designer may call only `Explore`; the remaining roles call no one.
- Maximum depth is 3 levels below the main session (ADJ-04).
- A handoff = ONE FILE + a self-contained message of ≤ 10 lines; the receiver does not see the sender's conversation.
- tech-lead → dev: task ID, acceptance criteria, touchpoints, `cmd.test_one`, branch, "edit only inside the touchpoints".
- dev → tech-lead: files changed, tests run with their real output, what is still missing.

Details: `handbook/who-calls-whom.md`.

## Model routing
- The strongest model goes where mistakes cost the most.
- haiku: classification, mechanical work. sonnet: coordination, dev, writer, maintainer, devops. opus: analyst, researcher, architect, designer, reviewer, qa, coach.
- Do not switch models mid-session. Override in `.team/config.json → models`.
