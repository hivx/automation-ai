# Ai đang chờ cái gì — đọc `/team:status`

`/team:status` tính vị trí từ artifact trong `docs/team/features/<ID>/`, không đọc con trỏ lưu sẵn. Kết quả trả lời ba điều: feature ở giai đoạn nào, ai đang giữ bóng, lệnh tiếp theo.

## Giai đoạn được tính thế nào
| Có artifact | Trạng thái |
|---|---|
| `intake.md` | intaken |
| `spec.md` có DoD | specified |
| `research.md` | researched |
| `arch-impact.md` hoặc tham chiếu `architecture.md` | architected |
| `design.md` | designed |
| `plan.md` + `tasks.md` | planned |
| mọi task đã tick | built |
| `acceptance.md` verdict accepted | verified |
| `asbuilt.md` + dấu Released | released |

Cổng bật mà chưa duyệt chặn mọi trạng thái sau nó.

## Ai đang chờ
| Status báo | Ai phải làm | Làm gì |
|---|---|---|
| `WAITING_FOR_APPROVAL Gn` | Người | Đọc artifact được nêu, thêm `Approved-by:` (hoặc `@claude approve Gn`), rồi `/team:run` |
| `WAITING_FOR_ANSWER` | Người | Trả lời câu hỏi (trong phiên hoặc bình luận issue), rồi `/team:run` |
| `BLOCKED` | Người hoặc tech-lead | Đọc lý do; sửa nguyên nhân; chạy lệnh tiếp tục được in ra |
| `DESIGN_CONFLICT` / `design-defect` | designer/architect, người duyệt lại | Sửa `design.md`, duyệt lại cổng liên quan |
| `IN_PROGRESS <agent>` | Đội | Chờ, hoặc `/team:session` để xem bàn giao |
| `READY` | Người | Gõ lệnh tiếp theo được in ra |

Mỗi lần dừng luôn có: lý do, việc nào, ai làm gì, lệnh để chạy tiếp. Thiếu một trong bốn thì báo bằng `/team:feedback`.
