# Playbook: integration

## Khi nào áp dụng
- Nối với API, dịch vụ hay hệ thống bên ngoài.
- Có xác thực, giới hạn tần suất, webhook hoặc đồng bộ dữ liệu.

## Cỡ mặc định
M (L khi nhiều hệ thống).

## Chuỗi
0. `/team:intake` → team-leader → `intake.md`.
1. `/team:research` → researcher → `research.md`: API, xác thực, giới hạn, môi trường sandbox.
2. `/team:architect` (impact) → architect → `arch-impact.md`.
3. `/team:design` → designer → `design.md`: hợp đồng, retry, idempotency, timeout.
4. `/team:plan` → tech-lead → `tasks.md`.
5. `/team:build` → tech-lead → dev, reviewer.
6. `/team:verify` → qa → `acceptance.md`: chạy trên sandbox của bên ngoài.
7. `/team:release` → devops.

## Cổng
G2, G3, G4, G5 (+ G1 khi có spec mới).

## Điểm dừng
- Chưa có tài khoản sandbox hoặc secret: dừng, báo người.

## Tiêu chí xong
- Kiểm trên sandbox đạt; retry và timeout có test; secret không nằm trong repo.

## Lỗi thường gặp
- Test gọi thẳng API thật.
- Retry không idempotent.

## Playbook liên quan
`new-feature`, `data-migration`.
