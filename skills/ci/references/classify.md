# Phân loại CI đỏ (STD-CI-4)

| Loại | Dấu hiệu trong log | Bằng chứng cần trước khi kết luận | Hành động | Không làm |
|---|---|---|---|---|
| code | assertion sai, exception trong code dự án, lỗi kiểu/lint ở file vừa đổi | chạy khe `cmd.*` tương ứng trên cùng SHA tại chỗ → cùng lỗi | trả team-leader: `/team:intake --type bug` | sửa code, sửa test |
| test chập chờn | lỗi thời gian chờ, thứ tự, cổng mạng bận; cùng test lúc đỏ lúc xanh | cùng SHA: đỏ → chạy lại một lần (`gh run rerun <id> --failed`) → xanh | dòng `debt.md` (tên test, hai run-id, số lần); báo team-leader | tắt test, thêm retry vào test, chạy lại nhiều lần |
| môi trường | runner hết đĩa, hạn mức API, DNS, dịch vụ ngoài sập | diff không đổi gì liên quan; lỗi nằm ngoài bước của dự án | chờ/chạy lại một lần; lặp lại → đổi runner/bước chuẩn bị trên PR riêng | đổi code |
| cấu hình | YAML sai, action sai bản, `ci.setup` lệch profile, biến môi trường thiếu | đọc file workflow + profile; chỉ ra dòng sai | sửa workflow trên `team/ci-<slug>` | nới bước kiểm |
| phụ thuộc | không phân giải được gói, lockfile lệch manifest, bản thượng nguồn mới hỏng | so lockfile với manifest; changelog thượng nguồn | `cmd.install` trên nhánh riêng; lỗi do bản mới → playbook dependency-upgrade | sửa tay lockfile |

## Thứ tự đọc log
1. Job nào đỏ đầu tiên (`--json jobs`), bước nào.
2. Dòng lỗi đầu tiên trong bước đó (bỏ qua các dòng "exit code 1", "Process completed" ở cuối).
3. SHA và nhánh; có trùng một lần đỏ trước trên nhánh nền không (`gh run list --branch <base> --limit 5`).

## Lỗi đã có trên nhánh nền
Nhánh nền cũng đỏ cùng lỗi → không phải do PR. Ghi rõ "đã đỏ trên `<base>` từ run <id>"; loại vẫn là một trong năm loại trên; PR đang xét không bị chặn vì lỗi này nhưng người phải được báo.
