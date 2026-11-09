#!/usr/bin/env bash
# log-run.sh — skill gọi ở cuối giai đoạn: ghi một dòng vào docs/team/metrics/runs.jsonl.
# Cờ (đều tùy chọn): --feature ID --stage S --agent A --skill K --result R --duration SEC
#   --turns N --rework N --size S|M|L --root DIR. Thiếu feature/stage → lấy từ .team/current.json.
# Dùng: log-run.sh --skill analyze --result SPECIFIED ; log-run.sh --help
set -uo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
[[ ${1:-} == --help || ${1:-} == -h ]] && { show_help "$0"; exit 0; }
team_init "$@"
declare -A v=([feature]="" [stage]="" [agent]="" [skill]="" [result]="" [duration]="" [turns]="" [rework]="" [size]="")
while (( $# )); do
  k="${1#--}"
  if [[ -n ${v[$k]+x} && $# -ge 2 ]]; then v[$k]="$2"; shift 2; else shift; fi
done
[[ -z ${v[feature]} ]] && v[feature]="$(current_feature)"
[[ -z ${v[stage]} ]] && v[stage]="$(current_stage)"
num() { [[ $1 =~ ^[0-9]+(\.[0-9]+)?$ ]] && echo "$1" || echo null; }
str() { [[ -n $1 ]] && jq -n --arg x "$1" '$x' || echo null; }
log_event "$(jq -nc --arg ts "$(date -Iseconds)" --argjson f "$(str "${v[feature]}")" --argjson s "$(str "${v[stage]}")" \
  --argjson a "$(str "${v[agent]}")" --argjson k "$(str "${v[skill]}")" --argjson r "$(str "${v[result]}")" \
  --argjson z "$(str "${v[size]}")" --argjson d "$(num "${v[duration]}")" --argjson t "$(num "${v[turns]}")" \
  --argjson w "$(num "${v[rework]}")" \
  '{ts:$ts, feature:$f, stage:$s, size:$z, agent:$a, skill:$k, turns:$t, duration_s:$d, result:$r, rework_round:$w}')"
echo "log-run: đã ghi docs/team/metrics/runs.jsonl"
