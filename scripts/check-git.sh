#!/usr/bin/env bash
# check-git.sh — PreToolUse hook (Bash): the team's git rules.
# Blocks (exit 2): push outside team/* (protected branches named explicitly), --force/-f/+refspec, push --delete,
#   rebase -i / reset --hard on a protected branch, commit --no-verify/-n, filter-branch/filter-repo.
# Warns (exit 0, stderr + additionalContext): commit message that breaks STD-NAME-5.
# Reads hook JSON from stdin: tool_input.command, cwd. Protected branches: config.protected_branches + base_branch.
# Usage: check-git.sh [--root DIR] < hook.json ; check-git.sh --help
set -uo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
[[ ${1:-} == --help || ${1:-} == -h ]] && { show_help "$0"; exit 0; }
team_init "$@"
read_input
cmd="$(input_get '.tool_input.command')"
[[ $cmd == *git* ]] || allow
python3 -I "$TEAMLIB" check-git --root "$TEAM_ROOT" <<<"$HOOK_INPUT"
