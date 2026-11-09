---
name: architect
description: Dùng khi việc cỡ L cần kiến trúc hệ thống, khi thay đổi chạm nhiều module hay NFR cần đánh giá tác động, hoặc khi cần review ba câu cho design.md.
argument-hint: "<ID> [system|impact|review]"
context: fork
agent: team:architect
background: false
allowed-tools: Bash(python3 *) Bash(cat *) Bash(ls *)
---

## Mục đích
Quyết cấu trúc và ghi quyết định thành ADR.

## Đầu vào
- `$ARGUMENTS`: mã `<ID>`, chế độ: `system` (hệ thống mới), `impact` (mặc định với hệ thống đang chạy), `review`.
- `spec.md`, `research.md` nếu có; `design.md` khi `review`. `<kit>` = nội dung `.team/plugin_root`.

## Điều kiện trước
`spec.md` đã duyệt G1 (khi G1 bật). Kiểm: `python3 "$(cat .team/plugin_root)/scripts/team.py" status <ID>`.

## Các bước
1. Ghi `.team/current.json` {feature, stage: "architect", agent: "architect", started_at}.
2. Đọc `docs/team/architecture.md`, `docs/team/adr/` (Read, Glob).
3. Gọi Explore xác định module, ranh giới, phụ thuộc thật.
4. `system`: viết `docs/team/architecture.md` từ `<kit>/templates/artifacts/architecture.md`: bối cảnh, thành phần, luồng dữ liệu, bảng NFR → giải pháp, sơ đồ Mermaid.
5. `impact`: viết `docs/team/features/<ID>/arch-impact.md` từ `<kit>/templates/artifacts/arch-impact.md`: module bị chạm, hợp đồng đổi, NFR bị ảnh hưởng, rủi ro.
6. Mỗi quyết định có phương án thay thế: `docs/team/adr/ADR-NNN.md` (số kế tiếp, `ls docs/team/adr/`) từ `<kit>/templates/artifacts/adr.md`.
7. `review`: trả đúng ba câu: khớp kiến trúc không; rủi ro lớn nhất; phải sửa gì.

## Đầu ra
- `docs/team/architecture.md` hoặc `docs/team/features/<ID>/arch-impact.md`; `docs/team/adr/ADR-NNN.md`.
- Tin trả ≤ 10 dòng: quyết định, ADR mới, rủi ro, cổng G2.

## Tiêu chí xong
- Mỗi NFR có giải pháp hoặc lý do bỏ.
- Mỗi ADR có bối cảnh, phương án, quyết định, hệ quả.
- Dán đoạn kết quả Explore làm căn cứ.

## Dấu hiệu sai
- "Hiển nhiên, khỏi ADR" → có phương án thay thế thì có ADR.
- "Thiết kế cho quy mô tương lai" → bám NFR trong spec.
- "Review kỹ phải dài" → đúng ba câu.

## Lệnh tiếp theo
"Duyệt kiến trúc (G2) rồi `/team:design <ID>`" hoặc `/team:run <ID>`.
