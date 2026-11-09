<!-- GENERATED — do not edit; run scripts/gen-guides.py -->
# Chọn playbook nào

team-leader chọn ở `/team:intake`: xét từ trên xuống, dòng đầu tiên khớp thắng; rồi mới định cỡ.
Nguồn: `workflows/README.md`. Chuỗi skill, cổng, điểm dừng của từng playbook nằm trong file playbook.

| Tín hiệu | Playbook | Cỡ mặc định |
|---|---|---|
| Repo có code, đội chưa từng làm (chưa có `.team/profile.json`) | [takeover](../../workflows/takeover.md) | — |
| Repo rỗng, dựng hệ thống từ đầu | [new-project](../../workflows/new-project.md) | L |
| Production đang hỏng, cần chữa ngay | [hotfix](../../workflows/hotfix.md) | S |
| Hành vi sai so với spec, tái hiện được, không gấp | [bug-fix](../../workflows/bug-fix.md) | S |
| Pipeline CI đỏ hoặc cần sửa workflow CI | [ci-fix](../../workflows/ci-fix.md) | S |
| Đổi yêu cầu của feature đã duyệt G1 | [change-request](../../workflows/change-request.md) | M |
| Nối với API/dịch vụ bên ngoài | [integration](../../workflows/integration.md) | M |
| Chuyển đổi hay nạp dữ liệu giữa schema/hệ thống | [data-migration](../../workflows/data-migration.md) | M |
| Nâng phiên bản thư viện, framework, runtime | [dependency-upgrade](../../workflows/dependency-upgrade.md) | M |
| Dọn code, không đổi hành vi | [refactor](../../workflows/refactor.md) | M |
| Chỉ tài liệu kỹ thuật, README | [docs-only](../../workflows/docs-only.md) | S |
| Tài liệu cho khách hàng/người dùng cuối | [client-docs](../../workflows/client-docs.md) | S |
| Chưa biết làm được không, cần thử | [spike](../../workflows/spike.md) | S |
| Đóng gói và đưa feature đã accepted lên môi trường | [release](../../workflows/release.md) | — |
| Nhìn lại cách đội làm việc | [retro](../../workflows/retro.md) | — |
| Hành vi mới cho hệ thống đang chạy (mọi trường hợp còn lại) | [new-feature](../../workflows/new-feature.md) | theo intake |

Chạy không người trông: `workflows/batch/` (build-all-tasks, verify-all, weekly-retro, clean-sweep).
