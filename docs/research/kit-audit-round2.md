# Kit quality audit — round 2 (P7)

- Date: 2026-11-10 · Claude Code 2.1.319 · BEFORE state: tag `pre-p7-round2` (= `v0.2.1`, commit e12c68c)
- Round number: 2. The prompt's formula (number of `v0.*` tags) gives 3 because of the patch tag `v0.2.1`; rounds are counted as the existing `pre-p7-round*` tags (1) + 1.
- Tool: `python3 scripts/kit-metrics.py` (bar defined in `scripts/skill-budgets.txt`, `skill-sections.txt`, `agent-sections.txt`)
- Round 2 scope: the 21 items in `scripts/quality-backlog.txt` (13 skills + 8 agents, exactly within the cap of 14 + 8).

## BEFORE
| Item | Class | Words | Budget | Headings | Rationalizations | Red flags | Verification | Description | refs | Score | At bar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| skill:asbuilt | full | 266 | 1200–2500 | 2/10 (order) | 0 | 3 | 0 | 127 | 0 | 19 | — |
| skill:session | full | 260 | 1200–2500 | 2/10 (order) | 0 | 3 | 0 | 117 | 0 | 19 | — |
| skill:architect | full | 277 | 1200–2500 | 2/10 (order) | 0 | 3 | 0 | 146 | 0 | 20 | — |
| skill:audit-kit | full | 272 | 1200–2500 | 2/10 (order) | 0 | 3 | 0 | 161 | 1 | 20 | — |
| skill:ci | full | 296 | 1200–2500 | 2/10 (order) | 0 | 3 | 0 | 117 | 0 | 20 | — |
| skill:clean | full | 298 | 1200–2500 | 2/10 (order) | 0 | 3 | 0 | 128 | 0 | 20 | — |
| skill:design | full | 277 | 1200–2500 | 2/10 (order) | 0 | 3 | 0 | 169 | 0 | 20 | — |
| skill:make-agent | full | 278 | 1200–2500 | 2/10 (order) | 0 | 3 | 0 | 146 | 1 | 20 | — |
| skill:make-skill | full | 316 | 1200–2500 | 2/10 (order) | 0 | 3 | 0 | 145 | 1 | 21 | — |
| skill:retro | full | 303 | 1200–2500 | 2/10 (order) | 0 | 3 | 0 | 112 | 0 | 21 | — |
| skill:research | full | 294 | 1200–2500 | 2/10 (order) | 0 | 4 | 0 | 128 | 0 | 22 | — |
| skill:release | full | 320 | 1200–2500 | 2/10 (order) | 0 | 4 | 0 | 109 | 0 | 23 | — |
| skill:onboard | full | 393 | 1200–2500 | 2/10 (order) | 0 | 4 | 0 | 157 | 1 | 26 | — |
| agent:researcher | agent | 334 | 600–1200 | 2/10 (order) | 0 | 0 | — | 132 | 0 | 28 | — |
| agent:writer | agent | 335 | 600–1200 | 2/10 (order) | 0 | 0 | — | 140 | 0 | 28 | — |
| agent:analyst | agent | 345 | 600–1200 | 2/10 (order) | 0 | 0 | — | 119 | 0 | 29 | — |
| agent:architect | agent | 348 | 600–1200 | 2/10 (order) | 0 | 0 | — | 140 | 0 | 29 | — |
| agent:coach | agent | 350 | 600–1200 | 2/10 (order) | 0 | 0 | — | 144 | 0 | 29 | — |
| agent:designer | agent | 342 | 600–1200 | 2/10 (order) | 0 | 0 | — | 133 | 0 | 29 | — |
| agent:devops | agent | 342 | 600–1200 | 2/10 (order) | 0 | 0 | — | 146 | 0 | 29 | — |
| agent:maintainer | agent | 346 | 600–1200 | 2/10 (order) | 0 | 0 | — | 149 | 0 | 29 | — |
| agent:dev | agent | 959 | 600–1200 | 10/10 | 9 | 6 | — | 143 | 0 | 100 | ✓ |
| agent:qa | agent | 924 | 600–1200 | 10/10 | 9 | 5 | — | 129 | 0 | 100 | ✓ |
| agent:reviewer | agent | 946 | 600–1200 | 10/10 | 9 | 6 | — | 128 | 0 | 100 | ✓ |
| agent:team-leader | agent | 1062 | 600–1200 | 10/10 | 9 | 6 | — | 164 | 0 | 100 | ✓ |
| agent:tech-lead | agent | 945 | 600–1200 | 10/10 | 9 | 6 | — | 130 | 0 | 100 | ✓ |
| skill:analyze | full | 1590 | 1200–2500 | 10/10 | 10 | 8 | 6 | 112 | 1 | 100 | ✓ |
| skill:build | full | 1504 | 1200–2500 | 10/10 | 10 | 8 | 6 | 136 | 1 | 100 | ✓ |
| skill:commit | full | 1501 | 1200–2500 | 10/10 | 12 | 7 | 6 | 82 | 2 | 100 | ✓ |
| skill:feedback | always | 263 | 0–400 | 4/4 | 6 | — | — | 103 | 0 | 100 | ✓ |
| skill:handbook | always | 375 | 0–400 | 4/4 | 6 | — | — | 84 | 0 | 100 | ✓ |
| skill:intake | always | 305 | 0–400 | 4/4 | 6 | — | — | 78 | 0 | 100 | ✓ |
| skill:plan | full | 1316 | 1200–2500 | 10/10 | 10 | 7 | 6 | 150 | 1 | 100 | ✓ |
| skill:pr | full | 1425 | 1200–2500 | 10/10 | 11 | 7 | 6 | 131 | 1 | 100 | ✓ |
| skill:run | always | 313 | 0–400 | 4/4 | 6 | — | — | 110 | 0 | 100 | ✓ |
| skill:status | always | 273 | 0–400 | 4/4 | 6 | — | — | 80 | 0 | 100 | ✓ |
| skill:takeover | full | 1510 | 1200–2500 | 10/10 | 10 | 7 | 6 | 135 | 1 | 100 | ✓ |
| skill:using-team | always | 395 | 0–400 | 4/4 | 6 | — | — | 138 | 0 | 100 | ✓ |
| skill:verify | full | 1552 | 1200–2500 | 10/10 | 13 | 10 | 6 | 118 | 1 | 100 | ✓ |

| Group | Items | Median words | % at bar | Median score |
|---|---|---|---|---|
| always | 6 | 309.0 | 100% | 100.0 |
| full | 20 | 309.5 | 35% | 21.5 |
| agent | 13 | 348 | 38% | 29 |
| discipline skills | 8 | 1502.5 | — | — |
| all | 39 | — | 46% | — |

## Open issues (blocker/major) → affected items
No blocker remains open after v0.2.1. Majors still open (`docs/kit-issues.md`; `evals/RESULTS.md` Round 1 has no eval that got worse):

| Issue | Severity | Affected items | Done in round 2 |
|---|---|---|---|
| K-06 headless in an untrusted directory ignores `permissions.allow` | major | `templates/project/github/workflows/team-feature.yml`, `workflows/batch/*`, skill `ci`, agent `devops`, `docs/08-channels.md` | generate `--allowedTools` from the profile with a script; ci/devops use that script |
| K-24 Bash of `bash: any` roles does not go through `protect.sh` | major | `hooks/hooks.json`, `scripts/protect.sh`, `scripts/teamlib.py` | attach `protect.sh` to Bash, check the write targets of shell commands |
| K-39 read-only still leaks (`sed e/w`, `sort -o`, `uniq IN OUT`, `tree -o`, `rg --pre`, `>&`, `<>`, `mkdir`) | major | `scripts/teamlib.py is_readonly`, `hooks/role-policy.json` | block each form, drop `mkdir`, test cases |
| K-40 read-only scripts matched by name | major | `scripts/teamlib.py`, `hooks/role-policy.json` | match the real path under `<kit>/scripts/`; a script that writes needs write permission on its target |

Minors tied to rewritten items: K-09, K-26 (onboard); K-27/K-43, K-44 (coach, audit-kit); K-38 (retro); K-45 (docs, size S verify); K-25 (`Bash(python3 *)` in skills); K-08 (detect-stack, takeover).

## AFTER (round 2 done, 2026-11-10)
| Group | Items | Median words | % at bar | Median score |
|---|---|---|---|---|
| always | 6 | 323.5 | 100% | 100.0 |
| full | 20 | 1436.5 | 100% | 100.0 |
| agent | 13 | 924 | 100% | 100 |
| discipline skills | 8 | 1502.0 | — | — |
| all | 39 | — | 100% | — |

`scripts/quality-backlog.txt` is empty; `kit-metrics.py --check` exits 0. Before round 2: full 309.5 words / 35% at bar; agent 348 / 38%; all 46%.

## Rewritten items
References read in full (paths under `/tmp/ref`, HEAD in `docs/research/reference-kits.md`); notes: `refnotes/D-docs-arch.md`, `E-ops.md`, `F-meta.md` (session scratchpad, summarized here).

| Item | Score before | Score after | Words before → after | References read | Taken | Dropped (reason) |
|---|---|---|---|---|---|---|
| skill:asbuilt | 19 | 100 | 266 → 1,527 | agent-skills/skills/documentation-and-adrs; agent-skills/references/definition-of-done.md; /tmp/ref/agents/plugins/documentation-generation/agents/docs-architect.md | design ↔ reality table per item + `file:line`; sourced sentences; Keep a Changelog groups; close debt after G4 (K-35); the four pr-body headings | "readability/SEO" metrics (invented numbers); README template with npm commands (stack commands) |
| skill:release | 23 | 100 | 320 → 1,364 | agent-skills/skills/shipping-and-launch; definition-of-done.md; awesome…/03-infrastructure/deployment-engineer.md | rollback plan before deploy; pick the version from tags + CHANGELOG; UAT stop point; post-deploy checks | rollout by flags/error budget (no slot); `git revert && git push` (pushes the base branch); automatic prod rollback |
| skill:research | 22 | 100 | 294 → 1,551 | agent-skills/skills/source-driven-development; awesome…/10-research-analysis/research-analyst.md | detect version → fetch source → cite; source hierarchy; `UNVERIFIED`; safe citation; upgrade/integration table | "ask the human when the version is missing" (a subagent cannot ask); researcher writes code from the docs itself |
| skill:architect | 20 | 100 | 277 → 1,431 | BMAD-METHOD/skills/bmad-architecture (+ references/reviewer-gate, headless, assets/spine-template); bmad-agent-architect; documentation-and-adrs; /tmp/ref/agents/plugins/c4-architecture/agents/c4-container.md | three-condition threshold test; ADR with a checkable `## Constraints`; dimension sweep; self-critique; containers from the deployment reality | interviewing the human (Coaching path); memlog; parallel reviewers; "future needs" (STD-DESIGN-5) |
| skill:design | 20 | 100 | 277 → 1,507 | agent-skills/skills/api-and-interface-design, spec-driven-development; /tmp/ref/agents/plugins/database-design/agents/database-architect.md; awesome…/01-core-development/api-designer.md | contract before flow; Hyrum; idempotency on all 6 points; migrations in batches; one log/metric per new path | "Commands" section in the spec (commands live in `cmd.*`); designer splits tasks; TypeScript naming rules |
| skill:ci | 20 | 100 | 296 → 1,348 | agent-skills/skills/ci-cd-and-automation; /tmp/ref/agents/plugins/cicd-automation/skills/github-actions-templates; deployment-engineer, devops-engineer | the 5 STD-CI-4 classes with evidence; one re-run; empty slot = "not configured"; rollback "verified" only after a real run | npm/vercel commands; agent fixes lint errors in code itself; auto-merge; removing slow tests from PRs |
| skill:clean | 20 | 100 | 298 → 1,363 | agent-skills/skills/code-simplification, deprecation-and-migration, observability-and-instrumentation; /tmp/ref/agents/plugins/code-refactoring/agents/legacy-modernizer.md | Chesterton's fence; characterization tests first; compare test names; `deprecate`, `observe` kinds; 500-line cap | language-specific examples; splitting monoliths; Sonar/CodeQL tools not in the profile |
| skill:audit-kit | 20 | 100 | 272 → 1,211 | agent-skills/skills/security-and-hardening; /tmp/ref/everything-claude-code/hooks/README.md, /tmp/ref/everything-claude-code/hooks/hooks.json, /tmp/ref/everything-claude-code/hooks/hermes/config-protection.py, /tmp/ref/everything-claude-code/rules/common/{hooks,security,agents}.md; BMAD retrospective/references/evidence-gathering.md | trust boundaries; hooks failing open; matchers covering tools; "checked and clean" vs "not checked"; dedupe against K-xx | application checklists (OWASP, STRIDE); hook kill switch; "stop everything, call a security agent" |
| skill:make-skill | 21 | 100 | 316 → 1,383 | superpowers/skills/writing-skills (+ discovery, bulletproofing, testing-skills-with-subagents, persuasion-principles, anthropic-best-practices); skills/skills/skill-creator (+ agents/grader, analyzer, comparator) | observable failure = red, first use = green; instruction form by failure type; near-miss trigger phrases; discrimination check; temp skill with the 8 items of SPEC §9 | HTML viewer, `.skill` packaging, scripts needing external libraries; "pushy" descriptions that summarize the process |
| skill:make-agent | 20 | 100 | 278 → 1,327 | writing-skills/anthropic-best-practices; awesome…/09-meta-orchestration/agent-organizer.md; everything-claude-code/the-longform-guide.md | capability match with citations; model by the cost of a mistake; `_temp` role (K-49); test cases outside `.claude/agents/` | agent that plans the team; BMAD personas; adding models to config |
| skill:session | 19 | 100 | 260 → 1,273 | agent-skills/skills/context-engineering, using-agent-skills; everything-claude-code/the-shortform-guide.md, the-longform-guide.md | handoff only what the artifacts lack; load = check (HEAD, approvals only from files); `/compact <focus>` line; budget from measurements | injecting memory into `--system-prompt`; turning off auto-compact; skills auto-generated at Stop |
| skill:onboard | 26 | 100 | 393 → 1,250 | everything-claude-code/CLAUDE.md, examples/CLAUDE.md, docs/SELECTIVE-INSTALL-ARCHITECTURE.md; writing-skills/references/CLAUDE_MD_TESTING.md; context-engineering | plan before writing; record source/write method per file; idempotent; close the exception on every exit; K-09, K-26 | installing into `~/.claude`; CLAUDE.md with hard-coded commands; installing plugins/MCP |
| skill:retro | 21 | 100 | 303 → 1,447 | BMAD-METHOD/skills/bmad-retrospective (SKILL, workflow, references/*); skill-creator/agents/{analyzer,comparator}; /tmp/ref/agents/plugins/incident-response/skills/postmortem-writing | skeleton first, re-runnable; list the sources; follow up on the previous retro; two decisions per bottleneck; minimum-sample rule (K-38); eval with a check the current version fails | multi-agent discussion; asking the human; writing ADRs; epic acceptance verdict |
| agent:analyst | 29 | 100 | 345 → 957 | agent-skills/skills/interview-me; BMAD-METHOD/skills/bmad-agent-analyst (+ assets); awesome…/08-business-product/business-analyst.md | stand on the business side; Outcome/…/Out of scope block; never invent NFR numbers; prioritizing when everything is "must have"; read-only Bash (K-52) | asking one question at a time and waiting; personas; designing the solution |
| agent:researcher | 28 | 100 | 334 → 844 | source-driven-development; research-analyst | as in the research skill; POC in its own worktree (K-48); inputs per playbook (K-68) | expert interviews, surveys |
| agent:architect | 29 | 100 | 348 → 866 | bmad-agent-architect; bmad-architecture; c4-container; awesome…/04-quality-security/architect-reviewer.md | settle only invariants; ratify before proposing; system mode writes arch-impact (K-46) | "also satisfy future needs" |
| agent:designer | 29 | 100 | 342 → 833 | api-and-interface-design; spec-driven-development; database-architect; api-designer | contract first; no task splitting (K-66) | language-specific naming rules; default pagination |
| agent:writer | 28 | 100 | 335 → 857 | documentation-and-adrs; docs-architect; awesome…/08-business-product/technical-writer.md | inputs per mode (K-67); never writes `Released:`/approvals | haiku model, WebFetch |
| agent:devops | 29 | 100 | 342 → 838 | ci-cd-and-automation; /tmp/ref/agents/plugins/cicd-automation/agents/deployment-engineer.md; /tmp/ref/agents/plugins/incident-response/agents/devops-troubleshooter.md; awesome…/03-infrastructure/devops-engineer.md | record the running version before deploy; red smoke = stop + propose; trigger only pipelines a human approved (STD-OPS-7, ADJ-24) | "fully automatic, no humans"; context-manager protocol; invented metrics |
| agent:maintainer | 29 | 100 | 346 → 830 | code-simplification; deprecation-and-migration; legacy-modernizer; awesome…/06-developer-experience/refactoring-specialist.md | as in the clean skill; release the branch for qa; write `tasks.md` (K-47, K-58) | "use proactively"; performance metrics |
| agent:coach | 29 | 100 | 350 → 958 | BMAD retrospective; postmortem-writing; everything-claude-code/rules/common/agents.md | one write list (K-43); design evals, do not run them; no blame; follow up on the previous retro | multi-agent discussion; asking the human |

Accompanying kit fixes (evidence from code or runs): K-06, K-08, K-09, K-24, K-26, K-27/K-43, K-28, K-30, K-38, K-39, K-40, K-44, K-45, K-46..K-75, K-78 (still open: K-53, K-62, K-65, K-72, K-76, K-77, K-79, K-80; plus K-18, K-25 from before) — `docs/kit-issues.md`.

After the evals and the end-to-end run, team-leader (1,105 words), intake (326), handbook (389), status, run, coach, make-skill, make-agent and audit-kit were tuned further for K-70..K-74; all still meet the bar (`kit-metrics.py --check` exits 0).
