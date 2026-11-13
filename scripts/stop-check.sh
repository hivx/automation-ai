#!/usr/bin/env bash
# stop-check.sh — Stop / SubagentStop hook: no stopping until the build is green.
# stop_hook_active = true → allow the stop (avoids a loop).
# When a build is active (.team/active-build-<ID>, or the old .team/active-build): takes the code files changed against config.base_branch (skipping docs, .team, .claude,
#   .github, build/cache directories, non-code files, helper files __init__/conftest/setup/fixtures/
#   helpers/utils); runs cmd.lint, cmd.typecheck (if set), cmd.test_one for each changed test file
#   (matching naming.test_file), check-structure.sh. Failure → exit 2 with the first 40 lines.
#   Only with config `enforcement: "block"`; in the default "warn" mode the build pass is skipped and the research
#   check below is a reminder (systemMessage), never a stop.
# When a researcher stops (or, outside a subagent, the current stage is research): the research.md of that
#   agent's feature (hook_feature: from its transcript) must have '## Sources' with at least one http URL.
# Commands run in the hook's `cwd` (the dev's worktree); configuration is read from the project root.
# Usage: stop-check.sh [--root DIR] < hook.json ; stop-check.sh --help
set -uo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
[[ ${1:-} == --help || ${1:-} == -h ]] && { show_help "$0"; exit 0; }
team_init "$@"
read_input
[[ "$(input_get '.stop_hook_active')" == "true" ]] && allow
WD="$(input_get '.cwd')"; [[ -d $WD ]] || WD="$TEAM_ROOT"

agent="$(input_get '.agent_type')"
feat="$(hook_feature)"
if [[ -n $feat && ( ${agent#team:} == researcher || ( -z $agent && "$(current_stage)" == research ) ) ]]; then
  f="$TEAM_ROOT/docs/team/features/$feat/research.md"
  if [[ ! -f $f ]] || ! awk '/^## Sources/{s=1;next} s && /https?:\/\//{ok=1} END{exit ok?0:1}' "$f"; then
    block "BLOCKED (research): ${f#"$TEAM_ROOT"/} must have a '## Sources' section with at least one http URL and its access date."
  fi
fi

[[ "$(enforcement)" == block ]] || allow  # warn mode: devs run their own tests; no lint/test pass at every stop
build_active || allow
cd "$WD" || allow
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || allow
base="$(config_get '.base_branch')"; base="${base:-main}"
git rev-parse --verify -q "$base" >/dev/null || base="HEAD"
docs_dir="$(profile_get '.structure.docs')"; docs_dir="${docs_dir:-docs}"
test_glob="$(python3 -I "$TEAMLIB" test-glob "$(profile_get '.naming.test_file')")"

mapfile -t changed < <( { git diff --name-only "$base"...HEAD 2>/dev/null; git diff --name-only HEAD 2>/dev/null;
  git ls-files --others --exclude-standard; } | sort -u | while IFS= read -r p; do
  [[ -f $p ]] || continue
  case "/$p" in
    /"$docs_dir"/*|/.team/*|/.claude/*|/.github/*|*/node_modules/*|*/dist/*|*/build/*|*/target/*|*/.venv/*|*/__pycache__/*|*/.dart_tool/*|*/.cache/*) continue ;;
  esac
  case "${p##*.}" in md|txt|json|yml|yaml|toml|lock|cfg|ini|csv|xml|png|jpg|jpeg|gif|svg|pdf|ico|env) continue ;; esac
  stem="$(basename "$p")"; stem="${stem%%.*}"
  case "$stem" in __init__|conftest|setup|fixtures|helpers|utils) continue ;; esac
  printf '%s\n' "$p"
done )
(( ${#changed[@]} )) || allow

out="$(mktemp)"; trap 'rm -f "$out"' EXIT
fail=0
run() { # run <label> <command>
  echo "\$ $2" >>"$out"
  if ! timeout 540 bash -c "$2" >>"$out" 2>&1; then echo "FAIL: $1" >>"$out"; fail=1; fi
}
lint="$(profile_get '.cmd.lint')"; [[ -n $lint ]] && run lint "$lint"
tc="$(profile_get '.cmd.typecheck')"; [[ -n $tc ]] && run typecheck "$tc"
one="$(profile_get '.cmd.test_one')"
if [[ -n $one && -n $test_glob ]]; then
  for p in "${changed[@]}"; do
    # shellcheck disable=SC2053
    [[ $(basename "$p") == $test_glob ]] || continue
    run "test_one $p" "${one//\{file\}/$(printf '%q' "$p")}"
  done
fi
run structure "bash $(printf '%q' "$KIT_DIR/scripts/check-structure.sh") --root $(printf '%q' "$WD")"
if (( fail )); then
  block "$(echo "BLOCKED (STD-TEST-3): the build is not clean — fix it before stopping (also STD-STYLE-2, STD-STRUCT-6)."; head -n 40 "$out")"
fi
allow
