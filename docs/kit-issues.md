# Kit issues (v0.1.0)

Sources: the P6 end-to-end run on the sample project `sample-existing` (Python, 24 commits), `/team:audit-kit` on the kit repo itself, and `scripts/audit-xref.py`. Severity: **blocker** (fixed in v0.1.0) · **major** · **minor**. Majors/minors still open are the v0.2 backlog.

| ID | Severity | Status | Where | Symptom | Fix |
|---|---|---|---|---|---|
| K-01 | blocker | fixed | takeover → profile-proposal | Proposed `cmd.test_one` with a `{module}` placeholder and an invented slot `cmd.test_all`; onboard wrote them into the profile verbatim; `stop-check.sh` only substitutes `{file}`, so every build task would be blocked. | The schema requires `cmd.test_one`/`cmd.format` to contain `{file}` (`check-profile.py` adds `pattern`); the profile-proposal template lists the correct slot names and the `{file}` rule. Takeover + onboard re-run: `python3 -m unittest {file}`, profile valid. |
| K-02 | blocker | fixed | run | A size S job stopped at G1 even though ADJ-09 drops G1 for size S: team-leader read `gates` in config itself instead of trusting `team.py`. | Skill `run`: gates come ONLY from the output of `team.py`. |
| K-03 | blocker | fixed (P5) | first onboard | A session without settings cannot read the kit directory. | `takeover`, `onboard` have `Read Glob` in `allowed-tools`; `Read(//<kit>/**)` goes into `settings.local.json`. |
| K-04 | major | fixed | handbook / headless | Writing `current.json` and the journal through Bash redirection is denied under `-p`; the journal lacked the line for the analyst call. | Handbook: write files with Write/Edit; build writes `diff.patch` with Write. |
| K-05 | major | fixed | protect.sh | Creating `CHANGELOG.md` at the root was blocked when `.` is not in `allowed_new_file_roots`, while the DoD requires a CHANGELOG. | `protect.sh` always allows creating `CHANGELOG.md` at the root; test case added. |
| K-06 | major | fixed (round 2) | headless / CI | In a directory that is not trusted (workspace trust), `-p` ignores the project's `permissions.allow`; `--allowedTools` must be passed. | The batch workflows, `team-feature.yml`, `weekly-retro` and `docs/08-channels.md` generate `--allowedTools` from `permissions.allow` in `.claude/settings.json` (jq), so stack commands are never copied by hand. |
| K-07 | minor | fixed | takeover | 11-file repo: T2 read files directly, not through Explore (reason recorded). | `tiers.md`: repos with < 30 files may be read directly at T2, stated in the tier table. |
| K-08 | minor | fixed (round 2) | takeover | Miscounted the lines of CLAUDE.md (116 instead of 120). | `detect-stack.sh` prints `ai_files` (line counts of CLAUDE.md, AGENTS.md, .claude/CLAUDE.md, CLAUDE.local.md, counted by the machine); takeover takes the numbers from there. |
| K-09 | minor | fixed (round 2) | onboard | AI-readiness was `clean-first`, yet onboard still ran once G0 was approved, only reminding to rewrite CLAUDE.md as manual work. | onboard reads the `Verdict:` line of ai-readiness: `clean-first` → stops before any write and asks for a separate confirmation, or re-run with `--accept-clean-first`; always closes with `stage: idle`. |
| K-10 | minor | fixed (P7) | feedback | The `feedback` skill appends to `feedback.jsonl` with `jq >>`; under `-p` this can be denied like K-04. | v0.2: `log-run.sh --feedback` writes the feedback line. |
| K-11 | blocker | fixed | team.py | `- [x] **T1 — …**` (bold T) was not counted as a ticked task → status stuck at `planned`, team-leader did not move on. | The task regex accepts `*`, `_`, `` ` `` before the task ID; test case added. |
| K-12 | major | fixed | team-leader | team-leader still wrote `current.json` and the journal with `printf` in Bash → denied under `-p`; journal lines missing. | The agent body says "(Write)" explicitly in steps 4 and 7. |
| K-13 | major | fixed | role-policy | Read-only commands blocked: reviewer `git worktree list`, `git ls-tree`; tech-lead `cd <worktree>`. | Added `cd` and git `ls-tree`, `for-each-ref`, `show-ref`, `worktree list` to the read-only list; test cases. |
| K-14 | major | fixed | dev / worktree | Rework round: the new dev sits in a different worktree and tries to point git at the old worktree → Claude Code refuses. | dev step 1: in a rework round, `git switch` to the task branch inside its own worktree. |
| K-15 | major | fixed (P7) | build / max_agents_per_feature | Size S used 2 devs + 2 reviewers (1 rework round) + analyst + tech-lead + qa > the S cap of 3; SPEC says size S has "automated verify, no separate qa", but the `verify` skill always forks to qa. | P7: the cap = the number of distinct ROLES team-leader calls itself (including forked skills), not counting the dev/reviewer that tech-lead calls or re-calls; size S = analyst, tech-lead, qa = 3. qa still does acceptance for size S (with a reduced automated check). |
| K-16 | minor | fixed (P7) | team-leader | Read `gates` in config and assumed G1 applies to size S even though `team.py` reported READY. | Added an "Applicable gates" column to `team.py status`; tracked in the next round. |
| K-17 | minor | fixed | gitignore.tmpl | Subagents' `.claude/worktrees/` shows up as untracked files. | Added to `gitignore.tmpl`. |
| K-18 | minor | open | scorecard.sh | `result` is guessed from words in the last message: dev wrote `DESIGN_CONFLICT`, Explore got `approve` just because the word appears. | v0.2: roles return a JSON line following `stage-result.json`; scorecard reads the `verdict` field. |
| K-19 | minor | fixed (P7) | team-leader | With a feature waiting at G4, team-leader refused new requests (a gate blocks its feature, not the whole team). | v0.2: stated explicitly in team-leader/intake: a gate blocks only its own feature. |
| K-20 | major | fixed | evals/run-eval.sh | The project copy lived inside the kit (plugin) directory → Claude Code refused writes ("sensitive file"); with-skill results were worthless. | The copy moved to `$EVAL_WORK_ROOT` outside the kit; re-run. |

## From `/team:audit-kit` run on the kit itself (2026-11-09, coach, $1.48)
Result: 7 high, 7 medium, 5 low. The report could not be written into the kit repo (same cause as K-20: plugin directory), so it was copied here.

| ID | Severity | Status | Where | Symptom | Fix |
|---|---|---|---|---|---|
| K-21 | major | fixed | teamlib.py (read-only) | `$(…)`, backticks, `python3 -c`, `bash -c`, `git -c core.pager=…`, `git diff --output`, `awk system()`, `sed --in-place`, `find -fprint` slipped through the read-only check. | Block those forms for read-only roles; drop `awk` from the list; test cases. |
| K-22 | major | fixed | hooks.json / teamlib.py | A local install drops the `team:` prefix, but the SubagentStop matcher and the Agent check still required it → stop-check did not run for dev; tech-lead was blocked from calling `dev`. | Matcher `^(team:)?(dev\|maintainer\|researcher)$`; normalize `subagent_type`; test cases. |
| K-23 | major | fixed | protect.sh | `.team/*`, `.claude/*` were always writable → dev could edit `profile.json` (changing the test command that stop-check runs). | Allow only `docs/team/**`, `.team/**` except profile/config (only during onboard), `.claude/{agent-memory,skills,agents,rules}/**`; test cases. |
| K-24 | major | fixed (round 2) | hooks.json | `protect.sh` was not attached to Bash: `bash: any` roles (dev, maintainer, devops, qa) could modify `protected_paths` through the shell (`>`, `tee`, `cp`, `sed -i`). | `protect.sh` is also attached to PreToolUse Bash for every role and the main session: `teamlib.protect_bash` recognizes the write targets of redirection, `tee`, `rm`/`touch`/`truncate`/`mkdir`, `mv` (source too), `cp`/`install`/`ln`, `sed -i`, `chmod`, `dd of=`; blocks `.git/`, settings, profile/config (outside onboard), `protected_paths`. It cannot see writes inside other scripts or paths containing shell variables (documented in `docs/06-install.md`); 10 test cases. |
| K-25 | minor | open | 18 skills | `Bash(python3 *)` in `allowed-tools` allows any `python3 -c`. | v0.2: narrow it to the kit's own scripts. |
| K-26 | minor | fixed (round 2) | onboard | The onboard exception for `cp *` did not check forbidden areas. | The onboard exception changes `cp *` to `cp-from-kit-templates`: every source must be under `<kit>/templates/`; 3 test cases. |
| K-27 | minor | fixed (round 2) | coach.md / audit-kit / role-policy | coach's write list differed between three places; coach stopped when `runs.jsonl` was missing while audit-kit still allowed the static checks. | One coach write list in `agents/coach.md` = `role-policy.json` (ADJ-23); audit-kit runs the static checks when data is missing, retro stops (inputs per mode in section 2 of coach). |
| K-28 | minor | fixed (round 2) | docs/01-process.md / team-feature.yml | The labels `team:decide`, `team:size:*` are mentioned in the docs but the workflow does not read them. | `team-feature.yml` puts the label list into the prompt: `team:size:*` → `--size`, `team:decide` → `--decide`. |
| K-29 | minor | fixed | teamlib.py | `cmd.*` matching had no word boundary (`pytest` matched `pytestfoo`). | Require whitespace after the prefix. |
| K-30 | minor | fixed (round 2) | hooks.json | The format hook did not apply to NotebookEdit. | PostToolUse `format.sh` also applies to NotebookEdit (reads `notebook_path`). |
| K-31 | minor | fixed | evals/config.json | `Bash(bash *)` ≈ unrestricted Bash. | Replaced with `Bash(bash <kit>/scripts/*)`, added by run-eval. |

## From evals and install checks (2026-11-09)
| ID | Severity | Status | Where | Symptom | Fix |
|---|---|---|---|---|---|
| K-32 | major | fixed | install-local.sh | A local install drops the prefix → the skills become `/status`, `/run`, `/verify`, `/feedback`, clashing with Claude Code's built-in commands/skills. | Local skills are renamed `team-<name>`; `team.py` prints `/team-<name>` when the kit sits in `.claude/team-kit`. |
| K-33 | minor | fixed (P7) | evals/using-team | Scenario 1 did not distinguish baseline from with-skill (checks too narrow or too weak). | P7: rewrote the scenario and checks. |
| K-34 | major | fixed (P7) | team-leader / build | Size S: team-leader called dev directly, not through `/team:build` → no reviewer (violates "always review"). | P7: for size S team-leader still calls `/team:build` (1 dev + reviewer). |

## P7 round 1 — end-to-end re-run (2026-11-09)
Closed by rewriting skills/agents: K-10 (feedback writes with Write), K-15 (role cap = number of distinct roles team-leader calls itself; size S: analyst, tech-lead, qa = 3), K-16/K-19 (gates only from `team.py`, blocking only their own feature), K-33 (using-team scenario s1 has 5 checks), K-34 (size S goes through `/team:build` with a reviewer — confirmed in the eval and end-to-end).

| ID | Severity | Status | Where | Symptom | Fix |
|---|---|---|---|---|---|
| K-35 | blocker | fixed | handbook Acceptance checklist #5, verify, qa, spec template | qa returned `rework` although 5/5 criteria passed, because the DoD required As-Built, CHANGELOG and user docs — things `/team:asbuilt` only writes AFTER G4. The loop could not exit. | Checklist #5: the build part of the DoD; the post-G4 part is noted, and `/team:release` re-checks it; release adds the CHANGELOG + docs condition. Verify re-run on the sample. |
| K-36 | blocker | fixed | protect.sh / teamlib.relpath | After K-23, NEW files in dev's worktree (`.claude/worktrees/<n>/…`) were blocked as if outside the allowed roots (dev could not write its report; new test files would be blocked too). | Paths inside a worktree are evaluated relative to the worktree; 3 test cases. |
| K-37 | blocker | fixed | teamlib role-policy (K-21) | Blocking `$(…)` for read-only roles also blocked the skill's own command: `python3 "$(cat .team/plugin_root)/scripts/team.py" status`. | Only the exact form `$(cat .team/plugin_root)` is replaced with the kit path; every other substitution stays blocked; 2 test cases. |
| K-38 | minor | fixed (round 2) | coach / retro | Retro produced 2 proposals (asbuilt, config-max-agents) based on one feature; low confidence but still valid under the new rule. | Minimum-sample rule in retro/coach: ≥ 2 occurrences across ≥ 2 features, or a trend over ≥ 3 runs → proposal; fewer (including a single cap overrun in config) → the `## Watch list` section. Proposals record the number of features, runs and the confidence. |

### Comparison with the P6 run (same sample project, same request)
| Metric | P6 (v0.1.0) | P7 round 1 | Notes |
|---|---|---|---|
| `/team:run` calls to reach verify | 3 (2 wrong stops: G1 at size S; bold task) | 1 | K-02, K-11 did not recur |
| Journal lines for FEAT-001 | 4 (analyst line missing) | 6 (every call has its reason first) | Some remark fields still "—" when there was no result yet |
| Roles team-leader called itself / S cap | 5 roles, journal wrongly said "3" | 3 / 3 (analyst, tech-lead, qa) | New counting definition (K-15) |
| Rework rounds | 1 | 0 (reviewer approve in round 1) | — |
| Wrong hook blocks | 3 (qa `python3 -c`, reviewer `git worktree list`, tech-lead `cd`) | 2 (K-36, K-37 — both caused by the P6 safety fixes) → fixed | New test cases prevent recurrence |
| Verify verdict | accepted | rework (K-35) → fix → re-run: `Verdict: accepted`, stopped at G4 ($1.25) | Checklist #5 passes with the new wording |
| Cost intake→verify | ≈ $3.9 (3 runs) | $3.29 (intake $0.26 + run $3.03) | — |

## From `/team:audit-kit` on v0.2.0 (2026-11-09, coach, $0.94)
11 issues (4 high, 3 medium, 4 low); no name drift, no new pair of contradictory rules. The report could not be written into the kit repo (as K-20), copied here.

| ID | Severity | Status | Where | Symptom | Fix |
|---|---|---|---|---|---|
| K-39 | major | fixed (round 2) | teamlib.py `is_readonly` / role-policy.json | Read-only still leaked: `sed 'e cmd'`, `sed 'w f'`, `sort -o f`, `uniq IN OUT`, `tree -o f`, `rg --pre cmd`; redirections `>&`, `<>` were not recognized; `mkdir` was in the read-only list. | `is_readonly`: blocks `sed` with an `e`/`w`/`W` command or the `s///e|w` flags and `-f`; `sort -o`, `uniq IN OUT`, `tree -o`, `rg --pre`, `date -s`, `file -C`; redirections `>&file`, `<>`; `mkdir` dropped from the read-only list; 13 test cases. |
| K-40 | major | fixed (round 2) | teamlib.py `readonly_scripts` | Matched by file name, not path: `validate.sh`/`team.py` in any directory counted as read-only; `log-run.sh`, `validate.sh` write files. | `readonly_scripts` becomes a table name → write target; the script must sit exactly in `<kit>/scripts/` (realpath, kit = teamlib's directory or `.team/plugin_root`). `log-run.sh` and `team.py scorecard` run only when the role may write `docs/team/metrics/**`; `--root` forbidden; `gen-guides.py` dropped (it writes the kit's docs); 6 test cases. |
| K-41 | major | fixed (v0.2.1) | check-git.sh / teamlib.py | `git -c core.hooksPath=/dev/null commit` skips the commit hooks; `git -c alias.x='!cmd'` runs arbitrary shell. | Block `-c` with `alias.*`, `core.hooksPath`, `core.sshCommand`, `core.pager`, `core.editor`, `core.fsmonitor`, `diff.external`, `credential.helper`, and `--exec-path`; 3 test cases. Narrowing `git *` in the allow-list: next round. |
| K-42 | major | fixed (v0.2.1) | skills/takeover | `allowed-tools` still had `Bash(bash *)` (the main session has no `agent_type`, so role-policy does not apply). | Narrowed to `Bash(bash ${CLAUDE_PLUGIN_ROOT}/scripts/{detect-stack,explore-cache}.sh *)`. |
| K-43 | minor | fixed (round 2) | coach.md / audit-kit / role-policy | K-27 persists: coach's write list differs across three places; this run hit exactly that conflict. | As K-27; `team.py scorecard` runs only when the role may write `docs/team/metrics/scorecard.json`. |
| K-44 | minor | fixed (round 2) | skills/audit-kit | Running audit-kit inside the kit repo itself (`<kit>` = project root) means the report cannot be written to the right place. | audit-kit: when `<kit>` equals or contains the project root → write no file, print the lines in the columns of `docs/kit-issues.md`; the kit-issues template uses the same columns and the blocker/major/minor severities. |
| K-45 | minor | fixed (round 2) | docs/01-process.md | Said "size S verify is automated" while verify always forks qa (correct under the new cap definition). | `docs/01-process.md`: size S verify is done by qa, with reduced checks, counted within the 3-role cap. |
Also raised again by the audit (already listed): K-24, K-06, K-30, K-28.

## P7 round 2 — reading references and rewriting 21 items (2026-11-10)
Found while reading references (`docs/research/kit-audit-round2.md`) and while rewriting; every item below has evidence from code or a run, not only from documentation.

| ID | Severity | Status | Where | Symptom | Fix |
|---|---|---|---|---|---|
| K-46 | blocker | fixed | skills/architect, team.py | `system` mode only wrote `docs/team/architecture.md`; `team.py` reads the feature's G2 gate from `arch-impact.md` → wrong `approved(None)` → the feature stuck at `WAITING_FOR_APPROVAL G2` forever. | `system` mode also writes a short `arch-impact.md` for the feature (section `## System mode`) carrying the G2 approval line. |
| K-47 | blocker | fixed | team.py | Playbooks without analyze (bug-fix, hotfix, refactor, dependency-upgrade, spike, ci-fix, docs-only) never passed `specified`; refactor has no `tasks.md` so it never reached `built` → `/team:verify` could not run. | `NO_SPEC_PLAYBOOKS`, `NO_PLAN_PLAYBOOKS` (ADJ-26); `/team:clean` writes `tasks.md` with T1 ticked; 6 test cases. |
| K-48 | major | fixed | role-policy (researcher) | A POC "in a worktree" (SPEC §3) was impossible: researcher may only write `docs/team/**`, and paths inside a worktree were mapped back to the main tree. | `worktree_write` for researcher: may write any file in `.claude/worktrees/<n>/` (ADJ-25); 3 test cases. |
| K-49 | major | fixed | teamlib.role_policy | Temp agents (make-agent) were not in role-policy → no path, Bash or agent limits. | The `_temp` role applies to agents marked `team: temp`: read-only Bash + basic git + `cmd.*`, may only call Explore; 3 test cases. make-agent forbids `permissionMode`/`hooks`/`mcpServers`. |
| K-50 | major | fixed | skills/session, handoff.sh | `session save` and the PreCompact/SessionEnd hooks wrote the same `.team/session/<id>.md` → manual notes overwritten. | `save` writes `notes-<ID>.md`; `session-start.sh` mentions both. |
| K-51 | minor | fixed | docs/05-tokens-and-memory.md | Said "the SessionStart hook warns above `context_warn_pct`" but no script reads that slot. | Docs corrected: level 1, session plan sets the compaction point; no hook can measure the context %. |
| K-52 | major | fixed | analyst, architect, designer, writer | No Bash, although their skills run `team.py status`, `explore-cache.sh`; eval analyze s1 (2026-11-09) showed analyst skipping the step and not writing `current.json` although allowed. | Added `Bash` (role-policy keeps it read-only, ADJ-27); section 1 of each agent states the exact write list. |
| K-53 | major | open | profile.schema / release / devops | No slot for the prod deploy and rollback commands, yet release, devops and STD-OPS-1 need them. | Interim: the commands live in `docs/team/ci.md` section Deploy, written through `/team:ci deploy-script` with a PR (ADJ-24). New slots (`deploy.prod`, `deploy.rollback`) proposed for the human to decide — SPEC §13 forbids inventing slots. |
| K-54 | minor | fixed | ci, devops, ci-fix, ci.md | STD-CI-4 has 5 classes; skills/agents/playbooks/templates used 4 differently named ones. | The 5 STD-CI-4 classes unified everywhere. |
| K-55 | minor | fixed | team-ci.yml / ci | The file header "edit the profile and re-run onboard" contradicted `ci setup/add-stage`. | New header: generated by onboard or `ci setup`; add steps through `/team:ci add-stage` (separate PR). |
| K-56 | major | fixed (round 2) | team-ci.yml | An empty `cmd.*` slot generated a `run: true` step → green without checking anything. | `team-ci.yml` template: an empty slot generates `echo "::warning::cmd.<slot> not configured …"` (a warning visible on CI, not silent); ci/devops record "not configured" in `ci.md`. |
| K-57 | minor | fixed | batch/weekly-retro.md | Pointed to `team-ci.yml` for the plugin install step (not there); two duplicate `claude_args` keys. | Install the plugin as in `team-feature.yml`; one `claude_args` with `--allowedTools`. |
| K-58 | minor | fixed | clean / maintainer / verify | Branch `team/<ID>-clean-<kind>` (skill) differed from `team/<ID>-<slug>` (agent), while verify checked out `team/<ID>`. | Unified as `team/<ID>`; maintainer releases the branch (`git switch --detach`) for qa. |
| K-59 | major | fixed | audit-kit | The "unused skill" check was wrong: SubagentStop lines have `skill: null`. | Check D1 matches forked skills by agent + stage; a skill that records no metrics → "no data". |
| K-60 | minor | fixed | asbuilt / pr / PR template | `pr` grepped for "four headings" that were never defined; the PR template merged three ideas into one heading. | PR template: `## Feature`, `## Why`, `## What changed`, `## How verified`; pr greps exactly these four headings. |
| K-61 | minor | fixed | release / asbuilt template | Who writes the `Released:` line differed between the skill and the template. | devops writes it after the prod smoke test is green (in both places). |
| K-62 | minor | open | role-policy (writer) | writer may only write `docs/**`, while the profile has the slot `structure.docs` (P4). | writer stops and reports when `structure.docs` differs from `docs/`; teamlib reads the slot in a later round. |
| K-63 | minor | fixed | evals/make-skill | The scenario said "8 sections" and only checked "file exists". | Temp skill standard = the 8 contents of SPEC §9, 300–1,000 words; discriminating checks (evidence, refusal case). |
| K-64 | minor | fixed | make-agent | Test cases `.claude/agents/<name>.tests.md` could be loaded as an agent. | Moved to `docs/team/agents/<name>.tests.md`. |
| K-65 | minor | open | role-policy (devops) | devops `write: *`, `bash: any` is broader than the contract (SPEC §3 `Bash(gh, ci)`). | The agent states its write list; narrow role-policy once teamlib can read the `structure.scripts` slot. |
| K-66 | minor | fixed | templates/artifacts/design.md | The touchpoints table had a `task` column → designer split tasks instead of tech-lead. | A "notes" column (why it is touched). |
| K-67 | minor | fixed | agents/writer | Required `acceptance.md` even for the docs-only/client-docs playbooks (which have no acceptance). | Inputs per mode. |
| K-68 | minor | fixed | agents/researcher | Required `spec.md` while dependency-upgrade, spike and integration start from intake. | Accept `intake.md` for those playbooks. |
| K-69 | minor | fixed | scripts/gen-guides.py | An example return message with a stray backtick in the Outputs section made the "want X type Y" table generate garbage. | Skip code blocks and do not match across lines. |
| K-70 | major | fixed | skills/intake, using-team | `using-team` and team-leader send raw requests to `/team:intake`, but intake had `disable-model-invocation: true` → team-leader sometimes did intake itself (eval BEFORE), sometimes stopped and made the human type the command (eval AFTER round 2: 2/5). | Removed `disable-model-invocation` from intake (it only writes `intake.md`, the journal, `current.json`); SPEC §3: team-leader does intake. |
| K-71 | minor | fixed | 16 skills/agents | End-to-end round 2: `bash "$(cat .team/plugin_root)/scripts/log-run.sh" …` required approval from Claude Code under `-p` (substitution = "multiple operations"), not from a hook; build/verify metrics were not recorded. | Skills/agents type `"<kit>/scripts/…"` with `<kit>` being the path read from `.team/plugin_root`; the handbook says so explicitly. role-policy still accepts the old form (K-37). |
| K-72 | major | open (Claude Code limitation, documented) | make-skill, make-agent, evals/make-skill | Under `-p`, writes to `.claude/skills/**` are always denied, even with `--allowedTools "Write(.claude/skills/**)"`, `Edit(...)`, `Edit` (4 forms tried, 2026-11-10). Eval make-skill s1 could not run the skill-creation branch. | Both skills say it explicitly: create only in an interactive session (the human approves the write); headless, print the content for the human to create. The eval's creation branch must be run by hand in an interactive session. |
| K-73 | major | fixed | agents/team-leader, skills/intake | Eval using-team s1 (round 2, after K-70): team-leader did intake, then stopped and printed `/team:analyze` (3/5); the BEFORE run went through the whole chain (5/5). The sentence "print the next command" in intake step 9 and team-leader step 11 let the model choose whether to stop or continue. | team-leader step 11: `READY` → continue as `/team:run --until-blocked`; stop only at a gate, a question, a block, a cap, or when the human typed exactly one command. intake step 9 distinguishes the human typing the command from team-leader receiving a raw request. |

## From `/team:audit-kit` in the round 2 end-to-end (2026-11-10, coach, $2.21)
coach ran on the sample project (kit outside the project root → K-44 allows writing files), reached S13 and ran out of its 40 turns before writing the report; the findings below were taken from the session transcript (coach's commands + output) and reproduced with test cases.

| ID | Severity | Status | Where | Symptom | Fix |
|---|---|---|---|---|---|
| K-74 | major | fixed | skills/audit-kit | 17 checks do not fit in 40 turns; the report was written once at the end, so running out of turns lost everything. | Step 2a: write the kit-issues skeleton first, write after each check group, a re-run continues with the checks marked "not run". |
| K-75 | major | fixed | teamlib.py (read-only, redirection, errors) | Still leaked for read-only roles: the prefixes `GIT_EXTERNAL_DIFF=`, `GIT_CONFIG_*`, `BASH_ENV=`; `git grep --open-files-in-pager`; `sort -uo`, `sort --compress-program`; `sed --in=` (GNU abbreviated long option); `cd src && echo x > docs/team/…` (redirection target computed from the root, not following `cd`); broken hook JSON or a missing `role-policy.json` → allowed. `protect-bash` missed `sort -o` and `sed --in=`. | Env prefixes only from a safe list (`LC_ALL`, `TZ`…), `sudo` forbidden; block abbreviated long options (`--i…` of sed, `--o…`/`--com…` of sort, `--s…` of date, `--c…` of file) and short-flag clusters containing `o`; redirection target follows `cd`; broken JSON or missing rules → block (exit 2); `protect-bash` recognizes the `sort -o` target; 14 test cases. |
| K-76 | minor | open | profiles/*.json | No profile puts lint/typecheck/test configuration or CI workflows into `protected_paths` → a `bash: any` role could loosen a gate by editing configuration. | Next round: add the common patterns to the sample profiles, weighing that devops needs to edit workflows (through a PR). |
| K-77 | minor | open | role-policy (qa) | qa has `bash: any` while SPEC §3 gives qa no Write/Edit. | Kept (qa needs to run arbitrary check commands); the qa contract forbids editing code/tests; revisit when teamlib can tell write commands apart. |
| K-78 | minor | fixed | SPEC §4 / docs/01-process.md | SPEC says size S has "verify (automated, no separate qa)"; the kit lets qa do acceptance for size S without an ADJ. | ADJ-29. |
| K-79 | minor | open | settings.json.tmpl / CI | The kit's bash scripts are only allowed in `settings.local.json` (the kit path differs per machine) → `--allowedTools` in CI does not include `bash <kit>/scripts/*` (`log-run.sh`). | Next round: allow by script-name pattern, or use `python3`/`team.py` for recording metrics. |
| K-80 | minor | open | skills/onboard | During the onboard session, `cp` from `<kit>/templates/` required permission from Claude Code ("sensitive file") even though the kit is the source; onboard had to Write the template content by hand (A-01 of that run). | Next round: use `render.py --out` for every template (including files without `{{…}}`). |
| K-81 | major | fixed (P9) | agents/team-leader, tech-lead, skills/run, build, handbook | P9 end-to-end with `output_language: vi`: assessment, spec, review, acceptance came out Vietnamese, but team-leader reason lines and build/verify journal lines were English. | Journal prose (reason lines included) explicitly follows `output_language` in the handbook rule and in the five writers; re-run on the same sample: every FEAT-002 journal line Vietnamese. |

### Round 2 end-to-end compared with round 1 (new sample project `sample-e2e3`, same request "Implement the feature the README promises", size S, decide)
| Metric | P7 round 1 (v0.2.0) | P7 round 2 (v0.3.0) | Notes |
|---|---|---|---|
| Onboard with AI-readiness `clean-first` | ran anyway (K-09) | stopped before any write, listed the cleanup; re-run with `--accept-clean-first` | K-09 closed |
| Playbook chosen by intake | new-feature (FEAT-001) | bug-fix (BUG-001: the README promises it, the code lacks it — with a reason + alternative) | went through the no-spec/no-plan chain → K-47 checked in practice: `built` → `verified` |
| `/team:run` calls to reach verify | 1 (+1 verify re-run after K-35) | 1 | — |
| Journal lines | 6 | 10 | every call has its reason first |
| Roles team-leader called itself / S cap | 3 / 3 | 2 / 3 (tech-lead, qa) | bug-fix has no analyze |
| Rework rounds | 0 | 1 (reviewer demanded red-then-green output in the review package) | correct under STD-TEST-1 |
| Wrong hook blocks | 2 (K-36, K-37) | 0 — every block was correct (coach `for`, unresolvable variable `$K`, tech-lead writing a file with `{ echo …}`); 1 approval prompt from Claude Code for `$(cat …)` (K-71, fixed) | — |
| Verify verdict | rework (K-35) → accepted | accepted the first time (7/7 criteria), stopped at G4 | — |
| Retro | 2 proposals from 1 feature (K-38) | 0 proposals, 4 watch items (minimum-sample rule) | K-38 closed |
| Audit-kit | 11 findings | ran out of turns at S13 before writing (K-74); 7 new findings taken from the transcript (K-75..K-80) | K-74, K-75 fixed in the round |
| Cost | intake→verify $3.29 | intake $0.20 + run $2.25 = $2.45; whole chain $6.50 | — |


## Acceptance against the requirements document (2026-11-10, v0.3.0) — FAIL and PARTIAL
Verdict: REJECTED (`docs/acceptance/acceptance-2026-11-10.md`). One line per requirement; full evidence in `docs/acceptance/traceability-2026-11-10.md`.

- REQ-A2-2 (must, PARTIAL): Never deploy to production by itself while the gate is on — Only guidance + team.py; no hook blocks the prod deploy command; devops role-policy `"write":["*"],"bash":"any"`
- REQ-A3-6 (must, PARTIAL): For small jobs team-leader handles them itself or delegates to ONE single agent — Size S = analyst + tech-lead + qa (+dev, reviewer): per ADJ-29/K-15, unlike "one single agent"
- REQ-A3-9 (must, PARTIAL): Never bypass an active gate (what must not go wrong must be the machine) — Self-approving a gate is forbidden only in words (team-leader.md:61); the machine does not block it
- REQ-A4-6 (must, PARTIAL): Full coach from version 1: algorithmic measurement, 5-cause diagnosis, proposals with diff + eval, size S canary; app… — Proposals are full-text overlays, no diff; coach cannot run evals (retro SKILL.md:15)
- REQ-B1-2 (must, PARTIAL): team-leader tools = Read, Grep, Glob, Bash(read), Agent, TaskCreate/Update, AskUserQuestion, Write(docs/team/*… — Missing TaskCreate/Update (ADJ-07), Skill added (ADJ-11); write area broader than docs/team/**
- REQ-B1-4 (must, PARTIAL): team-leader: may do (intake, playbook & size, ask/decide, calls with a reason, guard gates, escalate, journal, coordinat… — The body does not mention upsizing/downsizing midway (only in docs/01-process.md:33); temp skills only via using-team/SKILL.md:18
- REQ-B1-5 (must, PARTIAL): tech-lead tools = Read, Grep, Glob, Bash(git, test), Agent, Edit(docs/team/**) — Write, Skill added (ADJ-11); Bash limited in the right spirit (git + cmd.*), plus gh pr
- REQ-B1-8 (must, PARTIAL): coach tools = Read, Grep, Glob, Bash(read), Write(retro/**, proposals) — Skill and memory added; write area extended per ADJ-23
- REQ-B1-11 (must, PARTIAL): analyst tools = Read, Grep, Glob, Agent(Explore), AskUserQuestion, Write(docs/team/**) — AskUserQuestion dropped (ADJ-01), Bash (ADJ-27) and Skill added; the Explore limit is held by the hook
- REQ-B1-14 (must, PARTIAL): researcher tools = Read, Grep, Glob, Bash, WebFetch, WebSearch, Agent, Write(docs/team/**) — Skill added; Bash narrower than the table; writes the POC worktree (ADJ-25)
- REQ-B1-17 (must, PARTIAL): architect tools = Read, Grep, Glob, Agent, Write(docs/team/**) — Bash (ADJ-27) and Skill added
- REQ-B1-20 (must, PARTIAL): designer tools = Read, Grep, Glob, Agent, Write(docs/team/**) — Bash (ADJ-27) and Skill added
- REQ-B1-21 (must, PARTIAL): designer opus / high (sonnet at size S/M) / 40 — No step (team-leader, using-team, design) passes model sonnet: size S/M still runs opus
- REQ-B1-23 (must, PARTIAL): dev tools = Read, Edit, Write, Grep, Glob, Bash — Only Skill added (ADJ-11); isolation: worktree
- REQ-B1-26 (must, PARTIAL): reviewer tools = Read, Grep, Glob, Bash(read); memory: project — Only Skill added; test_hooks.sh:77-108 has many cases blocking reviewer write commands
- REQ-B1-29 (must, PARTIAL): qa tools = Read, Grep, Glob, Bash; memory: project — Write, Skill added (ADJ-11); bash any, so shell commands could edit code (forbidden only in text)
- REQ-B1-32 (must, PARTIAL): writer tools = Read, Grep, Glob, Write(docs/**, CHANGELOG) — Bash (ADJ-27), Skill added; README added reasonably because it is under "May do"
- REQ-B1-35 (must, PARTIAL): maintainer tools = Read, Edit, Write, Grep, Glob, Bash — Only Skill added (ADJ-11)
- REQ-B1-38 (must, PARTIAL): devops tools = Read, Edit, Write, Grep, Glob, Bash(gh, ci) — The Bash(gh, ci) limit is not enforced by the machine; "edit only CI workflows" is text only
- REQ-B1-40 (must, PARTIAL): devops: set up CI/CD, diagnose red (classify first), deploy/rollback/smoke scripts, docs/team/ci.md / never delete… — Good body (838 words, 7 lines); the prod deploy ban is text only, no hook blocks it
- REQ-B2-3 (should, PARTIAL): The who-calls-whom matrix is explicit and consistent — Internal contradictions; no hook blocks the team-leader→dev path
- REQ-B2-6 (must, PARTIAL): dev → tech-lead: files changed, tests with real output, what is still missing — The "what is still missing" field is not in dev's contract
- REQ-B3-2 (must, PARTIAL): haiku for triage / mechanical work — Only the built-in Explore uses haiku; the kit has no haiku path
- REQ-B3-5 (must, FAIL): Overriding models in config takes effect — Decorative key: changing config changes no model
- REQ-C1-1 (must, PARTIAL): Project takeover: `/team:takeover`, team-leader (+Explore, researcher), 5 artifacts assessment/ai-readiness/pro… — researcher has no role in the skill (only Explore); G0 is not in team.py, so `/team:status` does not show "waiting for G0".
- REQ-C1-10 (must, PARTIAL): Release: `/team:asbuilt`, `/team:pr`, `/team:release`; writer, tech-lead, devops; asbuilt/CHANGELOG/PR/depl… — G5 is held only by the skill/agent (LLM); the machine (team.py, hooks) does not block `Released:` when the prod approval is missing.
- REQ-C1-11 (must, PARTIAL): Operations: `/team:intake --type bug`, `/team:clean`, `/team:ci`, `/team:retro`; team-leader, maintainer, devop… — clean/ci/retro fork the right roles; defects.md has no template and no skill creates it.
- REQ-C3-1 (must, PARTIAL): S: a one-sentence diff, ≤ 3 files, no schema/API change; intake → reduced analyze without G1 → build with 1 dev → automat… — Deviates from the document per ADJ-29 (S still forks qa); the new-feature/bug-fix playbooks still say "no separate qa call" → internal drift.
- REQ-C3-3 (must, PARTIAL): L: multiple modules, new NFRs, > 5 days; all 9 stages; architecture mandatory; first task a walking skeleton — Architecture is "mandatory" only in next_cmd; the state machine lets it pass and also skips G2; research is skipped at L too (team.py:205).
- REQ-C3-6 (must, PARTIAL): Upsizing/downsizing midway records the reason in `intake.md` — agents/team-leader.md has no step that applies a size change and records it in intake.md; only a blank in the template.
- REQ-C4-6 (must, PARTIAL): Small items → record under the assumptions heading — Correct behavior, but the heading name differs from the document (S3 in docs/acceptance/spec-vs-requirements.md).
- REQ-C4-10 (must, PARTIAL): In CI: question → issue comment from the template, label `team:needs-answer`, stop with `WAITING_FOR_ANSWER` — CI defaults to decide (ask only with the team:ask label), so the CI question path rarely runs; live UNVERIFIED.
- REQ-C5-10 (must, FAIL): Behavior: a size S feature runs analyze → build (dev worktree, failing test first, reviewer, findings with STD codes) → ver… — Cause: REQ-E1-9
- REQ-C6-5 (must, PARTIAL): Stop when `feature_budget_usd` is exceeded — Nothing records cost per feature, so the condition cannot be measured; only batch has `--max-budget-usd`.
- REQ-C7-4 (must, PARTIAL): 4-tier scan → 3-sentence report → G0 → onboard; size L; gate G0 — Size differs (document: L).
- REQ-C7-6 (must, PARTIAL): intake → analyze → [research] → design → plan → build → verify → asbuilt → pr → release; M; G1, G3, G4 — The default size is not M; the verify line contradicts ADJ-29/the verify skill.
- REQ-C7-7 (must, PARTIAL): analyze --amend → architect (impact) → plan (insert) → build…; M; G1, G3 — team.py leads to design, not to architect impact then plan --insert as the playbook says; extra gates G2, G4.
- REQ-C7-8 (must, PARTIAL): intake(bug) → failing test first → build (1 task) → verify → pr; S; G4 if M — G4 applies at size S too (document: only at M); intake does not create defects.md as step 0 says.
- REQ-C7-9 (must, PARTIAL): intake(hotfix) → minimal build from prod → quick verify → pr → release prod (human approves) → full bug-fix aft… — The document has only G5; the repo also blocks at G4.
- REQ-C7-13 (must, FAIL): research (API, auth, limits) → architect (impact) → design (contract, retry, idempotent) → plan → build → v… — team.py:89 lacks integration in NO_SPEC_PLAYBOOKS: without spec.md it is stuck at intaken, and `/team:run` loops on research.
- REQ-C7-16 (must, PARTIAL): analyze (audience, scope) → writer → content review → pr; S/M; reduced G1 — The default size S loses G1, and team.py leads to build instead of writer (the size S check at team.py:203 comes before client-docs at :207).
- REQ-C8-14 (must, PARTIAL): State clearly what was scanned / not scanned / confidence — Following the template, the skill's own check (grep -c for the "scanned" marker ... ≥ 1 per file) would fail.
- REQ-D1-3 (must, PARTIAL): Level 3 rules are really blocked by the machine — docs/03-handbook.md:39 sets its own rule "level 3 must have a real hook"; 5 rules violate that rule
- REQ-D1-4 (must, PARTIAL): A level 1 rule violated ≥ 2 times → coach proposes raising the level — No way to count violations per code/level; one line, no method
- REQ-D2-2 (must, PARTIAL): STRUCT: new files within allowed_new_file_roots; tests follow the convention; never commit tool-generated files; artifacts co… — "Artifacts correctly named" is missing; "tool-generated files" lives under GIT
- REQ-D2-3 (must, PARTIAL): NAME: follow profile + codebase; names state intent; branch team/<ID>-<slug>; commit type(scope): description (<ID>); test… — NAME-3 is only the test file name
- REQ-D2-4 (must, PARTIAL): STYLE: the formatter decides; the linter is law; functions ≤ 50 lines, ≤ 4 parameters; no dead code; TODOs have an ID; comments say … — Missing the 50-line / 4-parameter function limit and TODOs with an ID
- REQ-D2-5 (must, PARTIAL): DESIGN: dependencies come in from outside; never modify third-party libraries; no hidden global state; API/schema changes have de… — Missing "dependencies come in from outside" (DI) and "no hidden global state"
- REQ-D2-6 (must, PARTIAL): TEST: fail first (mandatory for bugs); one behavior per test; never mock what is under test; no skip/xfail/only (block… — Missing "one behavior per test", "never mock what is under test"; "every task has a test" only indirectly
- REQ-D2-7 (must, PARTIAL): ERR: never swallow exceptions; actionable messages; logs with context and no secrets; validate at the boundary — "Errors have actionable messages" is not a rule
- REQ-D2-8 (must, PARTIAL): GIT: one task one small PR from the template; push only team/*; no force-push; squash merge; commits never contain fi… — Squash merge missing
- REQ-D2-9 (must, PARTIAL): CI: lint → typecheck → test → build → staging → smoke; red never merges; prod needs a human; no secrets in fil… — The full 6-step order and "jobs have a timeout" are not STD rules; only in the template
- REQ-D2-12 (must, PARTIAL): DEP: prefer libraries already present; pin + lockfile; no new library for work < 50 lines — "Prefer libraries already present" is missing as a separate rule
- REQ-D2-17 (must, PARTIAL): Two checklists "used verbatim" — The PR template is a paraphrase, not verbatim, written twice
- REQ-D2-18 (must, PARTIAL): Finding = severity / STD / file:line / description / fix; only blocker/major; minors merged into 1 line — The standard format is right; the agent adds a 6th column and writes the minor line differently from the template
- REQ-D4-2 (must, PARTIAL): docs/ holds only the overview, installation, the task → skill map, design rationale; never write knowledge twice — Process knowledge lives only in docs/ and many passages are written twice
- REQ-E1-2 (must, PARTIAL): `test_one` is mandatory — The key is required but an empty string passes; profiles/_template.json has an empty test_one; build/handbook stop only in words
- REQ-E1-3 (must, PARTIAL): `{file}` is the ONLY placeholder — Other placeholders are not forbidden; stop-check only substitutes `{file}`, so `{path}` would slip through verbatim
- REQ-E1-4 (must, PARTIAL): protected_paths always contains secrets, lockfiles, vendored code, prod configuration — Good template but no machine check; teamlib.py:22 defaults to only `.env`,`.env.*` when the profile is missing; `.git/**` is appended …
- REQ-E1-5 (must, PARTIAL): allowed_new_file_roots is a closed list (the document has src, tests, docs, scripts, .github, .claude, .team) — Profiles drop `.github/` from the roots (the document has it); onboard only works because it writes through `render.py`/`cp` in Bash, which the hook does not c…
- REQ-E1-7 (must, PARTIAL): Monorepo: root profile + per-directory `packages` overrides — Declarable, but no script/hook applies per-directory overrides
- REQ-E1-9 (must, FAIL): Behavior: the profile proposed by takeover and written by onboard must work with the kit's scripts (`naming.test_file` the… — Same class as K-01; the schema does not enforce the pattern
- REQ-E1-10 (must, PARTIAL): Behavior: the protected_paths of the onboarded profile include secrets (`.env*`, secrets directories), lockfiles, vendored code, prod conf… — The sample project has no lockfile/vendored code
- REQ-E2-3 (must, FAIL): protected_branches = main, master, develop, release — `develop` missing; `release` became `release/*`
- REQ-E2-6 (must, FAIL): approvers per gate `["@owner"]` — Empty = names not checked (release/SKILL.md:55 checks only when not empty)
- REQ-E4-2 (must, PARTIAL): deny: push to protected branches, force-push, rm -rf, Edit protected_paths, Read .env* — No deny for pushing protected branches; only the check-git.sh hook blocks it
- REQ-E4-4 (should, FAIL): `~/.claude/settings.json`: autoMemoryEnabled, personal plugins — No guide says to turn on auto memory
- REQ-E4-5 (must, PARTIAL): Permission mode: plan for analysis/architecture, acceptEdits for build, dontAsk + allowlist in CI/headless — Mostly only in docs; plugin agents ignore permissionMode
- REQ-E5-5 (should, PARTIAL): As needed: Playwright MCP (qa, ui), docs MCP (researcher), Sentry/Slack (devops, team-leader), tracker (in… — intake only uses gh
- REQ-E5-6 (should, PARTIAL): Do not install duplicate plugins (superpowers, commit-commands, pr-review-toolkit), hide them with skillOverrides; superpowers… — The sentence about plugin-dev is missing
- REQ-E5-7 (must, PARTIAL): Path-scoped rules say when to use which tool; skills name the tool per step; agents only the role's tools — The tool table exists but is not path-scoped
- REQ-F1-7 (must, PARTIAL): Imperative: EVERY agent checks the playbook/skill before working — Deviates from "every agent"
- REQ-F1-8 (must, PARTIAL): Rate artifacts, tied to agent/skill → feedback.jsonl; every role and human — reviewer/qa/coach cannot use it
- REQ-F1-18 (must, PARTIAL): Conditions → PR → CI → merge → staging → smoke → prod (G5); tech-lead, devops — Full process; the coordinating role is team-leader, not tech-lead
- REQ-F1-28 (must, PARTIAL): descriptions do not summarize the process — 2/26 narrate a chain of steps
- REQ-F1-30 (must, PARTIAL): Every step has a checkpoint and an exit condition — Stop conditions are scattered, not uniform per step
- REQ-F1-31 (must, PARTIAL): Anti-rationalization table + red flags — The 6 always-loaded skills have no red flags
- REQ-F1-33 (must, FAIL): Word budget: frequently loaded skills < 200 words, others < 500 — The repo follows P7 (CLAUDE.md rule 6), 2–5 times the document's cap
- REQ-F1-35 (must, FAIL): Every skill has a baseline → with-skill eval before release — 17 skills have no eval; build, commit, pr, takeover only have a README that was never run
- REQ-F2-5 (must, FAIL): Behavior: a request needing repeated expertise ("6 identical CRUD screens") → team-leader coordinates `/team:make-skill`… — team-leader treats it as new-feature M and stops at G1
- REQ-F3-5 (must, PARTIAL): Must have a sources heading with URLs — The behavior exists, but the heading is `## Sources`, not the Vietnamese heading the document names
- REQ-F5-1 (must, PARTIAL): Lazy loading, Explore, one session one feature, warning above context_warn_pct — No automatic warning
- REQ-F5-4 (must, PARTIAL): Reused ≥ 2 times or expensive; conclusions not process; date/version; size and file-count caps — The file-count cap is not enforced
- REQ-F5-5 (should, PARTIAL): Coach cleans up periodically; prompt cache: stable prefix, no model change mid-session, fan-out with the same model/tools — coach's memory/cache cleanup is in neither the agent nor a skill
- REQ-F5-6 (must, PARTIAL): Behavior: PreCompact/SessionEnd write `.team/session/<id>.md` ≤ handoff_max_lines, only information not in artifacts;… — Thin handoff content
- REQ-F6-2 (must, PARTIAL): calls, turns, time, rework/rejections, STD violations, tokens (local log), human interventions; compare with the median of the same size — Nobody writes std_violations/human_interventions into runs.jsonl → always 0
- REQ-F6-4 (must, PARTIAL): Feedback on the spot; warning when the threshold is exceeded twice — The warning is only in words; 3 roles cannot record feedback
- REQ-F6-6 (should, PARTIAL): Overlay header `# Overlay from retro <date>: <reason>` + version — Header + version present, but the wording is English, unlike the document
- REQ-F6-8 (must, PARTIAL): Measure redundant calls: agents/feature per size against max_agents_per_feature; periodic retro, kit-issues, audit-kit — No machine-computed measure; retro/audit-kit have it
- REQ-F6-9 (must, PARTIAL): Behavior: `/team:retro` produces `retro/<date>.md` with ≥ 1 proposal with diff + eval + canary; never edits agents/skills; d… — The proposal format has not been verified in practice
- REQ-F6-10 (must, PARTIAL): Behavior: a run writes `runs.jsonl` and `scorecard.json` — —
- REQ-G1-4 (must, PARTIAL): workflows/ 16 playbooks + `lot/` (3–4 scripted workflows) — Named `batch/` per SPEC.md:108, unlike the document's `lot/`
- REQ-G1-10 (must, PARTIAL): docs/00-tong-quan.md … 08-kenh-kich-hoat.md and docs/huong-dan/ (bat-dau-5-phut, muon-gi-go-gi, cay-quyet-dinh… — Content matches 1–1 but the names are English: per A5 and SPEC.md:168, contrary to G1
- REQ-H1-3 (must, PARTIAL): Scheduled tasks: retro, periodic clean-sweep; webhook after deploy → smoke; decide only — No mechanism/template for a post-deploy webhook → smoke
- REQ-H1-4 (must, PARTIAL): Headless `claude -p` with `--bare --max-turns --max-budget-usd --output-format json`; decide mandatory — Intentional deviation per ADJ-03 (--bare turns off hooks)
- REQ-H1-5 (must, PARTIAL): Projects (cloud): several features in parallel, approval in "Waiting on you", questions in the thread — Does not describe how to approve or ask in the thread
- REQ-H3-1 (must, PARTIAL): Claude Code syntax changes: must look up the docs + confirm the version; fallback syntax appendix — No version check at run time; the syntax appendix is only in automation-ai_prompts.md:217 (untracked)
- REQ-H3-3 (must, PARTIAL): Behavior hard to check: sample repo in P6; evals for discipline skills; size S canary — The sample repo is not in the kit; eval results are claims that were never re-run
- REQ-H3-7 (must, PARTIAL): Memory overflow: criteria for what is worth keeping; caps; coach cleans up — The key explore_cache_max_files is dead configuration; coach only cleans its own memory, not the explore/research cache
- REQ-H3-8 (must, FAIL): Vietnamese identifiers break scripts: a language rule; validate checks it — The rule exists (CLAUDE.md rule 4) but validate does not check the language of identifiers; keys are caught only thanks to additionalProperties
- REQ-I-3 (should, PARTIAL): Write skills like TDD: baseline without the skill → record the verbatim rationalizations → minimal skill → re-run; `evals/` — The verbatim rationalizations from the baseline are not stored; make-skill:13 describes a test-style way of writing
- REQ-I-5 (must, FAIL): Word budget 200/500 — CHANGELOG.md:69 "Dropped the old 200/500-word budget" (P7 bar); no ADJ records this; also deviates from SPEC.md:143
- REQ-J-5 (must, PARTIAL): Full coach; evals for discipline skills; user guides; GitHub Actions template — Partly because of coach (REQ-A4-6)
- REQ-J-6 (should, PARTIAL): GitLab CI left for version 2 (not done in version 1) — Small scope creep: a 15-line skeleton shipped, marked v2; the tracker/ci enum includes gitlab
