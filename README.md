Tiếng Việt: see [GUIDE-VI.md](GUIDE-VI.md)

# automation-ai — the `team` plugin for Claude Code

`automation-ai` is an installable set of AGENTS + SKILLS + RULES + GUIDES + PROCESSES for Claude Code. Install it into any software project (any language, any platform) and Claude Code becomes a professional IT team: it takes over the project and reports on its current state, takes a raw request and carries it all the way from analysis to release, stops only at the approval gates you turn on, and measures itself to propose improvements to itself. Each project's commands, structure and conventions live in `.team/profile.json`, not in the core.

**Status: v0.4.0 — usable; AI-facing text in English, artifacts in the language set by `output_language` (default Vietnamese; see [`GUIDE-VI.md`](GUIDE-VI.md)); two quality rounds done, every skill (26) and agent (13) meets the bar (see [`docs/research/kit-audit-round1.md`](docs/research/kit-audit-round1.md), [`kit-audit-round2.md`](docs/research/kit-audit-round2.md)); known limitations in [`CHANGELOG.md`](CHANGELOG.md).**

Full specification: [`SPEC.md`](SPEC.md). Documentation: [`docs/`](docs/00-overview.md).

## The 9-stage flow

```
 G0 takeover ──[G0]──► onboard            (existing codebases only)

 0 intake ─► 1 analyze ──[G1]──► 2 research ─► 3 architect ──[G2]──► 4 design ──[G2b]──►
 5 plan ──[G3]──► 6 build (dev ⇄ reviewer) ─► 7 verify ──[G4]──► 8 release ──[G5: always a human]──► 9 operate
                                                                                                    │
                     retro ◄── journal + scorecard ◄────────────────────────────────────────────────┘

 [Gn] = approval gate (on/off in .team/config.json; G5_prod always needs a human)
 Size S: intake → analyze → build → verify → release.  Size M skips architect.  Size L runs all 9 stages.
```

## Seven principles

1. **An agent is a person** — every role has a working contract; there is always a manager (`team-leader`) and a lead engineer (`tech-lead`).
2. **State lives on disk** — every stage leaves an artifact in `docs/team/`; the current position is computed from the artifacts.
3. **Machine before LLM** — hooks, permissions and scripts are LAW; rules, skills and CLAUDE.md are GUIDANCE.
4. **Platform-independent** — the core holds only process and roles; stack commands live in the profile's `cmd.*` slots.
5. **Call the right person, only when needed** — every call has a one-sentence reason recorded in the journal.
6. **Measure before fixing** — a quantitative scorecard + a qualitative journal; every change has evidence, an eval, a canary, a rollback.
7. **Humans decide** — gates are configuration; improvement proposals wait for human approval.

## Installation

Way 1 — marketplace (recommended), typed inside Claude Code:

```
/plugin marketplace add hivx/automation-ai
/plugin install team@automation-ai
```

Way 2 — `npx skills` (optional, if that CLI is available). Installs skills only, without agents and hooks, so the machine rules do not run:

```
npx skills add hivx/automation-ai
```

Way 3 — copy locally into the project's `.claude/` (no marketplace needed):

```
git clone https://github.com/hivx/automation-ai
automation-ai/scripts/install-local.sh [--dry-run] [--force] /path/to/project
```

With a local install, commands are `/team-<name>` instead of `/team:<name>`. Details, uninstalling and settings scopes: [`docs/06-install.md`](docs/06-install.md).

## The first hour on an existing codebase

1. `/team:takeover` — a cost-controlled 4-tier scan that changes nothing; writes `docs/team/assessment.md`, `ai-readiness.md`, `profile-proposal.md`, `debt.md`, `open-questions.md`.
2. Read the report, answer the open questions, add the line `Approved-by: <name> <YYYY-MM-DD>` at the top of `docs/team/ai-readiness.md` (gate G0).
3. `/team:onboard` — creates `.team/profile.json`, `.team/config.json`, the `team` block in `CLAUDE.md`, `.claude/settings.json`; prints the recommended plugin install commands (installs nothing itself).
4. `/team:intake "<raw request>"` — `team-leader` picks the playbook and the size; follow along with `/team:status`.

Step-by-step guide: [`docs/guides/first-day-on-existing-project.md`](docs/guides/first-day-on-existing-project.md).

## Everyday commands

| Task                                       | Command                                     | Who does it                    |
| ------------------------------------------ | ------------------------------------------- | ------------------------------ |
| Take over an existing project              | `/team:takeover`                          | team-leader (+ researcher)     |
| Configure the team for the project         | `/team:onboard`                           | team-leader                    |
| Hand in a new request                      | `/team:intake "<request>"`                | team-leader                    |
| Report a bug                               | `/team:intake --type bug "<description>"` | team-leader → dev             |
| Continue to the next gate                  | `/team:run`                               | team-leader → tech-lead       |
| See where things stand, who waits for whom | `/team:status`                            | team-leader                    |
| Save / reload a session                    | `/team:session`                           | team-leader                    |
| Acceptance                                 | `/team:verify`                            | qa                             |
| Open a pull request                        | `/team:pr`                                | tech-lead                      |
| Release                                    | `/team:release`                           | devops (a human approves prod) |
| Fix a red CI                               | `/team:ci`                                | devops                         |
| Clean up without changing behavior         | `/team:clean`                             | maintainer                     |
| Give feedback on the team                  | `/team:feedback "<feedback>"`             | team-leader                    |
| Look back and improve                      | `/team:retro`                             | coach                          |

Full table: [`docs/guides/want-x-type-y.md`](docs/guides/want-x-type-y.md).

## Repo layout

```
.claude-plugin/   plugin.json (team), marketplace.json (automation-ai)
agents/           13 roles: team-leader, tech-lead, coach, analyst, researcher, architect,
                  designer, dev, reviewer, qa, writer, maintainer, devops
skills/<name>/    26 skills = commands /team:<name>
workflows/        17 playbooks + batch/
hooks/            hooks.json (machine rules)
scripts/          validate.sh, install-local.sh, team.py, ... (bash + python3 stdlib + jq)
handbook/         STD.md (engineering handbook) and appendices
profiles/         sample profiles per stack
templates/        artifacts/, project/, schemas/
evals/            eval scenarios for the discipline skills
docs/             documentation
```

## Requirements

- Claude Code ≥ 2.1.
- `bash`, `python3` (standard library only), `jq`, `git`; `gh` is optional.

## License

MIT — see [`LICENSE`](LICENSE).
