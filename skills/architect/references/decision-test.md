# Phép thử ngưỡng kiến trúc

Một quyết định được chốt ở tầng kiến trúc (thành ADR) khi đủ ba điều:
1. **Có thể lệch:** hai phần được làm độc lập (hai task, hai dev, hai feature) có thể chọn khác nhau.
2. **Không hiển nhiên:** người làm giỏi không tự chọn giống nhau nếu không được nói.
3. **Đánh đổi thật:** mỗi phương án có cái mất đo được (hiệu năng, chi phí, độ phức tạp, khả năng đảo ngược).

Thiếu một điều → không phải ADR. Ghi vào `## Để designer quyết` với lý do ("chỉ một module dùng", "dự án đã có quy ước").

## Ví dụ
| Ứng viên | 1 | 2 | 3 | Kết luận |
|---|---|---|---|---|
| Ai được ghi bảng `invoices` | có (billing và notify) | không | có | ADR: chỉ billing ghi; notify nghe event |
| Định dạng lỗi API | có | có nếu dự án chưa có | thấp | dự án đã có `{code, message}` → theo quy ước, không ADR |
| Hàng đợi hay gọi đồng bộ khi gửi email | có | có | có (độ trễ vs độ phức tạp) | ADR |
| Tên trường `created_at` hay `createdAt` | có | không (theo `naming.*`) | không | để designer |
| Cache Redis "cho nhanh sau này" | — | — | — | không có NFR → bỏ (STD-DESIGN-5) |

## Ràng buộc kiểm được
Mỗi ADR có ít nhất một dòng reviewer kiểm được trên diff:
- "Chỉ `src/billing/**` ghi bảng invoices" → grep câu lệnh ghi trong module khác.
- "Mọi lời gọi ra ngoài qua `src/clients/` và có timeout" → grep import HTTP client ngoài thư mục đó.
- "Không module nào dưới `src/domain/` import `src/api/`" → chiều phụ thuộc.

Ràng buộc mơ hồ ("code phải sạch", "dễ mở rộng") không phải ràng buộc.

## Chiều cần quét
| Chiều | Câu hỏi |
|---|---|
| Môi trường và deploy | Mấy môi trường? Đơn vị deploy nào? Lệnh nằm ở `deploy.*`/`docs/team/ci.md`? |
| Chủ sở hữu dữ liệu | Mỗi thực thể một module chủ? Ai chỉ đọc? |
| Đường ghi trạng thái | Ghi đồng bộ, qua event, hay job? Thứ tự và trùng lặp? |
| Lỗi, log, cấu hình | Một kiểu lỗi? Log có ngữ cảnh, không dữ liệu nhạy cảm? Cấu hình đọc ở đâu? |
| Xác thực, phân quyền | Kiểm ở đâu (phía server)? Ai cấp quyền? |
| Tích hợp ngoài | Timeout, retry, idempotency (từ research `--integration`) |

Mỗi chiều kết thúc bằng một trong: **quyết** (dẫn ADR), **để designer** (lý do), **câu hỏi mở** (vào `questions.md` hoặc `## Assumptions decided by the team` ở chế độ decide).
