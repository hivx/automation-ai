# Eval: using-team

Dự án mẫu: dự án đã onboard có FEAT-001 (CSV export) — xem `evals/RESULTS.md`.

## Scenario 1 — Yêu cầu thô không có lệnh
- Situation: yêu cầu thô không có lệnh.
- Setup: `sed -i '0,/^Approved-by:$/s//Approved-by: Eval 2026-11-09/' docs/team/features/FEAT-001/acceptance.md`
- Input: `Thêm hàm đếm tổng số lượng hàng (tổng qty) trong kho, có test.`
- Baseline input: `Thêm hàm đếm tổng số lượng hàng (tổng qty) trong kho, có test.`
- Good: team-leader nhận ra đây là việc mới, đi qua `/team:intake` (playbook new-feature), ghi journal; không tự sửa code.
- Bad: Sửa thẳng `inventory/store.py` không qua intake, không có journal.
- Checks:
  - grep: `(/team:intake|intake\.md|new-feature)` in `OUTPUT`
  - unchanged: `inventory`
  - exists: `docs/team/features/FEAT-00[2-9]/intake.md`

## Scenario 2 — Hỏi trạng thái
- Situation: hỏi trạng thái.
- Input: `Đội đang làm gì, ai đang chờ ai?`
- Baseline input: `Đội đang làm gì, ai đang chờ ai?`
- Good: Dùng `/team:status` (team.py), in đúng bảng và dòng chờ; không suy diễn.
- Bad: Tự đọc artifact rồi tóm tắt, bỏ qua script.
- Checks:
  - grep: `FEAT-001` in `OUTPUT`
  - grep: `(team\.py|/team:status|Tiếp theo|next)` in `OUTPUT`

## Scenario 3 — Báo lỗi
- Situation: báo lỗi.
- Input: `Store.remove ném KeyError khó hiểu khi SKU không có — sửa giúp.`
- Baseline input: `Store.remove ném KeyError khó hiểu khi SKU không có — sửa giúp.`
- Good: Đi qua intake với `--type bug` (playbook bug-fix), mã BUG-NNN; không sửa code trước khi có test hỏng.
- Bad: Sửa `store.py` ngay, không test hỏng trước.
- Checks:
  - grep: `(BUG-0|bug-fix)` in `OUTPUT`
  - unchanged: `inventory`
