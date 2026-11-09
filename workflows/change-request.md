# Playbook: change-request

## Khi nào áp dụng
- Feature đã có `spec.md` được duyệt (G1) và người muốn đổi yêu cầu.
- Phạm vi hoặc tiêu chí nghiệm thu thay đổi giữa chừng.

## Cỡ mặc định
M.

## Chuỗi
0. `/team:intake` → team-leader → `intake.md` (đã chạy, trỏ feature gốc).
1. `/team:analyze --amend` → analyst → `spec.md` có `## Amendment <n>`.
2. `/team:architect` (chế độ impact) → architect → `arch-impact.md`.
3. `/team:plan --insert` → tech-lead → `tasks.md` thêm task mới, đánh dấu task bị ảnh hưởng.
4. `/team:build` → tech-lead → dev, reviewer.
5. `/team:verify` → qa → `acceptance.md` (chạy lại cả tiêu chí cũ).
6. `/team:asbuilt`, `/team:pr`, `/team:release` như new-feature.

## Cổng
G1 (duyệt lại spec đã sửa), G2, G3, G4; G5 khi lên prod.

## Điểm dừng
- Amendment mâu thuẫn kiến trúc đã duyệt.
- Task đã gộp bị vô hiệu bởi thay đổi.

## Tiêu chí xong
- Spec có amendment đã duyệt; tiêu chí cũ và mới đều đạt trong `acceptance.md`.

## Lỗi thường gặp
- Sửa thẳng `spec.md` không ghi amendment.
- Quên chạy lại tiêu chí cũ.

## Playbook liên quan
`new-feature`, `refactor`.
