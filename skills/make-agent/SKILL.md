---
name: make-agent
description: Dùng khi team-leader thấy một chuyên môn riêng của dự án đủ lớn để cần ngữ cảnh, bộ tool hoặc model riêng, mà không vai nào của kit đảm nhận được.
argument-hint: "<name> \"<nhu cầu một câu>\""
allowed-tools: Bash(ls *) Bash(cat *) Bash(date *)
---

## Mục đích
Tạo một agent tạm của dự án theo hợp đồng chuẩn của đội.

## Đầu vào
- `$ARGUMENTS`: tên (kebab-case, tiếng Anh) và nhu cầu.
- `docs/team/skills-registry.md`, `.team/config.json` (`limits.max_temp_skills` dùng chung cho agent tạm). `<kit>` = nội dung `.team/plugin_root`.

## Điều kiện trước
- Có nhu cầu một câu và lý do tại sao skill không đủ (cần ngữ cảnh riêng, tool riêng hoặc model riêng — `<kit>/handbook/tool-selection.md`).
- Chưa chạm trần temp.

## Các bước
1. Tìm trùng: 13 vai của kit, `.claude/agents/`, agent của plugin. Có vai đảm nhận được → từ chối.
2. Gom mẫu trong repo (Agent → Explore); cần docs ngoài → researcher.
3. Viết `.claude/agents/<name>.md` theo `${CLAUDE_SKILL_DIR}/references/agent-template.md`: mô tả bắt đầu "Giao khi", ≤ 300 ký tự; `tools` tối thiểu; `skills` phải có `handbook`; 10 mục của `<kit>/scripts/agent-sections.txt`, thân 600–1.200 chữ.
4. Dòng đầu thân: `<!-- team: temp, created <YYYY-MM-DD>, need: <nhu cầu> -->`.
5. `.claude/agents/<name>.tests.md`: 1–2 ca thử.
6. Đăng ký trong `docs/team/skills-registry.md` với loại `agent`, trạng thái `temp`.
7. Cập nhật ai gọi ai: chỉ team-leader hoặc tech-lead được gọi agent mới.
8. Journal: lý do + tên agent.

## Đầu ra
- `.claude/agents/<name>.md`, `.claude/agents/<name>.tests.md`; dòng mới trong registry.

## Tiêu chí xong
- Frontmatter có `skills: [handbook]`; 10 mục (có ví dụ tin trả và tin dừng 4 dòng); registry có dòng — dán cả hai.

## Dấu hiệu sai
- "Agent cho việc 2 phút" → làm tại chỗ hoặc skill.
- "Cho đủ mọi tool cho tiện" → tối thiểu.
- "Không cần handbook" → bắt buộc.

## Lệnh tiếp theo
Giao việc: team-leader hoặc tech-lead gọi agent mới kèm lý do trong journal.
