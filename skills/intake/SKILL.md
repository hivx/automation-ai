---
name: intake
description: Dùng khi người giao một yêu cầu thô, một số issue, một lỗi hay hotfix cho đội.
argument-hint: "\"<yêu cầu>\" | #<issue> [--type bug|hotfix|change] [--size S|M|L] [--decide]"
disable-model-invocation: true
allowed-tools: Bash(python3 *) Bash(cat *) Bash(ls *) Bash(gh issue view *)
---

## Mục đích
Nhận yêu cầu, gán mã, chọn playbook, cỡ và chế độ.

## Đầu vào
`$ARGUMENTS`: văn bản hoặc `#<số issue>` kèm cờ. `<kit>` = nội dung `.team/plugin_root`.

## Điều kiện trước
`.team/config.json` có. Kiểm: `python3 "$(cat .team/plugin_root)/scripts/team.py" status`.

## Các bước
1. `#<số>` và `tracker` = github → `gh issue view`.
2. Mã kế tiếp `FEAT-NNN` / `BUG-NNN` / `CHG-NNN` (`ls docs/team/features/`).
3. Playbook theo `<kit>/workflows/README.md`: loại việc trước, rồi cỡ; `--size` thắng.
4. Chế độ: `--decide` > `default_mode`.
5. Cần skill tạm cho chính bước phân tích → `/team:make-skill` ngay; không → ghi để plan.
6. Viết `docs/team/features/<ID>/intake.md` theo `<kit>/templates/artifacts/intake.md`.
7. Journal `docs/team/journal/<ID>.md` theo `<kit>/templates/artifacts/journal-entry.md`: `- <date> intake → team-leader | <playbook>, <cỡ>, <chế độ> | intake.md | — | good | <lý do>`.

## Đầu ra
`docs/team/features/<ID>/intake.md`, `docs/team/journal/<ID>.md`, `.team/current.json` {stage: intake}.

## Tiêu chí xong
`intake.md` có mã, playbook, cỡ, chế độ, lý do; dán đầu ra status.

## Dấu hiệu sai
- "Rõ rồi, khỏi định cỡ" → luôn định cỡ.
- "Bỏ journal" → ghi trước.
- "Bắt tay làm luôn" → chỉ intake.

## Lệnh tiếp theo
In bước 1 của playbook, ví dụ `/team:analyze <ID>`.
