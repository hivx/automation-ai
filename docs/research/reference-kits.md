# Reference kits

Research for P7 (how to write skills/agents). Shallow clone: `git clone --depth 1 <repo> /tmp/ref/<name>`. A later round re-studies only the repos whose HEAD differs from the hash below. Credits: `docs/credits.md`.

## Repos and HEAD (round 1, 2026-11-09)
| Repo | HEAD | Used for |
|---|---|---|
| addyosmani/agent-skills | 301b02b12bff98e4688e6984af6556802322bbde | skill structure (Overview · When to Use · Process · Common Rationalizations · Red Flags · Verification · See Also); TDD, planning, code review, git workflow, spec, interview |
| obra/superpowers | 22f0b463e7a5e579904dd6211a520321035526f7 | using-skills, writing-plans, executing-plans, subagent-driven-development, verification-before-completion |
| anthropics/skills | 2c5958ecac7cee2b583967a2c4981d0f4a75c579 | skill-creator, the SKILL.md specification |
| wshobson/agents | 9c61ab243def98f72da12abd41cfcf5bcd91af9d | agent-teams, debugger |
| VoltAgent/awesome-claude-code-subagents | ed74d115b7fb7026a22a4f816a8e3250f425e3b4 | code-reviewer, qa-expert, test-automator, multi-agent-coordinator |
| affaan-m/everything-claude-code | d2ef2680594f9a17526a6e1a2e18b3d242c5d17b | rules, hooks, settings (later round) |
| bmad-code-org/BMAD-METHOD | a867e1604b365d48ea03cbd109da1066ba0c84bc | agent personas, craft-subagents |
| ryoppippi/ccusage | 0c1bdd193524dcbbceef9caae3a5f4e8f8d06b9d | reading token logs (later round, for `measure.py --logs`) |

## Comparison (measured with `wc -w`, frontmatter excluded for SKILL.md)
| Kit | Skills | Median words per SKILL.md | Agents | Median words per agent | Common sections |
|---|---|---|---|---|---|
| addyosmani/agent-skills | 25 | 1,985 | 4 | 583 | Overview (26), When to Use (24), Common Rationalizations (24), Red Flags (24), Verification (24), See Also (8) |
| obra/superpowers | 15 | 1,246 | — | — | Overview, When to use, process, Red Flags, rationalization table |
| anthropics/skills | 19 | 1,149 | — | — | varies per skill |
| wshobson/agents | — | — | 202 | 951 | Capabilities, Behavioral traits, Response approach |
| VoltAgent subagents | — | — | 166 | 901 | Focus areas, checklist, communication protocol |
| **team — BEFORE (v0.1.0)** | 26 | 292 (full skills) · 191 (always-loaded) | 13 | 342 | 8 sections of its own |

## Where we are headed
The end-of-round update table ("AFTER") is at the end of this file.

## Where we are headed — AFTER round 1 (2026-11-09)
| Kit | Median words, full skills | Median words, discipline skills | Median words, agents | Sections |
|---|---|---|---|---|
| addyosmani/agent-skills | 1,985 | — | 583 | 7 standard sections |
| obra/superpowers | 1,246 | — | — | — |
| **team — AFTER round 1** | 303.5 (20 skills; 7 rewritten: 1,316–1,590) | **1,502.5** | 348 (13; 5 rewritten: 902–1,062) | 10 skill sections, 10 agent sections, 4 sections for always-loaded skills |

Note: the team's words were counted per Vietnamese syllable (each syllable is one word when split on whitespace), so the same content gave a "word" count about 1.3–1.5 times higher than English.

## Round 2 (2026-11-10)
HEAD compared with `git ls-remote`: 7 of 8 repos unchanged from the table above (repos not re-studied, but the reference files NOT read in round 1 were read for the 21 new items — list in `docs/research/kit-audit-round2.md`). `ryoppippi/ccusage` changed HEAD → `c782234083efada49302b2421458b6f7b622ef43`; not studied, because it only serves `measure.py --logs` and is not tied to any skill/agent in this round.

## Where we are headed — AFTER round 2 (2026-11-10)
| Kit | Median words, full skills | Median words, discipline skills | Median words, agents | % of items at the bar |
|---|---|---|---|---|
| addyosmani/agent-skills | 1,985 | — | 583 | — |
| obra/superpowers | 1,246 | — | — | — |
| wshobson/agents | — | — | 951 | — |
| VoltAgent subagents | — | — | 901 | — |
| **team — AFTER round 1** | 303.5 | 1,502.5 | 348 | 46% (18/39) |
| **team — AFTER round 2** | **1,436.5** (20 skills; 1,249–1,590) | **1,502** | **924** (13; 830–1,105) | **100% (39/39)** |

The team's numbers were measured with `scripts/kit-metrics.py` (body, frontmatter excluded; Vietnamese counted per syllable — see the note above).
