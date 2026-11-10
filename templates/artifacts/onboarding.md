Feature: <ID>
Stage: onboard
Author-agent: team-leader
Date: <YYYY-MM-DD>
Approved-by:
<!-- Gate: the approver fills in the line above as `Approved-by: <name> <YYYY-MM-DD>`. Leave it empty when there is no gate. -->

# Onboarding

## Created / skipped / manual work
Kit: `team` <version from plugin.json>. A rerun of onboard may only produce "skipped (already present)" for every row below.

| Status | File | Write method (create / merge JSON / insert block / skip) | Template source | Notes |
|---|---|---|---|---|
| created | `.team/profile.json` | create | profile-proposal.md / profiles/<stack>.json | |

## Trial run
| Slot | Command | Exit code | Output (excerpt) |
|---|---|---|---|
| cmd.install | | | |
| cmd.lint | | | |
| cmd.test | | | |

## Recommended plugins (not installed)
- `claude plugin install <name@marketplace>`

## Manual work for the human
- <...>
