# Batch: verify-all

## Khi nào áp dụng
- Có feature ở trạng thái built chưa nghiệm thu.
- Sau khi nâng phụ thuộc, muốn chạy lại nghiệm thu mọi feature đang mở.

## Cỡ mặc định
Không áp dụng.

## Chuỗi
Chế độ `decide` bắt buộc; không `--bare`.
1. `python3 "$(cat .team/plugin_root)/scripts/team.py" status` lấy danh sách feature built.
2. Với từng feature: `/team:verify <ID> --decide` → qa → `acceptance.md`.

```bash
claude -p "/team:verify FEAT-012 --decide" \
  --agent team:team-leader --permission-mode dontAsk \
  --allowedTools "$(jq -r '["Read","Grep","Glob","Write","Agent","Skill"] + (.permissions.allow // []) | join(",")' .claude/settings.json)" \
  --max-turns 80 --max-budget-usd 8 --output-format json
```

## Cổng
Viết `acceptance.md` nhưng KHÔNG duyệt G4; người duyệt.

## Điểm dừng
- Môi trường không chạy được; hết ngân sách.

## Tiêu chí xong
Sáng hôm sau: mỗi feature có `acceptance.md` với phán quyết; `/team:status` liệt kê G4 đang chờ người.

## Lỗi thường gặp
- Coi accepted là đã duyệt G4.

## Playbook liên quan
`batch/build-all-tasks.md`, `release`.
