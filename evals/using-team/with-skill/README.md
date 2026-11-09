# With skill — using-team

```bash
evals/run-eval.sh using-team <n> --project <dự-án-mẫu> --mode with-skill
```
Lệnh thật được chạy (in ra bằng `--dry-run`):
```bash
claude -p --plugin-dir <kit> --model <config.model> --permission-mode acceptEdits \
  --allowedTools=<config.allowed_tools>,Read(//<kit>/**) \
  --max-turns <config.max_turns> --max-budget-usd <config.max_budget_usd> --output-format json "<Input>"
```
Kết quả: `evals/using-team/out/<ngày>/s<n>-with-skill/` (`result.json`, `output.txt`, `work/`).
