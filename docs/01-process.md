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
| 7 | Acceptance | `/team:verify` | qa | `acceptance.md` (with Try it) | G4 on |
| 8 | Release | `/team:asbuilt`, `/team:pr`, `/team:release` | writer, tech-lead, devops | `asbuilt.md`, CHANGELOG, CLAUDE.md project block, PR | G5 always a human |
| 9 | Operations | `/team:intake --type bug`, `/team:clean`, `/team:ci`, `/team:retro` | team-leader, maintainer, devops, coach | `defects.md`, `debt.md`, `retro/` | — |

**Approving a gate:** add the line `Approved-by: <name> <YYYY-MM-DD>` at the top of the artifact (G5 uses `Approved-by-prod:`), or comment `@claude approve Gn` on the issue. A gate set to `false` in `.team/config.json` does not block.

**Status is computed, not stored:** `/team:status` reads the artifacts and tells you where a feature is. An enabled gate that is not yet approved blocks every later stage, even when the later artifacts already exist.

**Product before paperwork (ADJ-41):** the analyst's Read-back (you asked / you will see / switched on / not included / team additions, ≤ 5 lines) is shown to the human in every mode, before any code; each criterion quotes what it serves (caps S 5, M 12, L 24). Before `accepted`, qa runs the commit on a live instance with the feature switched on, walks the main flow where the requester works (a browser flow through any browser MCP) and hands the human ≤ 3 steps to try it.

**Lean docs (ADJ-41):** a feature folder holds only the stage artifacts (the table above plus `questions.md`, `review-NN.md`, `pr-body.md`, `source-*`), each under a KB budget (`limits.doc_kb`). `team.py docs <ID>` lists stray files and overruns; the write hook reminds at the moment of writing. The diff is read from git, never copied; rulings and reports live in return messages, commit bodies and in-place edits; process docs are committed once per stage.

**Artifact language:** artifact prose is written in `config.output_language` (`vi` by default, or `en`); machine-read anchors (`Approved-by:`, `## Definition of Done`, `Verdict: …`, statuses) stay in English. See `docs/04-profile.md`.

## Work size
The team calls only the roles the work needs (ADJ-36). A question, an explanation or a status check is answered by team-leader directly: no intake, no ID, no agent (Explore only when it spans several areas).

| Size | Signals | Chain |
|---|---|---|
| quick | Trivial: a text, a config value, one obvious line; ≤ 2 files; no schema/API/security change | intake → ONE dev called by team-leader → done (branch `team/<ID>`); no tech-lead, reviewer, qa or writer |
| S | The diff can be described in one sentence; ≤ 3 files; no schema/API change | intake → [short analyze for a feature, no G1] → build (tech-lead: 1 dev + 1 reviewer; acceptance written inside build, no qa) → pr (no As-Built) |
| M | One module; changes data or an API; 1–5 person-days | intake → analyze → [research] → plan (with a short `## Design`, ADJ-43) → build → verify → release; a separate design only in data-migration, integration, refactor |
| L | Several modules; new NFRs; > 5 person-days | all 9 stages; architecture is mandatory; the first task is a walking skeleton |

team-leader sets the size at intake. Force a size with `--size S|M|L` or the label `team:size:*`. A size change midway is recorded with its reason in `intake.md`.

## Ask or decide
- **`ask` (default):** ask only about unclear points whose consequences are LARGE or IRREVERSIBLE (deleting/migrating data, changing a public API, changing a business rule, cost). At most 5 questions per round, 2 rounds; each question has 2–4 options, a recommendation and the consequences. Small matters go into `## Assumptions decided by the team`.
- **`decide`:** no questions; every decision is recorded: what was chosen / why / the alternatives / how to fix it if wrong. Turn it on with `--decide`, the label `team:decide` or `default_mode`.
- **In CI:** questions become an issue comment + the label `team:needs-answer`, and the run stops with `WAITING_FOR_ANSWER`.
- Only the main session (team-leader) asks the human; other roles return their questions to team-leader (ADJ-01).

## The build loop
1. tech-lead picks the unblocked tasks from `tasks.md` and sends their devs in one message (a round).
2. dev (own worktree): write a failing test first → implement → `cmd.test_one` → `cmd.lint` → commit. This is the only test run per task.
3. One checkpoint per round (ADJ-42): tech-lead merges every finished task of the round into `team/<ID>`, with no test in between, then runs the full `cmd.test` once (ADJ-40). Green → one reviewer call covers everything merged since the last review and runs beside the next round's devs. Tests and review are never run per task. The reviewer works in a fresh context: tier 1 matches the spec → tier 2 quality; every finding carries an STD code; `major` only for a missed criterion, a test that cannot fail, security or data loss, a broken contract, an edit outside the touchpoints or an edge the criteria name (ADJ-39).
4. A `[risk]` task (authorization or secrets, migration or schema, money or data deletion, a contract used outside the feature, shared state) goes through the same checkpoint, but is ticked only after its review, so the tasks that depend on it wait.
5. One dev fixes a checkpoint's blockers/majors on one fix branch (≤ `max_rework` rounds); a tests-only fix closes its findings on its red-then-green evidence, a production fix is checked by the next checkpoint. One `review-NN.md` per checkpoint.
6. No tasks left, no open blocker/major, no production code after the last review → `/team:verify`.

### Results first (ADJ-43)
- **Before code:** size M goes from the spec straight to the plan, which carries a ≤ 40-line `## Design`; one research call per feature answers every open question at once.
- **No retest of an unchanged commit:** each round's green `cmd.test` writes the journal line `tested: <sha> <summary>`; verify and pr paste that line when the commit is the same, and run the suite only on a new commit (a rebase).
- **The lead sees progress:** after every stage the team-leader writes ≤ 3 lines in `output_language`: what works now, what is left, what is needed from the human. `team.py status` shows accepted work whose code is already in the main tree's branch as `DELIVERED` (nothing left for the team) and `--brief` folds it into one line.

A task is one vertical slice (1–4 criteria end to end, roughly 100–400 changed lines with tests, ≤ 6 files) and names concrete file paths; size M has at most 6 tasks, size L at most 12, more means several features. Every task pays a dev start-up, a merge and a test run, so tasks fold small pieces together instead of splitting them. The tech-lead decides local design points itself (names, internal signatures, fixtures); only a criterion, an outside contract, the schema, an ADR or a file outside the touchpoints goes back to the designer, all open points in one call. Two tasks that touch the same file never run in parallel; the build dispatches in rounds: each round is one message carrying every call that can start now (devs for ready tasks that share no file with a task in flight, fixes, the due checkpoint review), up to the dev and reviewer headcount, and never waits for a whole wave to be ticked (skill `build`). Independent Explore questions also go in one message. Nobody says "done" before pasting the output.

## Several features at once
One role can have several people: `limits.headcount.<role>` in `.team/config.json` (template defaults: dev 4 via `max_parallel_dev`, reviewer 4, architect 1, the other roles 2; a missing key means 1, dev from `max_parallel_dev`). A request with several independent items becomes one intake per item, run together. `/team:run --all` runs parallel waves: `team.py wave` picks every feature that can move now, caps each role at its headcount, keeps builds with overlapping `files:` apart and splits the team-wide dev/reviewer headcount between builds; the team-leader dispatches the whole wave in one message (skill `run`). The stages of ONE feature stay sequential.

## Several sessions at once
A project can run several Claude sessions at the same time, each with its own team. Each session works in its own lane: it records the items it works on and the files it holds (`team.py claim`), and sees the other lanes at start-up and in `/team:status`.
- Different items run in parallel with no question; the same item held by another session is a question for the human.
- The same file goes one session at a time (the task waits for a later round, other tasks keep running); different files run in parallel.
- IDs are allocated atomically; the main tree's branch never changes (feature branches are merged and tested in their own worktree).
Rules and commands: `handbook/sessions.md`.

## Stopping and escalation
The team stops when: a task is BLOCKED after `max_attempts`; `max_rework` is exceeded; it hits `DESIGN_CONFLICT` or a design-defect verdict; an enabled gate is not approved; `feature_budget_usd` is exceeded; it touches `protected_paths`; two rework rounds hit the same error.
Every stop states: the reason, which piece of work, who must do what, and the command to resume. Handling: `docs/guides/incidents.md`.

## Playbooks
17 playbooks in `workflows/`, chosen by type of work and then by size: see `docs/guides/decision-tree.md`.
