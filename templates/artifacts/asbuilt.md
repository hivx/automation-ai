Feature: <ID>
Stage: asbuilt
Author-agent: writer
Date: <YYYY-MM-DD>
Approved-by:
<!-- Gate: the approver fills in the line above as `Approved-by: <name> <YYYY-MM-DD>`. Leave it empty when there is no gate. -->

<!-- G5: the human adds `Approved-by-prod: <name> <YYYY-MM-DD>` at the top of this file before going to prod. -->
# As-Built <ID>

## Differences from design
| Design item | Actual | file:line | Reason |
|---|---|---|---|
| <...> | as designed / differs: <...> | | |

## Release notes (for users)
- What changed: <...>
- Who is affected: <...>
- What to do: <...>

## CHANGELOG
<entry added under [Unreleased]>

## Post-G4 debt
| DoD item qa flagged | Done | Recheck (command → result) |
|---|---|---|
| <CHANGELOG / README / docs> | <file> | <grep … → match> or "left for /team:release to check" |

## Rollback
<!-- /team:release writes this before the first deploy: trigger condition, command (from docs/team/ci.md), data part, expected duration -->

<!-- devops adds this line after a successful prod release: Released: <tag> <YYYY-MM-DD> -->
