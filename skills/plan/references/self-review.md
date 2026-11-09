# Tự kiểm kế hoạch (5 điểm) và mẫu khối giao diện

## 5 điểm — làm trước khi trả
| # | Điểm | Cách kiểm | Trượt thì |
|---|---|---|---|
| 1 | Phủ spec | Mỗi `AC-n` trong spec.md xuất hiện trong ít nhất một task | Thêm task hoặc thêm tiêu chí vào task chủ |
| 2 | Không chữ mơ hồ | Tìm "TBD", "xử lý biên", "tùy", "v.v." trong plan/tasks | Thay bằng tên file, tên test, giá trị |
| 3 | Tên nhất quán | Tên hàm/trường/route ở mục `Trả:` của task trước trùng mục `Nhận:` của task sau | Sửa một chỗ, ghi vào Ràng buộc chung |
| 4 | Trọng tâm review | ≤ 5 đầu vào biên/chế độ lỗi có test | Thêm test vào task chủ |
| 5 | Tỉ lệ | plan.md + tasks.md ngắn hơn phần code dự kiến | Bỏ code dán sẵn, giữ quyết định |

## Mẫu một task đầy đủ
```
- [ ] T3 — Từ chối mã OTP hết hạn — files: src/auth/otp.py, tests/auth/test_otp.py — test: tests/auth/test_otp.py — depends: T2
  - Tiêu chí: AC-2 (mã quá 5 phút trả lỗi 401)
  - Nhận: `verify_code(user_id: str, code: str, now: datetime) -> bool` (từ T2)
  - Trả: `OtpExpired` (ngoại lệ mới, dùng ở T4)
  - Kỳ vọng: `cmd.test_one` với tests/auth/test_otp.py → test_expired đạt
```

## Bảng một-file-một-chủ (plan.md)
| File | Task chủ | Task khác chạm | Thứ tự |
|---|---|---|---|
| src/auth/otp.py | T2 | T3 | T2 → T3 |
