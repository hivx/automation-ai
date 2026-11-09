# Playbook: release

## Khi nào áp dụng
- Một hay nhiều feature đã accepted, cần đóng gói và đưa lên môi trường.

## Cỡ mặc định
Không áp dụng.

## Chuỗi
1. `/team:asbuilt` → writer → release notes, mục CHANGELOG.
2. `/team:release` → devops: merge PR đã duyệt → gắn tag.
3. `deploy.staging` → `deploy.smoke` (devops).
4. UAT: người kiểm trên staging.
5. Prod: chỉ khi có `Approved-by-prod:`; sau đó `deploy.smoke`; ghi dấu Released vào `asbuilt.md`.

## Cổng
G4 (đã accepted), G5 luôn là người.

## Điểm dừng
- CI không xanh; smoke staging đỏ; chưa có `Approved-by-prod:`.
- Smoke prod đỏ: đề xuất rollback ngay.

## Tiêu chí xong
- Tag có; smoke staging và prod xanh, đầu ra được dán; dấu Released có.

## Lỗi thường gặp
- Deploy prod trước khi UAT xong.
- Không có lệnh rollback đã kiểm.

## Playbook liên quan
`hotfix`, `data-migration`.
