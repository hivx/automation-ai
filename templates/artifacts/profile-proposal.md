Feature: <ID>
Stage: takeover
Author-agent: team-leader
Date: <YYYY-MM-DD>
Approved-by:
<!-- Gate: the approver fills in the line above as `Approved-by: <name> <YYYY-MM-DD>`. Leave it empty when there is no gate. -->

# Proposed profile

Rules: use only slot names that exist in `profile.schema.json` (exactly as in the slot column below); `{file}` is the ONLY placeholder in a command (file path relative to the repo root); leave slots that do not apply empty. Check `cmd.test_one` by running it on a real test file.

| slot | value | evidence | confidence |
|---|---|---|---|
| stack | | <manifest file> | high / medium / low |
| cmd.install | | | |
| cmd.build | | | |
| cmd.test | | | |
| cmd.test_one | <command with {file}> | <ran with tests/…: output> | |
| cmd.lint | | | |
| cmd.typecheck | | | |
| cmd.format | <command with {file} or empty> | | |
| structure.src / structure.tests | | | |
| naming.test_file | | | |
| structure.allowed_new_file_roots | | <root folders from detect-stack> | |
| protected_paths | | <secrets, lockfiles, vendored, prod config> | |

## Uncertain slots (need the human to confirm)
- <...>

## Scanned / Not scanned / Confidence
<...>
