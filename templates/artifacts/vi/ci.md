Feature: <ID>
Stage: ci
Author-agent: devops
Date: <YYYY-MM-DD>
Approved-by:
<!-- Cổng: người duyệt điền dòng trên `Approved-by: <tên> <YYYY-MM-DD>`. Không có cổng thì để trống. -->

# CI/CD

## Pipeline
| Workflow | Kích hoạt | Bước | Runner |
|---|---|---|---|

## Lịch sử sự cố
| Ngày | Lần chạy | Phân loại STD-CI-4 (code / test chập chờn / môi trường / cấu hình / phụ thuộc) | Trích log | Cách sửa | PR |
|---|---|---|---|---|---|

## Deploy
- Staging: `deploy.staging` → `deploy.smoke`
- Prod: chỉ khi có `Approved-by-prod:`; rollback: <lệnh đã kiểm>
