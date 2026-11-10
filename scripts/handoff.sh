#!/usr/bin/env bash
# handoff.sh — PreCompact (manual|auto) and SessionEnd hook: writes the session handoff.
# Writes .team/session/<session_id>.md, at most memory.handoff_max_lines lines, only what is NOT in the artifacts:
# current feature/stage, open tasks, waiting/blocked lines, last 3 journal lines, first action of the next session.
# Usage: handoff.sh [--root DIR] < hook.json ; handoff.sh --help
set -uo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
[[ ${1:-} == --help || ${1:-} == -h ]] && { show_help "$0"; exit 0; }
team_init "$@"
read_input
cd "$TEAM_ROOT" 2>/dev/null || exit 0
[[ -d .team ]] || exit 0
sid="$(input_get '.session_id')"; sid="${sid:-manual}"
event="$(input_get '.hook_event_name')"
max="$(config_get '.memory.handoff_max_lines')"; max="${max:-40}"
feat="$(current_feature)"; stage="$(current_stage)"
mkdir -p .team/session
{
  echo "# Handoff $sid (${event:-manual}, $(date -Iseconds))"
  echo "- Feature/stage: ${feat:-—} / ${stage:-—} (agent $(jq -r '.agent // "—"' .team/current.json 2>/dev/null || echo —))"
  if [[ -n $feat && -f docs/team/features/$feat/tasks.md ]]; then
    open="$(grep -oE '^- \[ \] T[0-9]+' "docs/team/features/$feat/tasks.md" | awk '{print $4}' | paste -sd, -)"
    echo "- Open tasks: ${open:-none}"
  fi
  if [[ -n $feat ]]; then
    python3 -I "$KIT_DIR/scripts/team.py" status "$feat" --waiting --root "$TEAM_ROOT" 2>/dev/null | sed 's/^/- /' | head -n 5
    if [[ -f docs/team/journal/$feat.md ]]; then
      echo "- Latest journal:"; grep -v '^\s*$' "docs/team/journal/$feat.md" | grep -v '^#' | tail -n 3 | sed 's/^/  /'
    fi
    echo "- First action next session: $(python3 -I "$KIT_DIR/scripts/team.py" next "$feat" --root "$TEAM_ROOT" 2>/dev/null | head -n 1)"
  fi
} | head -n "$max" >".team/session/$sid.md"
exit 0
