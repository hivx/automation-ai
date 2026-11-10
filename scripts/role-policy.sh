#!/usr/bin/env bash
# role-policy.sh — PreToolUse hook (Edit|Write|NotebookEdit|Bash|Agent): per-role limits (ADJ-02).
# Reads agent_type from the hook JSON; when the role is listed in hooks/role-policy.json it checks:
#   file writes only into the `write` patterns; Bash per `bash` ("any" | "read-only" | {"allow": [...]});
#   Agent may only call a subagent_type listed in `agents`. A role not in the file → allowed.
# Usage: role-policy.sh [--root DIR] [--policy FILE] < hook.json ; role-policy.sh --help
set -uo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
[[ ${1:-} == --help || ${1:-} == -h ]] && { show_help "$0"; exit 0; }
team_init "$@"
policy="$KIT_DIR/hooks/role-policy.json"
for ((i = 1; i <= $#; i++)); do [[ ${!i} == --policy ]] && { j=$((i + 1)); policy="${!j}"; }; done
read_input
jq -e . >/dev/null 2>&1 <<<"$HOOK_INPUT" || block "BLOCKED (role-policy): malformed hook JSON — a safety hook does not allow what it cannot read."
[[ -n "$(input_get '.agent_type')" ]] || allow
python3 -I "$TEAMLIB" role-policy --root "$TEAM_ROOT" --policy "$policy" <<<"$HOOK_INPUT"
