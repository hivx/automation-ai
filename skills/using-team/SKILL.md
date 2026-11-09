---
name: using-team
description: Dùng khi bắt đầu bất kỳ việc gì không tầm thường trong dự án có đội team, trước khi hành động hay hỏi lại: kiểm skill và playbook phù hợp.
---

# Dùng đúng skill trước khi tự làm

## Tổng quan
Đội làm theo skill `/team:*` và playbook, không theo trí nhớ. Nạp sẵn cho team-leader và tech-lead; **subagent khác không khám phá lại**, chỉ dùng skill được giao.

## Quy trình
1. Trước mọi việc không tầm thường — trước cả câu hỏi làm rõ và trước khi gọi Explore — xác định loại việc:
   yêu cầu thô → `/team:intake`; repo chưa có profile → `/team:takeover`; cần spec → `/team:analyze`; đổi spec đã duyệt → `/team:analyze --amend`; đã có spec/design → `/team:plan`; có task → `/team:build`; hỏi tiến độ → `/team:status`.
2. Liệt kê skill tạm trong `.claude/skills/` (xem `docs/team/skills-registry.md`). Thứ tự ưu tiên: lời người > skill quy trình của kit > skill tạm > hành vi mặc định.
3. Có playbook cho loại việc trong `<kit>/workflows/` (`<kit>` = nội dung `.team/plugin_root`) → theo chuỗi của nó; skill cho các bước chi tiết. Lệch nhau → theo skill, báo `/team:feedback`.
4. Nhiều skill khớp → chạy nối tiếp, ghi cả chuỗi; không trộn hai quy trình.
5. Ghi một dòng journal `docs/team/journal/<ID>.md` (Write) TRƯỚC khi sửa artifact đầu tiên: skill/playbook đã chọn và vì sao.
6. Không skill nào khớp → ghi "không có skill phù hợp" + skill gần nhất đã loại + lý do; việc sẽ lặp lại → đề xuất `/team:make-skill`.

## Lý do tự bào chữa thường gặp
| Ý nghĩ | Làm đúng |
|---|---|
| "Chỉ là câu hỏi, không phải việc" | Câu hỏi dẫn tới hành động là việc; kiểm skill trước. |
| "Đọc repo cho có bối cảnh đã" | Skill chỉ cách khám phá; kiểm trước, rồi Explore. |
| "Tôi nhớ skill này rồi" | Skill có thể đã đổi; đọc bản hiện tại. |
| "Làm trước, ghi journal sau" | Ghi trước lần sửa đầu tiên; "sau" là không bao giờ. |
| "Hai skill gần giống, gộp lại" | Chạy một, nối tiếp cái kia. |
| "Tôi là subagent, nên khảo sát mọi skill" | Dùng skill được giao; khám phá là việc của team-leader. |

## Kiểm chứng
- Journal có dòng nêu `/team:<skill>` hoặc playbook, đứng trước lần sửa artifact đầu tiên.
- Skill được nêu tồn tại (`skills/<tên>/` hoặc `.claude/skills/<tên>/`).
- "Không có skill" luôn kèm skill gần nhất đã loại và lý do.
