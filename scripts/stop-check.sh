#!/usr/bin/env bash
# stop-check.sh — hook Stop / SubagentStop: chưa xanh thì chưa được dừng.
# stop_hook_active = true → cho dừng (tránh vòng lặp).
# Khi có .team/active-build: lấy file code đã đổi so với config.base_branch (bỏ docs, .team, .claude,
#   .github, thư mục build/cache, file không phải code, file phụ trợ __init__/conftest/setup/fixtures/
#   helpers/utils); chạy cmd.lint, cmd.typecheck (nếu có), cmd.test_one cho mỗi file test đã đổi
#   (khớp naming.test_file), check-structure.sh. Lỗi → thoát 2 với 40 dòng đầu.
# Khi stage hiện tại là research: research.md phải có '## Sources' kèm ít nhất một URL http.
# Lệnh chạy trong thư mục `cwd` của hook (worktree của dev), cấu hình đọc từ gốc dự án.
# Dùng: stop-check.sh [--root DIR] < hook.json ; stop-check.sh --help
set -uo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
[[ ${1:-} == --help || ${1:-} == -h ]] && { show_help "$0"; exit 0; }
team_init "$@"
read_input
[[ "$(input_get '.stop_hook_active')" == "true" ]] && allow
WD="$(input_get '.cwd')"; [[ -d $WD ]] || WD="$TEAM_ROOT"

stage="$(current_stage)"
if [[ $stage == research ]]; then
  f="$TEAM_ROOT/docs/team/features/$(current_feature)/research.md"
  if [[ ! -f $f ]] || ! awk '/^## Sources/{s=1;next} s && /https?:\/\//{ok=1} END{exit ok?0:1}' "$f"; then
    block "BLOCKED (research): ${f#"$TEAM_ROOT"/} phải có mục '## Sources' với ít nhất một URL http kèm ngày truy cập."
  fi
fi

[[ -f $TEAM_ROOT/.team/active-build ]] || allow
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
run() { # run <nhãn> <lệnh>
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
  { echo "BLOCKED (stop-check): build chưa sạch — sửa rồi mới dừng (STD-STYLE-2, STD-TEST-3, STD-STRUCT-6)."; head -n 40 "$out"; } >&2
  exit 2
fi
allow
