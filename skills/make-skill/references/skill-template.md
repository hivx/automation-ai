# Mẫu SKILL.md cho skill tạm

```markdown
---
name: <name>
description: Dùng khi <tình huống quan sát được>. (< 500 ký tự, không tóm tắt các bước)
argument-hint: "<tham số>"
allowed-tools: <tối thiểu, ví dụ Bash(cat *)>
---

<!-- team: temp, created <YYYY-MM-DD>, need: <nhu cầu một câu> -->

## Mục đích
<một dòng>

## Đầu vào
<file + ý nghĩa $ARGUMENTS>

## Điều kiện trước
<điều phải có; lệnh kiểm>

## Các bước
1. <bước — tool — khe profile nếu có>
2. <điểm kiểm>

## Đầu ra
<đường dẫn>

## Tiêu chí xong
<quan sát được; dán lệnh + đầu ra thật>

## Dấu hiệu sai
- "<lý do tự bào chữa>" → <làm đúng>
- …(≥ 3)

## Lệnh tiếp theo
<lệnh in cho người hoặc vai gọi>
```

Luật: tên thư mục = `name`; không `@file`; lệnh build/test/lint chỉ qua khe `cmd.*`; tài liệu dài để trong `references/`.
