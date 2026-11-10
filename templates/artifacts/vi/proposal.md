Feature: <ID>
Stage: retro
Author-agent: coach
Date: <YYYY-MM-DD>
Approved-by:
<!-- Cổng: người duyệt điền dòng trên `Approved-by: <tên> <YYYY-MM-DD>`. Không có cổng thì để trống. -->

# Đề xuất: <agent-or-skill> (từ retro <date>)

## Bằng chứng
| Chỉ số | Giá trị | Trung vị cùng cỡ | Nguồn |
|---|---|---|---|

Dòng journal liên quan: <trích>

## Chẩn đoán 5 nguyên nhân
| prompt | model/effort | đầu vào | profile/config | cỡ task | Kết luận |
|---|---|---|---|---|---|

## Thay đổi đề xuất (overlay, nội dung đầy đủ)
```markdown
# Overlay from retro <date>: <reason>
# version: <n>
<toàn bộ nội dung file mới>
```

## Eval (baseline vs có thay đổi, ≥ 3 kịch bản)
| # | Kịch bản | Kỳ vọng | Kiểm bằng |
|---|---|---|---|

## Canary
- Chạy trên <N> việc cỡ S; giữ khi <...>; rollback khi <...>; thay/bỏ khi <...>

## Rollback
<khôi phục bản trước: xóa overlay / trả file cũ>
