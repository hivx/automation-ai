# Baseline — commit without the skill

Run the scenario on a copy of the sample project, using a copy of the kit with the `skills/commit` folder REMOVED; the input is a natural-language sentence ("Baseline input" in `../scenarios.md`), not the `/team:commit` command.

```bash
evals/run-eval.sh commit <n> --project <sample-project> --mode baseline
```
The script builds the kit copy itself (tar excluding `skills/commit`), runs `claude -p --plugin-dir <copy> --max-turns/--max-budget-usd` as set in `evals/config.json`, and saves the results to `evals/commit/out/<date>/s<n>-baseline/`.
