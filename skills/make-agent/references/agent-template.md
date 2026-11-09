# Mẫu agent tạm

```markdown
---
name: <name>
description: Giao khi <tình huống>. (≤ 300 ký tự, nói KHI NÀO giao)
tools: <tối thiểu, tên tool trần, ví dụ Read, Grep, Glob, Bash, Skill>
model: <haiku|sonnet|opus>
effort: <low|medium|high>
maxTurns: <n>
skills:
  - handbook
---

<!-- team: temp, created <YYYY-MM-DD>, need: <nhu cầu một câu> -->

## 1. Danh tính
<là ai, báo cáo cho ai, được gọi ai (thường: không ai)>

## 2. Đầu vào bắt buộc
<danh sách; thiếu → trả về ≤ 5 dòng rồi dừng>

## 3. Quy trình
1. <bước — tool — khe profile>

## 4. Đầu ra
<đường dẫn; tin trả ≤ 10 dòng và các trường>

## 5. Tiêu chí xong
<quan sát được; dán lệnh + đầu ra thật>

## 6. Không bao giờ
- <4–7 dòng, kèm mã STD>

## 7. Dấu hiệu tự bào chữa
- "<lý do>" → <làm đúng> (3–5 dòng)

## 8. Dừng và leo thang
<điều kiện, báo ai, nêu: lý do, việc nào, ai làm gì, lệnh chạy tiếp>
```

Giới hạn đường dẫn/lệnh ghi trong thân và do hook role-policy thực thi; `tools` chỉ nhận tên tool.
