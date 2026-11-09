# Mẫu quét secret trong phần đã stage

Chạy trên `git diff --staged` (chỉ dòng thêm, bắt đầu bằng `+`). Có kết quả → dừng; ghi `file:dòng`, KHÔNG chép giá trị.

| Mẫu (regex, không phân biệt hoa thường) | Bắt gì |
|---|---|
| `(password|passwd|pwd)\s*[:=]\s*['"][^'"]{4,}` | Mật khẩu viết cứng |
| `(secret|token|api[_-]?key|access[_-]?key)\s*[:=]\s*['"][^'"]{8,}` | Khóa, token |
| `-----BEGIN [A-Z ]*PRIVATE KEY-----` | Khóa riêng |
| `AKIA[0-9A-Z]{16}` | Khóa truy cập dạng AWS |
| `gh[pousr]_[A-Za-z0-9]{30,}` | Token GitHub |
| `xox[baprs]-[A-Za-z0-9-]{10,}` | Token Slack |
| `://[^/\s:@]+:[^/\s@]+@` | Mật khẩu trong URL |

Lệnh mẫu: `git diff --staged | grep -nE '^\+' | grep -iE '<mẫu>'`.
Dương tính giả (giá trị mẫu trong test, ví dụ trong tài liệu) → ghi lý do trong báo cáo; không tắt quét.
