---
name: asbuilt
description: Dùng khi feature đã accepted và cần As-Built, release notes, mục CHANGELOG, cập nhật README và nội dung PR trước khi phát hành.
argument-hint: "<ID>"
context: fork
agent: team:writer
background: false
allowed-tools: Bash(python3 *) Bash(cat *)
---

## Mục đích
Ghi lại cái ĐÃ giao, khác thiết kế ở đâu, cho người đọc phù hợp.

## Đầu vào
- `$ARGUMENTS`: mã `<ID>`.
- `spec.md`, `design.md`, `acceptance.md`, file diff `docs/team/features/<ID>/diff.patch` (tech-lead tạo bằng `git diff <base_branch>...team/<ID>`). `<kit>` = nội dung `.team/plugin_root`.

## Điều kiện trước
`acceptance.md` có `Verdict: accepted`. Kiểm: `python3 "$(cat .team/plugin_root)/scripts/team.py" status <ID>`. Thiếu `diff.patch` → trả về, xin tech-lead tạo.

## Các bước
1. Ghi `.team/current.json` {feature, stage: "asbuilt", agent: "writer", started_at}.
2. Đọc `diff.patch` và `design.md`; so từng mục thiết kế với code đã giao.
3. `asbuilt.md` từ `<kit>/templates/artifacts/asbuilt.md`: điểm khác thiết kế (`file:line`, lý do); giống thì ghi "đúng thiết kế".
4. Release notes cho người dùng: đổi gì, ai bị ảnh hưởng, cần làm gì.
5. Mục mới dưới `## [Unreleased]` trong `CHANGELOG.md`.
6. README / tài liệu người dùng: sửa phần hành vi đã đổi, khớp `acceptance.md`.
7. `pr-body.md` từ mẫu PR của dự án: vì sao, đổi gì, cách kiểm, mã.

## Đầu ra
- `docs/team/features/<ID>/asbuilt.md`, `pr-body.md`; `CHANGELOG.md`; `README.md` hoặc `docs/**`.
- Tin trả ≤ 10 dòng: file đã ghi, điểm khác thiết kế, phần cần người đọc lại.

## Tiêu chí xong
- Mọi mục thiết kế đã được so; CHANGELOG có mục mới; dán đoạn diff làm căn cứ cho mỗi điểm khác.

## Dấu hiệu sai
- "Đúng thiết kế, viết một dòng" → vẫn so từng mục.
- "Release notes kỹ thuật cho nhanh" → viết cho người dùng.
- "Thêm tính năng sắp làm vào notes" → chỉ cái có trong diff.

## Lệnh tiếp theo
`/team:pr <ID>`, rồi `/team:release <ID>`.
