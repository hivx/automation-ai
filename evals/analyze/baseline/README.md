# Baseline — analyze without the skill

Run the scenario on a copy of the sample project, using a copy of the kit with the `skills/analyze` folder REMOVED; the input is a natural-language sentence ("Baseline input" in `../scenarios.md`), not the `/team:analyze` command.

```bash
evals/run-eval.sh analyze <n> --project <sample-project> --mode baseline
```
The script builds the kit copy itself (tar excluding `skills/analyze`), runs `claude -p --plugin-dir <copy> --max-turns/--max-budget-usd` as set in `evals/config.json`, and saves the results to `evals/analyze/out/<date>/s<n>-baseline/`.
