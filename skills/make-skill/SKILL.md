---
name: make-skill
description: Dùng khi team-leader thấy một task cần chuyên môn riêng của dự án mà kit chưa có, hoặc một chuỗi bước sẽ lặp lại, và đã nêu được nhu cầu một câu.
argument-hint: "<name> \"<nhu cầu một câu>\""
allowed-tools: Bash(ls *) Bash(cat *) Bash(date *)
---

## Mục đích
Tạo một skill tạm của dự án đúng chuẩn, dùng ngay, có đăng ký và hạn dùng.

## Đầu vào
- `$ARGUMENTS`: tên (kebab-case, tiếng Anh) và nhu cầu.
- `docs/team/skills-registry.md`, `.team/config.json` (`limits.max_temp_skills`). `<kit>` = nội dung `.team/plugin_root`.

## Điều kiện trước
- Có nhu cầu một câu; không có → từ chối.
- Số skill `temp` đang hoạt động trong registry < `limits.max_temp_skills`; đủ trần → từ chối, đề xuất `retired` skill cũ.

## Các bước
1. Tìm trùng: skill của kit (`<kit>/skills/`), `.claude/skills/`, skill của plugin đã cài (danh sách skill đang thấy). Trùng hoặc gần trùng → từ chối, chỉ ra skill có sẵn.
2. Gom mẫu trong repo (Agent → Explore): 2–3 file mẫu, quy ước, lệnh của profile. Cần docs ngoài → gọi researcher.
3. Viết `.claude/skills/<name>/SKILL.md` theo `${CLAUDE_SKILL_DIR}/references/skill-template.md`: mô tả bắt đầu "Dùng khi", 8 mục, ≤ 500 từ thân, `allowed-tools` tối thiểu, không ghi cứng lệnh stack.
4. Dòng đầu thân: `<!-- team: temp, created <YYYY-MM-DD>, need: <nhu cầu> -->`.
5. `references/tests.md`: 1–2 ca thử (đầu vào → kết quả mong đợi).
6. Đăng ký trong `docs/team/skills-registry.md` (mẫu `<kit>/templates/artifacts/skills-registry.md`): tên, nhu cầu, ngày tạo, trạng thái `temp`, lần dùng cuối.
7. Journal: một câu lý do + tên skill.

## Đầu ra
- `.claude/skills/<name>/SKILL.md`, `.claude/skills/<name>/references/tests.md`; dòng mới trong `docs/team/skills-registry.md`.

## Tiêu chí xong
- Skill mới có 8 mục, mô tả bắt đầu "Dùng khi", thân ≤ 500 từ (`wc -w` dán); registry có dòng (dán).

## Dấu hiệu sai
- "Tạo sẵn cho chắc" → chỉ khi có nhu cầu đang làm.
- "Gần giống skill có sẵn nhưng tôi viết lại" → dùng skill có sẵn.
- "Bỏ ca thử" → luôn có.

## Lệnh tiếp theo
Giao cho vai cần: "dùng `/<name>` cho bước X"; sau 30 ngày không dùng → `retired`.
