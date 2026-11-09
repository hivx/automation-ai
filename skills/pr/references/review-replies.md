# Trả lời bình luận review

## Bảng phân loại (lập trước khi tạo task nào)
| # | Bình luận (tóm tắt) | Kiểm với | Loại | Căn cứ | Việc |
|---|---|---|---|---|---|
| 1 | Hàm `to_csv` không escape dấu phẩy | code `report.py:12`, AC-1 | đồng ý | STD-ERR-2 | task T5 |
| 2 | "Nên thêm endpoint metrics đầy đủ" | Grep: không nơi nào dùng | không đồng ý | STD-DESIGN-5, spec non-goal | trả lời |
| 3 | "Chỗ này lạ" | — | cần làm rõ | — | hỏi lại |

## Mẫu trả lời
- Đồng ý, đã sửa: `Đã sửa ở a1b2c3d: escape dấu phẩy và ngoặc kép trong tên (STD-ERR-2); test tests/test_report.py::test_csv_quotes.`
- Không đồng ý: `Chưa đổi: spec FEAT-012 ghi metrics là non-goal và không có chỗ nào dùng (đã tìm "metrics" trong src/). Theo STD-DESIGN-5 đội không thêm phần chưa được yêu cầu. Nếu cần, mở intake mới.`
- Cần làm rõ: `"Chỗ này lạ" là về thứ tự cột hay về định dạng số? Đội chờ trả lời trước khi sửa các bình luận khác vì có thể liên quan.`
- Đã phản bác sai: `Tôi nhầm ở trên: trường hợp tên rỗng có xảy ra (test mới đỏ). Đã sửa ở d4e5f6a.`

## Không dùng
- "Bạn hoàn toàn đúng!", "Cảm ơn góp ý tuyệt vời" — không có thông tin.
- Đánh dấu resolved hàng loạt mà không trả lời.
- Hứa sửa mà không có task.
