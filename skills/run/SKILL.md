---
name: run
description: Dùng khi người muốn đội chạy tiếp feature tới giai đoạn hoặc cổng kế tiếp, hoặc chạy liên tục tới khi bị chặn.
argument-hint: "[<ID>] [--until-blocked]"
disable-model-invocation: true
allowed-tools: Bash(python3 *) Bash(cat *)
---

## Mục đích
Chạy giai đoạn kế tiếp của feature theo playbook.

## Đầu vào
`$ARGUMENTS`: mã feature (mặc định từ `.team/current.json`), `--until-blocked`.

## Điều kiện trước
`intake.md` của feature có.

## Các bước
1. `python3 "$(cat .team/plugin_root)/scripts/team.py" next <ID>` (Bash) → giai đoạn kế và cổng.
2. Cổng: CHỈ theo đầu ra `team.py` (đã tính cổng theo cỡ: S bỏ G1, G3); không tự đọc `gates` trong config. `WAITING_FOR_APPROVAL` → dừng, in cổng.
3. Bước kế là `/team:release` hoặc skill chỉ người gọi → in lệnh, dừng.
4. Ghi lý do vào journal, gọi skill kế (Skill).
5. Kiểm artifact mới bằng `team.py status`; ghi số liệu: `bash "<kit>/scripts/log-run.sh" --skill <skill> --result <kết quả>`.
6. `--until-blocked` → lặp bước 1; không → dừng.

## Đầu ra
Artifact của giai đoạn vừa chạy; journal.

## Tiêu chí xong
Dán đầu ra `team.py status` sau khi chạy.

## Dấu hiệu sai
- "Cổng chắc sẽ được duyệt" → dừng.
- "Gọi thêm giai đoạn cho nhanh" → đúng playbook.
- "Artifact thiếu cũng được" → dừng, báo.

## Lệnh tiếp theo
In lệnh từ `team.py next` hoặc cổng chờ duyệt.
