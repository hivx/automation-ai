# Quy tắc viết As-Built

## Đọc diff theo mục thiết kế
1. Lấy danh sách file từ `diff.patch`: Grep `^diff --git a/` → mỗi dòng một file.
2. Với từng touchpoint trong `design.md` mục 7: file có trong diff không?
   - Có, và loại thay đổi khớp ("mới"/"sửa") → đọc các hunk của file đó.
   - Không có → dòng "khác: không chạm (thiết kế dự kiến sửa)"; tìm lý do trong `tasks.md`.
3. File có trong diff mà không có trong touchpoints → dòng riêng "ngoài touchpoints", dẫn `review-NN.md` đã chấp nhận (reviewer chấm mục 2 của checklist).
4. Với các mục 2–6 của thiết kế (dữ liệu, API, luồng, quyền, migration): tìm hunk chứng minh từng điểm (tên trường, mã lỗi, kiểm quyền, file migration). Ghi `file:line` của dòng `+` đầu tiên trong hunk.

## Mẫu dòng bảng
| Mục thiết kế | Thực tế | file:line | Lý do |
|---|---|---|---|
| 3. API — `POST /otp/verify` trả 409 khi hết hạn | khác: trả 422 | src/auth/otp.py:41 | review-02: STD-ERR-3, dùng mã lỗi chung của dự án |
| 6. Migration 0007 | đúng thiết kế | migrations/0007_otp.py:1 | — |
| (ngoài touchpoints) src/auth/__init__.py | sửa export | src/auth/__init__.py:3 | review-01 chấp nhận (cần cho import) |

## Câu có nguồn
- Mỗi câu release notes: kết thúc bằng nguồn trong ngoặc khi viết nháp (`(AC-2)`, `(src/x.py)`); bản cuối cho người dùng có thể bỏ ngoặc nhưng nguồn phải còn trong As-Built.
- Giữ nguyên tên, số, đơn vị, lệnh, đường dẫn, điều kiện từ nguồn; không hứa mạnh hơn bằng chứng ("luôn", "mọi trường hợp" chỉ khi acceptance có biên/đường lỗi tương ứng).
- Không có nguồn → không viết; nếu cần cho người đọc thì ghi vào "Cần người đọc lại".

## Nhóm CHANGELOG (Keep a Changelog)
| Nhóm | Khi nào |
|---|---|
| Added | tính năng/lệnh/trường mới người dùng thấy |
| Changed | hành vi có sẵn đổi (kể cả phá vỡ — ghi rõ "phá vỡ" và trỏ di trú) |
| Deprecated | còn dùng được, sẽ gỡ; ghi hạn và cách thay |
| Removed | đã gỡ |
| Fixed | sửa lỗi (bug-fix, hotfix) |
| Security | sửa lỗ hổng; không mô tả cách khai thác |

Mỗi dòng: một câu, thì hiện tại, kết thúc `(<ID>)`. Không dòng nào cho thay đổi nội bộ không ai thấy (refactor thuần → nhóm Changed chỉ khi hành vi build/cài đặt đổi; còn lại bỏ).

## Người đọc
| `--audience` | Viết gì | Tránh |
|---|---|---|
| user | việc họ làm được, thay đổi họ thấy, việc họ phải làm | tên file, task, STD |
| dev | hợp đồng API, cấu hình, migration, cách nâng cấp | lời quảng cáo |
| client | lợi ích, phạm vi, điều kiện, mốc | chi tiết nội bộ; cần người duyệt nội dung → "Cần người đọc lại" |
