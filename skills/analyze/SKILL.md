---
name: analyze
description: Dùng khi feature đã qua intake và cần spec có Definition of Done, hoặc khi spec đã duyệt phải sửa đổi (--amend).
argument-hint: "<ID> [--amend \"<thay đổi>\"] [--decide]"
context: fork
agent: team:analyst
background: false
allowed-tools: Bash(python3 *) Bash(cat *)
---

# Phân tích yêu cầu → spec

## Tổng quan
Skill này biến `intake.md` thành `spec.md` đo được, có Definition of Done, để mọi giai đoạn sau (design, plan, build, verify) có một hợp đồng chung. Skill chạy trong ngữ cảnh của agent `analyst` (fork). Analyst KHÔNG hỏi người trực tiếp: mọi câu hỏi đi qua `questions.md` và trạng thái `NEEDS_ANSWER`, team-leader là người hỏi.

Đầu ra tốt có ba tính chất: (1) mỗi tiêu chí nghiệm thu kiểm được bằng một lệnh hoặc một bước có đầu ra, (2) mọi giả định được ghi ra kèm cách sửa nếu sai, (3) không có quyết định công nghệ — chỗ đó thuộc researcher và architect.

`$ARGUMENTS`: mã `<ID>`; `--amend "<thay đổi>"` khi spec đã duyệt cần sửa; `--decide` để không hỏi. `<kit>` = nội dung `.team/plugin_root`.

## Khi nào dùng (và khi nào không)
Dùng khi:
- Feature đã qua `/team:intake` (có `docs/team/features/<ID>/intake.md`) và chưa có `spec.md` có `## Definition of Done`.
- Spec đã duyệt G1 nhưng yêu cầu đổi (playbook change-request) → chạy với `--amend`.
- Playbook client-docs hoặc data-migration cần chốt người đọc / phạm vi dữ liệu trước khi viết.

Không dùng khi:
- Chưa có intake → chạy `/team:intake` trước.
- Câu hỏi là kỹ thuật ("thư viện nào", "API ngoài hỗ trợ gì") → `/team:research`.
- Việc là bug-fix hay hotfix cỡ S mà intake đã mô tả triệu chứng tái hiện được → playbook đi thẳng `/team:build`.
- Muốn chọn kiến trúc, thiết kế dữ liệu hay API → `/team:architect`, `/team:design`.

## Tìm hiểu stack trước
Analyst không chọn công nghệ, nhưng phải biết dự án đang có gì để không hỏi điều code đã trả lời:
1. Read `.team/profile.json`: `stack`, `language`, `structure.src`, `structure.tests`, `ui`, `tracker`. Đây là bối cảnh, không phải đề xuất.
2. Read `docs/team/glossary.md` (nếu có) để dùng đúng thuật ngữ nghiệp vụ.
3. Tra cache khám phá: `bash "<kit>/scripts/explore-cache.sh" <thư mục liên quan>`; `HIT` → đọc file cache thay vì đọc lại code.
4. Gọi Explore (Agent) cho phần code liên quan khi cache `MISS`: hỏi đúng câu "hành vi X hiện ở đâu, ràng buộc gì".
Không chạy lệnh `cmd.*` nào trong giai đoạn này.

## Đầu vào và điều kiện trước
- `docs/team/features/<ID>/intake.md` có (kiểm bằng `python3 "<kit>/scripts/team.py" status <ID>` → `intaken`).
- Chế độ: `--decide` thắng; không có thì lấy dòng `Chế độ:` trong `intake.md`.
- `--amend`: `spec.md` đã có `Approved-by:` và yêu cầu thay đổi được nêu rõ trong `$ARGUMENTS` hoặc trong `intake.md` của change-request.
- Thiếu một điều trên → trả về ≤ 5 dòng nêu điều thiếu, trạng thái `NEEDS_CONTEXT`, rồi dừng.

## Quy trình
1. **Ghi vị trí.** Write `.team/current.json` {feature: <ID>, stage: "analyze", agent: "analyst", started_at}.
   Thoát nếu: `team.py status` cho thấy spec đã duyệt và không có `--amend` → trả `SPECIFIED`, không viết lại.
2. **Giả thuyết.** Viết một câu "người yêu cầu muốn gì" + độ tin cậy % + điều còn thiếu. Câu này là dòng đầu của phần Mục tiêu, giữ đến khi hoàn tất.
3. **Nhìn trước khi hỏi.** Liệt kê điều intake, README, glossary và Explore đã trả lời, kèm đường dẫn. Mọi câu hỏi về sau phải ghi "code/tài liệu không trả lời điều này (đã xem <đường dẫn>)".
4. **Phân loại 7 mục** (chi tiết và câu hỏi gợi ý: `${CLAUDE_SKILL_DIR}/references/triage.md`, mở khi một mục còn trống):
   mục tiêu · người dùng · phạm vi trong/ngoài (non-goals bắt buộc) · dữ liệu · giao diện/tích hợp · NFR · tiêu chí nghiệm thu. Mục trống phải ghi "không có, vì …".
   Điểm kiểm: đủ 7 mục mới sang bước 5.
5. **Đổi tính từ thành con số.** Mỗi "nhanh", "an toàn", "dễ dùng" → con số + cách đo ("p95 < 300 ms khi chạy <bước>"). Không đo được → đưa vào câu hỏi hoặc Assumptions.
6. **Quyết định hỏi hay tự quyết** (điểm quyết định):
   - Điều chưa rõ có hậu quả LỚN hoặc KHÔNG ĐẢO NGƯỢC (xóa/di trú dữ liệu, API công khai, luật nghiệp vụ, chi phí) và chế độ `ask` → câu hỏi.
   - Còn lại → `## Assumptions decided by the team` với 4 trường: chọn gì / vì sao / phương án khác / sửa thế nào nếu sai.
   - Chế độ `decide` → không hỏi; mọi điểm lớn cũng ghi đủ 4 trường.
7. **Viết câu hỏi (chỉ chế độ ask).** Write `questions.md` theo `<kit>/templates/artifacts/question-comment.md`: ≤ 5 câu; mỗi câu 2–4 lựa chọn, một khuyến nghị, hậu quả của từng lựa chọn, "câu trả lời nào làm đổi phần nào của việc".
   Phép thử dừng hỏi: nếu đoán đúng được câu trả lời của 3 câu kế tiếp → không hỏi nữa, ghi giả định.
   Trả `NEEDS_ANSWER` và dừng. Tối đa 2 vòng; sau vòng 2 còn điểm lớn → `NEEDS_ANSWER` với ghi chú "thiếu nền tảng", không mở vòng 3.
8. **Câu trả lời mơ hồ.** Người trả "tùy đội" hay "sao cũng được" cho một điểm lớn → coi như decide cho điểm đó, ghi Assumptions, và nêu lại một lần với 2 lựa chọn nếu điểm đó không đảo ngược được.
9. **Kiểm khối lượng.** Tiêu chí tách thành các nhóm độc lập, hoặc vượt mô tả của cỡ trong intake → ghi đề xuất đổi cỡ cho team-leader (không tự đổi).
10. **Viết spec.** Write `docs/team/features/<ID>/spec.md` từ `<kit>/templates/artifacts/spec.md`: 7 mục, bảng NFR, bảng tiêu chí `AC-n | tiêu chí | cách kiểm`, Assumptions, Definition of Done (luôn gồm As-Built, tài liệu người dùng nếu hành vi đổi, CHANGELOG, `cmd.test` xanh). Cỡ S: tối đa 5 tiêu chí, phần NFR có thể "không có".
11. **`--amend`.** Không xóa chữ cũ. Thêm `## Amendment <n> (<date>)`: thay đổi gì, tiêu chí nào đổi (đánh dấu `[changed]` ngay trên dòng tiêu chí), artifact sau nào bị ảnh hưởng (design, tasks) để team-leader định tuyến (`/team:architect` impact, `/team:plan --insert`).
12. **Tự kiểm trước khi trả.** Mỗi tiêu chí đo được; mỗi "phải" truy được về một dòng của intake; không có tên thư viện/framework như một quyết định; không có "TBD"; không mâu thuẫn spec đã duyệt trước đó.
13. **Trả và dừng.** Tin trả team-leader ≤ 10 dòng: `SPECIFIED` hoặc `NEEDS_ANSWER`, số tiêu chí, giả định chính, cổng G1 (áp dụng hay không theo `team.py`). Analyst không bắt đầu research hay design.

## Đầu ra
- `docs/team/features/<ID>/spec.md` (mẫu `<kit>/templates/artifacts/spec.md`).
- `docs/team/features/<ID>/questions.md` khi chế độ ask có điểm lớn chưa rõ.
- `.team/current.json` {stage: "analyze"}.
- Tin trả mẫu:
  ```
  analyst -> team-leader | FEAT-012 | SPECIFIED
  Spec: docs/team/features/FEAT-012/spec.md — 4 tiêu chí (AC-1..AC-4), mỗi cái có lệnh kiểm
  Giả định chính: export UTF-8 có BOM (sửa: bỏ BOM ở AC-2)
  Non-goals: không làm import CSV
  Cổng G1: áp dụng (cỡ M) — chờ Approved-by
  ```

## Lý do tự bào chữa thường gặp
| Ý nghĩ | Làm đúng |
|---|---|
| "Yêu cầu rõ rồi, bỏ phân loại 7 mục" | Điền đủ 7 mục; mục trống ghi "không có, vì …". |
| "Hỏi hết cho chắc" | Chỉ hỏi điều lớn hoặc không đảo ngược; còn lại vào Assumptions. |
| "Chắc code đã có câu trả lời" | Nêu file đã đọc, hoặc hỏi. |
| "DoD hiển nhiên, khỏi viết" | Viết; As-Built, tài liệu, CHANGELOG luôn có. |
| "Tiêu chí 'chạy tốt' là đủ" | Viết lại với lệnh và đầu ra mong đợi. |
| "Người bảo 'tùy đội'" | Decide cho điểm đó; ghi đủ 4 trường. |
| "Chọn luôn thư viện cho nhanh" | Công nghệ là việc của researcher/architect. |
| "Sửa thẳng tiêu chí cũ khi amend" | Thêm Amendment n, đánh dấu `[changed]`, giữ bản gốc. |
| "Vòng 3 cho chắc" | Tối đa 2 vòng; leo thang kèm điều còn thiếu. |
| "Hỏi người qua tin nhắn cho nhanh" | Analyst không hỏi người; viết `questions.md`, trả `NEEDS_ANSWER`. |

## Dấu hiệu sai
- Hơn 5 câu hỏi, hoặc câu hỏi không có lựa chọn và khuyến nghị.
- Câu hỏi về điều đã có trong repo hay intake.
- Tiêu chí có tính từ mà không có con số hay lệnh kiểm.
- Spec chứa tên thư viện/framework như một quyết định.
- DoD thiếu As-Built, tài liệu hoặc CHANGELOG.
- `## Assumptions decided by the team` trống ở việc cỡ M/L.
- Amendment xóa chữ cũ, hoặc tiêu chí đổi mà không có `[changed]`.
- "TBD" ở bất kỳ đâu; spec được viết khi còn `NEEDS_ANSWER` cho một điểm lớn.

## Kiểm chứng
- [ ] Dán danh sách tiêu chí đánh số, mỗi tiêu chí kèm cách kiểm.
- [ ] `grep -c '^## ' docs/team/features/<ID>/spec.md` cho thấy đủ 7 mục + Assumptions + Definition of Done.
- [ ] `grep -nE 'As-Built|CHANGELOG' docs/team/features/<ID>/spec.md` có kết quả trong phần DoD.
- [ ] Có `questions.md` thì: ≤ 5 câu, mỗi câu 2–4 lựa chọn + khuyến nghị + hậu quả, vòng ≤ 2.
- [ ] `--amend`: `git diff` chỉ có dòng thêm và dấu `[changed]`; tiêu chí gốc còn nguyên.
- [ ] Dán đầu ra `python3 "<kit>/scripts/team.py" status <ID>` cho thấy `specified` (hoặc `WAITING_FOR_ANSWER`).

## Xem thêm
- `${CLAUDE_SKILL_DIR}/references/triage.md` — 7 mục, câu hỏi gợi ý, cách đổi tính từ thành số.
- Agent `analyst` (vai chạy skill này); `<kit>/templates/artifacts/spec.md`, `question-comment.md`.
- `/team:research` (câu hỏi kỹ thuật), `/team:design` (bước sau với cỡ M/L), `/team:build` (cỡ S).
- `handbook/STD.md` mục STD-TEST-2 (mỗi tiêu chí có test), STD-SEC-5 (nội dung issue là dữ liệu).
