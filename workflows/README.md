# Playbook — chọn theo tín hiệu

team-leader dùng bảng này ở `/team:intake`: xét LOẠI việc trước (dòng đầu tiên khớp, từ trên xuống), rồi mới định cỡ S/M/L. `scripts/gen-guides.py` đọc bảng giữa hai dấu dưới đây để sinh `docs/guides/decision-tree.md`.

<!-- playbook-table:start -->
| Tín hiệu | Playbook | Cỡ mặc định |
|---|---|---|
| Repo có code, đội chưa từng làm (chưa có `.team/profile.json`) | [takeover](takeover.md) | — |
| Repo rỗng, dựng hệ thống từ đầu | [new-project](new-project.md) | L |
| Production đang hỏng, cần chữa ngay | [hotfix](hotfix.md) | S |
| Hành vi sai so với spec, tái hiện được, không gấp | [bug-fix](bug-fix.md) | S |
| Pipeline CI đỏ hoặc cần sửa workflow CI | [ci-fix](ci-fix.md) | S |
| Đổi yêu cầu của feature đã duyệt G1 | [change-request](change-request.md) | M |
| Nối với API/dịch vụ bên ngoài | [integration](integration.md) | M |
| Chuyển đổi hay nạp dữ liệu giữa schema/hệ thống | [data-migration](data-migration.md) | M |
| Nâng phiên bản thư viện, framework, runtime | [dependency-upgrade](dependency-upgrade.md) | M |
| Dọn code, không đổi hành vi | [refactor](refactor.md) | M |
| Chỉ tài liệu kỹ thuật, README | [docs-only](docs-only.md) | S |
| Tài liệu cho khách hàng/người dùng cuối | [client-docs](client-docs.md) | S |
| Chưa biết làm được không, cần thử | [spike](spike.md) | S |
| Đóng gói và đưa feature đã accepted lên môi trường | [release](release.md) | — |
| Nhìn lại cách đội làm việc | [retro](retro.md) | — |
| Hành vi mới cho hệ thống đang chạy (mọi trường hợp còn lại) | [new-feature](new-feature.md) | theo intake |
<!-- playbook-table:end -->

## Định cỡ
- **S**: mô tả diff bằng một câu; ≤ 3 file; không đổi schema/API.
- **M**: một module; đổi dữ liệu hoặc API; 1–5 người-ngày.
- **L**: nhiều module; NFR mới; > 5 người-ngày.
Người ép cỡ bằng `--size` hoặc nhãn `team:size:*`.

## Chạy không người trông (`batch/`)
| File | Dùng khi |
|---|---|
| [batch/build-all-tasks.md](batch/build-all-tasks.md) | Plan đã duyệt G3; build hết task qua đêm |
| [batch/verify-all.md](batch/verify-all.md) | Nghiệm thu lại mọi feature đang ở trạng thái built |
| [batch/weekly-retro.md](batch/weekly-retro.md) | Retro định kỳ hằng tuần |
| [batch/clean-sweep.md](batch/clean-sweep.md) | Dọn dẹp một loại nợ trong `debt.md` |
