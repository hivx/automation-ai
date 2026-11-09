# Playbook: new-feature

## Khi nào áp dụng
- Người xin thêm hành vi mới cho hệ thống đang chạy.
- Không phải sửa lỗi, không đổi spec đã duyệt.

## Cỡ mặc định
Theo intake (S, M hoặc L).

## Chuỗi
0. `/team:intake` → team-leader → `intake.md` (đã chạy).
1. `/team:analyze` → analyst → `spec.md` (cỡ S: bản ngắn, không G1).
2. [`/team:research` → researcher → `research.md`: khi spec còn câu hỏi kỹ thuật.]
3. [`/team:architect` → architect → `arch-impact.md`: chỉ cỡ L.]
4. `/team:design` → designer → `design.md` (bỏ qua ở cỡ S).
5. `/team:plan` → tech-lead → `plan.md`, `tasks.md` (bỏ qua ở cỡ S).
6. `/team:build` → tech-lead → dev, reviewer (cỡ S: 1 dev).
7. `/team:verify` → qa → `acceptance.md` (cỡ S: kiểm tự động, không gọi qa riêng).
8. `/team:asbuilt` → writer → `asbuilt.md`.
9. `/team:pr` → tech-lead → PR.
10. `/team:release` → devops.

## Cổng
G1, G3, G4 (+ G2 khi cỡ L, G5 khi lên prod). Cỡ S không qua G1 và G3.

## Điểm dừng
- Cổng bật chưa duyệt; analyst trả `NEEDS_ANSWER`; reviewer báo design-defect.

## Tiêu chí xong
- `acceptance.md` accepted; As-Built và CHANGELOG có; PR mở hoặc đã merge.

## Lỗi thường gặp
- Định cỡ S cho việc đổi schema/API.
- Gom nhiều tính năng vào một feature.
- Bỏ As-Built vì "đúng thiết kế".

## Playbook liên quan
`change-request` (đổi spec đã duyệt), `integration`, `bug-fix`.
