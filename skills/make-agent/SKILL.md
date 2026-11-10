---
name: make-agent
description: Dùng khi team-leader thấy một chuyên môn riêng của dự án đủ lớn để cần ngữ cảnh, bộ tool hoặc model riêng, mà không vai nào của kit đảm nhận được và một skill tạm không đủ.
argument-hint: "<name> \"<nhu cầu một câu>\" [--evidence <journal|review|task>]"
allowed-tools: Bash(ls *) Bash(cat *) Bash(date *)
---

# Tạo agent tạm của dự án

## Tổng quan
Skill này tạo một agent tạm trong `.claude/agents/<name>.md` theo đúng hợp đồng 10 mục của đội — chỉ khi một skill tạm không đủ vì việc cần ngữ cảnh riêng, bộ tool riêng hay model riêng (`handbook/tool-selection.md`, hàng "agent"). Ví dụ đúng: một chuyên gia giao diện cần nạp sẵn design system và dùng Playwright MCP mà không vai nào có. Ví dụ sai: một việc hai phút, hay một bước lặp lại (đó là skill).

Agent tạm là một người với hợp đồng: làm gì, không làm gì, đầu vào, đầu ra, tiêu chí xong, tool, trần lượt — không phải nhân vật. Nó không hỏi người (subagent không có `AskUserQuestion`), không gọi vai khác (chỉ Explore), và chỉ team-leader gọi nó. Hook role-policy áp giới hạn mặc định `_temp` cho mọi agent có dấu `team: temp`; frontmatter `tools` là giới hạn cứng còn lại, nên chọn tối thiểu.

Skill chạy trong phiên chính (team-leader được ghi `.claude/agents/**`, `docs/team/**`). `$ARGUMENTS`: tên (kebab-case, tiếng Anh), nhu cầu, bằng chứng. `<kit>` = nội dung `.team/plugin_root`.

## Khi nào dùng (và khi nào không)
Dùng khi:
- Việc cần tool mà không vai nào có (MCP đã cài cho dự án, công cụ đo riêng).
- Việc cần ngữ cảnh lớn nạp sẵn (design system, đặc tả giao thức) mà nạp vào vai có sẵn sẽ làm đầy ngữ cảnh của vai đó.
- Việc cần model khác vai đang làm vì giá của sai lầm khác (ví dụ kiểm hợp đồng pháp lý cần opus trong khi dev dùng sonnet).

Không dùng khi:
- Một skill tạm là đủ → `/team:make-skill`.
- Một trong 13 vai đảm nhận được (kể cả khi kèm một skill tạm).
- Việc một lần, hay chỉ muốn "một agent cho gọn".
- tech-lead cần gọi agent đó: hook chỉ cho tech-lead gọi dev, reviewer, Explore — agent tạm do team-leader gọi.

## Tìm hiểu stack trước
1. Read `<kit>/handbook/tool-selection.md` từ hàng đầu: dừng ở hàng đầu tiên khớp; chỉ hàng "agent" mới hợp lệ ở đây.
2. Read mô tả của 13 vai `<kit>/agents/*.md` và `.claude/agents/*.md`; plugin agent đã cài.
3. Read `.team/config.json`: `limits.max_temp_skills` (dùng chung cho skill và agent tạm), `models`.
4. Read `docs/team/skills-registry.md`: số mục `temp` đang hoạt động.
5. Tool cần có thật: MCP phải đã được cài cho dự án; chưa có → in lệnh cài cho người, không thêm cấu hình `mcpServers`.

## Đầu vào và điều kiện trước
- Nhu cầu một câu + bằng chứng + lý do skill không đủ (ngữ cảnh / tool / model — nêu cụ thể cái nào và vì sao).
- Chưa chạm trần temp; đủ trần → từ chối, đề xuất `retired`.
- Tên chưa trùng vai nào, agent dự án nào, agent plugin nào.
- Phiên tương tác: ghi vào `.claude/agents/` luôn cần người duyệt, headless không cấp trước được (K-72). Headless → in nội dung file vào tin trả, trạng thái `NEEDS_ANSWER`.

## Quy trình
1. **Kiểm lý do agent.** Đi `tool-selection.md` từ trên xuống; ghi hàng dừng. Không phải hàng agent → từ chối, chỉ hướng (hook, script, rule, skill).
2. **Khớp năng lực.** Với từng vai có thể đảm nhận: trích dòng mô tả và nói vì sao không đủ. Có vai đủ (kể cả kèm skill tạm) → từ chối, gợi ý `/team:make-skill`.
3. **Gom mẫu.** Agent → Explore: file mẫu, quy ước, khe profile. Cần docs ngoài → researcher qua team-leader.
4. **Chọn model theo giá của sai lầm** (SPEC §3): haiku cho việc máy móc, sonnet cho dựng và điều phối, opus khi sai đắt. Ghi lý do vào registry.
5. **Chọn tool tối thiểu.** Không `AskUserQuestion`; `Agent` chỉ khi thân nói rõ chỉ gọi Explore; MCP ghi đủ tên. Không dùng `permissionMode`, `hooks`, `mcpServers` trong frontmatter.
6. **Viết** `.claude/agents/<name>.md` theo `${CLAUDE_SKILL_DIR}/references/agent-template.md`: mô tả bắt đầu "Giao khi", ≤ 300 ký tự; `skills` nạp sẵn handbook (`team:handbook`; cài cục bộ `team-handbook`); 10 mục của `<kit>/scripts/agent-sections.txt`, có ví dụ tin trả (dòng đầu `<name> -> team-leader | <ID> | <TRẠNG THÁI>`) và tin dừng 4 dòng.
7. **Dòng đánh dấu** đầu thân: `<!-- team: temp, created <YYYY-MM-DD>, need: <nhu cầu>, evidence: <nguồn>, why-agent: <…> -->`. Dấu `team: temp` là thứ hook dùng để áp giới hạn `_temp` — thiếu là agent chạy không giới hạn vai.
8. **Ca thử.** Write `docs/team/agents/<name>.tests.md` (KHÔNG trong `.claude/agents/`, nơi mọi `.md` có thể bị nạp như agent): 1–2 ca với đầu vào là tin giao ≤ 10 dòng, kết quả mong đợi, kiểm phân biệt được (ví dụ dòng đầu tin trả đúng dạng).
9. **Kiểm máy.** `grep -c '^## [0-9]' .claude/agents/<name>.md` = 10; `wc -w` thân; frontmatter không có khóa cấm. Dán.
10. **Đăng ký.** Edit `docs/team/skills-registry.md`: loại `agent`, trạng thái `temp`, nhu cầu + bằng chứng, model + lý do, đường dẫn ca thử.
11. **Ai gọi.** Ghi vào registry: "người gọi: team-leader". Nếu tech-lead cần nó trong build → team-leader gọi giữa các task, hoặc đề xuất nâng thành vai của kit (người duyệt).
12. **Thử một lần** với ca 1 trên đúng model đã chọn: dòng đầu tin trả phải đúng dạng; agent trích được một dòng của handbook (bằng chứng handbook đã nạp). Journal ghi kết quả; `runs` +1.

## Đầu ra
- `.claude/agents/<name>.md`; `docs/team/agents/<name>.tests.md`; dòng mới trong `docs/team/skills-registry.md`; dòng journal.
- Tin cho người:
  ```
  make-agent ui-specialist | đã tạo (temp)
  Lý do agent: tool riêng (Playwright MCP đã cài) + ngữ cảnh design system 9.000 chữ; tool-selection dừng ở hàng "agent"
  Vai đã so: dev (không có Playwright, ngữ cảnh build), qa (chỉ nghiệm thu) — không đủ
  File: ui-specialist.md trong .claude/agents/ (10 mục, 780 chữ, sonnet); ca thử trong docs/team/agents/ (2 ca)
  Giới hạn: role-policy _temp (Bash chỉ-đọc + git + cmd.*, chỉ Explore); không khóa permissionMode/hooks
  Thử ca 1: dòng đầu "ui-specialist -> team-leader | FEAT-009 | DONE"; trích handbook STD-TEST-1
  Tiếp: team-leader giao FEAT-009 bước kiểm giao diện, ghi lý do vào journal
  ```

## Lý do tự bào chữa thường gặp
| Ý nghĩ | Làm đúng |
|---|---|
| "Một agent riêng gọn hơn skill" | Đi hết `tool-selection.md`; agent chỉ khi cần ngữ cảnh/tool/model riêng có bằng chứng. |
| "Cho đủ tool để agent tự xoay xở" | Tool tối thiểu; `tools` là giới hạn cứng. |
| "Để agent hỏi người cho nhanh" | Không có `AskUserQuestion`; `NEEDS_ANSWER` về người gọi. |
| "Agent này gọi dev, reviewer luôn" | Subagent không gọi nhau; chỉ Explore. |
| "permissionMode: bypassPermissions để khỏi bị hỏi" | Không bao giờ; nó gỡ luật máy (P3). |
| "opus cho chắc" | Theo giá của sai lầm; ghi lý do. |
| "Không cần handbook" | Bắt buộc nạp; kiểm bằng một lần thử. |
| "Ca thử để cạnh agent cho tiện" | Đặt ở `docs/team/agents/`, không trong `.claude/agents/`. |
| "tech-lead gọi agent này trong build" | Hook chặn; team-leader gọi hoặc đề xuất nâng thành vai. |

## Dấu hiệu sai
- Mô tả không bắt đầu "Giao khi" hoặc > 300 ký tự.
- `tools` có `Agent` mà thân không giới hạn ở Explore; có `AskUserQuestion`.
- Frontmatter có `permissionMode`, `hooks` hay `mcpServers`.
- Thiếu ví dụ tin trả hay tin dừng 4 dòng; thiếu dấu `team: temp`.
- Agent cho việc một lần; không có dòng registry loại `agent`.
- File ca thử nằm trong `.claude/agents/`.

## Kiểm chứng
- [ ] Frontmatter được dán: `name` = tên file, mô tả "Giao khi", `tools` tối thiểu, không khóa cấm.
- [ ] `grep -c '^## [0-9]'` = 10 và `wc -w` thân được dán.
- [ ] Dòng đánh dấu có `team: temp`, `evidence:`, `why-agent:`.
- [ ] `grep '<name>' docs/team/skills-registry.md`: loại agent, model + lý do, người gọi.
- [ ] Một lần thử ca 1: dòng đầu tin trả đúng dạng, trích được handbook.

## Xem thêm
- `${CLAUDE_SKILL_DIR}/references/agent-template.md` — mẫu 10 mục, giới hạn máy `_temp`, nơi đặt ca thử. Mở ở bước 6 và 8.
- `/team:make-skill`; `handbook/tool-selection.md`, `handbook/who-calls-whom.md`.
- `hooks/role-policy.json` (vai `_temp`); `<kit>/templates/artifacts/skills-registry.md`.
