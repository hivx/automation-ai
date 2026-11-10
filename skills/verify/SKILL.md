---
name: verify
description: Dùng khi mọi task của feature đã tick và cần nghiệm thu độc lập từng tiêu chí bằng lệnh chạy thật trước khi phát hành.
argument-hint: "<ID>"
context: fork
agent: team:qa
background: false
allowed-tools: Bash(python3 *) Bash(cat *) Bash(git *)
---

# Nghiệm thu bằng lệnh thật

## Tổng quan
Skill này ra phán quyết `accepted` / `rework` / `design-defect` cho một feature đã build, bằng cách CHẠY LẠI từng tiêu chí trên đúng commit sẽ đi vào PR và dán đầu ra thật. Skill chạy trong ngữ cảnh `qa` (fork). qa không sửa code, không sửa test, không tin mô tả của dev hay kết quả CI cũ: bằng chứng duy nhất là đầu ra lệnh qa vừa chạy, gắn với một commit.

Dòng `Verdict:` là thứ máy đọc (`team.py` dựa vào nó để biết feature `verified`); viết sai dạng là feature không qua được (K-18).

`$ARGUMENTS`: mã `<ID>`. `<kit>` = nội dung `.team/plugin_root`.

## Khi nào dùng (và khi nào không)
Dùng khi:
- `team.py status <ID>` báo `built` (mọi task đã tick).
- Sau rework, để nghiệm thu lại.
- Playbook dependency-upgrade, data-migration, refactor cần kiểm đầy đủ trước PR.

Không dùng khi:
- Còn task chưa tick → `/team:build`.
- Muốn review chất lượng code từng task → đó là reviewer trong `/team:build`.
- Cần phát hành → `/team:asbuilt`, `/team:pr`, `/team:release` sau khi G4 duyệt.

## Tìm hiểu stack trước
1. Read `.team/profile.json`: `cmd.test`, `cmd.test_one`, `cmd.lint`, `cmd.typecheck`, `cmd.build`, `cmd.migrate`, `test.skip_markers`, `protected_paths`, `ui`.
2. Read `.team/config.json`: `base_branch`.
3. Lệnh kiểm tiêu chí lấy từ cột "cách kiểm" trong `spec.md` và test plan trong `design.md`; nếu cần lệnh khác, chỉ dùng khe `cmd.*` hoặc lệnh đọc dữ liệu. Không viết script kiểm mới.

## Đầu vào và điều kiện trước
- `docs/team/features/<ID>/spec.md` (tiêu chí + DoD), `design.md` (test plan, cỡ M/L), `tasks.md` tick đủ.
- `python3 "<kit>/scripts/team.py" status <ID>` báo `built`; không → trả lại, dừng.
- Nhánh `team/<ID>` checkout được, cây sạch.

## Quy trình
1. **Ghi vị trí.** Write `.team/current.json` {feature, stage: "verify", agent: "qa", started_at}.
2. **Gắn với commit.** `git switch team/<ID>`; `git status --porcelain` phải rỗng (cây bẩn → dừng, báo); `git rev-parse HEAD` → ghi đầu `acceptance.md`. Mọi bằng chứng phải sinh SAU lệnh này, trên commit này. Nếu nhánh đổi giữa chừng (có commit mới), ghi commit mới và chạy lại mọi tiêu chí — bằng chứng của commit cũ không còn giá trị.
3. **Đọc lại yêu cầu.** Đọc lại toàn bộ tiêu chí và DoD trong `spec.md`, lập danh sách; không suy ra từ việc test xanh.
4. **Cổng cho từng tiêu chí** — xác định lệnh → chạy mới → đọc đủ đầu ra, mã thoát, số lỗi → so với tiêu chí → mới viết kết luận. Mỗi dòng: `tiêu chí | lệnh | mã thoát | đầu ra (trích) | test phủ | kết luận`. Chi tiết và bảng "khẳng định cần gì": `${CLAUDE_SKILL_DIR}/references/evidence.md`.
5. **Bằng chứng hồi quy (bug-fix).** Tiêu chí "lỗi đã sửa" cần test tái hiện: đầu ra ĐỎ trước khi sửa phải có trong báo cáo dev hoặc `review-NN.md`; không có → `rework` với yêu cầu "dán đầu ra đỏ của test tái hiện". qa không tự hoàn tác code để thử.
6. **Ngoài đường thuận.** Tiêu chí có đầu vào → chạy ít nhất một lệnh cho đường lỗi hoặc giá trị biên mà test plan nêu. Chỉ có bằng chứng đường thuận → ghi khoảng trống.
7. **Chất lượng test.** Với mỗi tiêu chí, tìm test phủ nó (file::tên) và đọc: assertion có nêu đúng tiêu chí không (giá trị mong đợi viết cứng, không tính bằng chính code đang kiểm; không chỉ kiểm mock). Test không phủ → `rework` (STD-TEST-2); test không bao giờ trượt → `rework` (STD-TEST-5).
8. **Kiểm chung.** `cmd.test`, `cmd.lint`, `cmd.typecheck` (nếu có), `cmd.build` (nếu có): dán mã thoát và số lỗi. Cảnh báo lạ trong đầu ra (deprecation, lỗi in ra nhưng mã thoát 0) là một ghi chú trong bảng kiểm chung; lỗi bị nuốt mà mã thoát vẫn 0 là `rework` (STD-ERR-1).
9. **Dấu bỏ qua và assertion yếu đi.** Grep `git diff <base_branch>...team/<ID>` tìm mọi chuỗi trong `test.skip_markers`, và các dòng assertion bị xóa hay nới (STD-TEST-4, STD-TEST-5). Dán kết quả, kể cả khi rỗng.
10. **Migration** (nếu có `cmd.migrate` và diff có migration): ghi số liệu dự kiến trước, chạy lên → xuống → lên, đối soát số lượng (STD-OPS-2, STD-OPS-3).
11. **Giao diện** (`ui: true`): Playwright MCP nếu có; không có → tiêu chí đó là `KHÔNG KIỂM ĐƯỢC` và trả `NEEDS_ANSWER` để team-leader xin người ảnh chụp (qa không hỏi người trực tiếp).
12. **Lỗi trước khi kết luận (điểm quyết định).** Một lệnh đỏ → phân loại: test sai / code sai / môi trường / chập chờn.
    - Chập chờn: ghi 3 lần chạy; chập chờn = `rework` + dòng trong `debt.md`, không bao giờ `accepted`.
    - Môi trường không chạy được: không kết luận; trả `BLOCKED` kèm lệnh và lỗi.
    - Lỗi đã có trên `base_branch`: ghi tên, không che.
13. **DoD.** Chấm phần DoD của build (test, code, tài liệu sửa trong task). As-Built, CHANGELOG và tài liệu người dùng được viết ở `/team:asbuilt` SAU G4: không có thì KHÔNG phải lý do `rework` — ghi "chủ: writer, sau G4" và lệnh kiểm để `/team:release` kiểm lại. README đã có mà mô tả SAI hành vi vừa chạy → `rework`. Đối chiếu `git diff --name-only` với `protected_paths` (STD-SEC-1).
14. **Phán quyết** theo `${CLAUDE_SKILL_DIR}/references/evidence.md`:
    - `accepted`: mọi tiêu chí đạt, phần DoD của build đủ, Acceptance checklist 6/6, không mục `KHÔNG KIỂM ĐƯỢC`.
    - `rework`: code/test/tài liệu thiếu nhưng thiết kế đúng; mỗi tiêu chí trượt có lệnh tái hiện và task chủ (T<N>).
    - `design-defect`: code khớp thiết kế nhưng thiết kế/spec không thể thỏa tiêu chí (tiêu chí mâu thuẫn, NFR bất khả).
15. **Viết** `docs/team/features/<ID>/acceptance.md` từ `<kit>/templates/artifacts/acceptance.md` (Write): commit, bảng tiêu chí, kiểm chung, checklist 6 mục, DoD, mục `KHÔNG KIỂM ĐƯỢC` nếu có, và dòng cuối dạng chính xác `Verdict: accepted` (hoặc `rework`, `design-defect`).
16. **Trả** team-leader ≤ 10 dòng; ghi số liệu nếu được giao (`bash "<kit>/scripts/log-run.sh" --skill verify --result <verdict>`).

## Đầu ra
- `docs/team/features/<ID>/acceptance.md` (mẫu `<kit>/templates/artifacts/acceptance.md`).
- `.team/current.json` {stage: "verify"}.
- Tin trả mẫu:
  ```
  qa -> team-leader | FEAT-012 | rework
  Commit kiểm: a9d41e0 (team/FEAT-012). File: docs/team/features/FEAT-012/acceptance.md
  Đạt 3/4 tiêu chí; trượt AC-2: <cmd.test_one tests/auth/test_otp.py> → exit 1, "AssertionError: 200 != 401" (task T3)
  cmd.test exit 0; cmd.lint exit 0; skip marker mới: 0
  DoD thiếu: CHANGELOG (STD-DOC-3). Checklist 6: 4 đạt, 2 trượt
  Tiếp: /team:build FEAT-012 --task T3, rồi /team:verify FEAT-012
  ```

## Lý do tự bào chữa thường gặp
| Ý nghĩ | Làm đúng |
|---|---|
| "Dev nói đã chạy qua" | Tự chạy và dán đầu ra. |
| "CI xanh rồi" | CI là commit khác, lúc khác; chạy trên HEAD đang nghiệm thu. |
| "Lint qua thì build ổn" | Chạy `cmd.build` (hoặc typecheck) riêng. |
| "Tiêu chí này hiển nhiên đạt" | Chạy một lệnh chạm đúng hành vi đó; dán. |
| "Đã chạy lúc nãy trong phiên" | Chạy lại trên commit đã ghi. |
| "Migration xuống hiếm khi dùng" | Lên → xuống → lên, đối soát. |
| "Không lệnh nào kiểm được tiêu chí này" | Ghi `KHÔNG KIỂM ĐƯỢC`, trả `NEEDS_ANSWER`; không accept bằng cách đọc. |
| "README lệch chút thôi" | `rework` (STD-DOC-2). |
| "Test chập chờn, chạy lại tới khi xanh" | Chập chờn = rework + `debt.md`. |
| "Code đúng thiết kế mà kết quả sai" | `design-defect`, không phải rework. |
| "Sửa assertion cho xong" | qa không sửa code hay test; ghi `rework`. |
| "Đầu ra trong tin của dev đủ rồi" | Chỉ đầu ra qa vừa chạy, trên commit đã ghi. |
| "Đường thuận qua là đủ" | Chạy thêm biên/đường lỗi mà test plan nêu; thiếu thì ghi khoảng trống. |

## Dấu hiệu sai
- Chữ "chắc", "có vẻ", "hình như" trong `acceptance.md`.
- Đầu ra dán không kèm lệnh hoặc mã thoát; hai tiêu chí có đầu ra giống hệt.
- Đầu ra có trước commit ghi ở đầu file; `acceptance.md` không có commit.
- Số tiêu chí trong `acceptance.md` khác `spec.md`.
- `accepted` khi còn dòng trượt, còn `KHÔNG KIỂM ĐƯỢC`, hoặc có dấu skip mới.
- Migration chỉ chạy chiều lên.
- Dòng phán quyết không đúng dạng `Verdict: <giá trị>`.
- `rework` mà không có lệnh tái hiện và task chủ cho từng tiêu chí trượt.
- qa đã ghi file ngoài `acceptance.md` và memory của mình.
- Số liệu (thời gian, tỉ lệ phủ) không truy được về một lệnh đã chạy.

## Kiểm chứng
- [ ] `git rev-parse HEAD` của `team/<ID>` ở đầu `acceptance.md`.
- [ ] Mỗi tiêu chí một dòng có lệnh, mã thoát, đầu ra; số dòng bằng số tiêu chí trong spec.
- [ ] Đầu ra `cmd.test`, `cmd.lint`, `cmd.typecheck` (nếu có) kèm số lỗi.
- [ ] Kết quả grep dấu skip và assertion bị xóa trong diff được dán (kể cả rỗng).
- [ ] Bảng tiêu chí → test phủ.
- [ ] `grep -E '^Verdict: (accepted|rework|design-defect)$' acceptance.md` có đúng một dòng; `team.py status <ID>` khớp.

## Xem thêm
- `${CLAUDE_SKILL_DIR}/references/evidence.md` — bảng khẳng định/bằng chứng, quyết định phán quyết, phân loại lỗi.
- Agent `qa`; `<kit>/templates/artifacts/acceptance.md`.
- `/team:build --task T<N>` (rework), `/team:design` (design-defect), `/team:asbuilt` (sau G4).
- `handbook/STD.md`: Acceptance checklist (6), STD-TEST-2/4/5/7, STD-OPS-2/3, STD-DOC-1/2/3.
