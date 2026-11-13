# Changelog

All notable changes to the kit are recorded here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [Semantic Versioning](https://semver.org/). Entries up to 0.3.0 are kept in their original Vietnamese (historical); entries from 0.4.0 on are English.

## [Unreleased]

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
