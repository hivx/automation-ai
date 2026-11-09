Feature: <ID>
Stage: design
Author-agent: designer
Date: <YYYY-MM-DD>
Approved-by:
<!-- Cổng: người duyệt điền dòng trên `Approved-by: <tên> <YYYY-MM-DD>`. Không có cổng thì để trống. -->

# Design <ID> — <tiêu đề>

## 1. Bối cảnh
<trích spec; kiến trúc liên quan>

## 2. Mô hình dữ liệu
<thực thể, trường, ràng buộc>

## 3. API / hợp đồng
<endpoint/hàm, đầu vào, đầu ra, lỗi; phiên bản>

## 4. Luồng
1. <...>

## 5. Quyền
<ai được làm gì; kiểm ở đâu>

## 6. Migration và rollback
- Lên: <...>
- Xuống: <...>
- Đối soát: <...>

## 7. Touchpoints
| file | change | task |
|---|---|---|
| <đường/dẫn> | mới / sửa | T1 |

## 8. Test plan
| Tiêu chí | Test | Loại |
|---|---|---|
| AC-1 | <file test::tên> | unit / integration / e2e |
