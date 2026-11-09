#!/usr/bin/env bash
# run-all.sh — chạy mọi test của kit: hook, team.py status, measure.py. Thoát khác 0 nếu có test hỏng.
# Dùng: scripts/tests/run-all.sh ; validate.sh --strict và CI gọi script này.
set -uo pipefail
[[ ${1:-} == --help || ${1:-} == -h ]] && { sed -n '2,3p' "$0" | sed 's/^# \{0,1\}//'; exit 0; }
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
rc=0
for t in test_hooks.sh test_team_status.sh; do
  echo "== $t"
  bash "$HERE/$t" | tail -n 1 || rc=1
  [[ ${PIPESTATUS[0]} == 0 ]] || rc=1
done
echo "== test_measure.py"
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s "$HERE" -p 'test_*.py' 2>&1 | tail -n 3 || rc=1
[[ ${PIPESTATUS[0]} == 0 ]] || rc=1
echo "run-all: $([[ $rc == 0 ]] && echo PASS || echo FAIL)"
exit $rc
