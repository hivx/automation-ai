Feature: <ID>
Stage: plan
Author-agent: tech-lead
Date: <YYYY-MM-DD>
Approved-by:
<!-- Cổng: người duyệt điền dòng trên `Approved-by: <tên> <YYYY-MM-DD>`. Không có cổng thì để trống. -->

# Tasks <ID>

Mỗi task là một lát cắt dọc: một hành vi kèm test, tối đa 5 file, khoảng 15–30 phút; tối đa 4 dòng mỗi task. File này chỉ chứa dòng task, dấu tick và một dòng `baseline:` (không ghi nhật ký tiến độ). Hai task chung file thì phụ thuộc nhau. Đánh dấu `BLOCKED: <lý do>` cuối dòng khi bị chặn.

- [ ] T1 — <tiêu đề> — files: <đường/dẫn, ...> — test: <file test> — depends: —
- [ ] T2 — <tiêu đề> — files: <...> — test: <...> — depends: T1
