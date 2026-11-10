# Batch: weekly-retro

## Khi nào áp dụng
- Hằng tuần, khi có ít nhất một feature hoặc góp ý mới trong tuần.

## Cỡ mặc định
Không áp dụng.

## Chuỗi
Chế độ `decide` bắt buộc; không `--bare`.
1. `/team:retro --decide` → coach → `docs/team/retro/<date>.md`, `docs/team/proposals/<date>/`.

```yaml
on:
  schedule:
    - cron: "0 1 * * 1"   # 08:00 thứ Hai giờ Việt Nam
jobs:
  retro:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - id: tools   # K-06: runner bỏ qua permissions.allow; truyền lại bằng --allowedTools
        run: echo "list=$(jq -r '["Read","Grep","Glob","Write","Agent","Skill"] + (.permissions.allow // []) | join(",")' .claude/settings.json)" >> "$GITHUB_OUTPUT"
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          plugin_marketplaces: "https://github.com/<owner>/automation-ai.git"
          plugins: "team@automation-ai"
          claude_args: "--max-turns 60 --max-budget-usd 5 --allowedTools '${{ steps.tools.outputs.list }}'"
          prompt: "/team:retro --decide"
```
Cách cài plugin và quyền cho job: như `templates/project/github/workflows/team-feature.yml`. Kết quả (`docs/team/retro/`, `proposals/`) được commit lên nhánh `team/retro-<date>` và mở PR bằng tay hoặc bằng bước `gh pr create` thêm vào job.

## Cổng
Đề xuất chỉ là ghi chú chờ duyệt; không áp gì.

## Điểm dừng
- Thiếu số liệu; hết ngân sách.

## Tiêu chí xong
Sáng thứ Hai người đọc `docs/team/retro/<date>.md` và từng file đề xuất, rồi duyệt hoặc bỏ.

## Lỗi thường gặp
- Tự áp overlay trong job định kỳ.

## Playbook liên quan
`retro`.
