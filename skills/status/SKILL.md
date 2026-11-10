---
name: status
description: Use when the human asks where a feature stands, who is waiting on whom, or what is blocked.
argument-hint: "[<ID>]"
allowed-tools: Bash(python3 *) Bash(cat *)
---

# Team status

## Overview
Print the state computed from artifacts (no stored pointer) and who is waiting on whom. `$ARGUMENTS`: a feature ID; empty = every feature. Writes no files.

## Process
1. Check that `docs/team/` exists. If not → print: project has code → `/team:takeover`; empty repo → `/team:onboard --new`; stop.
2. Run (Bash): `python3 "<kit>/scripts/team.py" status $ARGUMENTS` (`<kit>` = the path read from `.team/plugin_root`, typed literally).
3. Print the output VERBATIM in a code block, including the "Applicable gates" column.
4. For each `WAITING_FOR_APPROVAL`, `WAITING_FOR_ANSWER`, `BLOCKED`, `REWORK`, `DESIGN_DEFECT` row: one line "Waiting on the human: <work> — <file>".
5. Print the next command exactly as the script's "Next" column gives it.
6. Script fails → print the error verbatim and `<kit>/scripts/team.py --help`; stop. Do not infer.

## Common rationalizations
| Thought | Correct action |
|---|---|
| "The script failed, I'll read the artifacts and guess" | Print the error and stop; only the script computes state. |
| "Config enables G1, so the size-S feature is waiting on G1" | Trust the "Applicable gates" column; the script already applied the size. |
| "Add a comment to be helpful" | Format only; comments belong in `/team:retro`. |
| "Summarize the table to keep it short" | Print it verbatim; the human needs the exact words to approve. |
| "A feature waits on G4, so the whole team is stalled" | A gate blocks only its own feature. |
| "No features, print an empty table" | Print the starting command `/team:intake "<request>"`. |

## Verification
- The script output is pasted verbatim.
- Each waiting state has exactly one "Waiting on the human" line.
- The next command matches the "Next" column.
