# Playbook: refactor

## Khi nào áp dụng
- Cần dọn cấu trúc, tên, code chết, phụ thuộc thừa mà KHÔNG đổi hành vi.
- Nợ trong `docs/team/debt.md` đến lượt xử lý.

## Cỡ mặc định
M.

## Chuỗi
0. `/team:intake` → team-leader → `intake.md`.
1. `/team:design` (bản ngắn) → designer → `design.md`: phạm vi, touchpoints, cách chứng minh hành vi không đổi.
2. `/team:clean <kind>` → maintainer → commit; một loại dọn dẹp mỗi lần.
3. `/team:verify` → qa → `acceptance.md`: đầu ra `cmd.test` trước == sau.
4. `/team:pr` → tech-lead → PR.

## Cổng
G2b BẬT cho playbook này (người duyệt `design.md`); G4 nếu bật.

## Điểm dừng
- Test trước và sau khác nhau.
- Dọn dẹp buộc phải đổi hành vi: tách thành `new-feature` hoặc `change-request`.

## Tiêu chí xong
- Hai đầu ra `cmd.test` (trước/sau) giống nhau được dán; lint/typecheck sạch; mỗi PR một loại.

## Lỗi thường gặp
- Trộn sửa lỗi vào refactor.
- Dọn toàn repo trong một PR.

## Playbook liên quan
`bug-fix`, `dependency-upgrade`.
