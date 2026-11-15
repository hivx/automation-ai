# Session lanes: several Claude sessions on one project

A project can have several Claude sessions open at once, each running its own team. Each session works in its own **lane**: it records what it works on and which files it holds, and checks the other lanes before it starts. Different work runs in parallel; the same work is a question for the human; the same file goes one session at a time. `team.py` = `python3 "<kit>/scripts/team.py"`, `<kit>` = the content of `.team/plugin_root`.

## The rules
1. **One position per session.** A stage records where this session is with `team.py claim <ID> --stage <stage> --agent <role>`. The position lives in `.team/session/<session_id>.json` (the session id is `$CLAUDE_CODE_SESSION_ID`, shared by the subagents of the session). Never write `.team/current.json`: it was one file for every session and it is retired.
2. **Different item → just work.** No question, no waiting.
3. **Same item → ask the human.** `claim` exit 3 prints `CONFLICT <ID>: session <s> holds it (stage, agent, last activity)`. team-leader asks with AskUserQuestion: *leave it to that session* (recommended while it is active) / *take it over here* (`claim <ID> --take-over`; the other session reads a NOTICE at its next claim and stops) / *work on something else*. Any other role stops and returns `BLOCKED` with the CONFLICT line; it never takes over on its own.
4. **Same request twice → ask at intake.** Before assigning an ID, compare the request with the items in `team.py sessions --others` and the open items in `team.py status`. Same goal, or the same touchpoints for the same behavior → ask: *leave it to the session or item that has it* / *fold it into that ID* (`change-request`) / *run it here as a new item* (shared files then take turns). Different work → no question. The ID comes from `team.py new-id FEAT|BUG|CHG`: it creates `docs/team/features/<ID>/` atomically and claims it, so two sessions never get the same ID.
5. **Same file → one at a time; different files → in parallel.** Before a dev starts a task, its caller claims the task's files: `team.py claim <ID> --task T<N> --files <files from tasks.md>`. Exit 4 `BUSY` = another active session holds one of them: claim nothing, start the other ready tasks now and retry this one next round. With nothing else ready, `--wait 110` waits just under the Bash tool's 2-minute default; still `BUSY` → repeat a few times, then report. Release after the merge: `team.py release <ID> --task T<N>`; on every exit of the stage: `team.py release <ID> --files`. Playbook quick: team-leader claims T1's touchpoints before calling the dev and releases them when T1 is ticked.
6. **Shared resources take turns too.** `@shared-state`: when `test.shared_state` is true, every full `cmd.test` or `cmd.migrate` runs while holding it (`claim <ID> --files @shared-state --wait 110`, repeated while `BUSY`; `release <ID> --files @shared-state` right after). `@main-tree`: the only way to move the main checkout off its branch (rule 7). A resource claim expires after 30 minutes.
7. **Never switch the main tree's branch.** Other sessions read and edit the main checkout. A feature branch lives in its own worktree: `git worktree add .claude/worktrees/<ID> team/<ID>` (once), and merges and `cmd.test` run there. When `cmd.test` only works in the main checkout (its runtime loads the code from there), hold `@main-tree`, switch, merge, test, switch back to `base_branch`, release. Uncommitted changes in the main tree that are not yours stay untouched; ask the human whose they are.
8. **Artifacts are per ID.** `docs/team/features/<ID>/**` and `docs/team/journal/<ID>.md` belong to the session holding `<ID>`; nobody else writes them. Shared files (`CHANGELOG.md`, `docs/team/architecture.md`, ADRs, `CLAUDE.md`) are edited with Edit right after a fresh read, never rewritten whole.

## What the hooks do
- **SessionStart** registers the lane and lists the other live sessions and what they hold (`team.py sessions --open`).
- **PreToolUse Edit/Write** (`protect.sh`): a file another active session holds → `RULE (reminder, not enforced)` (default) or a block with `enforcement: "block"`: do another task first. An edit in the main tree is recorded for this session for 30 minutes, so the others see it.
- **SessionEnd** (`handoff.sh`) writes the handoff, then releases every claim of the session.

## When a lane ends or idles
- A lane ends when its Claude process exits; a crashed session is detected by its process id, so its claims stop counting without anyone cleaning up. Without a process id, a day of silence ends it.
- After `limits.session_idle_min` minutes (default 120) without activity a lane is **idle**: its items still need the human's answer before anyone takes them, but its file claims no longer make other sessions wait.

## Commands
| Command | Does | Exit |
|---|---|---|
| `claim <ID> [--stage S --agent A]` | record the item (and this session's position) | 0, 3 CONFLICT |
| `claim <ID> --task T<N> --files F…` | hold files or `@resources`, all or nothing (`--wait SEC`) | 0, 3, 4 BUSY |
| `claim <ID> --take-over` | take the item from another session (only after the human says so) | 0 |
| `release <ID> [--task T<N> \| --files [F…]]` | drop a task's files, some files, all files of the item, or the item | 0 |
| `release --all` | drop everything of this session (SessionEnd) | 0 |
| `sessions [--others]` | the live sessions, their items and held files | 0 |
| `new-id FEAT` | the next free ID, created and claimed | 0 |
| `status` / `wave` | column `Session` (`this`, another session's id, `—`); `wave` holds items other sessions hold | 0 |
