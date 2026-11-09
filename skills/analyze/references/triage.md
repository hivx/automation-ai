# Phân loại 7 mục — câu hỏi gợi ý

Mỗi mục: điền từ intake, README, glossary, Explore trước; chỉ thành câu hỏi khi hậu quả lớn hoặc không đảo ngược.

| Mục | Phải trả lời | Câu hỏi gợi ý | Dấu hiệu còn thiếu |
|---|---|---|---|
| Mục tiêu | Vì sao làm, giá trị cho ai, đo bằng gì | "Nếu không làm thì mất gì?" | Chỉ có giải pháp, không có vấn đề |
| Người dùng | Ai dùng, trong tình huống nào, bao nhiêu người | "Ai bấm nút này, lúc nào?" | "Người dùng" chung chung |
| Phạm vi trong/ngoài | Có gì, KHÔNG có gì (non-goals) | "Việc gần giống nào cố ý để ngoài?" | Không có dòng non-goal |
| Dữ liệu | Thực thể, trường, khối lượng, dữ liệu nhạy cảm, giữ bao lâu | "Có xóa/đổi dữ liệu đã có không?" | Không nói tới dữ liệu cũ |
| Giao diện / tích hợp | Màn hình, API, hệ thống ngoài, định dạng | "Ai/hệ thống nào gọi cái này?" | Định dạng vào/ra không rõ |
| NFR | Hiệu năng, bảo mật, khả dụng, truy cập, quy định | "Chậm đến đâu thì không chấp nhận?" | Tính từ không có số |
| Tiêu chí nghiệm thu | Mỗi hành vi một tiêu chí, lệnh/bước kiểm, đầu ra mong đợi | "Bạn sẽ kiểm bằng cách nào để chấp nhận?" | Tiêu chí không có cách kiểm |

## Đổi tính từ thành con số
| Tính từ | Câu viết lại | Cách kiểm |
|---|---|---|
| nhanh | p95 < N ms cho thao tác X với M bản ghi | lệnh đo trong test plan |
| an toàn | chỉ vai Y đọc được trường Z; thử với vai khác trả lỗi 403 | test truy cập |
| dễ dùng | hoàn thành việc X trong ≤ N bước | bước kiểm có ảnh chụp |
| đúng | đầu ra khớp mẫu `<file mẫu>` từng byte | so khớp trong test |

## Định dạng một câu hỏi (questions.md)
```
1. <câu hỏi> — vì sao cần: <phần việc sẽ đổi theo câu trả lời>
   - a) <lựa chọn> — hậu quả: <...>
   - b) <lựa chọn> — hậu quả: <...>
   - Khuyến nghị: b, vì <...>
   - Đã xem: <đường dẫn file/tài liệu không trả lời được>
```

## Bốn trường của một quyết định (decide / Assumptions)
`chọn: … | vì: … | phương án khác: … | sửa nếu sai: …`
