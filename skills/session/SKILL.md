---
name: session
description: Dùng khi bắt đầu, lưu hoặc nạp lại một phiên làm việc dài: chọn kênh, model theo vai, ngân sách và điểm nén ngữ cảnh.
argument-hint: "[plan|save|load] [<ID>]"
disable-model-invocation: true
allowed-tools: Bash(python3 *) Bash(cat *) Bash(jq *) Bash(ls *)
---

## Mục đích
Lập kế hoạch phiên và giữ bàn giao để phiên sau chạy tiếp đúng chỗ.

## Đầu vào
- `$ARGUMENTS`: `plan` (mặc định), `save` hoặc `load`, kèm mã feature.
- `.team/config.json` (`models`, `limits.feature_budget_usd`, `limits.context_warn_pct`, `memory.handoff_max_lines`).

## Điều kiện trước
Feature có `intake.md`. Kiểm: `python3 "$(cat .team/plugin_root)/scripts/team.py" status`.

## Các bước
1. `plan`:
   1. Chọn kênh: tương tác (cần hỏi người, cổng bật) hay headless (`decide`, mọi cổng còn lại đã duyệt). Headless sửa file thì không `--bare`.
   2. Liệt kê giai đoạn còn lại và vai, model của từng vai (`jq .models .team/config.json`). Không đổi model giữa phiên.
   3. Ngân sách: `feature_budget_usd` chia theo giai đoạn; headless → `--max-turns`, `--max-budget-usd`.
   4. Điểm nén chủ động: cuối mỗi giai đoạn; cảnh báo khi vượt `context_warn_pct`.
   5. Một feature mỗi phiên.
2. `save`: viết `.team/session/<id>.md` ≤ `handoff_max_lines` dòng, chỉ điều CHƯA có trong artifact (quyết định dở, câu hỏi chờ, lệnh tiếp).
3. `load`: Read `.team/session/` mới nhất + `team.py status`; tóm tắt 5 dòng.
4. Ghi journal một dòng.

## Đầu ra
- `plan`: `.team/session/plan.md`.
- `save`: `.team/session/<id>.md`.

## Tiêu chí xong
- File có, đúng trần dòng (`wc -l` dán).
- `plan.md` có kênh, model từng vai, ngân sách, điểm nén.

## Dấu hiệu sai
- "Chép lại cả artifact cho chắc" → chỉ phần khác.
- "Đổi sang model mạnh giữa chừng" → không đổi giữa phiên.
- "Gộp hai feature một phiên" → tách phiên.

## Lệnh tiếp theo
In lệnh kế từ `team.py next`, hoặc lệnh `claude -p …` đầy đủ nếu chọn headless.
