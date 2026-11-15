#!/usr/bin/env bash
# test_sessions.sh — session lanes (ADJ-38): two fake sessions on one project; checks claim / release / new-id / busy,
# the CONFLICT and BUSY exit codes, take-over notices, `status` and `wave` seeing the other session's items.
set -uo pipefail
KIT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
mkdir -p "$T/.team" "$T/docs/team/features"; cp "$KIT/templates/project/team/config.json" "$T/.team/config.json"
pass=0; failn=0
tp() { python3 -I "$KIT/scripts/team.py" "$@" --root "$T"; }
expect() { # expect <description> <want exit> <want substring> <command...>
  local d=$1 want=$2 sub=$3 out got; shift 3
  out="$("$@" 2>&1)"; got=$?
  if [[ $got == "$want" && $out == *"$sub"* ]]; then pass=$((pass + 1)); echo "ok   $d (exit $got)";
  else failn=$((failn + 1)); echo "FAIL $d: want exit $want with '$sub', got $got — ${out:0:240}"; fi
}

expect "new-id gives A the first ID"            0 "FEAT-001" tp new-id FEAT --session A
expect "new-id never repeats an ID"             0 "FEAT-002" tp new-id FEAT --session B
printf '# Intake FEAT-001 — Export CSV\n- Playbook: new-feature\n- Size: M\n- Mode: ask\n' > "$T/docs/team/features/FEAT-001/intake.md"
expect "same item from another session → CONFLICT" 3 "CONFLICT FEAT-001" tp claim FEAT-001 --stage analyze --session B
expect "A holds task files"                      0 "claimed FEAT-001 T1" tp claim FEAT-001 --task T1 --files src/a.py src/b.py --session A
expect "B on a file A holds → BUSY"              4 "BUSY FEAT-002 T3: src/a.py" tp claim FEAT-002 --task T3 --files src/a.py,src/c.py --session B
expect "BUSY claims nothing (all or nothing)"    0 "" test "$(jq -r '.files | has("src/c.py")' "$T/.team/session/B.json")" = false
expect "B on other files runs in parallel"       0 "claimed FEAT-002 T4" tp claim FEAT-002 --task T4 --files src/c.py --session B
expect "sessions lists the other lane"           0 "src/a.py (FEAT-001 T1)" tp sessions --session B
expect "status shows who holds what"             0 "FEAT-001" env CLAUDE_CODE_SESSION_ID=B python3 -I "$KIT/scripts/team.py" status --json --root "$T"
got="$(CLAUDE_CODE_SESSION_ID=B python3 -I "$KIT/scripts/team.py" status --json --root "$T" | jq -r '[.[] | .held_by] | join(",")')"
expect "status held_by from B's view ($got)"     0 "" test "$got" = "A,this"
expect "wave holds the other session's item"     0 "held by session A" env CLAUDE_CODE_SESSION_ID=B python3 -I "$KIT/scripts/team.py" wave --root "$T"
expect "A releases T1"                           0 "released FEAT-001 T1" tp release FEAT-001 --task T1 --session A
expect "B's task now gets the file"              0 "claimed FEAT-002 T3" tp claim FEAT-002 --task T3 --files src/a.py --session B
expect "--wait gives up with BUSY"               4 "BUSY" tp claim FEAT-001 --task T5 --files src/a.py --wait 1 --session A
expect "hook check: busy file"                   4 "being changed by session B" tp busy "$T/src/a.py" --session A
expect "hook check: worktree path maps to repo"  4 "src/a.py" tp busy "$T/.claude/worktrees/agent-1/src/a.py" --session A
expect "hook check: docs/team never held"        0 "" tp busy "$T/docs/team/features/FEAT-001/spec.md" --session A
expect "take-over moves the item"                0 "took over FEAT-001" tp claim FEAT-001 --stage build --agent tech-lead --take-over --session B
expect "the old holder is told"                  3 "NOTICE: FEAT-001 was taken over" tp claim FEAT-001 --stage plan --session A
expect "next follows this session's position"    0 "FEAT-001" env CLAUDE_CODE_SESSION_ID=B python3 -I "$KIT/scripts/team.py" next --root "$T"
expect "release --all ends B's lane"             0 "released everything" tp release --all --session B
expect "an ended lane holds nothing"             0 "claimed FEAT-001" tp claim FEAT-001 --stage plan --session A
jq '.seen = 0 | .transcript = "" | .pid = null' "$T/.team/session/A.json" > "$T/a.tmp" && mv "$T/a.tmp" "$T/.team/session/A.json"
expect "a day of silence ends a lane without pid" 0 "claimed FEAT-001" tp claim FEAT-001 --stage verify --session C
echo "test_sessions: $pass passed, $failn failed"
(( failn == 0 ))
