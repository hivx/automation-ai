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
<danh sách; thiếu → trả về ≤ 5 dòng, NEEDS_CONTEXT, rồi dừng>

## 3. Tìm hiểu stack trước
<khe profile cần đọc; không đoán lệnh>

## 4. Quy trình
1. <bước — tool — khe profile — điểm kiểm>

## 5. Đầu ra
<đường dẫn; Ví dụ tin trả ≤ 10 dòng, dòng đầu là trạng thái>

## 6. Tiêu chí xong
<quan sát được; dán lệnh + đầu ra thật>

## 7. Không bao giờ
- <4–7 dòng, kèm mã STD>

## 8. Lý do tự bào chữa thường gặp
| Ý nghĩ | Làm đúng |
|---|---|
| "<lý do>" | <làm đúng> |  (≥ 6 dòng)

## 9. Dấu hiệu sai
- <≥ 3 dòng>

## 10. Dừng và leo thang
<điều kiện, báo ai; tin dừng 4 dòng: DỪNG / Việc / Ai làm gì / Chạy tiếp>
```

Giới hạn đường dẫn/lệnh ghi trong thân và do hook role-policy thực thi; `tools` chỉ nhận tên tool.
