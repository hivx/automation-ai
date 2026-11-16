Feature: <ID>
Stage: plan
Author-agent: tech-lead
Date: <YYYY-MM-DD>
Approved-by:
<!-- Cổng: người duyệt điền dòng trên `Approved-by: <tên> <YYYY-MM-DD>`. Không có cổng thì để trống. -->

# Tasks <ID>

Mỗi task là một lát cắt dọc: 1–4 tiêu chí trọn vẹn, khoảng 100–400 dòng thay đổi kèm test, tối đa 6 file; cỡ M tối đa 6 task, cỡ L tối đa 12; tối đa 4 dòng mỗi task. Thêm `[risk]` cuối dòng cho task đụng phân quyền hay bí mật, migration hay schema, tiền hay xóa dữ liệu, hợp đồng dùng ngoài feature, hoặc trạng thái dùng chung: mọi task được test và review gộp ở mốc của lượt; task phụ thuộc vào task `[risk]` chờ mốc đó review xong. File này chỉ chứa dòng task, dấu tick và một dòng `baseline:` (không ghi nhật ký tiến độ). Hai task chung file thì phụ thuộc nhau. Đánh dấu `BLOCKED: <lý do>` cuối dòng khi bị chặn.

- [ ] T1 — <tiêu đề> — files: <đường/dẫn, ...> — test: <file test> — depends: —
- [ ] T2 — <tiêu đề> — files: <...> — test: <...> — depends: T1 [risk]
