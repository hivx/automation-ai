Feature: <ID>
Stage: analyze
Author-agent: analyst
Date: <YYYY-MM-DD>
Approved-by:
<!-- Cổng: người duyệt điền dòng trên `Approved-by: <tên> <YYYY-MM-DD>`. Không có cổng thì để trống. -->

# Spec <ID> — <tiêu đề>

## Đọc lại yêu cầu
<!-- ≤ 5 dòng, bằng lời của người yêu cầu, không mã. Team-leader đưa khối này cho người xem ở mọi chế độ. -->
- Anh/chị yêu cầu: "<trích nguyên văn yêu cầu>"
- Anh/chị sẽ thấy: <làm ở đâu (màn hình, phiếu, lệnh) → làm gì → thấy gì xảy ra>
- Bật sẵn: <có / tắt vì anh/chị muốn có công tắc, hoặc vì <rủi ro>>
- Không gồm: <phần ngoài phạm vi lớn nhất>
- Đội đề xuất thêm (chỉ làm khi anh/chị chọn): <… hoặc không có>

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
<!-- Mỗi tiêu chí phục vụ yêu cầu: cột "Từ" trích lời yêu cầu, dòng tài liệu nguồn hoặc câu trả lời. Trần: S 5, M 12, L 24. -->
| Mã | Tiêu chí (đo được) | Từ | Cách kiểm |
|---|---|---|---|
| AC-1 | <...> | "<lời yêu cầu>" | <lệnh hoặc bước có đầu ra> |

## Assumptions decided by the team
- <giả định> — vì <lý do>; sai thì <cách sửa>

## Definition of Done
- [ ] Mọi AC đạt, đầu ra được dán trong acceptance.md
- [ ] Đã chạy thử như người yêu cầu: tính năng đang bật và luồng chính chạy trên bản đang chạy (verify: Try it)
- [ ] As-Built viết xong (asbuilt.md) — sau G4, `/team:asbuilt`
- [ ] README/tài liệu người dùng cập nhật nếu hành vi đổi — sau G4, `/team:asbuilt`
- [ ] Mục CHANGELOG — sau G4, `/team:asbuilt`
- [ ] CI xanh

## Amendment <n> (<YYYY-MM-DD>)
<chỉ khi --amend, ngay trong file này (không bao giờ tách file addendum): thay đổi gì; tiêu chí đánh dấu [changed]>
