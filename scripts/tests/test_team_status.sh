#!/usr/bin/env bash
# test_team_status.sh — builds a temporary project tree with artifacts and approval marks, checks where `team.py status` puts each feature.
set -uo pipefail
KIT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
mkdir -p "$T/.team"; cp "$KIT/templates/project/team/config.json" "$T/.team/config.json"
pass=0; failn=0
F() { mkdir -p "$T/docs/team/features/$1"; printf '%b' "$3" > "$T/docs/team/features/$1/$2"; }
expect() { # expect <ID> <jq expression> <expected value> <description>
  local got; got="$(python3 -I "$KIT/scripts/team.py" status "$1" --json --root "$T" | jq -r ".[0] | $2")"
  if [[ $got == "$3" ]]; then pass=$((pass + 1)); echo "ok   $4 ($got)"; else failn=$((failn + 1)); echo "FAIL $4: want '$3' got '$got'"; fi
}
OK="Approved-by: Lan 2026-11-09\n"
INTAKE_M="# Intake FEAT-001 — Export CSV\n- Playbook: new-feature\n- Size: M\n- Mode: ask\n"
SPEC="# Spec\n\n## Definition of Done\n- x\n"
# Vietnamese labels of older projects, written as UTF-8 bytes so this file stays English: Size, Verdict.
VI_SIZE='C\xe1\xbb\xa1'; VI_VERDICT='Ph\xc3\xa1n quy\xe1\xba\xbft'

F FEAT-001 intake.md "$INTAKE_M"
expect FEAT-001 .stage intaken "intake only → intaken"
expect FEAT-001 .title "Export CSV" "title drops the 'Intake FEAT-001 —' prefix"
expect FEAT-001 .next "/team:analyze FEAT-001" "next after intake"

F FEAT-001 spec.md "$SPEC"
expect FEAT-001 '.status + " " + .gate' "WAITING_FOR_APPROVAL G1_spec" "unapproved spec → waiting on G1"
F FEAT-001 design.md "# Design\n"
expect FEAT-001 '.stage + " " + .status + " " + .gate' "specified WAITING_FOR_APPROVAL G1_spec" "unapproved spec with design.md → still blocked at G1"
expect FEAT-001 '.blocked_later | join(",")' "designed" "records the blocked later artifact"

F FEAT-001 spec.md "$OK$SPEC"
expect FEAT-001 '.stage + " " + .status' "designed READY" "G1 approved, G2b off → designed"
F FEAT-001 plan.md "# Plan\n"; F FEAT-001 tasks.md "- [x] T1 — a\n- [ ] T2 — b\n"
expect FEAT-001 '.status + " " + .gate' "WAITING_FOR_APPROVAL G3_plan" "unapproved plan → waiting on G3"
F FEAT-001 plan.md "$OK# Plan\n"
expect FEAT-001 '.stage + " " + .next' "planned /team:build FEAT-001" "plan approved, open tasks left → planned"
F FEAT-001 tasks.md "- [x] T1 — a\n- [ ] T2 — b BLOCKED: missing secret\n"
expect FEAT-001 .status BLOCKED "task marked BLOCKED → BLOCKED"
F FEAT-001 tasks.md "- [x] T1 — a\n- [x] **T2 — b** (bold)\n"
expect FEAT-001 .stage built "every task ticked (bold T included) → built"
F FEAT-001 acceptance.md "# Acceptance\n$VI_VERDICT: rework\n"
expect FEAT-001 '.stage + " " + .status' "built REWORK" "verdict rework (legacy Vietnamese label) → REWORK"
F FEAT-001 acceptance.md "# Acceptance\nVerdict: accepted\n"
expect FEAT-001 '.status + " " + .gate' "WAITING_FOR_APPROVAL G4_uat" "accepted but unapproved → waiting on G4"
F FEAT-001 acceptance.md "${OK}Verdict: accepted\n"
expect FEAT-001 .next "/team:asbuilt FEAT-001" "G4 approved → asbuilt"
F FEAT-001 asbuilt.md "# As-Built\n"
expect FEAT-001 '.stage' "verified" "asbuilt without Released → verified"
F FEAT-001 asbuilt.md "Approved-by-prod: Lan 2026-11-10\n# As-Built\nReleased: v1.0.0 2026-11-10\n"
expect FEAT-001 '.stage + " " + .status' "released RELEASED" "Released → released"

F BUG-002 intake.md "# Intake BUG-002 — Accent bug\n- Playbook: bug-fix\n- $VI_SIZE: S\n"
expect BUG-002 .next "/team:build BUG-002" "bug-fix after intake (legacy size label) → build"
F BUG-002 spec.md "$SPEC"
expect BUG-002 '.stage + " " + .status' "specified READY" "size S: G1 does not apply"
expect BUG-002 '.gates | join(",")' "G2_arch,G4_uat,G5_prod" "size S: applicable gates exclude G1, G3"
F BUG-002 tasks.md "- [x] T1 — fix\n"
expect BUG-002 .stage built "size S needs no plan.md → built"

F CHG-003 intake.md "# Intake CHG-003 — Cleanup\n- Playbook: refactor\n- Size: M\n"
F CHG-003 spec.md "$OK$SPEC"; F CHG-003 design.md "# Design\n"
expect CHG-003 '.status + " " + .gate' "WAITING_FOR_APPROVAL G2b_design" "refactor always enables G2b"

F REF-005 intake.md "# Intake REF-005 — Remove dead code\n- Playbook: refactor\n- Size: M\n"
expect REF-005 .next "/team:design REF-005 --short" "refactor without spec → design --short"
F REF-005 design.md "$OK# Design\n"
expect REF-005 '.stage + " " + .status' "designed READY" "refactor needs no spec.md (K-47)"
expect REF-005 .next "/team:clean <kind> (playbook refactor)" "refactor designed → clean"
F REF-005 tasks.md "- [x] T1 — clean dead-code\n"
expect REF-005 .stage built "refactor: clean writes tasks.md, no plan.md needed (K-47)"
expect REF-005 .next "/team:verify REF-005" "refactor built → verify"
F BUG-006 intake.md "# Intake BUG-006 — Bug\n- Playbook: bug-fix\n- Size: M\n"
F BUG-006 tasks.md "- [x] T1 — reproduction test + fix\n"
expect BUG-006 .stage built "bug-fix size M needs no spec/plan (K-47)"

jq '.gates.G1_spec=false' "$T/.team/config.json" > "$T/c" && mv "$T/c" "$T/.team/config.json"
F FEAT-004 intake.md "$INTAKE_M"; F FEAT-004 spec.md "$SPEC"
expect FEAT-004 '.stage + " " + .status' "specified READY" "gate disabled in config does not block"
F FEAT-005 intake.md "$INTAKE_M"; F FEAT-005 questions.md "1. ?\n"
expect FEAT-005 .status WAITING_FOR_ANSWER "questions.md without spec → waiting for an answer"

out="$(python3 -I "$KIT/scripts/team.py" status --root "$T")"
if grep -q "Waiting on the human: approve G2b_design" <<<"$out"; then pass=$((pass + 1)); echo "ok   table has a 'Waiting on the human' line"; else failn=$((failn + 1)); echo "FAIL table lacks the waiting line"; fi
# wave: parallel dispatch across features, capped by limits.headcount; overlapping builds wait
W="$(mktemp -d)"; mkdir -p "$W/.team"
jq '.limits.headcount={"analyst":2,"tech-lead":2,"dev":5,"reviewer":4}' "$KIT/templates/project/team/config.json" > "$W/.team/config.json"
G() { mkdir -p "$W/docs/team/features/$1"; printf '%b' "$3" > "$W/docs/team/features/$1/$2"; }
for i in 1 2 3; do G FEAT-01$i intake.md "$INTAKE_M"; done
for i in 4 5 6; do G FEAT-01$i intake.md "$INTAKE_M"; G FEAT-01$i spec.md "$OK$SPEC"; G FEAT-01$i design.md "$OK# d\n"; G FEAT-01$i plan.md "$OK# p\n"; done
G FEAT-014 tasks.md "- [ ] T1 — a — files: src/a.py, src/b.py — test: t — depends: —\n"
G FEAT-015 tasks.md "- [ ] T1 — a — files: src/b.py — test: t — depends: —\n"
G FEAT-016 tasks.md "- [ ] T1 — a — files: src/c.py — test: t — depends: —\n"
G FEAT-017 intake.md "$INTAKE_M"; G FEAT-017 spec.md "$SPEC"
wj="$(python3 -I "$KIT/scripts/team.py" wave --json --root "$W")"; rm -rf "$W"
wexp() { local got; got="$(jq -r "$1" <<<"$wj")"
  if [[ $got == "$2" ]]; then pass=$((pass + 1)); echo "ok   $3 ($got)"; else failn=$((failn + 1)); echo "FAIL $3: want '$2' got '$got'"; fi; }
wexp '[.dispatch[] | select(.role=="analyst") | .id] | join(",")' "FEAT-011,FEAT-012" "wave: 2 analysts take 2 features at once"
wexp '[.held[] | select(.id=="FEAT-013") | .reason] | join("")' "headcount analyst=2 in use" "wave: 3rd analyze waits for a free analyst"
wexp '[.dispatch[] | select(.skill=="build") | .id] | join(",")' "FEAT-014,FEAT-016" "wave: file-disjoint builds run together"
wexp '[.held[] | select(.id=="FEAT-015") | .reason] | join("")' "shares files with a build in this wave: src/b.py" "wave: build sharing a file waits"
wexp '[.dispatch[] | select(.skill=="build") | .devs] | join(",")' "2,2" "wave: team-wide 5 devs split between 2 builds"
wexp '[.held[] | select(.id=="FEAT-017") | .reason] | join("")' "WAITING_FOR_APPROVAL" "wave: a feature at a gate is not dispatched"
wexp '.headcount.designer // "default"' "default" "wave: roles without headcount default to 1"

echo "test_team_status: $pass passed, $failn failed"
(( failn == 0 ))
