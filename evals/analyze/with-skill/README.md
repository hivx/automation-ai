# With skill — analyze

```bash
evals/run-eval.sh analyze <n> --project <sample-project> --mode with-skill
```
The actual command that runs (printed by `--dry-run`):
```bash
claude -p --plugin-dir <kit> --model <config.model> --permission-mode acceptEdits \
  --allowedTools=<config.allowed_tools>,Read(//<kit>/**) \
  --max-turns <config.max_turns> --max-budget-usd <config.max_budget_usd> --output-format json "<Input>"
```
Results: `evals/analyze/out/<date>/s<n>-with-skill/` (`result.json`, `output.txt`, `work/`).
