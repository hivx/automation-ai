# Phiên mẫu (dàn ý)

Ba dàn ý để biết phiên thật trông thế nào. Không phải kịch bản bắt buộc.

## 1. Ngày đầu trên dự án có sẵn
1. Người: `/team:takeover`.
2. team-leader: T0 (cây thư mục, manifest, git log) → T1 (README, docs) → T2 lấy mẫu module nóng. Không chạy T3 vì không có mâu thuẫn.
3. Kết quả: `assessment.md` trả lời 3 câu; `ai-readiness.md` kết luận "chỉnh profile"; 6 câu hỏi mở.
4. Người: trả lời câu hỏi, thêm `Approved-by:` vào `ai-readiness.md`.
5. Người: `/team:onboard` → đội ghi `.team/profile.json`, in lệnh cài plugin LSP khuyên dùng.
6. Người: `/team:status` → "chưa có feature; sẵn sàng nhận intake".

## 2. Tính năng mới cỡ M
1. Người: `/team:intake "Cho phép khách hủy đơn trong 30 phút"`.
2. team-leader: playbook new-feature, cỡ M (đổi dữ liệu, một module). Ghi lý do vào journal.
3. analyst: 7 mục phân loại → 2 câu hỏi (hoàn tiền thế nào; đơn đã giao một phần) → team-leader hỏi người → `spec.md` có DoD. Dừng ở G1.
4. Người duyệt G1, `/team:run`.
5. designer: `design.md` có touchpoints và test plan. tech-lead: `plan.md`, `tasks.md` 7 task. Dừng ở G3.
6. Người duyệt G3, `/team:run`.
7. tech-lead → dev ×2 song song (không chung file) → reviewer → 1 vòng sửa một major về xử lý lỗi (mã `STD-ERR-n`) → tick đủ 7 task.
8. qa: chạy từng tiêu chí, dán đầu ra; migration lên/xuống. `acceptance.md`: accepted. Dừng ở G4.
9. Người duyệt G4. writer: `asbuilt.md`; tech-lead: `/team:pr`. Release prod cần `Approved-by-prod:`.

## 3. Sửa lỗi cỡ S
1. Người: `/team:intake --type bug "Xuất CSV mất dấu tiếng Việt"`.
2. team-leader: playbook bug-fix, cỡ S, một dev.
3. dev: viết test hỏng trước (dán đầu ra đỏ) → sửa → `cmd.test_one` xanh → `cmd.lint` sạch → commit.
4. reviewer: approve. Verify tự động.
5. tech-lead: `/team:pr`. journal ghi 4 dòng.
