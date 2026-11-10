# Batch: build-all-tasks

## Khi nào áp dụng
- Feature đã có `tasks.md` và G3 đã duyệt (hoặc tắt).
- Muốn build hết task ngoài giờ, không người trông.

## Cỡ mặc định
M hoặc L (cỡ S chạy tay nhanh hơn).

## Chuỗi
Chế độ `decide` bắt buộc. Không dùng `--bare` (hook phải chạy, ADJ-03).
1. `/team:build <ID> --decide` → tech-lead → dev, reviewer cho từng task chưa tick.
2. Hết task hoặc gặp điểm dừng → ghi kết quả.

```bash
claude -p "/team:build FEAT-012 --decide" \
  --agent team:team-leader --permission-mode dontAsk \
  --allowedTools "$(jq -r '["Read","Grep","Glob","Edit","Write","Agent","Skill"] + (.permissions.allow // []) | join(",")' .claude/settings.json)" \
  --max-turns 200 --max-budget-usd 20 --output-format json \
  > docs/team/metrics/batch-build-FEAT-012.json
```
`--allowedTools` lấy từ `permissions.allow` mà onboard ghi (có các khe `cmd.*`): thư mục chưa được tin (CI, máy mới) thì `-p` bỏ qua `permissions.allow`, nên phải truyền lại bằng cờ (K-06). Mẫu GitHub Actions đầy đủ: `templates/project/github/workflows/team-feature.yml`.

## Cổng
Không vượt cổng nào. G4 trở đi chờ người.

## Điểm dừng
- Mọi điểm dừng của `/team:build`; hết `--max-turns` hoặc `--max-budget-usd`.

## Tiêu chí xong
Sáng hôm sau người đọc: `/team:status`, `tasks.md` (task đã tick), `review-NN.md`, `docs/team/journal/<ID>.md`, và JSON kết quả (`subtype`, `total_cost_usd`).

## Lỗi thường gặp
- Chạy khi plan chưa duyệt.
- Ngân sách quá thấp làm dừng giữa task.

## Playbook liên quan
`new-feature`, `batch/verify-all.md`.
