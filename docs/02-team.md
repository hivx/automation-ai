# 02 — Đội

Nguồn chuẩn: `SPEC.md` §3 và các file `agents/*.md`. Điều chỉnh: ADJ-01, ADJ-02, ADJ-04, ADJ-07, ADJ-10 trong `docs/00-overview.md`.

## Mười ba vai
Bảng dưới đây SINH từ frontmatter của `agents/*.md` bằng `scripts/gen-team-table.py`; không sửa tay. Việc làm / không làm, đầu vào, đầu ra của từng vai nằm trong chính file agent.

<!-- team-table:start -->
| Vai | Giao khi | Tools | Model | Effort | maxTurns | Memory | Isolation | Skills nạp sẵn |
|---|---|---|---|---|---|---|---|---|
| [team-leader](../agents/team-leader.md) | người dùng đưa yêu cầu mới, hỏi tiến độ hay duyệt cổng, hoặc khi cần chọn playbook, định cỡ việc và điều phối các vai khác. Chạy làm agent của phiên chính. | Read, Grep, Glob, Bash, Agent, AskUserQuestion, Write, Skill | sonnet | low | 30 | — | — | handbook, using-team |
| [tech-lead](../agents/tech-lead.md) | một feature đã có spec/design được duyệt và cần lập kế hoạch, chia task, điều phối dev và reviewer, gộp nhánh hoặc mở PR. | Read, Grep, Glob, Bash, Agent, Edit, Write, Skill | sonnet | medium | 60 | — | — | handbook, using-team |
| [coach](../agents/coach.md) | chạy retro, khi scorecard có bất thường, khi góp ý vượt ngưỡng, hoặc khi cần kiểm toán bộ kit và đề xuất sửa agent/skill có bằng chứng. | Read, Grep, Glob, Bash, Write, Skill | opus | high | 40 | project | — | handbook |
| [analyst](../agents/analyst.md) | có yêu cầu thô cần biến thành spec có Definition of Done, hoặc khi cần sửa đổi spec đã duyệt (chế độ --amend). | Read, Grep, Glob, Bash, Agent, Write, Skill | opus | high | 40 | — | — | handbook |
| [researcher](../agents/researcher.md) | spec còn câu hỏi kỹ thuật cần docs chính thức, khi so sánh phương án, nâng cấp phụ thuộc, tích hợp API ngoài, hoặc cần POC. | Read, Grep, Glob, Bash, WebFetch, WebSearch, Agent, Write, Skill | opus | high | 50 | — | — | handbook |
| [architect](../agents/architect.md) | việc cỡ L cần kiến trúc, khi thay đổi chạm nhiều module hoặc NFR, khi cần quyết định ADR, hoặc khi cần review ba câu cho design.md. | Read, Grep, Glob, Bash, Agent, Write, Skill | opus | high | 40 | — | — | handbook |
| [designer](../agents/designer.md) | spec đã duyệt cần thiết kế chi tiết trước khi lập kế hoạch: dữ liệu, API, luồng, quyền, migration, touchpoints và test plan. | Read, Grep, Glob, Bash, Agent, Write, Skill | opus | high | 40 | — | — | handbook |
| [dev](../agents/dev.md) | tech-lead (hoặc team-leader với việc cỡ S) có một task cụ thể với touchpoints và tiêu chí, cần viết test và code trong worktree riêng. | Read, Edit, Write, Grep, Glob, Bash, Skill | sonnet | medium | 60 | — | worktree | handbook |
| [reviewer](../agents/reviewer.md) | một task đã có commit của dev và cần review độc lập trong ngữ cảnh sạch trước khi gộp, chấm theo Review checklist (10). | Read, Grep, Glob, Bash, Skill | opus | high | 25 | project | — | handbook |
| [qa](../agents/qa.md) | mọi task của feature đã tick và cần nghiệm thu độc lập từng tiêu chí bằng lệnh chạy thật, theo Acceptance checklist (6). | Read, Grep, Glob, Bash, Write, Skill | opus | high | 40 | project | — | handbook |
| [writer](../agents/writer.md) | feature đã accepted và cần As-Built, release notes, mục CHANGELOG, cập nhật README hoặc nội dung PR; hoặc khi việc chỉ là tài liệu (docs-only, client-docs). | Read, Grep, Glob, Bash, Write, Skill | sonnet | medium | 30 | — | — | handbook |
| [maintainer](../agents/maintainer.md) | cần dọn dẹp KHÔNG đổi hành vi: code chết, đổi tên, cấu trúc, phụ thuộc thừa, test mồ côi, đơn giản hóa, ngừng dùng API cũ, bổ sung quan sát. | Read, Edit, Write, Grep, Glob, Bash, Skill | sonnet | medium | 60 | — | worktree | handbook |
| [devops](../agents/devops.md) | pipeline CI đỏ, khi cần dựng hoặc sửa CI/CD, viết script deploy, rollback, smoke, hoặc khi phát hành lên staging hay prod đã có duyệt G5. | Read, Edit, Write, Grep, Glob, Bash, Skill | sonnet | medium | 60 | — | — | handbook |
<!-- team-table:end -->

Agent tạm: `.claude/agents/<tên>.md` trong dự án, chỉ tạo khi team-leader thấy cần (`/team:make-agent`).

Trường `tools` chỉ ghi tên tool: docs không cho giới hạn đường dẫn/lệnh ở đó (thử nghiệm: `Bash(git status *)` vẫn cấp cả Bash). Giới hạn của từng vai (ví dụ team-leader chỉ ghi `docs/team/**`) ghi trong thân agent và do hook role-policy thực thi (ADJ-02).

## Ai gọi ai
```
người ⇄ phiên chính = team-leader          (chỉ ở đây có AskUserQuestion)
          ├─► analyst, researcher, architect, designer, writer, maintainer, devops, coach, qa
          ├─► dev                            (chỉ việc cỡ S một task)
          └─► tech-lead ─► dev, reviewer
team-leader, tech-lead, analyst, researcher, architect, designer ─► Explore   (chỉ để đọc code)
```
- Chỉ team-leader và tech-lead gọi vai khác. analyst, researcher, architect, designer chỉ được gọi `Explore`; các vai còn lại không gọi ai.
- Độ sâu tối đa 3 tầng dưới phiên chính (ADJ-04).
- Bàn giao = MỘT FILE + tin nhắn tự đủ ≤ 10 dòng; người nhận không thấy hội thoại của người gửi.
- tech-lead → dev: mã task, tiêu chí nghiệm thu, touchpoints, `cmd.test_one`, nhánh, "chỉ sửa trong touchpoints".
- dev → tech-lead: file đã đổi, test đã chạy kèm đầu ra thật, còn thiếu gì.

Chi tiết: `handbook/who-calls-whom.md`.

## Định tuyến model
- Model mạnh nhất ở nơi sai đắt nhất.
- haiku: phân loại, việc cơ học. sonnet: điều phối, dev, writer, maintainer, devops. opus: analyst, researcher, architect, designer, reviewer, qa, coach.
- Không đổi model giữa phiên. Ghi đè trong `.team/config.json → models`.
