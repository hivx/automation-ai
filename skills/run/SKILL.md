---
name: run
description: Dùng khi người muốn đội chạy tiếp feature tới giai đoạn hoặc cổng kế tiếp, hoặc chạy liên tục tới khi bị chặn.
argument-hint: "[<ID>] [--until-blocked]"
disable-model-invocation: true
allowed-tools: Bash(python3 *) Bash(cat *)
---

# Chạy tiếp feature

## Tổng quan
Chạy giai đoạn kế tiếp của feature theo playbook và cổng. `$ARGUMENTS`: mã feature (mặc định từ `.team/current.json`), `--until-blocked` để lặp tới khi bị chặn. Không bao giờ vượt cổng.

## Quy trình
1. Kiểm `docs/team/features/<ID>/intake.md` có; không có → in `/team:intake`, dừng.
2. Bash: `python3 "<kit>/scripts/team.py" next <ID>` và `status <ID>` (`<kit>` = đường dẫn đọc từ `.team/plugin_root`, gõ thẳng).
3. Cổng: CHỈ theo đầu ra `team.py` (đã tính theo cỡ: S bỏ G1, G3; refactor/data-migration bật G2b). Không tự đọc `gates` trong config. `WAITING_FOR_*` → dừng, in việc người cần làm.
4. Lệnh kế là skill chỉ người gọi được (`/team:release`, `/team:ci`) → in lệnh, dừng.
5. Ghi journal một câu lý do (Write), rồi gọi skill kế (Skill). Cỡ S vẫn đi qua `/team:build` để có reviewer.
6. Sau skill: chạy lại `team.py status <ID>`; giai đoạn không đổi → dừng và báo (không chạy lại cùng skill).
7. Ghi số liệu: `bash "<kit>/scripts/log-run.sh" --skill <skill> --result <kết quả>`.
8. `--until-blocked` → về bước 2; không → dừng.

## Lý do tự bào chữa thường gặp
| Ý nghĩ | Làm đúng |
|---|---|
| "Cổng chắc sẽ được duyệt" | Dừng ở cổng. |
| "Config bật G1 nên phải chờ" | Tin `team.py`; cỡ S không có G1. |
| "Cỡ S, gọi thẳng dev cho nhanh" | Vẫn `/team:build` (dev + reviewer). |
| "Status chưa đổi, chạy lại build" | Dừng và báo; artifact có thể sai định dạng. |
| "Feature khác chờ cổng nên dừng hết" | Cổng chỉ chặn feature của nó. |
| "Bỏ log-run cho nhanh" | Số liệu là đầu vào của retro. |

## Kiểm chứng
- Dán đầu ra `team.py status <ID>` sau mỗi giai đoạn.
- Mỗi skill đã gọi có một dòng journal.
- Lần dừng nêu: lý do, việc nào, ai làm gì, lệnh chạy tiếp.
