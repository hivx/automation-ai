# Playbook: data-migration

## Khi nào áp dụng
- Chuyển, biến đổi hoặc nạp dữ liệu giữa schema/hệ thống.
- Có rủi ro mất hoặc sai dữ liệu.

## Cỡ mặc định
M (L khi nhiều hệ thống).

## Chuỗi
0. `/team:intake` → team-leader → `intake.md`.
1. `/team:analyze` → analyst → `spec.md`: phạm vi dữ liệu, số lượng, quy tắc đối soát.
2. `/team:design` → designer → `design.md`: ánh xạ trường, migration, rollback.
3. `/team:plan` → tech-lead → `tasks.md`.
4. `/team:build` → dev: chạy thử trên BẢN SAO dữ liệu (`cmd.migrate`), không đụng dữ liệu thật.
5. `/team:verify` → qa → `acceptance.md`: đối soát số lượng; migration lên/xuống.
6. `/team:release` → devops → chạy trong khung giờ đã hẹn, có kế hoạch rollback.

## Cổng
G1, G2b (bật cho playbook này), G3, G4, G5.

## Điểm dừng
- Đối soát lệch; không có rollback đã kiểm; chưa có khung giờ.

## Tiêu chí xong
- Đối soát khớp trên bản sao và trên thật; rollback đã chạy thử.

## Lỗi thường gặp
- Chạy thử trên dữ liệu thật.
- Migration không có chiều xuống.

## Playbook liên quan
`release`, `integration`.
