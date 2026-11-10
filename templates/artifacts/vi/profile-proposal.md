Feature: <ID>
Stage: takeover
Author-agent: team-leader
Date: <YYYY-MM-DD>
Approved-by:
<!-- Cổng: người duyệt điền dòng trên `Approved-by: <tên> <YYYY-MM-DD>`. Không có cổng thì để trống. -->

# Profile đề xuất

Luật: chỉ dùng tên khe có trong `profile.schema.json` (đúng như cột slot dưới đây); `{file}` là chỗ thay DUY NHẤT trong lệnh (đường dẫn file tương đối từ gốc repo); khe không áp dụng để rỗng. Kiểm lệnh `cmd.test_one` bằng cách chạy nó với một file test có thật.

| slot | value | evidence | confidence |
|---|---|---|---|
| stack | | <file manifest> | cao / tb / thấp |
| cmd.install | | | |
| cmd.build | | | |
| cmd.test | | | |
| cmd.test_one | <lệnh có {file}> | <đã chạy với tests/…: đầu ra> | |
| cmd.lint | | | |
| cmd.typecheck | | | |
| cmd.format | <lệnh có {file} hoặc rỗng> | | |
| structure.src / structure.tests | | | |
| naming.test_file | | | |
| structure.allowed_new_file_roots | | <thư mục gốc từ detect-stack> | |
| protected_paths | | <secret, lockfile, vendored, prod config> | |

## Khe chưa chắc (cần người xác nhận)
- <...>

## Đã quét / Chưa quét / Độ tin cậy
<...>
