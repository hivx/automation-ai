# Batch: clean-sweep

## Khi nào áp dụng
- `docs/team/debt.md` có mục loại dọn dẹp lặp lại (code chết, tên, phụ thuộc thừa...).
- Muốn dọn định kỳ, mỗi lần một loại.

## Cỡ mặc định
S hoặc M.

## Chuỗi
Chế độ `decide` bắt buộc; không `--bare`.
1. `/team:clean <kind> --decide` → maintainer: `cmd.test` trước → dọn → `cmd.test` sau.
2. `/team:pr` → tech-lead → PR một loại dọn dẹp.

```bash
claude -p "/team:clean dead-code --decide" \
  --agent team:team-leader --permission-mode dontAsk \
  --allowedTools "$(jq -r '["Read","Grep","Glob","Edit","Write","Agent","Skill"] + (.permissions.allow // []) | join(",")' .claude/settings.json)" \
  --max-turns 120 --max-budget-usd 6 --output-format json
```

## Cổng
G2b nếu bật; merge PR do người.

## Điểm dừng
- Test trước và sau khác nhau; dọn dẹp buộc đổi hành vi.

## Tiêu chí xong
Sáng hôm sau: một PR mở, mô tả có đầu ra test trước/sau; `debt.md` cập nhật.

## Lỗi thường gặp
- Gộp nhiều loại trong một lần chạy.

## Playbook liên quan
`refactor`.
