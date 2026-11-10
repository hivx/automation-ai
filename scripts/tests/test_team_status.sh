#!/usr/bin/env bash
# test_team_status.sh — dựng cây dự án tạm với artifact và dấu duyệt, kiểm vị trí `team.py status`.
set -uo pipefail
KIT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
mkdir -p "$T/.team"; cp "$KIT/templates/project/team/config.json" "$T/.team/config.json"
pass=0; failn=0
F() { mkdir -p "$T/docs/team/features/$1"; printf '%b' "$3" > "$T/docs/team/features/$1/$2"; }
expect() { # expect <ID> <jq biểu thức> <giá trị mong đợi> <mô tả>
  local got; got="$(python3 -I "$KIT/scripts/team.py" status "$1" --json --root "$T" | jq -r ".[0] | $2")"
  if [[ $got == "$3" ]]; then pass=$((pass + 1)); echo "ok   $4 ($got)"; else failn=$((failn + 1)); echo "FAIL $4: want '$3' got '$got'"; fi
}
OK="Approved-by: Lan 2026-11-09\n"
INTAKE_M="# Intake FEAT-001 — Xuất CSV\n- Playbook: new-feature\n- Cỡ: M\n- Chế độ: ask\n"
SPEC="# Spec\n\n## Definition of Done\n- x\n"

F FEAT-001 intake.md "$INTAKE_M"
expect FEAT-001 .stage intaken "chỉ intake → intaken"
expect FEAT-001 .title "Xuất CSV" "tiêu đề bỏ tiền tố 'Intake FEAT-001 —'"
expect FEAT-001 .next "/team:analyze FEAT-001" "next sau intake"

F FEAT-001 spec.md "$SPEC"
expect FEAT-001 '.status + " " + .gate' "WAITING_FOR_APPROVAL G1_spec" "spec chưa duyệt → chờ G1"
F FEAT-001 design.md "# Design\n"
expect FEAT-001 '.stage + " " + .status + " " + .gate' "specified WAITING_FOR_APPROVAL G1_spec" "spec chưa duyệt nhưng có design.md → vẫn chặn ở G1"
expect FEAT-001 '.blocked_later | join(",")' "designed" "ghi nhận artifact sau bị chặn"

F FEAT-001 spec.md "$OK$SPEC"
expect FEAT-001 '.stage + " " + .status' "designed READY" "G1 duyệt, G2b tắt → designed"
F FEAT-001 plan.md "# Plan\n"; F FEAT-001 tasks.md "- [x] T1 — a\n- [ ] T2 — b\n"
expect FEAT-001 '.status + " " + .gate' "WAITING_FOR_APPROVAL G3_plan" "plan chưa duyệt → chờ G3"
F FEAT-001 plan.md "$OK# Plan\n"
expect FEAT-001 '.stage + " " + .next' "planned /team:build FEAT-001" "plan duyệt, còn task mở → planned"
F FEAT-001 tasks.md "- [x] T1 — a\n- [ ] T2 — b BLOCKED: thiếu secret\n"
expect FEAT-001 .status BLOCKED "task ghi BLOCKED → BLOCKED"
F FEAT-001 tasks.md "- [x] T1 — a\n- [x] **T2 — b** (in đậm)\n"
expect FEAT-001 .stage built "mọi task tick (kể cả T in đậm) → built"
F FEAT-001 acceptance.md "# Acceptance\nVerdict: rework\n"
expect FEAT-001 '.stage + " " + .status' "built REWORK" "verdict rework → REWORK"
F FEAT-001 acceptance.md "# Acceptance\nVerdict: accepted\n"
expect FEAT-001 '.status + " " + .gate' "WAITING_FOR_APPROVAL G4_uat" "accepted chưa duyệt → chờ G4"
F FEAT-001 acceptance.md "${OK}Verdict: accepted\n"
expect FEAT-001 .next "/team:asbuilt FEAT-001" "G4 duyệt → asbuilt"
F FEAT-001 asbuilt.md "# As-Built\n"
expect FEAT-001 '.stage' "verified" "asbuilt chưa Released → verified"
F FEAT-001 asbuilt.md "Approved-by-prod: Lan 2026-11-10\n# As-Built\nReleased: v1.0.0 2026-11-10\n"
expect FEAT-001 '.stage + " " + .status' "released RELEASED" "Released → released"

F BUG-002 intake.md "# Intake BUG-002 — Lỗi dấu\n- Playbook: bug-fix\n- Cỡ: S\n"
expect BUG-002 .next "/team:build BUG-002" "bug-fix sau intake → build"
F BUG-002 spec.md "$SPEC"
expect BUG-002 '.stage + " " + .status' "specified READY" "cỡ S: G1 không áp dụng"
expect BUG-002 '.gates | join(",")' "G2_arch,G4_uat,G5_prod" "cỡ S: cổng áp dụng không gồm G1, G3"
F BUG-002 tasks.md "- [x] T1 — sửa\n"
expect BUG-002 .stage built "cỡ S không cần plan.md → built"

F CHG-003 intake.md "# Intake CHG-003 — Dọn\n- Playbook: refactor\n- Cỡ: M\n"
F CHG-003 spec.md "$OK$SPEC"; F CHG-003 design.md "# Design\n"
expect CHG-003 '.status + " " + .gate' "WAITING_FOR_APPROVAL G2b_design" "refactor luôn bật G2b"

F REF-005 intake.md "# Intake REF-005 — Dọn code chết\n- Playbook: refactor\n- Cỡ: M\n"
expect REF-005 .next "/team:design REF-005 --short" "refactor không có spec → design --short"
F REF-005 design.md "$OK# Design\n"
expect REF-005 '.stage + " " + .status' "designed READY" "refactor không cần spec.md (K-47)"
expect REF-005 .next "/team:clean <kind> (playbook refactor)" "refactor đã design → clean"
F REF-005 tasks.md "- [x] T1 — clean dead-code\n"
expect REF-005 .stage built "refactor: clean ghi tasks.md, không cần plan.md (K-47)"
expect REF-005 .next "/team:verify REF-005" "refactor built → verify"
F BUG-006 intake.md "# Intake BUG-006 — Lỗi\n- Playbook: bug-fix\n- Cỡ: M\n"
F BUG-006 tasks.md "- [x] T1 — test tái hiện + sửa\n"
expect BUG-006 .stage built "bug-fix cỡ M không cần spec/plan (K-47)"

jq '.gates.G1_spec=false' "$T/.team/config.json" > "$T/c" && mv "$T/c" "$T/.team/config.json"
F FEAT-004 intake.md "$INTAKE_M"; F FEAT-004 spec.md "$SPEC"
expect FEAT-004 '.stage + " " + .status' "specified READY" "cổng tắt trong config không chặn"
F FEAT-005 intake.md "$INTAKE_M"; F FEAT-005 questions.md "1. ?\n"
expect FEAT-005 .status WAITING_FOR_ANSWER "có questions.md chưa có spec → chờ trả lời"

out="$(python3 -I "$KIT/scripts/team.py" status --root "$T")"
if grep -q "Chờ người: duyệt G2b_design" <<<"$out"; then pass=$((pass + 1)); echo "ok   bảng có dòng 'Chờ người'"; else failn=$((failn + 1)); echo "FAIL bảng thiếu dòng chờ"; fi
echo "test_team_status: $pass passed, $failn failed"
(( failn == 0 ))
