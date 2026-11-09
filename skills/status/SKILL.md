---
name: status
description: Dùng khi người hỏi feature đang ở đâu, ai đang chờ ai, hay việc gì đang bị chặn.
argument-hint: "[<ID>]"
allowed-tools: Bash(python3 *) Bash(cat *)
---

# Trạng thái đội

## Tổng quan
In trạng thái tính từ artifact (không con trỏ lưu sẵn) và ai đang chờ ai. `$ARGUMENTS`: mã feature; rỗng = mọi feature. Không ghi file.

## Quy trình
1. Kiểm `docs/team/` có. Không có → in: dự án có code → `/team:takeover`; repo rỗng → `/team:onboard --new`; dừng.
2. Chạy (Bash): `python3 "$(cat .team/plugin_root)/scripts/team.py" status $ARGUMENTS`.
3. In NGUYÊN đầu ra trong khối mã, kể cả cột "Cổng áp dụng".
4. Với mỗi dòng `WAITING_FOR_APPROVAL`, `WAITING_FOR_ANSWER`, `BLOCKED`, `REWORK`, `DESIGN_DEFECT`: một dòng "Chờ người: <việc> — <file>".
5. In lệnh tiếp theo đúng như cột "Tiếp theo" của script.
6. Script lỗi → in nguyên lỗi và `<kit>/scripts/team.py --help`; dừng. Không suy diễn.

## Lý do tự bào chữa thường gặp
| Ý nghĩ | Làm đúng |
|---|---|
| "Script lỗi, tôi tự đọc artifact rồi đoán" | In lỗi, dừng; trạng thái chỉ do script tính. |
| "Config bật G1 nên feature cỡ S đang chờ G1" | Tin cột "Cổng áp dụng"; script đã tính theo cỡ. |
| "Thêm nhận xét cho hữu ích" | Chỉ định dạng; nhận xét để `/team:retro`. |
| "Tóm tắt bảng cho gọn" | In nguyên; người cần đúng chữ để duyệt. |
| "Feature chờ G4 nên cả đội đứng" | Cổng chỉ chặn feature của nó. |
| "Không có feature, in bảng rỗng" | In lệnh bắt đầu `/team:intake "<yêu cầu>"`. |

## Kiểm chứng
- Đầu ra script được dán nguyên văn.
- Mỗi trạng thái chờ có đúng một dòng "Chờ người".
- Lệnh tiếp theo trùng cột "Tiếp theo".
