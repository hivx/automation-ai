#!/usr/bin/env bash
# check-git.sh — hook PreToolUse (Bash): luật git của đội.
# Chặn (thoát 2): push ngoài team/* (nhánh bảo vệ nêu rõ), --force/-f/+refspec, push --delete,
#   rebase -i / reset --hard trên nhánh bảo vệ, commit --no-verify/-n, filter-branch/filter-repo.
# Cảnh báo (thoát 0, stderr + additionalContext): message commit sai STD-NAME-5.
# Đọc JSON hook từ stdin: tool_input.command, cwd. Nhánh bảo vệ: config.protected_branches + base_branch.
# Dùng: check-git.sh [--root DIR] < hook.json ; check-git.sh --help
set -uo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
[[ ${1:-} == --help || ${1:-} == -h ]] && { show_help "$0"; exit 0; }
team_init "$@"
read_input
cmd="$(input_get '.tool_input.command')"
[[ $cmd == *git* ]] || allow
python3 -I "$TEAMLIB" check-git --root "$TEAM_ROOT" <<<"$HOOK_INPUT"
