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
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "/team:retro --decide"
          claude_args: "--max-turns 60 --max-budget-usd 5"
```
Bước cài plugin và mở PR kết quả: `templates/project/github/workflows/team-ci.yml`.

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
