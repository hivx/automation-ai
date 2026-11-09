# Playbook: docs-only

## Khi nào áp dụng
- Chỉ đổi tài liệu kỹ thuật, README, comment; không đổi code chạy.

## Cỡ mặc định
S.

## Chuỗi
0. `/team:intake` → team-leader → `intake.md`.
1. writer (team-leader gọi qua Agent) → `docs/**`, `README.md`.
2. `/team:pr` → tech-lead → PR; bật tự merge khi CI xanh (`gh pr merge --auto`), vẫn theo luật bảo vệ nhánh.

## Cổng
Không.

## Điểm dừng
- Diff chạm file ngoài `docs/**` và `README.md`: chuyển playbook khác.

## Tiêu chí xong
- PR chỉ chứa tài liệu; CI xanh; nội dung khớp code hiện tại.

## Lỗi thường gặp
- Lén sửa code trong PR tài liệu.
- Tài liệu mô tả hành vi chưa có.

## Playbook liên quan
`client-docs`.
