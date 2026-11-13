#!/usr/bin/env bash
# lib.sh — shared functions for the hooks and scripts of the `team` kit. Only bash + jq + python3 stdlib.
# Usage: . "$(dirname "${BASH_SOURCE[0]}")/lib.sh"; team_init "$@"
#
#   team_init [--root DIR]   sets TEAM_ROOT: --root > $CLAUDE_PROJECT_DIR > $PWD
#   read_input               reads the hook JSON from stdin once into HOOK_INPUT
#   input_get <jq-path>      gets a field from HOOK_INPUT (empty if absent)
#   profile_get <jq-path>    reads .team/profile.json
#   config_get <jq-path>     reads .team/config.json (falls back to the kit's default config)
#   rel_path <path>          path relative to TEAM_ROOT (empty if outside)
#   is_protected <rel>       0 if it matches protected_paths or .git/**
#   under_allowed_roots <rel> 0 if it is under structure.allowed_new_file_roots
#   log_event <json>         appends one line to docs/team/metrics/runs.jsonl
#   current_stage / current_feature   read .team/current.json
#   hook_feature / hook_stage / build_active   per-feature state for parallel waves
#   block <msg>              prints to stderr, exits 2 (the hook blocks)
#   allow                    exits 0

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

show_help() { # show_help <script>: prints the comment block at the top of the file
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
# hook_feature: the feature of the subagent that fired the hook (from its transcript), else current.json.
hook_feature() {
  local tp f=""; tp="$(input_get '.agent_transcript_path')"
  [[ -n $tp ]] && f="$(python3 -I "$TEAMLIB" agent-feature "$tp")"
  [[ -n $f ]] && echo "$f" || current_feature
}
# hook_stage: current.json's stage only when it describes the hook's feature (parallel waves), else empty.
hook_stage() { [[ "$(hook_feature)" == "$(current_feature)" ]] && current_stage; }
# build_active: a build is running (.team/active-build-<ID> per feature; the old single .team/active-build still counts).
build_active() { compgen -G "$TEAM_ROOT/.team/active-build*" >/dev/null; }

# enforcement: config `enforcement` = "block" makes a rule violation stop the tool (exit 2). Anything else (default
# "warn") lets the tool run and hands the rule to Claude as context: skills and rules guide the work, hooks remind.
enforcement() { [[ "$(jq -r '.enforcement // empty' "$TEAM_ROOT/.team/config.json" 2>/dev/null)" == block ]] && echo block || echo warn; }
remind() { # remind <message>: the rule as a reminder, never a stop (PreToolUse/PostToolUse → additionalContext, else systemMessage)
  local msg="${1/#BLOCKED/RULE (reminder, not enforced)}" ev; ev="$(input_get '.hook_event_name')"
  printf '%s\n' "$msg" >&2
  if [[ $ev == PreToolUse || $ev == PostToolUse ]]; then
    jq -nc --arg e "$ev" --arg m "$msg" '{hookSpecificOutput:{hookEventName:$e, additionalContext:$m}}'
  else
    jq -nc --arg m "$msg" '{systemMessage:$m}'
  fi
}
block() { [[ "$(enforcement)" == block ]] && { printf '%s\n' "$*" >&2; exit 2; }; remind "$*"; exit 0; }
allow() { exit 0; }
