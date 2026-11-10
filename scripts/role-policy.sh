#!/usr/bin/env bash
# role-policy.sh — hook PreToolUse (Edit|Write|NotebookEdit|Bash|Agent): giới hạn theo vai (ADJ-02).
# Đọc agent_type từ JSON hook; vai có trong hooks/role-policy.json thì kiểm:
#   ghi file chỉ vào mẫu `write`; Bash theo `bash` ("any" | "read-only" | {"allow": [...]});
#   Agent chỉ gọi subagent_type trong `agents`. Vai không có trong file → cho qua.
# Dùng: role-policy.sh [--root DIR] [--policy FILE] < hook.json ; role-policy.sh --help
set -uo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
[[ ${1:-} == --help || ${1:-} == -h ]] && { show_help "$0"; exit 0; }
team_init "$@"
policy="$KIT_DIR/hooks/role-policy.json"
for ((i = 1; i <= $#; i++)); do [[ ${!i} == --policy ]] && { j=$((i + 1)); policy="${!j}"; }; done
read_input
jq -e . >/dev/null 2>&1 <<<"$HOOK_INPUT" || block "BLOCKED (role-policy): JSON hook hỏng — hook an toàn không cho qua khi không đọc được đầu vào."
[[ -n "$(input_get '.agent_type')" ]] || allow
python3 -I "$TEAMLIB" role-policy --root "$TEAM_ROOT" --policy "$policy" <<<"$HOOK_INPUT"
