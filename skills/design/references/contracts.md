# Hợp đồng, idempotency, migration, test plan

## Hợp đồng của một điểm vào
| Phần | Ghi gì |
|---|---|
| Đầu vào | trường, kiểu, bắt buộc/tùy chọn, giới hạn; nơi kiểm (biên) |
| Đầu ra | trường, kiểu, thứ tự (nếu có ý nghĩa), giá trị mặc định |
| Lỗi | mã + điều kiện + thông điệp, theo kiểu lỗi chung của dự án |
| Phiên bản | giữ nguyên / thêm (tương thích) / mới (phá vỡ) + hướng dẫn di trú |

Hành vi quan sát được (mã lỗi, nội dung thông điệp, thứ tự kết quả, mặc định) là hợp đồng dù không ai ghi — có người sẽ phụ thuộc vào nó. Đổi chúng = đổi hợp đồng.

Thứ tự ưu tiên khi cần đổi: thêm trường tùy chọn → thêm điểm vào mới → phiên bản mới. Không bao giờ đổi nghĩa một trường đang có.

## Idempotency (gọi ra ngoài hoặc nhận lời gọi có retry)
1. Khóa suy từ ý định nghiệp vụ (ví dụ mã đơn + hành động), không sinh mới cho mỗi lần thử.
2. Giành quyền nguyên tử: ràng buộc duy nhất trên khóa; không "đọc xem có chưa rồi chèn".
3. Cùng khóa, khác nội dung → lỗi rõ ràng (không lặng lẽ trả kết quả cũ).
4. Bản trùng đang chạy: chọn một — từ chối, chờ, hay trả "đang xử lý".
5. Giữ khóa lâu hơn đường retry dài nhất của bên gọi.
6. Kết cục ba trạng thái: thành công / thất bại / không rõ (timeout) — "không rõ" phải có cách đối soát.

## Migration theo lô
| Mục | Ghi gì |
|---|---|
| Số liệu dự kiến | số hàng trước, số hàng sau, cách đếm |
| Lên | các bước; bảng lớn → lô N hàng, có điểm dừng an toàn |
| Xuống | các bước đảo; dữ liệu mất khi xuống thì nêu rõ và cần người duyệt |
| Đối soát | truy vấn so số lượng/tổng sau mỗi chiều |
| Chuyển đổi | thứ tự deploy code và migration (mở rộng → chuyển → thu hẹp khi đổi schema đang dùng) |
| Rollback | điều kiện kích hoạt, tiêu chí thành công |

## Mẫu dòng test plan
| Tiêu chí | Test | Loại | Đường lỗi/biên |
|---|---|---|---|
| AC-1 xuất CSV có tiêu đề | tests/test_export.py::test_header_row | unit | — |
| AC-2 tồn kho rỗng | tests/test_export.py::test_empty_inventory | unit | biên: 0 dòng |
| AC-3 tên có dấu phẩy | tests/test_export.py::test_quote_comma | unit | lỗi: ký tự đặc biệt |
| NFR-1 10.000 dòng < 2 s | tests/perf/test_export_perf.py::test_10k | integration | biên |

Cột Test là `file::tên` theo `naming.test_file`; lệnh chạy là `cmd.test_one` với `{file}`, không ghi lệnh stack.
