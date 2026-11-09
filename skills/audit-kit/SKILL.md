---
name: audit-kit
description: Dùng khi cần kiểm toán chính bộ kit team đang chạy trong dự án: skill không ai dùng, agent chạm trần lượt, chỉ dẫn mâu thuẫn, tài liệu lệch tên, lỗ hổng an toàn.
argument-hint: "[--since <YYYY-MM-DD>]"
disable-model-invocation: true
context: fork
agent: team:coach
background: false
allowed-tools: Bash(python3 *) Bash(cat *) Bash(jq *) Bash(ls *)
---

## Mục đích
Tìm lỗi của bộ kit (không phải của dự án) và ghi vào `docs/team/kit-issues.md`.

## Đầu vào
- `$ARGUMENTS`: mốc thời gian.
- Kit tại `<kit>` (nội dung `.team/plugin_root`), `.claude/skills/`, `.claude/agents/`, `docs/team/metrics/`.

## Điều kiện trước
Có `docs/team/metrics/runs.jsonl`; không có thì chỉ chạy các kiểm tĩnh (bước 4–6).

## Các bước
Chi tiết kiểm: `${CLAUDE_SKILL_DIR}/references/checks.md`.
1. Ghi `.team/current.json` {feature: "audit-kit", stage: "audit", agent: "coach", started_at}.
2. Skill không dùng: so danh sách skill với số lần chạy trong `runs.jsonl` từ mốc (jq).
3. Agent chạm `maxTurns`: đếm lần chạy có `turns` ≥ `maxTurns` của agent.
4. Chỉ dẫn mâu thuẫn: Grep các cặp luật trái nhau trong agents/skills/rules (ví dụ một nơi "luôn", nơi khác "không bao giờ" cùng việc).
5. Lệch tên: tên skill/agent trong `docs/` không có trong `skills/` hoặc `agents/`.
6. An toàn: hook có thể bị lách (matcher thiếu tool), `allowed-tools` quá rộng (`Bash` trần, `Bash(*)`), skill tạm không có trong `skills-registry.md`.
7. Ghi `docs/team/kit-issues.md` từ `<kit>/templates/artifacts/kit-issues.md`: mỗi vấn đề một dòng `mức | loại | file | bằng chứng | đề xuất`.

## Đầu ra
- `docs/team/kit-issues.md`.
- Tin trả ≤ 10 dòng: số vấn đề theo mức, ba vấn đề nặng nhất.

## Tiêu chí xong
- Mỗi vấn đề có bằng chứng (lệnh + đầu ra hoặc `file:line`).

## Dấu hiệu sai
- "Sửa luôn file kit" → chỉ ghi vấn đề.
- "Không có số liệu thì bỏ" → vẫn chạy kiểm tĩnh.
- "Ghi lỗi của dự án vào đây" → chỉ lỗi của kit.

## Lệnh tiếp theo
In: "Xem `docs/team/kit-issues.md`; báo vấn đề của kit lên repo `automation-ai`."
