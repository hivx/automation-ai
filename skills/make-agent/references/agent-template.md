# Mẫu agent tạm

Agent tạm theo cùng hợp đồng 10 mục của kit (`<kit>/scripts/agent-sections.txt`), thân khuyến nghị 400–1.200 chữ. Là hợp đồng làm việc, không phải nhân vật.

```markdown
---
name: <name>
description: Giao khi <tình huống>. (bắt đầu "Giao khi", ≤ 300 ký tự, nói KHI NÀO giao)
tools: <tối thiểu, tên tool trần; không AskUserQuestion; Agent chỉ khi thân giới hạn ở Explore>
model: <haiku|sonnet|opus — theo giá của sai lầm; lý do ghi ở registry>
effort: <low|medium|high>
maxTurns: <n>
skills:
  - team:handbook   # cài cục bộ: team-handbook
---

<!-- team: temp, created <YYYY-MM-DD>, need: <nhu cầu một câu>, evidence: <nguồn>, why-agent: <ngữ cảnh|tool|model riêng: ...> -->

## 1. Danh tính
<là ai, báo cáo cho ai (team-leader), được gọi ai (chỉ Explore hoặc không ai); không hỏi người — câu hỏi trả về NEEDS_ANSWER>

## 2. Đầu vào bắt buộc
<đúng những gì người gọi phải đưa: mã, file, tiêu chí; thiếu → ≤ 5 dòng, NEEDS_CONTEXT, dừng>

## 3. Tìm hiểu stack trước
<khe profile cần đọc; không đoán lệnh>

## 4. Quy trình
1. <bước — tool — khe profile — điểm kiểm>

## 5. Đầu ra
<đường dẫn>
Ví dụ tin trả (≤ 10 dòng, dòng đầu `<name> -> team-leader | <ID> | <TRẠNG THÁI>`):

## 6. Tiêu chí xong
<quan sát được; dán lệnh + đầu ra thật>

## 7. Không bao giờ
- <≥ 4 dòng, kèm mã STD>

## 8. Lý do tự bào chữa thường gặp
| Ý nghĩ | Làm đúng |
|---|---|
| "<lý do>" | <làm đúng> |  (≥ 6 dòng)

## 9. Dấu hiệu sai
- <≥ 3 dòng>

## 10. Dừng và leo thang
<điều kiện; tin dừng 4 dòng trong khối code: DỪNG / Việc / Ai làm gì / Chạy tiếp>
```

Ca thử: `docs/team/agents/<name>.tests.md` (KHÔNG đặt trong `.claude/agents/` — mọi `.md` ở đó có thể bị nạp như một agent).

Giới hạn máy cho agent tạm: hook role-policy áp vai `_temp` cho mọi agent có dấu `team: temp` — ghi được (protect.sh vẫn chặn vùng cấm), Bash chỉ-đọc + git cơ bản + khe `cmd.*`, chỉ gọi Explore. Không dùng các khóa frontmatter `permissionMode`, `hooks`, `mcpServers` (agent dự án tôn trọng chúng và có thể vượt luật máy của kit).
