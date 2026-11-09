# Playbook: takeover

## Khi nào áp dụng
- Repo đã có code, đội chưa từng làm (chưa có `.team/profile.json`).
- Người hỏi "dự án này làm gì, tới đâu, làm gì tiếp".
- Đổi chủ dự án hoặc nhận dự án từ đội khác.

## Cỡ mặc định
Không áp dụng (chỉ đọc, không sửa code).

## Chuỗi
1. `/team:takeover` → team-leader (+Explore, researcher) → quét T0 siêu dữ liệu → T1 tài liệu → T2 đối chiếu lấy mẫu → [T3 đọc sâu: chỉ khi T2 thấy mâu thuẫn, module không có tài liệu, hoặc `--full`].
2. Báo cáo 3 câu hỏi → `docs/team/assessment.md`, `ai-readiness.md`, `profile-proposal.md`, `debt.md`, `open-questions.md`.
3. Người duyệt `ai-readiness.md` (G0).
4. `/team:onboard` → team-leader → `.team/`, `.claude/`, khối `CLAUDE.md`, `docs/team/onboarding.md`.

## Cổng
- G0: người thêm `Approved-by:` vào `docs/team/ai-readiness.md`.

## Điểm dừng
- Sau bước 2: chờ G0.
- Tầng quét vượt ngân sách mà chưa trả lời được: dừng, ghi "chưa quét" và độ tin cậy.

## Tiêu chí xong
- 5 báo cáo có mục đã quét / chưa quét / độ tin cậy.
- G0 đã duyệt; onboard in bảng đã tạo / bỏ qua / việc tay.
- Không file nào của dự án bị sửa trước onboard.

## Lỗi thường gặp
- Đọc sâu cả repo ngay từ đầu (bỏ qua T0–T2).
- Tin README mà không đối chiếu code.
- Chạy onboard trước khi G0 được duyệt.

## Playbook liên quan
`new-project` (repo rỗng), `new-feature` (việc đầu tiên sau onboard), `refactor` (nợ trong `debt.md`).
