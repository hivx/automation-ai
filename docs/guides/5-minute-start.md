# Bắt đầu trong 5 phút

1. **Cài** (trong Claude Code):
   ```
   /plugin marketplace add <owner>/automation-ai
   /plugin install team@automation-ai
   ```
2. **Mở dự án**: `cd <dự-án> && claude`.
3. **Dự án đã có code?**
   - Có: `/team:takeover`. Đọc `docs/team/assessment.md` và `docs/team/ai-readiness.md`. Thêm `Approved-by: <tên> <YYYY-MM-DD>` vào đầu `ai-readiness.md`.
   - Chưa (repo rỗng): bỏ qua bước này.
4. **Cấu hình đội**: `/team:onboard` (repo rỗng: `/team:onboard --new`). Kiểm tra `.team/profile.json`: nhất là `cmd.test_one`.
5. **Giao việc đầu tiên**: `/team:intake "Thêm nút xuất CSV cho danh sách đơn hàng"`.
6. **Theo dõi**: `/team:status`. Khi đội dừng ở cổng, đọc artifact được nhắc tới, thêm dòng `Approved-by:` rồi `/team:run`.

Muốn đội tự chạy không hỏi: `/team:intake --decide "<yêu cầu>"`. Muốn tắt hẳn cổng: đặt `false` trong `.team/config.json → gates`; "tự động hoàn toàn" = mọi cổng `false` trừ `G5_prod`, và `default_mode: "decide"`.

Tiếp theo: `want-x-type-y.md`, `decision-tree.md`.
