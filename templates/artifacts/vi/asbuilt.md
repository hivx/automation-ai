Feature: <ID>
Stage: asbuilt
Author-agent: writer
Date: <YYYY-MM-DD>
Approved-by:
<!-- Cổng: người duyệt điền dòng trên `Approved-by: <tên> <YYYY-MM-DD>`. Không có cổng thì để trống. -->

<!-- G5: người điền `Approved-by-prod: <tên> <YYYY-MM-DD>` lên đầu file trước khi lên prod. -->
# As-Built <ID>

## Differences from design
| Mục thiết kế | Thực tế | file:line | Lý do |
|---|---|---|---|
| <...> | đúng thiết kế / khác: <...> | | |

## Release notes (cho người dùng)
- Đổi gì: <...>
- Ai bị ảnh hưởng: <...>
- Cần làm gì: <...>

## CHANGELOG
<mục đã thêm dưới [Unreleased]>

## CLAUDE.md
<CLAUDE.md: +<a> −<d> dòng (<các mục>), mỗi dòng một nguồn (review-NN / defects / hunk diff) — hoặc: CLAUDE.md: unchanged (check passed)>
- `check-claude-md.py`: <dòng tổng kết>

## Nợ sau G4
| Mục DoD qa ghi chủ | Đã làm | Kiểm lại (lệnh → kết quả) |
|---|---|---|
| <CHANGELOG / README / tài liệu> | <file> | <grep … → khớp> hoặc "để /team:release kiểm" |

## Rollback
<!-- /team:release viết trước lần deploy đầu: điều kiện kích hoạt, lệnh (từ docs/team/ci.md), phần dữ liệu, thời gian dự kiến -->

<!-- devops thêm dòng sau khi lên prod thành công: Released: <tag> <YYYY-MM-DD> -->
