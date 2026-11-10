# Choosing a tool: hook, script, rule, skill or agent

Use this table before adding anything to the kit or to a project's `.claude/`. Go from the top down and stop at the first row that matches.

## Decision table
| # | If the job needs to... | Use | Why |
|---|---|---|---|
| 1 | Happen 100% of the time, with no room for error | hook + script (and `permissions.deny` if it blocks a permission) | The machine always runs it; an LLM can ignore text (STD level 3) |
| 2 | Compute something or read data | script | Deterministic, cheap, costs no tokens |
| 3 | Carry static knowledge tied to one kind of path | rule with `paths:` in `.claude/rules/` | Loaded only when a matching file is touched |
| 4 | Run a multi-step process with checkpoints | skill | Loaded on call; steps, stop points, evidence |
| 5 | Have its own context, tool set or model | agent | Clean context, narrow permissions, fitting model |

Side rule: anything that can be written as a hook is NOT written as a rule.

## Examples
| Job | Choice | Note |
|---|---|---|
| Block edits to `.env` files | PreToolUse hook + `permissions.deny` | Row 1; slot `protected_paths` |
| Know the project's test command | slot `cmd.test_one` in the profile, read by a script | Row 2; never write the command into a skill/agent |
| Work out which stage a feature is in | script (`team.py status`) | Row 2; state is computed from artifacts |
| Format a file after every edit | PostToolUse hook calling a script that reads `formatters_by_ext` | Row 1 |
| How to write a migration in this repo | rule with `paths:` pointing at the migration directory | Row 3; loaded only when a migration is touched |
| Test conventions of the test directory | rule with `paths:` pointing at `structure.tests` | Row 3 |
| Run acceptance | skill `verify` | Row 4; many steps, output must be pasted |
| Take over a project layer by layer | skill `takeover` | Row 4; per-layer budget, stop points |
| Review in a clean context | agent `reviewer` | Row 5; does not see the dev's conversation, strong model |
| Read many files to find where to edit | built-in agent `Explore` | Row 5; keeps the main context lean |
| Forbid pushing to protected branches | PreToolUse(Bash) hook + `permissions.deny` | Row 1; NOT written as a rule |

## Signs of a wrong choice
- **A rule that should be a hook:** the rule says "never", "always" or "must" about a tool action that can be recognized (editing a path, a git command). Turn it into a hook.
- **A skill that is only prose:** the skill has no numbered steps, no checkpoints and asks for no evidence. Rewrite it as a process or turn it into a rule.
- **An agent for a two-minute job:** calling an agent for one command or one file read. Do it in place or use a script.
- **A script that calls an LLM to "judge":** computation must be deterministic. Hand the part that needs judgment to an agent.
- **Knowledge written in two places:** a rule and a skill say the same thing. Keep one place; the other points to it.
- **Stack commands written into a skill/agent/hook:** always read them from the `cmd.*` slots.
