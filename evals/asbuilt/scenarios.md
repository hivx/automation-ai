# Eval: asbuilt

Dự án mẫu: dự án đã onboard có FEAT-001 (CSV export) đã `Verdict: accepted`, chờ G4 — xem `evals/RESULTS.md`. Setup thêm dòng duyệt G4. Dự án mẫu giữ CHANGELOG ở `docs/CHANGELOG.md` (do T1 tạo). Lần chạy 2026-11-10: check CHANGELOG ban đầu trỏ nhầm `CHANGELOG.md` ở gốc và check `^## Đổi gì` được thêm SAU khi chạy; cả hai bản được chấm lại trên thư mục làm việc đã lưu.

## Scenario 1 — Feature đã accepted và duyệt G4
- Situation: FEAT-001 đã nghiệm thu; người duyệt G4.
- Setup: `sed -i '0,/^Approved-by:$/s//Approved-by: Lan 2026-11-10/' docs/team/features/FEAT-001/acceptance.md`
- Input: `/team:asbuilt FEAT-001`
- Baseline input: `Viết As-Built, CHANGELOG và nội dung PR cho FEAT-001.`
- Good: `asbuilt.md` so từng mục với diff, CHANGELOG có dòng `(FEAT-001)` dưới `[Unreleased]`, `pr-body.md` có bốn tiêu đề mà `/team:pr` grep, nợ sau G4 của qa được đóng.
- Bad: As-Built chép lại thiết kế; CHANGELOG bị đổi thành số phiên bản; pr-body thiếu "Cách kiểm"; code bị sửa.
- Checks:
  - exists: `docs/team/features/FEAT-001/asbuilt.md`
  - grep: `FEAT-001` in `docs/CHANGELOG.md`
  - grep: `Unreleased` in `docs/CHANGELOG.md`
  - grep: `^## Đổi gì` in `docs/team/features/FEAT-001/pr-body.md`
  - grep: `^## Cách kiểm` in `docs/team/features/FEAT-001/pr-body.md`
  - grep: `^## Vì sao` in `docs/team/features/FEAT-001/pr-body.md`
  - absent: `^Released:` in `docs/team/features/FEAT-001/asbuilt.md`
  - unchanged: `inventory/`
