# 01 — Process

Source of truth: `SPEC.md` §4–§5. This page is the quick read for humans. Adjustments: `docs/00-overview.md` (ADJ-09).

## Nine stages and their gates
Artifacts live in `docs/team/features/<ID>/` unless stated otherwise.

| # | Stage | Command | Role | Artifact | Default gate |
|---|---|---|---|---|---|
| G0 | Project takeover | `/team:takeover` | team-leader (+Explore, researcher) | `docs/team/assessment.md`, `ai-readiness.md`, ... | G0 on for existing projects |
| 0 | Request intake | `/team:intake` | team-leader | `intake.md` | — |
| 1 | Analysis | `/team:analyze` | analyst | `spec.md` (with DoD) | G1 on |
| 2 | Research | `/team:research` | researcher | `research.md` + cache `docs/team/research/` | — |
| 3 | Architecture | `/team:architect` | architect | `docs/team/architecture.md` or `arch-impact.md`, `adr/` | G2 on |
| 4 | Detailed design | `/team:design` | designer | `design.md` | G2b off |
| 5 | Planning | `/team:plan` | tech-lead | `plan.md`, `tasks.md` | G3 on |
| 6 | Build | `/team:build` | tech-lead → dev, reviewer | code, commits, `review-NN.md` | — |
| 7 | Acceptance | `/team:verify` | qa | `acceptance.md` | G4 on |
| 8 | Release | `/team:asbuilt`, `/team:pr`, `/team:release` | writer, tech-lead, devops | `asbuilt.md`, CHANGELOG, PR | G5 always a human |
| 9 | Operations | `/team:intake --type bug`, `/team:clean`, `/team:ci`, `/team:retro` | team-leader, maintainer, devops, coach | `defects.md`, `debt.md`, `retro/` | — |

**Approving a gate:** add the line `Approved-by: <name> <YYYY-MM-DD>` at the top of the artifact (G5 uses `Approved-by-prod:`), or comment `@claude approve Gn` on the issue. A gate set to `false` in `.team/config.json` does not block.

**Status is computed, not stored:** `/team:status` reads the artifacts and tells you where a feature is. An enabled gate that is not yet approved blocks every later stage, even when the later artifacts already exist.

**Artifact language:** artifact prose is written in `config.output_language` (`vi` by default, or `en`); machine-read anchors (`Approved-by:`, `## Definition of Done`, `Verdict: …`, statuses) stay in English. See `docs/04-profile.md`.

## Work size
| Size | Signals | Chain |
|---|---|---|
| S | The diff can be described in one sentence; ≤ 3 files; no schema/API change | intake → short analyze (no G1) → build (1 dev + reviewer) → verify (qa, shortened check; counts toward the 3-role cap: analyst, tech-lead, qa — K-15) → release |
| M | One module; changes data or an API; 1–5 person-days | intake → analyze → [research] → design → plan → build → verify → release |
| L | Several modules; new NFRs; > 5 person-days | all 9 stages; architecture is mandatory; the first task is a walking skeleton |

team-leader sets the size at intake. Force a size with `--size S|M|L` or the label `team:size:*`. A size change midway is recorded with its reason in `intake.md`.

## Ask or decide
- **`ask` (default):** ask only about unclear points whose consequences are LARGE or IRREVERSIBLE (deleting/migrating data, changing a public API, changing a business rule, cost). At most 5 questions per round, 2 rounds; each question has 2–4 options, a recommendation and the consequences. Small matters go into `## Assumptions decided by the team`.
- **`decide`:** no questions; every decision is recorded: what was chosen / why / the alternatives / how to fix it if wrong. Turn it on with `--decide`, the label `team:decide` or `default_mode`.
- **In CI:** questions become an issue comment + the label `team:needs-answer`, and the run stops with `WAITING_FOR_ANSWER`.
- Only the main session (team-leader) asks the human; other roles return their questions to team-leader (ADJ-01).

## The build loop
1. tech-lead picks an unblocked task from `tasks.md`.
2. dev (own worktree): write a failing test first → implement → `cmd.test_one` → `cmd.lint` → commit.
3. reviewer (fresh context): tier 1 matches the spec → tier 2 quality; every finding carries an STD code.
4. dev fixes blockers/majors (≤ `max_rework` rounds).
5. tech-lead ticks the task, writes `review-NN.md`, merges into `team/<ID>`, runs `cmd.test`.
6. No tasks left → `/team:verify`.

A task takes 2–5 minutes and names concrete file paths. Two tasks that touch the same file never run in parallel. Nobody says "done" before pasting the output.

## Stopping and escalation
The team stops when: a task is BLOCKED after `max_attempts`; `max_rework` is exceeded; it hits `DESIGN_CONFLICT` or a design-defect verdict; an enabled gate is not approved; `feature_budget_usd` is exceeded; it touches `protected_paths`; two rework rounds hit the same error.
Every stop states: the reason, which piece of work, who must do what, and the command to resume. Handling: `docs/guides/incidents.md`.

## Playbooks
16 playbooks in `workflows/`, chosen by type of work and then by size: see `docs/guides/decision-tree.md`.
