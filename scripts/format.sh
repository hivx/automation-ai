#!/usr/bin/env bash
# format.sh — PostToolUse hook (Edit|Write|NotebookEdit): runs the formatter for the file extension from formatters_by_ext.
# Replaces {file} with the relative path; a missing or failing formatter is skipped. Always exits 0.
# Usage: format.sh [--root DIR] < hook.json ; format.sh --help
set -uo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
[[ ${1:-} == --help || ${1:-} == -h ]] && { show_help "$0"; exit 0; }
team_init "$@"
read_input
path="$(input_get '.tool_input.file_path // .tool_input.notebook_path')"
[[ -z $path ]] && exit 0
rel="$(rel_path "${path//\\//}")"
[[ -z $rel || ! -f $TEAM_ROOT/$rel ]] && exit 0
ext=".${rel##*.}"
[[ $rel == *.* ]] || exit 0
fmt="$(profile_get ".formatters_by_ext[\"$ext\"]")"
[[ -z $fmt ]] && exit 0
quoted="$(printf '%q' "$rel")"
cmdline="${fmt//\{file\}/$quoted}"
first="${cmdline%% *}"
command -v "$first" >/dev/null 2>&1 || exit 0
( cd "$TEAM_ROOT" && timeout 50 bash -c "$cmdline" ) >/dev/null 2>&1 || true
exit 0
