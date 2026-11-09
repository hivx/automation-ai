Feature: <ID>
Stage: analyze
Author-agent: analyst
Date: <YYYY-MM-DD>
Approved-by:
<!-- Cổng: người duyệt điền dòng trên `Approved-by: <tên> <YYYY-MM-DD>`. Không có cổng thì để trống. -->

# Spec <ID> — <tiêu đề>

## Mục tiêu
<vì sao làm; giá trị cho ai>

## Người dùng
<ai dùng, trong tình huống nào>

## Phạm vi
- Trong: <...>
- Ngoài: <...>

## Dữ liệu
<thực thể, trường, khối lượng; dữ liệu nhạy cảm>

## Giao diện / tích hợp
<API, màn hình, hệ thống ngoài>

## NFR
| Mã | Yêu cầu | Đo bằng |
|---|---|---|
| NFR-1 | <...> | <...> |

## Tiêu chí nghiệm thu
| Mã | Tiêu chí (đo được) | Cách kiểm |
|---|---|---|
| AC-1 | <...> | <lệnh hoặc bước có đầu ra> |

## Assumptions decided by the team
- <giả định> — vì <lý do>; sai thì <cách sửa>

## Definition of Done
- [ ] Mọi AC đạt, đầu ra được dán trong acceptance.md
- [ ] As-Built viết xong (asbuilt.md)
- [ ] README/tài liệu người dùng cập nhật nếu hành vi đổi
- [ ] Mục CHANGELOG
- [ ] CI xanh

## Amendment <n> (<YYYY-MM-DD>)
<chỉ khi --amend: thay đổi gì; tiêu chí đánh dấu [changed]>
