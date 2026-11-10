#!/usr/bin/env bash
# check-structure.sh — checks the structure of changes against config.base_branch (STD-STRUCT-1, STD-NAME-3).
#   1. Every NEW file (committed, staged or untracked) is under structure.allowed_new_file_roots
#      (except docs/team/, .team/, .claude/).
#   2. A new test file matches naming.test_file (under structure.tests, or a name containing "test" when colocated).
#   3. No generated files staged (STD-GIT-5): *.pyc, node_modules/, dist/, build/ (unless that directory is an allowed root).
# Prints one line per problem; exits 1 when there are problems, 0 when clean.
# Usage: check-structure.sh [--root DIR] ; check-structure.sh --help
set -uo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
[[ ${1:-} == --help || ${1:-} == -h ]] && { show_help "$0"; exit 0; }
team_init "$@"
cd "$TEAM_ROOT" || exit 0
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0
[[ -f .team/profile.json ]] || { echo "check-structure: no .team/profile.json yet — skipped"; exit 0; }
base="$(config_get '.base_branch')"; base="${base:-main}"
git rev-parse --verify -q "$base" >/dev/null || base="HEAD"
tests_dir="$(profile_get '.structure.tests')"
test_glob="$(python3 -I "$TEAMLIB" test-glob "$(profile_get '.naming.test_file')")"
mapfile -t roots < <(profile_get '.structure.allowed_new_file_roots[]?')
problems=0
report() { echo "$1"; problems=$((problems + 1)); }

mapfile -t newfiles < <( { git diff --name-only --diff-filter=A "$base"...HEAD 2>/dev/null;
  git diff --cached --name-only --diff-filter=A; git ls-files --others --exclude-standard; } | sort -u )
for f in "${newfiles[@]}"; do
  [[ -z $f ]] && continue
  case "$f" in docs/team/*|.team/*|.claude/*) continue ;; esac
  under_allowed_roots "$f" || report "$f: new file outside allowed_new_file_roots (STD-STRUCT-1)"
  name="$(basename "$f")"; stem="${name%%.*}"
  case "$stem" in __init__|conftest|setup|fixtures|helpers|utils) continue ;; esac
  [[ -z $test_glob ]] && continue
  is_test=0
  if [[ -n $tests_dir && $tests_dir != colocated && $f == "$tests_dir"/* && $name == *.* && ${name##*.} != md ]]; then is_test=1; fi
  if [[ $tests_dir == colocated && ${name,,} == *test* ]]; then is_test=1; fi
  # shellcheck disable=SC2053
  if (( is_test )) && [[ $name != $test_glob ]]; then report "$f: test file name does not match naming.test_file '$test_glob' (STD-NAME-3)"; fi
done

while IFS= read -r f; do
  [[ -z $f ]] && continue
  top="${f%%/*}"
  skip=0; for r in "${roots[@]}"; do [[ $top == "${r%%/*}" ]] && skip=1; done
  case "$f" in
    *.pyc|*/__pycache__/*) report "$f: generated file is staged (STD-GIT-5)" ;;
    node_modules/*|*/node_modules/*|dist/*|build/*) (( skip )) || report "$f: build/dependency directory is staged (STD-GIT-5)" ;;
  esac
done < <(git diff --cached --name-only)

(( problems )) && exit 1
echo "check-structure: OK"
exit 0
