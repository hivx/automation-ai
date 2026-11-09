# Eval: takeover

Dự án mẫu: dự án đã onboard có FEAT-001 (CSV export) — xem `evals/RESULTS.md`.

## Scenario 1 — Dự án nhỏ có lệch tài liệu
- Situation: dự án nhỏ có lệch tài liệu.
- Setup: `rm -rf docs .team .claude`
- Input: `/team:takeover`
- Baseline input: `Tìm hiểu dự án này: làm gì, tới đâu, việc tiếp theo; viết báo cáo, không sửa gì.`
- Good: 5 báo cáo; T0 bằng detect-stack; phát hiện to_csv thiếu và test skip; T3 không chạy; có bảng Đã quét/Chưa quét/Độ tin cậy.
- Bad: Sửa code; không có bảng tầng; không thấy test skip.
- Checks:
  - exists: `docs/team/assessment.md`
  - exists: `docs/team/ai-readiness.md`
  - exists: `docs/team/profile-proposal.md`
  - exists: `docs/team/debt.md`
  - exists: `docs/team/open-questions.md`
  - grep: `to_csv` in `docs/team/assessment.md`
  - grep: `skip` in `docs/team/assessment.md`
  - grep: `Đã quét` in `docs/team/assessment.md`
  - unchanged: `inventory`

## Scenario 2 — CLAUDE.md cũ
- Situation: claude.md cũ.
- Setup: `rm -rf docs .team .claude`
- Input: `/team:takeover`
- Baseline input: `Đánh giá mức sẵn sàng cho AI của repo này.`
- Good: ai-readiness đề nghị viết lại CLAUDE.md (mô tả Django không tồn tại).
- Bad: Giữ CLAUDE.md.
- Checks:
  - grep: `(Viết lại|rewrite)` in `docs/team/ai-readiness.md`
  - unchanged: `CLAUDE.md`

## Scenario 3 — Profile đề xuất hợp lệ
- Situation: profile đề xuất hợp lệ.
- Setup: `rm -rf docs .team .claude`
- Input: `/team:takeover`
- Baseline input: `Đề xuất lệnh test/lint cho repo này.`
- Good: `cmd.test_one` có `{file}`; chỉ dùng tên khe của schema.
- Bad: Chỗ thay `{module}` hoặc khe `cmd.test_all`.
- Checks:
  - grep: `cmd\.test_one.*\{file\}` in `docs/team/profile-proposal.md`
  - absent: `cmd\.test_all` in `docs/team/profile-proposal.md`
