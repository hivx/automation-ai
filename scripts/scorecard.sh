#!/usr/bin/env bash
# scorecard.sh — hook SubagentStop: ghi một lần chạy của agent vào docs/team/metrics/runs.jsonl.
# Trường: ts, feature, stage, size, agent (agent_type), agent_id, skill(null), turns (đếm tin assistant
# trong agent_transcript_path), duration_s (timestamp đầu/cuối), result (đoán từ last_assistant_message),
# rework_round(null), transcript. Thiếu trường nào → null. Chỉ ghi khi dự án đã có docs/team/.
# Dùng: scorecard.sh [--root DIR] < hook.json ; scorecard.sh --help
set -uo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
[[ ${1:-} == --help || ${1:-} == -h ]] && { show_help "$0"; exit 0; }
team_init "$@"
read_input
[[ -d $TEAM_ROOT/docs/team ]] || exit 0
agent="$(input_get '.agent_type')"; [[ -z $agent ]] && exit 0
tp="$(input_get '.agent_transcript_path')"; tp="${tp/#\~/$HOME}"
turns=null; dur=null
if [[ -f $tp ]]; then
  turns="$(jq -s '[.[] | select(.type == "assistant")] | length' "$tp" 2>/dev/null || echo null)"
  dur="$(jq -rs '[.[] | .timestamp? // empty | sub("\\.[0-9]+Z$"; "Z") | fromdateiso8601] | if length > 1 then (max - min) else null end' "$tp" 2>/dev/null || echo null)"
fi
msg="$(input_get '.last_assistant_message')"
result=done
for v in design-defect request-changes approve accepted rework BLOCKED NEEDS_ANSWER DESIGN_CONFLICT SPECIFIED; do
  [[ $msg == *"$v"* ]] && { result="$v"; break; }
done
feat="$(current_feature)"
size="$(grep -oiE '(cỡ|size)[^A-Za-z]*[SML]\b' "$TEAM_ROOT/docs/team/features/$feat/intake.md" 2>/dev/null | head -n 1 | grep -oE '[SML]$' || true)"
log_event "$(jq -nc --arg ts "$(date -Iseconds)" --arg f "$feat" --arg s "$(current_stage)" --arg z "$size" \
  --arg a "$agent" --arg id "$(input_get '.agent_id')" --argjson t "${turns:-null}" --argjson d "${dur:-null}" \
  --arg r "$result" --arg tp "$tp" \
  '{ts:$ts, feature:$f, stage:$s, size:(if $z == "" then null else $z end), agent:$a, agent_id:$id, skill:null,
    turns:$t, duration_s:$d, result:$r, rework_round:null, transcript:(if $tp == "" then null else $tp end)}')"
exit 0
