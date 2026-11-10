#!/usr/bin/env bash
# log-session.sh — PostCompact and SessionEnd hook: session metrics into docs/team/metrics/sessions.jsonl.
# PostCompact: {ts, event:"compact", session_id, feature, stage, trigger}; counts the session's compactions.
# SessionEnd:  {ts, event:"end", session_id, feature, stage, reason, duration_s, compactions}.
# Usage: log-session.sh [--root DIR] < hook.json ; log-session.sh --help
set -uo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
[[ ${1:-} == --help || ${1:-} == -h ]] && { show_help "$0"; exit 0; }
team_init "$@"
read_input
cd "$TEAM_ROOT" 2>/dev/null || exit 0
[[ -d docs/team ]] || exit 0
mkdir -p docs/team/metrics .team/session
sid="$(input_get '.session_id')"; event="$(input_get '.hook_event_name')"
feat="$(current_feature)"; stage="$(current_stage)"; now="$(date -Iseconds)"
count_file=".team/session/$sid.compactions"
if [[ $event == PostCompact ]]; then
  n=$(( $(cat "$count_file" 2>/dev/null || echo 0) + 1 )); echo "$n" >"$count_file"
  jq -nc --arg ts "$now" --arg sid "$sid" --arg f "$feat" --arg s "$stage" --arg t "$(input_get '.trigger')" \
    '{ts:$ts, event:"compact", session_id:$sid, feature:$f, stage:$s, trigger:$t}' >>docs/team/metrics/sessions.jsonl
  exit 0
fi
start="$(cat ".team/session/$sid.start" 2>/dev/null || true)"
dur=null; [[ -n $start ]] && dur=$(( $(date +%s) - start ))
jq -nc --arg ts "$now" --arg sid "$sid" --arg f "$feat" --arg s "$stage" --arg r "$(input_get '.reason')" \
  --argjson d "$dur" --argjson c "$(cat "$count_file" 2>/dev/null || echo 0)" \
  '{ts:$ts, event:"end", session_id:$sid, feature:$f, stage:$s, reason:$r, duration_s:$d, compactions:$c}' \
  >>docs/team/metrics/sessions.jsonl
exit 0
