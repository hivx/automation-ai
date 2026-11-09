# Playbook: bug-fix

## Khi nào áp dụng
- Hành vi sai so với spec hoặc tài liệu; tái hiện được.
- Không gấp đến mức phải chữa thẳng trên prod.

## Cỡ mặc định
S.

## Chuỗi
0. `/team:intake --type bug` → team-leader → `intake.md`, mục mới trong `docs/team/defects.md`.
1. `/team:build` → dev (1 task): viết test hỏng tái hiện lỗi TRƯỚC, dán đầu ra đỏ → sửa → `cmd.test_one` xanh → reviewer.
2. `/team:verify` → qa (cỡ S: kiểm tự động) → `acceptance.md`.
3. `/team:pr` → tech-lead → PR.

## Cổng
G4 nếu bật; G5 khi phát hành prod.

## Điểm dừng
- Không tái hiện được lỗi: dừng, hỏi thêm dữ liệu.
- Sửa cần đổi thiết kế: chuyển sang `change-request`.

## Tiêu chí xong
- Có đầu ra đỏ trước và xanh sau của test tái hiện; `cmd.test` xanh; `defects.md` cập nhật.

## Lỗi thường gặp
- Sửa trước, viết test sau.
- Test chỉ kiểm triệu chứng, không kiểm nguyên nhân.
- Sửa thêm chỗ khác "tiện tay".

## Playbook liên quan
`hotfix`, `change-request`.
