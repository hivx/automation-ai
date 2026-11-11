# 06 — Installation

Requirements: Claude Code ≥ 2.1; `bash`, `python3`, `jq`, `git`; `gh` optional.

## Three ways to install
| Method | Command | Agents | Hooks | Command names |
|---|---|---|---|---|
| 1. Marketplace (recommended) | `/plugin marketplace add hivx/automation-ai` then `/plugin install team@automation-ai` | yes | yes | `/team:<name>` |
| 2. `npx skills` (optional) | `npx skills add hivx/automation-ai` | no | no | `/<name>` |
| 3. Local copy | `scripts/install-local.sh [--dry-run] [--force] <project>` | yes (unprefixed names) | yes (merged into `.claude/settings.json`) | `/team-<name>` |

- Method 1 also works from the shell: `claude plugin marketplace add hivx/automation-ai`, `claude plugin install team@automation-ai`.
- Method 2 has no machine rules (hooks); it is only good for trying out the skills.
- Method 3 copies `agents/` → `.claude/agents/`, `skills/` → `.claude/skills/`, the rest → `.claude/team-kit/`, and writes `.team/plugin_root`. Re-running is safe; files that differ from the target are skipped unless `--force` is given (exit code 1 when a file was skipped).
- Trying the kit unpackaged: from the project directory, `claude --plugin-dir /path/to/automation-ai`.

## After installing: takeover → onboard
1. Project already has code: `/team:takeover` → read `docs/team/` → approve `ai-readiness.md` (G0).
2. Empty repo: skip takeover and run `/team:onboard --new`.
3. `/team:onboard` creates `.team/profile.json`, `.team/config.json`, the `<!-- team:start -->…<!-- team:end -->` block in `CLAUDE.md` (inserted, never overwritten), `.claude/settings.json`, `.claude/rules/`, GitHub templates. It also sets `team-leader` as the main-session agent (ADJ-01). Set `output_language` in `.team/config.json` (`vi` default, or `en`) to choose the prose language of artifacts (`docs/04-profile.md`).

## Three settings scopes
| Scope | File | Used for |
|---|---|---|
| Project (committed) | `.claude/settings.json` | `enabledPlugins`; `agent`; `permissions.allow` from `cmd.*` + safe git; `permissions.deny`: pushing protected branches, force-push, `rm -rf`, editing `protected_paths`, reading `.env*`; project-specific hooks; `skillOverrides` to hide duplicate skills |
| Local (gitignored) | `.claude/settings.local.json` | Customizations for your machine only |
| User | `~/.claude/settings.json` | Personal habits across every project |

Permission mode per stage: `plan` during analysis/architecture; `acceptEdits` during build; `dontAsk` + a minimal allowlist for CI/headless. Set it in settings or with a CLI flag (plugin agents ignore `permissionMode`).

## Plugin and MCP policy
- The kit writes no MCP server and no other plugin.
- The profile declares `plugins.required` / `plugins.recommended`; onboard prints the install commands but does not install; SessionStart warns when something is missing (does not block).
- Recommended by default: the language's LSP plugin, security-guidance, github/gitlab.
- On demand: Playwright MCP (qa when `ui: true`), a library-docs MCP (researcher), Sentry/Slack (devops/team-leader), a tracker (intake).
- Do not install plugins that duplicate `team` (superpowers, commit-commands, pr-review-toolkit). If one is mandatory, hide the duplicate skills with `skillOverrides`.

## Uninstalling
- Marketplace: `/plugin uninstall team@automation-ai`, then `/plugin marketplace remove automation-ai` if you no longer use it.
- Local: delete the `.claude/agents/` and `.claude/skills/` entries the kit copied (see the install-local log), `.claude/team-kit/`, `.team/plugin_root`.
- The team's data (`docs/team/`, `.team/profile.json`, `.team/config.json`) belongs to the project: keep or delete it as you like. The `team` block in `CLAUDE.md` sits between the `team:start`/`team:end` markers; delete the whole block.

## Installed hooks (machine rules)
The plugin's `hooks/hooks.json`; in a local install, `install-local.sh` merges the same content into `.claude/settings.json` with the path `${CLAUDE_PROJECT_DIR}/.claude/team-kit/scripts/`.

| Event | Script | What it does |
|---|---|---|
| PreToolUse `Edit\|Write\|NotebookEdit` | `protect.sh`, `role-policy.sh` | Blocks `protected_paths`, `.git/`, `.claude/settings*.json`, new files outside `allowed_new_file_roots`; per-role write limits |
| PreToolUse `Bash` | `check-git.sh`, `protect.sh`, `role-policy.sh` | Only `team/*` (and tags) may be pushed; blocks force-push, `--delete`, `--no-verify`, `reset --hard`/`rebase -i` on protected branches; warns on a malformed message; shell commands that write/delete in forbidden areas (redirection, `tee`, `rm`, `mv`, `cp`, `sed -i`, … — writes inside another script are not visible); per-role commands |
| PreToolUse `Agent` | `role-policy.sh` | Who may call whom (`handbook/who-calls-whom.md`) |
| PostToolUse `Edit\|Write\|NotebookEdit` | `format.sh` | Formatter per `formatters_by_ext` |
| Stop; SubagentStop `team:dev\|maintainer\|researcher` | `stop-check.sh` | When a build is active (`.team/active-build-<ID>`, or the older `.team/active-build`): lint, typecheck, tests of changed files, structure; for a researcher (its feature read from its transcript): `## Sources` with URLs is mandatory |
| SubagentStop (every agent) | `scorecard.sh` | Writes one line to `docs/team/metrics/runs.jsonl` |
| SessionStart | `session-start.sh` | Writes `.team/plugin_root`, loads the status summary |
| PreCompact, SessionEnd | `handoff.sh` | Session handoff |
| PostCompact, SessionEnd | `log-session.sh` | Session metrics |

Per-role limits live in `hooks/role-policy.json`; a session with no agent (the human working directly) has no per-role limits, only the other hooks.

## Notes on settings
- `skillOverrides` in `.claude/settings.json` is empty by default. Use it to hide another plugin's duplicate skills: `{"<plugin>:<skill>": "off"}` or `"user-invocable-only"`. JSON does not allow comments, so the note lives here.
- `Read(//<kit>/**)` sits in `.claude/settings.local.json` (per machine) so that agents can read the kit's `handbook/STD-short.md`.
- `.claude/settings*.json` cannot be changed with Edit/Write (the hook blocks it); change it through `/team:onboard` or edit it by hand.
