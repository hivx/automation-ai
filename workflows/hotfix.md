# Playbook: hotfix

## Khi nào áp dụng
- Production đang hỏng, ảnh hưởng người dùng ngay.
- Người yêu cầu chữa trước, làm đầy đủ sau.

## Cỡ mặc định
S.

## Chuỗi
0. `/team:intake --type hotfix` → team-leader → `intake.md`.
1. `/team:build` → dev: nhánh `team/<ID>-hotfix` tách từ nhánh đang chạy prod; sửa tối thiểu; có test tái hiện nếu viết được trong vài phút.
2. `/team:verify` (nhanh) → qa → `acceptance.md`: tiêu chí sửa + smoke.
3. `/team:pr` → tech-lead → PR vào nhánh prod.
4. `/team:release` → devops → prod CHỈ khi có `Approved-by-prod:`.
5. Mở ngay `bug-fix` đầy đủ (test, nguyên nhân gốc) và ghi vào `defects.md`.

## Cổng
G5 luôn là người. Các cổng khác theo config.

## Điểm dừng
- Chưa có `Approved-by-prod:`.
- Sửa cần hơn một thay đổi nhỏ: dừng, báo người.

## Tiêu chí xong
- Prod smoke xanh; `bug-fix` tiếp theo đã được mở.

## Lỗi thường gặp
- Bỏ luôn bug-fix đầy đủ sau khi prod hết lỗi.
- Gộp thêm thay đổi khác vào hotfix.

## Playbook liên quan
`bug-fix`, `release`, `ci-fix`.
