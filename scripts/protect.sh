#!/usr/bin/env bash
# protect.sh — PreToolUse hook (Edit|Write|NotebookEdit|Bash): blocks writes into forbidden areas.
# Bash (K-24): recognizable write targets (redirection, tee, rm, mv, cp, sed -i, …) — see teamlib.protect_bash.
# Blocks (exit 2): .git/**, .claude/settings*.json, protected_paths (STD-SEC-1);
#   a NEW file outside structure.allowed_new_file_roots (STD-STRUCT-1).
# Always allowed: docs/team/**, .team/** (except profile/config outside onboard), .claude/{agent-memory,skills,agents,rules}/**, CHANGELOG.md at the root.
# Reads hook JSON from stdin: tool_name, tool_input.file_path | tool_input.notebook_path.
# Usage: protect.sh [--root DIR] < hook.json ; protect.sh --help
set -uo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
[[ ${1:-} == --help || ${1:-} == -h ]] && { show_help "$0"; exit 0; }
team_init "$@"
read_input
if [[ "$(input_get '.tool_name')" == Bash ]]; then
  # K-24: write targets of a shell command (redirection, tee, rm, mv, cp, sed -i, …) go through the same forbidden-area rules.
  printf '%s' "$HOOK_INPUT" | python3 -I "$TEAMLIB" protect-bash --root "$TEAM_ROOT" || exit 2
  allow
fi
path="$(input_get '.tool_input.file_path // .tool_input.notebook_path')"
[[ -z $path ]] && allow
path="${path//\\//}"
rel="$(rel_path "$path")"
[[ -z $rel ]] && allow   # outside the project (for example the user's memory)

case "$rel" in
  .git|.git/*) block "BLOCKED (STD-SEC-1): do not edit inside .git/." ;;
  .claude/settings.json|.claude/settings.local.json)
    block "BLOCKED (STD-SEC-1): $rel changes only through /team:onboard or by the human." ;;
  .team/profile.json|.team/config.json)
    [[ "$(current_stage)" == onboard ]] && allow
    block "BLOCKED (STD-SEC-1): $rel changes only through /team:onboard or by the human." ;;
  docs/team/*|.team/*|.claude/agent-memory/*|.claude/skills/*|.claude/agents/*|.claude/rules/*) allow ;;
  CHANGELOG.md) allow ;;   # the DoD requires CHANGELOG at the root (STD-DOC-3)
esac

if pat="$(python3 -I "$TEAMLIB" is-protected --root "$TEAM_ROOT" "$rel")"; then
  block "BLOCKED (STD-SEC-1): '$rel' matches protected_paths ('$pat'). The human edits it by hand, or fixes protected_paths in .team/profile.json if it was declared by mistake."
fi

if [[ ! -e $TEAM_ROOT/$rel ]] && ! under_allowed_roots "$rel"; then
  roots="$(profile_get '.structure.allowed_new_file_roots | join(", ")')"
  block "BLOCKED (STD-STRUCT-1): new file '$rel' is outside allowed_new_file_roots ($roots). Put the file in the right place, or ask the human to add the directory to the profile."
fi
allow
