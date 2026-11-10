# Kit quality audit — round 1 (P7)

- Date: 2026-11-09 · Claude Code 2.1.319 · BEFORE state: tag `pre-p7-round1` (= `v0.1.0`, commit a6b7036)
- Tool: `python3 scripts/kit-metrics.py` (bar defined in `scripts/skill-budgets.txt`, `skill-sections.txt`, `agent-sections.txt`)
- Bar: always-loaded skills ≤ 400 words, 4 sections; other skills 1,200–2,500 words, 10 sections; agents 600–1,200 words, 10 sections.

## BEFORE
| Item | Class | Words | Budget | Headings | Rationalizations | Red flags | Verification | Description | refs | Score | At bar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| skill:asbuilt | full | 266 | 1200–2500 | 2/10 (order) | 0 | 3 | 0 | 127 | 0 | 19 | — |
| skill:commit | full | 242 | 1200–2500 | 2/10 (order) | 0 | 3 | 0 | 82 | 0 | 19 | — |
| skill:make-agent | full | 267 | 1200–2500 | 2/10 (order) | 0 | 3 | 0 | 146 | 1 | 19 | — |
| skill:session | full | 260 | 1200–2500 | 2/10 (order) | 0 | 3 | 0 | 117 | 0 | 19 | — |
| skill:architect | full | 277 | 1200–2500 | 2/10 (order) | 0 | 3 | 0 | 146 | 0 | 20 | — |
| skill:audit-kit | full | 272 | 1200–2500 | 2/10 (order) | 0 | 3 | 0 | 161 | 1 | 20 | — |
| skill:ci | full | 296 | 1200–2500 | 2/10 (order) | 0 | 3 | 0 | 117 | 0 | 20 | — |
| skill:clean | full | 298 | 1200–2500 | 2/10 (order) | 0 | 3 | 0 | 128 | 0 | 20 | — |
| skill:design | full | 277 | 1200–2500 | 2/10 (order) | 0 | 3 | 0 | 169 | 0 | 20 | — |
| skill:plan | full | 282 | 1200–2500 | 2/10 (order) | 0 | 3 | 0 | 150 | 0 | 20 | — |
| skill:pr | full | 290 | 1200–2500 | 2/10 (order) | 0 | 3 | 0 | 131 | 0 | 20 | — |
| skill:make-skill | full | 305 | 1200–2500 | 2/10 (order) | 0 | 3 | 0 | 145 | 1 | 21 | — |
| skill:retro | full | 303 | 1200–2500 | 2/10 (order) | 0 | 3 | 0 | 112 | 0 | 21 | — |
| skill:research | full | 294 | 1200–2500 | 2/10 (order) | 0 | 4 | 0 | 128 | 0 | 22 | — |
| skill:verify | full | 274 | 1200–2500 | 2/10 (order) | 0 | 4 | 0 | 118 | 0 | 22 | — |
| skill:analyze | full | 325 | 1200–2500 | 2/10 (order) | 0 | 4 | 0 | 112 | 0 | 23 | — |
| skill:release | full | 304 | 1200–2500 | 2/10 (order) | 0 | 4 | 0 | 109 | 0 | 23 | — |
| skill:build | full | 350 | 1200–2500 | 2/10 (order) | 0 | 4 | 0 | 136 | 0 | 24 | — |
| skill:onboard | full | 393 | 1200–2500 | 2/10 (order) | 0 | 4 | 0 | 157 | 1 | 26 | — |
| skill:takeover | full | 433 | 1200–2500 | 2/10 (order) | 0 | 4 | 0 | 135 | 1 | 27 | — |
| agent:qa | agent | 337 | 600–1200 | 2/10 (order) | 0 | 0 | — | 129 | 0 | 28 | — |
| agent:researcher | agent | 334 | 600–1200 | 2/10 (order) | 0 | 0 | — | 132 | 0 | 28 | — |
| agent:writer | agent | 335 | 600–1200 | 2/10 (order) | 0 | 0 | — | 140 | 0 | 28 | — |
| agent:analyst | agent | 345 | 600–1200 | 2/10 (order) | 0 | 0 | — | 119 | 0 | 29 | — |
| agent:architect | agent | 348 | 600–1200 | 2/10 (order) | 0 | 0 | — | 140 | 0 | 29 | — |
| agent:coach | agent | 350 | 600–1200 | 2/10 (order) | 0 | 0 | — | 144 | 0 | 29 | — |
| agent:designer | agent | 342 | 600–1200 | 2/10 (order) | 0 | 0 | — | 133 | 0 | 29 | — |
| agent:dev | agent | 342 | 600–1200 | 2/10 (order) | 0 | 0 | — | 143 | 0 | 29 | — |
| agent:devops | agent | 342 | 600–1200 | 2/10 (order) | 0 | 0 | — | 146 | 0 | 29 | — |
| agent:maintainer | agent | 346 | 600–1200 | 2/10 (order) | 0 | 0 | — | 149 | 0 | 29 | — |
| agent:reviewer | agent | 349 | 600–1200 | 2/10 (order) | 0 | 0 | — | 128 | 0 | 29 | — |
| agent:team-leader | agent | 345 | 600–1200 | 2/10 (order) | 0 | 0 | — | 164 | 0 | 29 | — |
| agent:tech-lead | agent | 342 | 600–1200 | 2/10 (order) | 0 | 0 | — | 130 | 0 | 29 | — |
| skill:feedback | always | 222 | 0–400 | 0/4 (order) | 0 | — | — | 103 | 0 | 50 | — |
| skill:handbook | always | 182 | 0–400 | 0/4 (order) | 0 | — | — | 84 | 0 | 50 | — |
| skill:intake | always | 194 | 0–400 | 0/4 (order) | 0 | — | — | 78 | 0 | 50 | — |
| skill:run | always | 189 | 0–400 | 0/4 (order) | 0 | — | — | 110 | 0 | 50 | — |
| skill:status | always | 138 | 0–400 | 0/4 (order) | 0 | — | — | 80 | 0 | 50 | — |
| skill:using-team | always | 200 | 0–400 | 0/4 (order) | 0 | — | — | 138 | 0 | 50 | — |

| Group | Items | Median words | % at bar | Median score |
|---|---|---|---|---|
| always | 6 | 191.5 | 0% | 50.0 |
| full | 20 | 292.0 | 0% | 20.0 |
| agent | 13 | 342 | 0% | 29 |
| discipline skills | 8 | 297.5 | — | — |
| all | 39 | — | 0% | — |

## Open issues (blocker/major) → affected items
No blocker remains open after v0.1.0. Majors still open (from `docs/kit-issues.md`, `evals/RESULTS.md`):

| Issue | Severity | Affected items | Round 1 handling |
|---|---|---|---|
| K-34 size S skips the reviewer (team-leader calls dev directly) | major | agent team-leader, skill build, skill run | Rewrite: size S still goes through `/team:build` (1 dev + reviewer) |
| K-15 definition of `max_agents_per_feature`; size S verify always forks qa | major | agent team-leader, skill verify, config | Rewrite: count distinct ROLES, not re-calls within a rework round |
| K-16/K-19 team-leader reads gates wrongly, a gate blocks the whole team | minor→affects behavior | agent team-leader, skill run, intake | Rewrite: gates come only from `team.py`, and block only their own feature |
| K-33 the using-team eval does not distinguish the two modes | minor | evals/using-team | Rewrite scenario 1 |
| K-06 headless must pass `--allowedTools` | major | workflows/batch, team-feature.yml | Later round (not skill/agent content) |
| K-24 Bash of `bash: any` roles does not go through protect | major | hooks, teamlib | Later round (machine rule) |

## AFTER (round 1 done, 2026-11-09)
| Group | Items | Median words | % at bar | Median score |
|---|---|---|---|---|
| always | 6 | 309 | 100% | 100 |
| full | 20 | 303.5 | 35% (7/20) | 21.5 |
| agent | 13 | 348 | 38% (5/13) | 29 |
| discipline skills | 8 | **1,502.5** | — | — |
| all | 39 | — | 46% (18/39) | — |

100% of rewritten items meet the bar (18/18). Items not yet rewritten are listed in `scripts/quality-backlog.txt` (21 items).

## Rewritten items
Ref: A = `/tmp/ref/agent-skills/skills`, AA = `/tmp/ref/agent-skills/agents`, S = `/tmp/ref/superpowers/skills`, V = `/tmp/ref/awesome-claude-code-subagents/categories`, W = `/tmp/ref/agents/plugins`, B = `/tmp/ref/BMAD-METHOD`. Detailed reading notes: `refnotes/A-planning.md`, `B-build.md`, `C-agents.md` (scratch of the P7 session).

| Item | Score before | Score after | Words before → after | References read | Taken | Dropped |
|---|---|---|---|---|---|---|
| skill:using-team | 50 | 100 | 200 → 395 | A/using-agent-skills, S/using-superpowers, S/writing-skills | table of work type → skill; priority order; subagents do not re-discover | "1% means you must call it"; TodoWrite; skills of other plugins |
| skill:handbook | 50 | 100 | 182 → 375 | S/verification-before-completion | write files with Write; rationalization table | — |
| skill:status | 50 | 100 | 138 → 273 | S/subagent-driven-development (resuming) | print output verbatim; gates per the "Applicable gates" column | — |
| skill:run | 50 | 100 | 189 → 313 | S/executing-plans | gates only from team.py (K-02); size S through build (K-34); stop when the stage does not change | running continuously without stopping |
| skill:intake | 50 | 100 | 194 → 305 | A/spec-driven-development | a gate blocks only its own feature (K-19) | — |
| skill:feedback | 50 | 100 | 222 → 263 | — | write with Write (K-10) | — |
| skill:analyze | 23 | 100 | 325 → 1,590 | A/interview-me, A/spec-driven-development, S/brainstorming | hypothesis + confidence; look before asking; stop-asking test; turn adjectives into numbers; vague answers | asking the human one question at a time; spec template with stack commands; design doc |
| skill:plan | 20 | 100 | 282 → 1,316 | A/planning-and-task-breakdown, S/writing-plans | file map first; Receives/Returns block; shared constraints; 5-point self-check; never overwrite an unfinished plan | tasks/plan.md path; hard-coded commands; handoff menu |
| skill:takeover | 27 | 100 | 433 → 1,510 | A/context-engineering, A/source-driven-development, B/preparing-a-repo-for-agents | claim/reality table; doc staleness; budget line per tier; suspicious content; final read-only check | looking up external docs; writing AGENTS.md at takeover |
| skill:build | 24 | 100 | 350 → 1,504 | S/subagent-driven-development (+prompt, fix-loop, preflight, resuming), S/executing-plans, S/test-driven-development, A/test-driven-development, A/incremental-implementation | DONE/…/BLOCKED statuses; red for the right reason; BASE..HEAD; review package; scoped re-review; loop breaker; resume from disk | reviewer runs tests; 5 rounds; separate ledger directory; merge into base |
| skill:verify | 22 | 100 | 274 → 1,510 | S/verification-before-completion, A/code-review-and-quality, A/debugging-and-error-recovery | gate per criterion; pinned to a commit; table of what a claim needs; defect classification; regression evidence | qa reverts code itself; merge menu |
| skill:commit | 19 | 100 | 242 → 1,501 | A/git-workflow-and-versioning, A/incremental-implementation, A/code-review-and-quality | review what is staged; secret scan; atomicity test; handling failing hooks; save points | feature/ branches; reset --hard; bisect |
| skill:pr | 20 | 100 | 290 → 1,425 | S/receiving-code-review, S/finishing-a-development-branch, S/requesting-code-review | test after rebase; classify comments before fixing; YAGNI; no pleasantries; check CI | local merge; gh api for reply threads; force-push |
| agent:team-leader | 29 | 100 | 345 → 1,062 | W/agent-teams/team-lead, V/09-meta-orchestration/{multi-agent-coordinator,agent-organizer}, B/craft-subagents | count roles (K-15); handoff through files; act on the returned status; resume from artifacts | peer-to-peer messaging; a separate coordinator role |
| agent:tech-lead | 29 | 100 | 342 → 945 | S/subagent-driven-development (fix-loop, handling-reports, cannot-verify, preflight), W/agent-teams/team-lead | preflight; BASE; loop breaker with a ruling; "not verifiable" section | re-calling the same dev with SendMessage; ban on parallelism |
| agent:dev | 29 | 100 | 342 → 959 | S/subagent-driven-development/implementer-prompt, W/agent-teams/team-implementer, AA/test-engineer, W/debugging-toolkit/debugger | red for the right reason; baseline; "see but do not touch"; return status | asking the human; do-everything checklist |
| agent:reviewer | 29 | 100 | 349 → 946 | S/subagent-driven-development/{task-reviewer,re-review}-prompt, AA/code-reviewer, W/agent-teams/team-reviewer, AA/security-auditor | tests before code; missing/extra/misunderstood; an explanation does not lower the severity; confirmed/suspected | reviewer with Write/Edit; invented numeric thresholds |
| agent:qa | 28 | 100 | 337 → 902 | V/04-quality-security/{qa-expert,test-automator}, AA/test-engineer, S/verification-before-completion | pinned to a commit; beyond the happy path; NOT VERIFIABLE → NEEDS_ANSWER; 3 runs for flaky tests | qa writes tests; invented metrics |
