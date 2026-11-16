# Changelog

All notable changes to the kit are recorded here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [Semantic Versioning](https://semver.org/). Entries up to 0.3.0 are kept in their original Vietnamese (historical); entries from 0.4.0 on are English.

## [Unreleased]

## [0.6.9] - 2026-11-16

Results first: fewer steps before code, no retest of an unchanged commit, progress the lead can see (owner request, ADJ-43, SPEC-OVERRIDES entry 12, K-104).

### Added
- `team.py status`: `DELIVERED` — accepted work whose code is already in the main tree's branch (`team/<ID>` merged into HEAD, or its code commits `type(scope): … (<ID>)` reachable from HEAD after the branch was deleted); its Next says nothing is left for the team. `--brief` lists active work first and folds delivered items into `team: delivered N: …`. Tests in `test_team_status.sh`.
- team-leader and `/team:run`: after every stage, ≤ 3 lines for the human in `output_language`: what works now, what is left, what is needed from them.

### Changed
- Size M new-feature: `team.py next` goes from the spec to `/team:plan`; `plan.md` carries a ≤ 40-line `## Design` (template `plan.md` and `vi/`). `/team:design` stays for size L and the data-migration, integration, refactor playbooks.
- `/team:research`: one call per feature, every open question at once.
- No retest of an unchanged commit: each round's green `cmd.test` writes the journal line `tested: <sha> <summary>`; `/team:verify` (qa) and `/team:pr` paste it for the same commit and run the suite only on a new one; `/team:pr` rebases only when the base branch moved.

## [0.6.8] - 2026-11-16

One checkpoint per round: test and review together (owner request, ADJ-42, SPEC-OVERRIDES entry 11, K-103).

### Changed
- `/team:build` and tech-lead: after a round, every finished task and fix is merged with no test in between (the per-merge `cmd.test_one` of 0.6.6 is gone), the full `cmd.test` runs once, then ONE reviewer call covers everything merged since the last review (`REVIEWED..team/<ID>`), beside the next round's devs. Due at ≥ 3 unreviewed tasks, an unreviewed `[risk]` task, or the end.
- `[risk]` tasks are no longer reviewed alone before their merge: they join the checkpoint and are ticked only after it, so their dependents wait.
- Rework: one dev per checkpoint on `team/<ID>-fix-K`; the next checkpoint marks the old findings `ADDRESSED`/`NOT ADDRESSED`, no separate re-review call. Done = every task ticked, no open blocker/major, no production code after the last review.
- reviewer, dev, plan, `docs/01-process.md`, templates `tasks.md` and `review.md` (English and `vi/`).

## [0.6.7] - 2026-11-16

Product before paperwork: try it like the requester, read the request back, lean docs and lean tests (owner request, ADJ-41, SPEC-OVERRIDES entry 10, K-102).

### Added
- `team.py docs [<ID>]`: lists stray files in `docs/team/features/<ID>/` (only the stage artifacts are allowed: intake, questions, spec, research, arch-impact, design, plan, tasks, review-NN, acceptance, asbuilt, pr-body, source-*), artifacts over their KB budget, criteria over the size cap, and journal problems; `team.py status` adds one "Docs over budget" line and `--json` a `docs_problems` count.
- `protect.sh` checks every write under `docs/team/` (`team.py docs --hook`): a stray file, an artifact or journal over its budget after the write, or a Write over an existing journal (append with Edit) gets the rule as a reminder (`enforcement: "block"` stops it).
- Config `limits.doc_kb` (KB budget per artifact kind, a number or {S,M,L}) and `limits.max_criteria` (S 5, M 12, L 24).
- `/team:verify` step "Try it": on a running instance of the commit, the feature switched on, qa walks the main flow where the requester works (any browser MCP for a browser flow) and writes ≤ 3 steps for the human; `accepted` needs it. Size S writes the Try it row inside `/team:build`. Templates `acceptance.md` (+ `vi/`) get a `## Try it` section.
- qa lists browser MCP servers in `tools` (`mcp__claude-in-chrome__*`, `mcp__playwright__*`, `mcp__plugin_playwright_playwright__*`); `scripts/allowed-tools.txt` registers them.
- `/team:analyze` writes a Read-back block (you asked / you will see / switched on / not included / team additions) at the top of `spec.md` and in its return message; the team-leader shows it to the human in every mode, and shows qa's Try it steps after `accepted`.
- STD-TEST-9 (lean tests).

### Changed
- Spec criteria quote what they serve (`From` column); the team's own ideas go to Team additions; caps S 5 / M 12 / L 24, more → split. What was asked for is switched on by default.
- Size caps move from lines to KB (spec S 6 / M 15 / L 25, design M 30 / L 50, plan 12, tasks 12, review 6, acceptance 15, journal 20), checked by `team.py docs` instead of `wc -l`.
- `/team:build` no longer writes `diff.patch`; `/team:asbuilt` and writer read the diff with `git diff <base_branch>...team/<ID>`. Dev reports live in the return message and the commit body, never a `dev-T*.md` file. Process docs are committed once per stage, never per tick.
- STD-TEST-8 covers the edges the criteria or design name; other edges are the dev's call. ADR constraints are checked in review, not by a test suite per ADR. A task that replaces behavior retires its old tests, and qa accepts those deletions.
- `/team:intake` sizes the change, not its importance (L needs several modules and new NFRs; unsure → the smaller size).
- The team-leader never asks the human about the kit's own process (gates, merges, limits, red tests). Journals are appended with Edit.

## [0.6.6] - 2026-11-15

Tests run once per round, not after every merge (owner request, ADJ-40, SPEC-OVERRIDES entry 9, K-101).

### Changed
- `/team:build` and tech-lead: after each merge only the merged task's `test:` files run (`cmd.test_one`); the full `cmd.test` runs once per round, after the round's last merge. Green → the round's merged tasks are ticked; red → the merge that turned a test red is found (that test file at each merge of the round, oldest first), the task stays unticked and one dev fixes it on `team/<ID>-fix-K`, merged first in the next round. Rules in `skills/build/references/handoffs.md` § Tests in the loop.
- No dev call only to rerun tests for evidence: a missing GREEN comes from the tech-lead's merge check, a missing RED goes back in a rework call.
- dev: each test run is one foreground call (Bash `timeout` up to 600000 ms) that waits inside itself when the test site is busy, never a loop of short checks; reruns only after a change; the other test files of the touched module run once.
- `test.shared_state` (profile schema, `docs/04-profile.md`): now describes the `@shared-state` hold, not a per-merge cadence.

## [0.6.5] - 2026-11-15

Few, larger tasks; review by risk (owner request, ADJ-39, SPEC-OVERRIDES entry 8, K-100).

### Changed
- `/team:plan`: a task delivers 1–4 criteria end to end (~100–400 changed lines with tests, ≤ 6 files); fold small pieces, do not split them; caps M 6 / L 12 tasks, a bigger plan returns `BLOCKED` with a proposed feature split. `Receives:`/`Returns:` only for names other tasks or modules consume. `[risk]` marks tasks touching authorization or secrets, a migration or schema, money or data deletion, an outside contract or shared state.
- `/team:build`: a `[risk]` task is reviewed before its merge; other tasks merge on red-then-green evidence and share one checkpoint review (`REVIEWED..team/<ID>`, every 3 merged tasks and at the end; journal `reviewed: <sha>`). One `review-NN.md` per review call. Checkpoint findings go to one fix branch `team/<ID>-fix-K`; a tests-only fix merges without re-review. The tech-lead decides local design points itself and sends the rest to the team-leader in one report.
- `reviewer` and the handbook Finding format: `major` is defined (missed criterion, test that cannot fail, security or data loss, broken contract, edit outside the touchpoints, a named edge untested); other edges and hand-made mutants are minor and never block.
- `dev`: a private helper or test name that differs from the task text is the dev's call; only a consumed contract is a `DESIGN_CONFLICT`.
- `/team:design` answers a build's `DESIGN_CONFLICT` report in one call, in place in `design.md`; `/team:architect` reviews a design once.
- Templates `tasks.md` and `review.md` (English and `vi/`).

## [0.6.4] - 2026-11-14

Session lanes: several sessions on one project (owner request, ADJ-38, SPEC-OVERRIDES entry 7, K-99).

### Added
- `team.py claim` / `release` / `sessions` / `new-id` / `busy`: each Claude session records the items it works on and the files or `@resources` it holds in `.team/session/<session_id>.json`. Same item held by another live session → exit 3 `CONFLICT` (team-leader asks the human); a file another active session holds → exit 4 `BUSY` (the task waits for a later round); different work runs in parallel.
- `handbook/sessions.md`: the rules of session lanes (one place; skills and agents point to it).
- `@shared-state` (full `cmd.test`/`cmd.migrate` when `test.shared_state` is true) and `@main-tree` (the only way to move the main checkout off its branch) resources, expiring after 30 minutes.
- Config `limits.session_idle_min` (default 120): an idle lane keeps its items but its file claims no longer make others wait.
- Tests: `scripts/tests/test_sessions.sh`; lane cases in `test_hooks.sh`.

### Changed
- The session position replaces `.team/current.json` (retired): every stage runs `team.py claim <ID> --stage <stage> --agent <role>` instead of writing the shared file; hooks read this session's lane (`lib.sh`, `teamlib.py`).
- SessionStart registers the lane and lists the other live sessions and what they hold; SessionEnd (`handoff.sh`) releases every claim of the session; a resumed session reads its own handoff first.
- `protect.sh` reminds (blocks with `enforcement: "block"`) when an Edit/Write targets a file another active session holds, and records main-tree edits for 30 minutes.
- `team.py status` has a `Session` column (`this`, another session's id, `—`); `team.py wave` holds items other sessions hold; `team.py next` follows this session's position.
- intake: asks the human only when the same work is held by another session or open elsewhere; IDs come from `team.py new-id` (atomic, never the same ID twice).
- build/tech-lead: claim each task's files before its dev (`BUSY` → later round), release after the merge and on every exit; merges and `cmd.test` run in the feature worktree, never by switching the main tree. verify/qa/pr work in the feature worktree; playbook quick claims T1's files.
- `hooks/role-policy.json`: `.team/current.json` dropped from the write lists; stage exceptions follow the session position.

## [0.6.3] - 2026-11-13

Read lean, act more (owner request, ADJ-37, SPEC-OVERRIDES entry 6, K-98).

### Changed
- handbook: a lean reading rule replaces "Read STD-short before anything else": never re-read a file already in context or the running skill; files over 200 lines are read by section; only reviewer and qa read STD-short, once.
- build/tech-lead: `tasks.md` keeps only task lines, ticks and `baseline:`; BASE = `git merge-base team/<ID> team/<ID>-task-N`; one journal line per round; no re-reads of tasks.md, the journal or kit files in the loop. Handoffs carry the quoted criteria, the design section headings and the `baseline:` line.
- dev: reads only the touchpoints and the named design sections, runs no full suite (tech-lead runs `cmd.test` after each merge; quick runs it once), commits directly with git.
- reviewer: reads STD-short once and the named design sections only; memory files stay ≤ 40 lines.
- Tasks are vertical slices (one behavior with its tests, ≤ 5 files, ~15–30 minutes) instead of 2–5 minute steps.
- Size caps: spec.md S 60 / M 150 / L 250 lines; design.md M 300 / L 500 (amendments edit sections in place, no addendum files); plan.md 150; ≤ 4 lines per task.

## [0.6.2] - 2026-11-13

Right-size the team: only the roles the work needs (owner request, ADJ-36, K-97).

### Added
- Playbook `quick` (17th): a trivial change (text, config value, one obvious line; ≤ 2 files; no schema/API/security) → team-leader calls ONE dev, done when T1 is ticked; no tech-lead, reviewer, qa or writer.

### Changed
- A question, explanation or status check is answered by team-leader directly: no intake, no ID, no agent (team-leader step 3, `using-team`).
- Size S: build (tech-lead, 1 dev + 1 reviewer) writes `acceptance.md` itself; no `/team:verify` (qa) and no As-Built; `/team:pr` writes a short body. `team.py` sends an accepted size S feature straight to `/team:pr`. Supersedes ADJ-29.
- `team.py wave` holds quick work as a "team-leader step" and finished quick work as "done".

## [0.6.1] - 2026-11-13

Only `/team:release` stays human-only (owner decision, ADJ-35).

### Changed
- `/team:takeover`, `/team:onboard`, `/team:run`, `/team:retro`, `/team:audit-kit`, `/team:session`, `/team:ci` are callable by Claude (`disable-model-invocation` removed). team-leader runs takeover/onboard itself when a project has no profile; gates still apply (G0 before onboard, G5 before prod).
- `/team:release` (merge, tag, deploy) stays a command only the human types; `validate.sh` checks `HUMAN_ONLY_SKILLS="release"`.

## [0.6.0] - 2026-11-13

CLAUDE.md describes the project, and the team keeps it true (owner request, ADJ-32, SPEC-OVERRIDES entry 3). Build-loop fixes from the first real project (`erp_ai`, Frappe; K-82..K-89 in `docs/kit-issues.md`). Independent work runs at the same time (owner request, ADJ-33, SPEC-OVERRIDES entry 4; K-92..K-95).

### Added
- Project block in the project's `CLAUDE.md` (`<!-- project:start -->…<!-- project:end -->`, ≤ 150 lines): what the system is, commands copied from `cmd.*`, layout, domain terms, conventions, gotchas. Template `templates/artifacts/claude-md.md` (+ `vi/`).
- `scripts/check-claude-md.py`: one block of each kind, project before team, line budgets (150 / 25 / 200), no `{{` or `<fill:` left, no stale path in the project block. Read-only for every role. Tests in `test_check_claude_md.py`.
- `## CLAUDE.md` section in the As-Built and retro templates.
- Hooks remind instead of block (owner decision, ADJ-34, SPEC-OVERRIDES entry 5, K-96): config `enforcement` `"warn"` (default, also when the key is missing) lets every tool run and hands the broken rule to Claude as context; stop-check skips its lint/test pass. `"block"` restores the old stops. The team can now edit `.team/profile.json`/`config.json` in decide mode (K-91).
- STD-GIT-8 (owner decision): no AI attribution in commits or PRs. `check-git.sh` blocks a `git commit` or `gh pr create|edit|merge` whose message (inline or `-F`/`--body-file`) has a `Co-Authored-By:` trailer or a "Generated with Claude" line; the settings template sets `attribution` to empty and `includeCoAuthoredBy: false`.
- `test.shared_state` profile slot (K-87): tests that share one database or site never run as two full suites at once.
- Build baseline (K-88): the first build run records the red tests that already existed; green = nothing red outside that list.
- `team.py status` shows a Tasks column (`done/total`).

### Changed
- `/team:onboard` writes the project block from the takeover reports and adopts an old CLAUDE.md into it (one reason row per cut or corrected line in `onboarding.md`); re-running onboard on a project onboarded earlier adds the missing block.
- `/team:asbuilt` (writer) step 8 keeps the project block true after every feature (paths, `cmd.*`, terms, conventions, traps; prune before adding) and applies the open `## CLAUDE.md` lines of the latest retro. writer may now write `CLAUDE.md` (role-policy).
- `/team:retro` step 12 runs the check and turns repeated project-knowledge misses into CLAUDE.md lines instead of overlays.
- `/team:takeover` gives keep / cut / rewrite per CLAUDE.md section for onboard to apply; a wrong CLAUDE.md is no longer manual work for the human.
- Team block retitled "Working with the AI team", placed after the project block; its command line moved to the project block's Commands.
- role-policy allows each segment of a multi-segment `cmd.*` value (`cd ../.. && bench …`), and `render.py` adds one allow entry per subcommand, so tech-lead runs `cmd.test` itself instead of through a dev (K-82).
- `/team:run --until-blocked` and `--all` count ticked tasks as progress, so a build that ran out of turns is resumed instead of stopping the loop (K-83).
- Build: the review package travels in the reviewer handoff (range + dev's RED/GREEN lines), never as a `review-pkg-*` file or diff copy; one `review-NN.md` per task (K-84). Merged task branches and dev worktrees are removed after the tick (K-85). Every dev handoff carries the feature's recurring review findings (K-86).
- Build dispatches in rounds instead of waves (K-92): each round is ONE message with every call that can start now (devs for ready tasks that share no file with a task in flight, rework devs, reviewers); it never waits for a whole wave to be ticked.
- Config template defaults (K-93): `max_parallel_dev` 2 → 4; `headcount` reviewer 2 → 4, tech-lead, analyst, researcher, designer, qa, writer 1 → 2, architect stays 1. Projects onboarded earlier keep their values.
- Independent Explore questions go out as one Explore call each in one message (analyze, design, architect, takeover); intake gives each independent item of a request its own ID so the items run as one wave (K-94).
- `team.py metrics`/`scorecard` and `measure.py` count one row per `agent_id` (the last one): SubagentStop repeated tech-lead's row each time a dev or reviewer it called stopped (K-95).
- `session-start.sh` no longer creates `.team/` in repos that were never taken over; takeover and onboard write `.team/plugin_root` on first run (K-89).

## [0.5.0] - 2026-11-11

A team has fixed roles but a variable number of people per role (owner request, ADJ-31).

### Added
- `limits.headcount.<role>` in `config.json` and `config.schema.json` (optional; default 1; dev falls back to `max_parallel_dev`, reviewer to dev).
- `team.py wave [--json]`: the features that can move now, one agent each, capped per role; builds whose `tasks.md` `files:` overlap wait; the team-wide dev/reviewer headcount is split between the builds of a wave (`devs=`, `reviewers=`). Tests in `test_team_status.sh`.
- `/team:run --all`: parallel waves; the team-leader sends every wave item as an Agent call in ONE message (`skills/run/references/parallel-wave.md`).
- `teamlib.py agent-feature`, `lib.sh` `hook_feature` / `hook_stage` / `build_active`.

### Changed
- Build flag is per feature: `.team/active-build-<ID>` (the old `.team/active-build` still counts) in `build`, tech-lead, role-policy, gitignore, evals.
- `stop-check.sh` checks the research Sources of the researcher's own feature (read from its transcript) instead of `current.json`; `scorecard.sh` records the subagent's own feature. Tests in `test_hooks.sh`.
- `settings.json.tmpl` allows the commands forked skills used to grant (`cat`, `ls`, `git branch/rev-parse/merge/show/ls-tree/fetch/rebase/push`, `.team/active-build-*`), because wave agents do not get a skill's `allowed-tools`. Projects onboarded earlier add them by hand.
- `log-run.sh` is called with `--feature` from `run`.

## [0.4.1] - 2026-11-11

### Changed
- Model routing by the shape of the work (owner decision, `SPEC-OVERRIDES.md` entry 2): team-leader, tech-lead → fable; dev, maintainer, devops → opus; analyst, researcher, coach → sonnet; architect, designer, reviewer, qa stay opus; writer stays sonnet. Updated in `agents/*.md`, `templates/project/team/config.json`, `docs/02-team.md`, `make-agent` and its agent template, `GUIDE-VI.md`.
- Build runs in waves (owner request): ready tasks that share no file are dispatched together, one Agent `team:dev` call per task in ONE message (each in its own worktree), up to `limits.max_parallel_dev`; their reviewers likewise; merges stay serial. Before, the loop picked one task at a time, so `max_parallel_dev` was never used. Updated in `skills/build`, `agents/tech-lead.md`, `docs/01-process.md`.
- `scripts/audit-xref.py` skips `docs/requirements/` and `docs/acceptance/` in its name checks, like `check-lang.py` and `validate.sh`.

### Added
- `docs/requirements/raw/`: the owner's raw inputs (understanding document v1, prompt chain P0–P6), linked from `docs/00-overview.md`.

## [0.4.0] - 2026-11-10

Language switch (P9; owner decision, `SPEC-OVERRIDES.md` entry 1): AI-facing text is English, owner-facing Vietnamese lives only in `GUIDE-VI.md`, and artifacts written inside a project follow the new `output_language` slot (default `vi`). Machine-read anchors never change language. Semantics are unchanged: same roles, tools, models, gates, stages, playbooks, slots, scripts, hooks, artifact paths, 86 STD rules, section structure and word-budget bands.

### Converted to English (files per group, commits `docs(lang): …`)
- handbook 7 (STD.md: 86 rules before and after; STD-short regenerated) · agents 13 · always-loaded skills 5 · discipline skills and references 41 · workflows 21 · templates and profiles 71 (25 English artifact templates, 25 new Vietnamese copies in `templates/artifacts/vi/`, project templates, schemas, profiles) · docs 21 · README and CLAUDE.md 2 · evals 27 · scripts, tests and hooks 41.
- Skill descriptions start with `Use when …`, agent descriptions with `Delegate when …`; required headings are English (`scripts/skill-sections.txt`, `agent-sections.txt`, workflow headings in `validate.sh`).
- PR-body headings are now `## Feature`, `## Why`, `## What changed`, `## How verified` (asbuilt writes them, pr greps them).
- Hook block messages are English and carry the STD code (`BLOCKED (STD-SEC-1): …`); `role-policy` and `research` blocks have no STD rule and keep their hook name (explained in the guide).
- `team.py` prints English and still reads old Vietnamese intake/verdict labels.

### Added
- `output_language` in `templates/project/team/config.json` and `config.schema.json` (enum `vi` | `en`, default `vi`); the handbook skill states the artifact-language rule once (template folder by language, prose in that language, journal lines included, anchors English); writing skills and agents point to it.
- `GUIDE-VI.md`: the owner's Vietnamese control file — 10 hand-written sections (incl. a 59-pair Vietnamese ↔ English glossary and the owner's decision log in section 9) and 8 blocks generated by `scripts/gen-vi-guide.py` from the repo (26 skills, 13 agents, 16 playbooks, gates, every config/profile key, 86 STD codes, anchors, stats); one-liners in `scripts/vi-strings.json`.
- `scripts/anchors.txt` (anchor list + forbidden translated forms), `scripts/check-lang.py` (no translated anchor; no Vietnamese outside the allowlist), `scripts/diff-structure.py` (structure proof between two refs), `scripts/measure-context.py` (chars/words/tokens; tiktoken optional), `scripts/heading-map.txt`.
- `SPEC-OVERRIDES.md`; amendment to A5 in `docs/requirements/ban-hieu-yeu-cau.md`; ADJ-30 in `docs/00-overview.md`; `docs/research/language-switch.md`.

### Validator
- `validate.sh --strict` now also runs `check-lang.py` and `gen-vi-guide.py --check` (stale generated blocks or a skill/agent/STD code/config key without a Vietnamese line → FAIL); historical records (`docs/acceptance/**`, `docs/requirements/**`) are skipped by the kit-path scan.

### Measured (`docs/research/language-switch.md`)
- Always-loaded context: −6.3% tokens with `o200k_base`, −27.7% with `cl100k_base` (proxies; Claude's tokenizer is not public). Per-feature load: −5.4% / −27.0%. The saving is smaller than expected: English bodies were deepened to stay in the word-budget bands (characters +15%).
- Evals (`evals/RESULTS.md`, "Language switch"): using-team s1 4/5 → 5/5, verify s1 4/4 → 4/4, analyze s1 4/4 → 4/4 (cost −20%), asbuilt s1 5/8 → 8/8 (heading change); no regression.
- End-to-end on fresh copies of the sample project: `output_language: vi` → assessment, spec, review, acceptance in Vietnamese with English anchors; `en` → all artifacts English. The `vi` run wrote journal lines in English (K-81), fixed and re-run: journal in Vietnamese.

### Fixed during P9
- K-81: journal lines (team-leader reason lines, build/verify lines) ignored `output_language`.
- check-lang and the guide skipped heading anchors (`## …` lines) when loading `anchors.txt`.
- Handbook: `output_language` defaults to `vi` when no `.team/config.json` exists yet (takeover).

## [0.3.0] - 2026-11-10

Vòng 2 nâng chất lượng (P7): 21 mục còn lại trong backlog được viết lại tới chuẩn; mọi skill và agent (39/39) đạt chuẩn. Sửa 4 major và 2 blocker tìm thấy khi đọc tham khảo và viết lại.

### Viết lại tới chuẩn (chữ trước → sau)
- Skill đầy đủ (10 mục, kèm `references/`): asbuilt 266 → 1.527, release 320 → 1.364, research 294 → 1.551, architect 277 → 1.431, design 277 → 1.507, ci 296 → 1.348, clean 298 → 1.363, audit-kit 272 → 1.211, make-skill 316 → 1.383, make-agent 278 → 1.327, session 260 → 1.273, onboard 393 → 1.250, retro 303 → 1.447.
- Agent (10 mục, ví dụ tin trả, tin dừng 4 dòng): analyst 345 → 957, researcher 334 → 844, architect 348 → 866, designer 342 → 833, writer 335 → 857, devops 342 → 838, maintainer 346 → 830, coach 350 → 958.
- Trung vị chữ: skill đầy đủ 309,5 → 1.436,5; agent 348 → 924; skill kỷ luật 1.502 (≥ 1.500). Mục đạt chuẩn: 18/39 → 39/39; `scripts/quality-backlog.txt` rỗng.
- Tham khảo vòng 2: agent-skills (documentation-and-adrs, shipping-and-launch, source-driven-development, api-and-interface-design, ci-cd-and-automation, code-simplification, deprecation-and-migration, observability-and-instrumentation, security-and-hardening, context-engineering), superpowers writing-skills, anthropics skill-creator, BMAD (architecture, analyst, retrospective), everything-claude-code (hooks, rules, cài đặt), wshobson/VoltAgent agents (`docs/research/kit-audit-round2.md`, `docs/credits.md`).

### Security
- K-24: `protect.sh` gắn vào PreToolUse Bash: lệnh shell ghi/xóa `.git/`, settings, profile/config, `protected_paths` bị chặn (chuyển hướng, `tee`, `rm`, `mv`, `cp`, `sed -i`, `chmod`, `dd`…) cho mọi vai.
- K-39: chỉ-đọc không còn lọt qua `sed e/w`, `sort -o`, `uniq IN OUT`, `tree -o`, `rg --pre`, `date -s`, `file -C`, `>&file`, `<>`; bỏ `mkdir`.
- K-40: script chỉ-đọc so theo đường dẫn thật dưới `<kit>/scripts/`; script có ghi (`log-run.sh`, `team.py scorecard`) cần quyền ghi đích.
- K-49: agent tạm có dấu `team: temp` chịu vai `_temp` (Bash chỉ-đọc + git cơ bản + `cmd.*`, chỉ Explore).
- K-26: ngoại lệ onboard chỉ cho `cp` từ `<kit>/templates/`.
- K-75 (từ audit-kit trong end-to-end): chặn tiền tố env nguy hiểm (`GIT_EXTERNAL_DIFF=`, `GIT_CONFIG_*`, `BASH_ENV=`, `sudo`), tên dài viết tắt của GNU (`sed --in=`, `sort --o…/--com…`), `git grep --open-files-in-pager`, `sort -uo`; đích chuyển hướng tính theo `cd`; JSON hook hỏng hay thiếu `role-policy.json` → chặn thay vì cho qua; `protect-bash` nhận `sort -o`.

### Fixed
- K-46 (blocker): architect chế độ `system` viết thêm `arch-impact.md` của feature để mang cổng G2.
- K-47 (blocker): `team.py` không còn kẹt với playbook không có analyze/plan (bug-fix, hotfix, refactor, dependency-upgrade, spike, ci-fix, docs-only); `/team:clean` ghi `tasks.md` để refactor tới `built`.
- K-06: batch workflow, `team-feature.yml`, `weekly-retro` sinh `--allowedTools` từ `permissions.allow`.
- K-70: `intake` để Claude gọi được (ADJ-28) — `using-team` trỏ tới một skill chỉ người gọi được. K-73: team-leader đi tiếp tới khi gặp cổng/câu hỏi/chặn, thay vì dừng sau mỗi giai đoạn. K-71: skill gõ đường dẫn kit thật thay cho `$(cat .team/plugin_root)` (headless đòi duyệt). K-74: audit-kit ghi dần, chạy lại làm tiếp.
- K-48 POC của researcher trong worktree riêng; K-50 `session save` không còn bị hook ghi đè; K-52 analyst/architect/designer/writer có Bash chỉ-đọc; K-56 khe CI rỗng hiện cảnh báo thay vì `true`.
- K-08, K-09, K-27/K-43, K-28, K-30, K-38, K-44, K-45, K-51, K-54, K-55, K-57..K-61, K-63, K-64, K-66..K-69 (`docs/kit-issues.md`).

### Changed
- Mẫu PR: `## Vì sao`, `## Đổi gì`, `## Cách kiểm` tách riêng (pr grep đúng bốn tiêu đề); mẫu ADR thêm `## Ràng buộc`; mẫu asbuilt thêm `## Nợ sau G4`, `## Rollback`; mẫu kit-issues dùng cột và mức của repo kit; mẫu design bỏ cột `task`; registry có loại, bằng chứng, ca thử.
- `/team:clean` thêm loại `deprecate`, `observe`; nhánh `team/<ID>`.
- Skill tạm theo 8 nội dung SPEC §9 (300–1.000 chữ); chuẩn đầy đủ khi đưa lên kit.
- ADJ-23..ADJ-29 trong `docs/00-overview.md`.

### Eval và end-to-end
- `evals/RESULTS.md` Round 2: using-team s1 5/5 → 5/5 (sau hai lần chạy lộ K-70, K-73 và sửa); verify s1 4/4 → 4/4; asbuilt s1 (mới) 6/7 → 7/7; make-skill s1 không kết luận được (K-72).
- End-to-end trên dự án mẫu mới: onboard dừng đúng ở `clean-first`; BUG-001 (bug-fix, không spec/plan) build 1 vòng sửa → verify accepted 7/7 → dừng ở G4; retro 0 đề xuất, 4 theo dõi; audit-kit hết lượt (K-74), 7 phát hiện mới (`docs/kit-issues.md`).

### Còn mở
- K-53 (major): chưa có khe `deploy.prod`/`deploy.rollback` — đề xuất cho người quyết; tạm dùng `docs/team/ci.md` (ADJ-24).
- K-72 (major, giới hạn Claude Code): `-p` không ghi được `.claude/skills/**`, `.claude/agents/**` — make-skill/make-agent chỉ tạo ở phiên tương tác.
- K-18, K-25, K-62, K-65, K-76, K-77, K-79, K-80 (minor).

## [0.2.1] - 2026-11-09

### Security
- K-41: chặn `git -c` với khóa nguy hiểm (`alias.*`, `core.hooksPath`, …) và `--exec-path` — bỏ qua hook hoặc chạy shell tùy ý.
- K-42: `takeover` thu hẹp `allowed-tools` từ `Bash(bash *)` về đúng hai script của kit.
- Ghi nhận từ `/team:audit-kit` trên v0.2.0: K-39..K-45 (`docs/kit-issues.md`).

## [0.2.0] - 2026-11-09

Vòng 1 nâng chất lượng (P7): cùng vai, giai đoạn, cổng, artifact và khe; viết lại cách skill/agent làm việc, có bằng chứng.

### Viết lại tới chuẩn (chữ trước → sau)
- Skill nạp thường xuyên (≤ 400 chữ, 4 mục): using-team 200 → 395, handbook 182 → 375, status 138 → 273, run 189 → 313, intake 194 → 305, feedback 222 → 263.
- Skill đầy đủ (1.200–2.500 chữ, 10 mục, kèm `references/`): analyze 325 → 1.590, plan 282 → 1.316, takeover 433 → 1.510, build 350 → 1.504, verify 274 → 1.510, commit 242 → 1.501, pr 290 → 1.425.
- Agent (600–1.200 chữ, 10 mục, ví dụ tin trả, tin dừng 4 dòng): team-leader 345 → 1.062, tech-lead 342 → 945, dev 342 → 959, reviewer 349 → 946, qa 337 → 902.
- Trung vị chữ của 8 skill kỷ luật: 297,5 → 1.502,5. Mục đạt chuẩn: 0/39 → 18/39 (100% mục đã viết lại).
- Tham khảo: addyosmani/agent-skills, obra/superpowers, wshobson/agents, VoltAgent subagents, BMAD-METHOD (`docs/research/reference-kits.md`, `docs/credits.md`).

### Validator
- `scripts/kit-metrics.py` (đo, score 0–100, `--check`); chuẩn trong `scripts/skill-budgets.txt`, `skill-sections.txt`, `agent-sections.txt`.
- Bỏ ngân sách cũ 200/500 chữ và trần 350 chữ cho agent, bỏ danh sách 8 tiêu đề cũ; `validate.sh` chạy `kit-metrics.py --check`. Mục chưa đạt: `scripts/quality-backlog.txt` (21 mục, chỉ được rút ngắn).

### Eval (`evals/RESULTS.md`, Round 1)
- using-team s1: BEFORE 3/5 → AFTER 5/5 (AFTER có analyze + reviewer; BEFORE giao thẳng dev, bỏ review).
- verify s1: 4/4 → 4/4 (rẻ hơn 8%); analyze s1: 4/4 → 4/4.

### Vấn đề của kit
- Đóng: K-10, K-15, K-16, K-19, K-33, K-34 (viết lại); K-35 DoD lệch thời điểm verify/asbuilt, K-36 file mới trong worktree bị chặn, K-37 thay thế `$(cat .team/plugin_root)` bị chặn (blocker, sửa trong vòng).
- Mở: K-06, K-24 (major), K-08, K-09, K-18, K-25..K-28, K-30, K-38 (minor) — `docs/kit-issues.md`.

## [0.1.0] - 2026-11-09

Bản dùng được đầu tiên của plugin `team`. Đã chạy end-to-end trên dự án mẫu: takeover → G0 → onboard → một feature cỡ S (analyze → build → verify, dừng ở G4) → retro.

### Bộ kit gồm
- 13 agent (`agents/`), 26 skill (`skills/`), 16 playbook + 4 batch workflow (`workflows/`).
- Hook cho 8 sự kiện qua 9 script (`hooks/hooks.json`, `hooks/role-policy.json`); tổng 25 script bash/python3 stdlib trong `scripts/`.
- Sổ tay `handbook/STD.md`: 12 mảng, 86 quy tắc, checklist review (10) và nghiệm thu (6); `STD-short.md` sinh tự động.
- 6 profile (`_template`, python, node-ts, go, java-maven, flutter), 3 schema, 25 template artifact, 15 template dự án (CLAUDE.md, settings, rules, GitHub/GitLab CI, PR/issue, CODEOWNERS, gitignore).
- Test: 62 ca hook, 23 ca `team.py status`, 9 unit test `measure.py`; `validate.sh --strict` (gồm `audit-xref.py`) chạy trong CI.
- Eval cho 8 skill kỷ luật (`evals/`, `run-eval.sh`); kết quả trong `evals/RESULTS.md`.

### Hạn chế đã biết
- Mở (major): K-06 headless ở thư mục chưa được tin phải truyền `--allowedTools`; K-15 định nghĩa `max_agents_per_feature` và verify cỡ S; K-24 Bash của vai `bash: any` không qua `protect.sh`. Chi tiết và minor: `docs/kit-issues.md`.
- Ngôn ngữ văn xuôi là tiếng Việt; ngân sách chữ đếm theo âm tiết nên thân skill/agent còn ngắn (P7 sẽ nâng).
- Phạm vi v2 theo SPEC: GitLab CI đầy đủ (hiện là khung), scorecard nâng cao, canary tự động, đưa skill tạm lên kit, cấu hình MCP mẫu.

### Đã sửa khi chạy end-to-end (P6)
- Blocker: K-01 `cmd.test_one` sai chỗ thay (schema bắt `{file}`), K-02 cổng theo cỡ, K-03 quyền đọc kit lần đầu, K-11 task in đậm không được tính.
- Major: K-04/K-12 ghi file bằng Write, K-05 CHANGELOG ở gốc, K-13 lệnh chỉ-đọc bị chặn nhầm, K-14 worktree vòng sửa, K-20 eval ghi trong thư mục plugin, K-21..K-23 lỗ hổng chỉ-đọc, matcher cài cục bộ, vùng luôn-cho-ghi quá rộng.

### Added (P1–P5)
- Khung repo: manifest plugin `team` và marketplace `automation-ai`.
- `scripts/validate.sh` (kiểm tĩnh, `--strict`) và `scripts/install-local.sh` (cài cục bộ).
- `SPEC.md`, `README.md`, `CLAUDE.md`, tài liệu `docs/` và `docs/guides/`.
- CI `validate.yml` (tạm `continue-on-error` tới P4).
- Sổ tay kỹ thuật `handbook/STD.md` (12 mảng, 86 quy tắc, 2 checklist) và bản rút gọn sinh tự động `STD-short.md`.
- Phụ lục `tool-selection.md`, `tool-map.md`, `who-calls-whom.md`.
- Schema `profile.schema.json`, `config.schema.json`; `scripts/check-profile.py`; `scripts/gen-handbook-short.py`.
- Profile mẫu: `_template`, `python`, `node-ts`, `go`, `java-maven`, `flutter`; config mặc định `templates/project/team/config.json`.
- `validate.sh` kiểm bản rút gọn cũ/sửa tay và kiểm profile/config theo schema.
- 13 agent trong `agents/` (hợp đồng 8 mục, ≤ 350 từ) và skill `handbook`, `using-team`.
- `scripts/gen-team-table.py` sinh bảng vai trong `docs/02-team.md`; `scripts/allowed-tools.txt`.
- `validate.sh` kiểm agent: tiền tố mô tả, tool trong allowlist, 8 tiêu đề đúng thứ tự, ngân sách chữ, bảng vai đồng bộ.
- 16 playbook, `workflows/README.md` (bảng tín hiệu → playbook) và 4 batch workflow.
- 24 skill còn lại; `skills/README.md`, `docs/guides/want-x-type-y.md`, `docs/guides/decision-tree.md` sinh bằng `scripts/gen-guides.py`.
- Khe config mới `limits.max_temp_skills` (mặc định 5).
- `validate.sh --strict` bắt buộc trong CI; kiểm cấu trúc skill/playbook, `agent: team:<vai>`, đường dẫn kit (`scripts/pending-paths.txt`).
- Hook `hooks/hooks.json` + `hooks/role-policy.json`; script `lib.sh`, `teamlib.py`, `protect.sh`, `check-git.sh`, `role-policy.sh`, `format.sh`, `stop-check.sh`, `check-structure.sh`, `session-start.sh`, `handoff.sh`, `log-session.sh`, `scorecard.sh`, `log-run.sh`, `detect-stack.sh`, `explore-cache.sh`, `render.py`, `team.py`, `measure.py`.
- 22 template artifact, `stage-result.json`, template dự án (CLAUDE.md, settings, rules, GitHub/GitLab CI, PR/issue, CODEOWNERS, gitignore).
- Test `scripts/tests/` (hook, team.py status, measure.py) chạy trong `validate.sh --strict` và CI.
- `install-local.sh` nối hook và bỏ tiền tố plugin khi cài cục bộ.
