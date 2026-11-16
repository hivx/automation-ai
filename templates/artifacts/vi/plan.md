Feature: <ID>
Stage: plan
Author-agent: tech-lead
Date: <YYYY-MM-DD>
Approved-by:
<!-- Cổng: người duyệt điền dòng trên `Approved-by: <tên> <YYYY-MM-DD>`. Không có cổng thì để trống. -->

# Plan <ID>

- Nhánh feature: `team/<ID>` từ `<base_branch>`
- Số task: <n>; song song tối đa: <limits.max_parallel_dev>

## Design (cỡ M, không có design.md; tối đa 40 dòng)
- Hợp đồng và thay đổi schema: <endpoint / field / migration, đúng tên>
- Touchpoints: <file — đổi gì>
- Test cho từng tiêu chí: <AC-n → file test>

## Thứ tự
1. <nhóm task, lý do thứ tự>

## Nhóm song song
- <T2, T3> (không chung file)

## Rủi ro
| Rủi ro | Dấu hiệu | Cách xử lý |
|---|---|---|

## Walking skeleton (cỡ L)
<T1 chạy đầu-cuối gồm những gì>
