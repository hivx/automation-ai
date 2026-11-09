---
name: using-team
description: Dùng khi bắt đầu bất kỳ việc gì không tầm thường trong dự án có đội team, trước khi hành động hay hỏi lại: kiểm skill và playbook phù hợp.
---

# Dùng đúng skill trước khi tự làm

Trước mọi hành động không tầm thường:
1. Liệt kê skill `/team:*` và skill tạm trong `.claude/skills/` (xem `docs/team/skills-registry.md`).
2. Có skill khớp → dùng, theo đúng các bước.
3. Có playbook cho loại việc trong `<kit>/workflows/` → theo playbook (`<kit>` = nội dung `.team/plugin_root`).
4. Không tự chế quy trình mà một skill đã có.
5. Ghi một dòng vào `docs/team/journal/<ID>.md`: skill/playbook đã chọn và vì sao.

Không skill nào khớp → ghi "không có skill phù hợp" + lý do, rồi làm.

| Ý nghĩ | Làm đúng |
|---|---|
| "Việc này quá nhỏ, cần gì skill" | Việc nhỏ vẫn có playbook cỡ S; theo nó. |
| "Tôi nhớ skill này rồi" | Skill có thể đã đổi; đọc lại. |
| "Làm trước, ghi journal sau" | Ghi lựa chọn trước khi làm. |
| "Skill này thừa cho trường hợp này" | Vẫn dùng; góp ý bằng `/team:feedback`. |
| "Tôi có cách tốt hơn" | Đề xuất qua `/team:retro`, không lách. |
| "Chỉ đọc code thôi, không tính" | Đọc nhiều file → dùng Explore. |

Bằng chứng: dòng journal ghi lựa chọn.
