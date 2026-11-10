Feature: <ID>
Stage: verify
Author-agent: qa
Date: <YYYY-MM-DD>
Approved-by:
<!-- Cổng: người duyệt điền dòng trên `Approved-by: <tên> <YYYY-MM-DD>`. Không có cổng thì để trống. -->

# Acceptance <ID>

Verdict: <accepted | rework | design-defect>

## Tiêu chí
| criterion | command | output excerpt | verdict |
|---|---|---|---|
| AC-1 | `<lệnh>` | `<đầu ra thật>` | đạt / không |

## Kiểm chung
- `cmd.test`: <đầu ra>
- `cmd.lint`: <đầu ra>
- `cmd.typecheck`: <đầu ra>
- Dấu skip mới trong diff: <không có | danh sách>
- Migration lên/xuống: <đầu ra | không áp dụng>

## Acceptance checklist (6)
<1–6: đạt / trượt (mã STD)>

## DoD
- [ ] As-Built  - [ ] README/tài liệu  - [ ] CHANGELOG
