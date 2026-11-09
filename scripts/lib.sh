#!/usr/bin/env bash
# lib.sh — hàm dùng chung cho hook và script của kit `team`. Chỉ bash + jq + python3 stdlib.
# Dùng: . "$(dirname "${BASH_SOURCE[0]}")/lib.sh"; team_init "$@"
#
#   team_init [--root DIR]   đặt TEAM_ROOT: --root > $CLAUDE_PROJECT_DIR > $PWD
#   read_input               đọc JSON hook từ stdin một lần vào HOOK_INPUT
#   input_get <jq-path>      lấy trường từ HOOK_INPUT (rỗng nếu không có)
#   profile_get <jq-path>    đọc .team/profile.json
#   config_get <jq-path>     đọc .team/config.json (thiếu thì đọc config mặc định của kit)
#   rel_path <path>          đường dẫn tương đối so với TEAM_ROOT (rỗng nếu nằm ngoài)
#   is_protected <rel>       0 nếu khớp protected_paths hoặc .git/**
#   under_allowed_roots <rel> 0 nếu nằm dưới structure.allowed_new_file_roots
#   log_event <json>         nối một dòng vào docs/team/metrics/runs.jsonl
#   current_stage / current_feature   đọc .team/current.json
#   block <msg>              in stderr, thoát 2 (hook chặn)
#   allow                    thoát 0

KIT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEAMLIB="$KIT_DIR/scripts/teamlib.py"
TEAM_ROOT=""
HOOK_INPUT=""

team_init() {
  TEAM_ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
  while (( $# )); do
    case "$1" in
      --root) TEAM_ROOT="$2"; shift 2 ;;
      --root=*) TEAM_ROOT="${1#--root=}"; shift ;;
      *) shift ;;
    esac
  done
  TEAM_ROOT="$(cd "$TEAM_ROOT" 2>/dev/null && pwd || echo "$TEAM_ROOT")"
  export TEAM_ROOT
}

show_help() { # show_help <script>: in khối chú thích đầu file
  sed -n '2,/^[^#]/p' "$1" | sed '$d' | sed 's/^# \{0,1\}//'
}

read_input() {
  if [[ -z $HOOK_INPUT && ! -t 0 ]]; then HOOK_INPUT="$(cat)"; fi
}

input_get() { jq -r "$1 // empty" <<<"$HOOK_INPUT" 2>/dev/null; }

profile_get() {
  local f="$TEAM_ROOT/.team/profile.json"
  [[ -f $f ]] && jq -r "$1 // empty" "$f" 2>/dev/null
}

config_get() {
  local f="$TEAM_ROOT/.team/config.json"
  [[ -f $f ]] || f="$KIT_DIR/templates/project/team/config.json"
  jq -r "$1 // empty" "$f" 2>/dev/null
}

rel_path() { python3 -I "$TEAMLIB" relpath --root "$TEAM_ROOT" "$1"; }
is_protected() { python3 -I "$TEAMLIB" is-protected --root "$TEAM_ROOT" "$1" >/dev/null; }
under_allowed_roots() { python3 -I "$TEAMLIB" allowed-root --root "$TEAM_ROOT" "$1" >/dev/null; }

log_event() {
  local dir="$TEAM_ROOT/docs/team/metrics"
  mkdir -p "$dir" 2>/dev/null || return 0
  jq -c . <<<"$1" >>"$dir/runs.jsonl" 2>/dev/null || true
}

current_stage() { jq -r '.stage // empty' "$TEAM_ROOT/.team/current.json" 2>/dev/null; }
current_feature() { jq -r '.feature // empty' "$TEAM_ROOT/.team/current.json" 2>/dev/null; }

block() { printf '%s\n' "$*" >&2; exit 2; }
allow() { exit 0; }
