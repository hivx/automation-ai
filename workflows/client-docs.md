# Playbook: client-docs

## Khi nào áp dụng
- Tài liệu cho khách hàng hay người dùng cuối: hướng dẫn, giới thiệu, ghi chú phát hành.
- Người đọc không phải dev.

## Cỡ mặc định
S (M khi nhiều tài liệu).

## Chuỗi
0. `/team:intake` → team-leader → `intake.md`.
1. `/team:analyze` → analyst → `spec.md`: người đọc, phạm vi, mức chi tiết, định dạng.
2. writer (team-leader gọi qua Agent) → tài liệu trong `docs/**`.
3. Người duyệt nội dung (review nội dung, không phải review code).
4. `/team:pr` → tech-lead → PR.

## Cổng
G1 (người đọc và phạm vi); duyệt nội dung ở bước 3.

## Điểm dừng
- Chưa rõ người đọc; nội dung cần thông tin nghiệp vụ đội không có.

## Tiêu chí xong
- Người duyệt nội dung; mọi bước trong tài liệu khớp hành vi thật.

## Lỗi thường gặp
- Viết cho dev thay vì cho người đọc đã nêu.
- Ảnh chụp lỗi thời.

## Playbook liên quan
`docs-only`, `release`.
