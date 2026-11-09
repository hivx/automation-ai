---
name: research
description: Dùng khi spec còn câu hỏi kỹ thuật, cần so sánh phương án, đọc changelog trước khi nâng cấp, tìm hiểu API ngoài, hoặc làm spike.
argument-hint: "<ID> \"<câu hỏi>\""
context: fork
agent: team:researcher
background: false
allowed-tools: Bash(python3 *) Bash(cat *) Bash(git worktree *)
---

## Mục đích
Trả lời câu hỏi kỹ thuật bằng nguồn chính thức có ngày, kèm khuyến nghị.

## Đầu vào
- `$ARGUMENTS`: mã `<ID>` và câu hỏi.
- `docs/team/features/<ID>/spec.md`. `<kit>` = nội dung `.team/plugin_root`.

## Điều kiện trước
`spec.md` hoặc `intake.md` (spike) có. Kiểm: `python3 "$(cat .team/plugin_root)/scripts/team.py" status <ID>`.

## Các bước
1. Ghi `.team/current.json` {feature, stage: "research", agent: "researcher", started_at}.
2. Tìm cache `docs/team/research/<topic>@<version>.md` (Glob). Đúng phiên bản → dùng lại, ghi "từ cache".
3. Lấy phiên bản đang dùng từ manifest của dự án (Read).
4. Đọc docs chính thức đúng phiên bản (WebFetch); WebSearch chỉ để tìm trang chính thức.
5. Mỗi khẳng định: URL + ngày truy cập.
6. So sánh phương án trong bảng: tiêu chí, ưu, nhược, rủi ro, chi phí.
7. POC khi cần: `git worktree add` thư mục tạm; ghi lệnh + đầu ra; `git worktree remove` sau đó.
8. Viết `research.md` từ `<kit>/templates/artifacts/research.md`; mục `## Sources` bắt buộc (hook Stop kiểm).
9. Nháp ADR khi có quyết định kiến trúc: ghi "chờ architect quyết".
10. Lưu cache kết luận theo `<topic>@<version>`.

## Đầu ra
- `docs/team/features/<ID>/research.md`, `docs/team/research/<topic>@<version>.md`.
- Tin trả ≤ 10 dòng: câu trả lời, khuyến nghị, độ tin cậy, file.

## Tiêu chí xong
- `## Sources` có URL + ngày cho mọi khẳng định.
- POC (nếu có): lệnh và đầu ra thật được dán; `git worktree list` cho thấy đã gỡ.

## Dấu hiệu sai
- "Tôi nhớ API này" → đọc docs đúng phiên bản.
- "Blog này đủ" → tìm docs chính thức.
- "Giữ code POC dùng luôn" → xóa; dev viết lại theo design.
- "Tôi chọn luôn" → architect quyết.

## Lệnh tiếp theo
Cỡ L: `/team:architect <ID>`; còn lại: `/team:design <ID>` hoặc `/team:run <ID>`.
