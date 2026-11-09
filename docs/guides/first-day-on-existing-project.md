# Ngày đầu trên dự án có sẵn

Mục tiêu: trước khi đội sửa một dòng code, bạn và đội cùng biết dự án làm gì, đã tới đâu, việc tiếp theo là gì.

## Trước khi bắt đầu
- Cài plugin (`docs/06-install.md`).
- Làm việc trên nhánh sạch. takeover không sửa file của dự án; nó chỉ ghi vào `docs/team/`.

## Bước 1 — `/team:takeover`
- Đội quét theo tầng: T0 siêu dữ liệu → T1 tài liệu → T2 đối chiếu lấy mẫu → T3 chỉ khi cần (hoặc `--full`).
- Kết quả trong `docs/team/`:
  - `assessment.md` — ba câu trả lời + phụ lục sức khỏe stack (build/test có chạy không, lint, coverage, phụ thuộc lỗi thời/CVE, secret lộ, test chập chờn).
  - `ai-readiness.md` — CLAUDE.md, `.claude/`, plugin, MCP, AGENTS.md hiện có: giữ / cắt / viết lại; kết luận: sẵn sàng / chỉnh profile / dọn trước.
  - `profile-proposal.md` — profile đề xuất, mỗi khe có bằng chứng.
  - `debt.md` — nợ kỹ thuật: chặn / nên làm / để sau.
  - `open-questions.md` — tối đa 10 câu.

## Bước 2 — Đọc và duyệt (cổng G0)
1. Đọc mục "đã quét / chưa quét / độ tin cậy" trước.
2. Kiểm `profile-proposal.md`: nhất là `cmd.test_one`, `protected_paths`, `allowed_new_file_roots`.
3. Trả lời `open-questions.md` ngay trong file.
4. Thêm `Approved-by: <tên> <YYYY-MM-DD>` lên đầu `ai-readiness.md`.

## Bước 3 — `/team:onboard`
- Ghi `.team/profile.json`, `.team/config.json`, `.claude/settings.json` (quyền, nhánh bảo vệ, team-leader làm agent phiên chính), `.claude/rules/`, khối `team` trong `CLAUDE.md`.
- In lệnh cài plugin khuyên dùng; bạn tự quyết cài.
- Commit các file này.

## Bước 4 — Việc đầu tiên
- Chọn việc nhỏ (cỡ S) để đo đội: một lỗi trong `debt.md` hoặc `open-questions.md`.
- `/team:intake --type bug "<mô tả>"`, theo dõi bằng `/team:status`.
- Cuối ngày: đọc `docs/team/journal/`. Thấy đội chậm/sai ở đâu → `/team:feedback`.
