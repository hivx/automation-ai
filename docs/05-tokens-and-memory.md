# 05 — Tokens and memory

Source of truth: `SPEC.md` §9 (Memory). This page explains the reasoning.

## Five tiers
| Tier | What it is | Where it lives | Who writes it |
|---|---|---|---|
| 0 Context budget | Lazy loading: path-scoped rules, skills on demand, handbook preloaded; exploration through `Explore`; one feature per session; a warning when `context_warn_pct` is exceeded | — | `/team:session plan` sets the compaction points per stage (level 1: no hook can read the context %); the SessionStart hook restates the rules after compaction |
| 1 Session state | A handoff of ≤ 40 lines, only what differs from the artifacts | `.team/session/<id>.md` (gitignored) | PreCompact, SessionEnd hooks; loaded at SessionStart |
| 2 Feature artifacts | spec, design, plan, review, acceptance... | `docs/team/features/<ID>/` | the roles |
| 3 Project knowledge | Split in two: Claude Code's auto memory (local machine: habits, machine quirks) and `docs/team/` (shared, readable by CI: ADRs, versioned research cache, As-Built, glossary, hashed explore cache) | `~/.claude/projects/...` and `docs/team/` | the roles, following the rules |
| 4 Agent memory | `memory: project` for reviewer, qa, coach; small, dated | the agent's memory directory | that agent itself |

## The "is it worth keeping?" test
Keep it when: it is reused ≥ 2 times OR it is expensive to recreate. When keeping it:
- Keep the conclusion, not the process.
- Record a date or version so you know when it expires.
- Have a cap on size and number of files.
- coach cleans up periodically.

## Keeping the prompt cache
- The start of the prompt stays stable; do not inject changing data at the top.
- Do not switch models mid-session.
- When splitting work in parallel: same model, same tool set. Cost grows with `limits.headcount` (agents running at once).
- Compact proactively at stage boundaries; do not wait until the context is full.

## Tips for users
- One feature per session. After finishing a stage you may run `/team:session` and open a new session: the state is on disk.
- Context full: see `docs/guides/incidents.md`.

## Scripts and hooks that do this
| Job | Where |
|---|---|
| Write a handoff of ≤ `memory.handoff_max_lines` lines before compaction and at session end | `scripts/handoff.sh` (PreCompact, SessionEnd hooks) → `.team/session/<session_id>.md` |
| Reload: status summary, latest handoff, restating the 6 rules after compaction | `scripts/session-start.sh` (SessionStart hook, `additionalContext`) |
| Count compactions per session/feature | `scripts/log-session.sh` (PostCompact, SessionEnd hooks) → `docs/team/metrics/sessions.jsonl` |
| Explore cache keyed by directory hash | `scripts/explore-cache.sh <dir>` → `HIT`/`MISS` with `docs/team/explore/<slug>.md` (`hash:` line) |
| Status computed from artifacts (no pointer) | `scripts/team.py status` |
