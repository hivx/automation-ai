#!/usr/bin/env bash
# protect.sh — hook PreToolUse (Edit|Write|NotebookEdit): chặn ghi vào vùng cấm.
# Chặn (thoát 2): .git/**, .claude/settings*.json, protected_paths (STD-SEC-1);
#   file MỚI ngoài structure.allowed_new_file_roots (STD-STRUCT-1).
# Luôn cho phép: docs/team/**, .team/** (trừ profile/config ngoài onboard), .claude/{agent-memory,skills,agents,rules}/**, CHANGELOG.md ở gốc.
# Đọc JSON hook từ stdin: tool_name, tool_input.file_path | tool_input.notebook_path.
# Dùng: protect.sh [--root DIR] < hook.json ; protect.sh --help
set -uo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
[[ ${1:-} == --help || ${1:-} == -h ]] && { show_help "$0"; exit 0; }
team_init "$@"
read_input
path="$(input_get '.tool_input.file_path // .tool_input.notebook_path')"
[[ -z $path ]] && allow
path="${path//\\//}"
rel="$(rel_path "$path")"
[[ -z $rel ]] && allow   # ngoài dự án (ví dụ memory của người dùng)

case "$rel" in
  .git|.git/*) block "BLOCKED (STD-SEC-1): không sửa trong .git/." ;;
  .claude/settings.json|.claude/settings.local.json)
    block "BLOCKED (STD-SEC-1): $rel chỉ đổi qua /team:onboard hoặc do người sửa." ;;
  .team/profile.json|.team/config.json)
    [[ "$(current_stage)" == onboard ]] && allow
    block "BLOCKED (STD-SEC-1): $rel chỉ đổi qua /team:onboard hoặc do người sửa." ;;
  docs/team/*|.team/*|.claude/agent-memory/*|.claude/skills/*|.claude/agents/*|.claude/rules/*) allow ;;
  CHANGELOG.md) allow ;;   # DoD đòi CHANGELOG ở gốc (STD-DOC-3)
esac

if pat="$(python3 -I "$TEAMLIB" is-protected --root "$TEAM_ROOT" "$rel")"; then
  block "BLOCKED (STD-SEC-1): '$rel' khớp protected_paths ('$pat'). Người sửa tay, hoặc sửa protected_paths trong .team/profile.json nếu khai nhầm."
fi

if [[ ! -e $TEAM_ROOT/$rel ]] && ! under_allowed_roots "$rel"; then
  roots="$(profile_get '.structure.allowed_new_file_roots | join(", ")')"
  block "BLOCKED (STD-STRUCT-1): file mới '$rel' nằm ngoài allowed_new_file_roots ($roots). Đặt file đúng chỗ, hoặc xin người thêm thư mục vào profile."
fi
allow
