---
name: analyze
description: Dùng khi feature đã qua intake và cần spec có Definition of Done, hoặc khi spec đã duyệt phải sửa đổi (--amend).
argument-hint: "<ID> [--amend \"<thay đổi>\"] [--decide]"
context: fork
agent: team:analyst
background: false
allowed-tools: Bash(python3 *) Bash(cat *)
---

## Mục đích
Biến `intake.md` thành `spec.md` đo được, có DoD.

## Đầu vào
- `$ARGUMENTS`: mã `<ID>`, `--amend "<thay đổi>"`, `--decide`.
- `docs/team/features/<ID>/intake.md`; `spec.md` khi `--amend`. `<kit>` = nội dung `.team/plugin_root`.

## Điều kiện trước
`intake.md` có. Kiểm: `python3 "$(cat .team/plugin_root)/scripts/team.py" status <ID>`.

## Các bước
1. Ghi `.team/current.json` {feature: <ID>, stage: "analyze", agent: "analyst", started_at}.
2. Đọc `intake.md`; chế độ = `--decide` hoặc chế độ ghi trong `intake.md`.
3. Gọi Explore đọc code liên quan (Agent).
4. Phân loại 7 mục: mục tiêu, người dùng, phạm vi trong/ngoài, dữ liệu, giao diện, NFR, tiêu chí nghiệm thu.
5. Chế độ ask: điều lớn hoặc không đảo ngược chưa rõ → `questions.md` (≤ 5 câu, 2–4 lựa chọn, khuyến nghị, hậu quả) → trả `NEEDS_ANSWER`, dừng. Tối đa 2 vòng.
6. Chế độ decide: ghi mỗi quyết định: chọn gì / vì sao / phương án khác / sửa thế nào nếu sai.
7. Viết `spec.md` từ `<kit>/templates/artifacts/spec.md`: 7 mục, `## Assumptions decided by the team`, `## Definition of Done` (luôn gồm As-Built, tài liệu, CHANGELOG).
8. Cỡ S: bản ngắn, tối đa 5 tiêu chí.
9. `--amend`: thêm `## Amendment <n> (<date>)`, đánh dấu `[changed]` ở tiêu chí đổi; không xóa tiêu chí cũ.

## Đầu ra
- `docs/team/features/<ID>/spec.md`; `questions.md` khi hỏi.
- Tin trả cho team-leader ≤ 10 dòng: `SPECIFIED` hoặc `NEEDS_ANSWER`, số tiêu chí, giả định chính, cổng G1.

## Tiêu chí xong
- Mỗi tiêu chí có cách kiểm bằng lệnh hoặc bước có đầu ra.
- Dán danh sách tiêu chí trong tin trả.

## Dấu hiệu sai
- "Yêu cầu rõ, bỏ 7 mục" → vẫn đủ 7 mục.
- "Hỏi cả điều nhỏ" → ghi vào Assumptions.
- "Chọn luôn thư viện" → để researcher.
- "Sửa thẳng tiêu chí cũ khi amend" → thêm amendment.

## Lệnh tiếp theo
Cỡ S: `/team:build <ID>`. Có G1: "Duyệt `spec.md` rồi `/team:run <ID>`". `NEEDS_ANSWER`: team-leader hỏi người theo `questions.md`.
