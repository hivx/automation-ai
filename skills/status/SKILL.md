---
name: status
description: Dùng khi người hỏi feature đang ở đâu, ai đang chờ ai, hay việc gì đang bị chặn.
argument-hint: "[<ID>]"
allowed-tools: Bash(python3 *) Bash(cat *)
---

## Mục đích
In trạng thái tính từ artifact và ai đang chờ.

## Đầu vào
`$ARGUMENTS`: mã feature; rỗng = mọi feature.

## Điều kiện trước
`docs/team/` có. Không có → in `/team:takeover` hoặc `/team:onboard`.

## Các bước
1. `python3 "$(cat .team/plugin_root)/scripts/team.py" status $ARGUMENTS` (Bash).
2. In nguyên đầu ra.
3. Mỗi dòng `WAITING_FOR_APPROVAL`, `WAITING_FOR_ANSWER`, `BLOCKED`: thêm dòng "Chờ người: <việc> — <file>".
4. Không suy diễn ngoài đầu ra script.

## Đầu ra
Chỉ in ra màn hình; không ghi file.

## Tiêu chí xong
Đầu ra script được dán nguyên văn.

## Dấu hiệu sai
- "Script lỗi, tôi tự đoán" → in lỗi, dừng.
- "Thêm nhận xét" → chỉ định dạng.
- "Đọc artifact để tóm tắt" → script làm.

## Lệnh tiếp theo
In lệnh `team.py` gợi ý, thường là `/team:run <ID>`.
