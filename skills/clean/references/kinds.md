# Từng loại dọn dẹp: bằng chứng và bẫy

| Loại | Bằng chứng bắt buộc | Bẫy thường gặp |
|---|---|---|
| dead-code | grep tên + dạng chuỗi (đăng ký động, reflection), grep điểm vào trong `structure.config`, danh sách export — tất cả rỗng; một dòng "tồn tại vì" | code chỉ được gọi qua cấu hình hay plugin; API công khai (phải deprecate) |
| naming | danh sách tên cũ → mới; grep tên cũ sau đổi = 0 (trừ CHANGELOG); một họ định danh mỗi commit | đổi tên trong chuỗi hiển thị cho người dùng (đó là hành vi); tên trong dữ liệu đã lưu |
| structure | `git diff -M --stat`: rename ≥ 90% giống; import cập nhật; thư mục mới dưới `allowed_new_file_roots` | sửa logic "tiện tay" trong file vừa chuyển |
| deps | grep import = 0; manifest đổi; đầu ra `cmd.install`; `cmd.build` + `cmd.test` sau | gói chỉ dùng lúc build/test; gói kéo theo plugin; manifest trong `protected_paths` |
| tests | code đích đã mất, hoặc assertion trùng test khác (dẫn cả hai `file::tên`) | test "trông" mồ côi nhưng phủ đường lỗi duy nhất |
| simplify | mỗi phép: `cmd.test_one` trên test phủ trước khi sang phép sau | bỏ xử lý lỗi, gộp hai nhánh có khác biệt nhỏ, đổi thứ tự có tác dụng phụ |
| deprecate | cái thay thế chạy được (test); dấu deprecate có cái thay + hạn gỡ; grep chỗ dùng trước khi gỡ hẳn | gỡ ngay khi còn chỗ dùng; deprecate schema (sang data-migration) |
| observe | 2–4 câu hỏi vận hành; log có cấu trúc, nhãn hữu hạn, không dữ liệu nhạy cảm; test giữ nguyên | ghi PII, nhãn vô hạn (id người dùng làm nhãn metric), log trong vòng lặp nóng |

## Test đặc tả (characterization)
Khi vùng cần dọn không có test phủ và design cho phép:
1. Commit riêng, TRƯỚC đường nền: test ghi lại hành vi HIỆN TẠI (kể cả hành vi lạ) — không sửa code.
2. Chạy test mới: phải xanh trên code cũ.
3. Đường nền (bước 3) chạy sau commit này.
Không viết test đặc tả trong cùng commit với thay đổi.

## Khi nào dừng
- `cmd.test` sau khác trước (số, tên, kết quả).
- Phạm vi vượt 500 dòng.
- Đích là API công khai hoặc dữ liệu đã lưu.
- Cần đổi `protected_paths` (manifest, lockfile, cấu hình prod).
- Hàng rào Chesterton không giải thích được cho một đoạn quan trọng.
