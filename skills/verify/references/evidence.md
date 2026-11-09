# Bằng chứng nghiệm thu

## Khẳng định cần gì
| Khẳng định | Cần | Không đủ |
|---|---|---|
| "Test qua" | Đầu ra `cmd.test` trên commit đã ghi, 0 lỗi, mã thoát 0 | Lần chạy trước, CI cũ, lời dev |
| "Build ổn" | `cmd.build` mã thoát 0 | Lint qua |
| "Lỗi đã sửa" | Test tái hiện triệu chứng gốc: đỏ trước sửa (do dev dán), xanh bây giờ | Test mới chỉ xanh |
| "Tiêu chí AC-n đạt" | Lệnh trong cột "cách kiểm" + đầu ra khớp mong đợi | Đọc code thấy đúng |
| "Migration an toàn" | Lên → xuống → lên đều mã thoát 0, số lượng khớp | Chỉ chiều lên |
| "Tài liệu đúng" | Lệnh/bước trong README chạy được, khớp hành vi | README có nhắc tới |

## Dòng bằng chứng
`AC-2 | <cmd.test_one tests/auth/test_otp.py> | exit 1 | AssertionError: 200 != 401 | tests/auth/test_otp.py::test_expired | trượt`

## Phân loại lỗi trước khi kết luận
| Loại | Dấu hiệu | Phán quyết |
|---|---|---|
| Code sai | Test đúng tiêu chí, code trả sai | rework (task chủ) |
| Test sai | Test kiểm điều khác tiêu chí, hoặc không bao giờ trượt | rework (STD-TEST-5) |
| Chập chờn | Cùng commit, kết quả khác nhau giữa 3 lần | rework + `debt.md` (STD-TEST-7) |
| Môi trường | Lệnh không chạy được (thiếu dịch vụ, quyền) | BLOCKED, không kết luận |
| Thiết kế | Code khớp design, design không thỏa tiêu chí | design-defect |

## Acceptance checklist (6) — trích nguyên văn từ handbook/STD.md khi chấm
Ghi từng mục: đạt / trượt + mã STD.
