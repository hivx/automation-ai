# Playbook: ci-fix

## Khi nào áp dụng
- Pipeline CI đỏ trên nhánh chính hoặc trên PR không đổi phần liên quan.
- Workflow CI cần sửa hoặc thêm bước.

## Cỡ mặc định
S.

## Chuỗi
0. `/team:intake` → team-leader → `intake.md`.
1. `/team:ci fix` → devops: chẩn đoán, PHÂN LOẠI trước theo STD-CI-4 (code / test chập chờn / môi trường / cấu hình / phụ thuộc).
2. Lỗi thật trong code → chuyển `bug-fix`. Còn lại → devops sửa CI.
3. `/team:pr` → tech-lead → PR RIÊNG cho thay đổi CI; `docs/team/ci.md` cập nhật.

## Cổng
Không cổng riêng; review PR theo luật repo.

## Điểm dừng
- Lỗi thật trong code; thiếu quyền hoặc secret.

## Tiêu chí xong
- CI xanh trên PR sửa; phân loại và trích log ghi trong `docs/team/ci.md`.

## Lỗi thường gặp
- Tắt bước test để cho xanh.
- Chạy lại nhiều lần thay vì phân loại.

## Playbook liên quan
`bug-fix`, `release`.
