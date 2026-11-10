# Baseline — using-team without the skill

Run the scenario on a copy of the sample project, using a copy of the kit with the `skills/using-team` folder REMOVED; the input is a natural-language sentence ("Baseline input" in `../scenarios.md`), not the `/team:using-team` command.

```bash
evals/run-eval.sh using-team <n> --project <sample-project> --mode baseline
```
The script builds the kit copy itself (tar excluding `skills/using-team`), runs `claude -p --plugin-dir <copy> --max-turns/--max-budget-usd` as set in `evals/config.json`, and saves the results to `evals/using-team/out/<date>/s<n>-baseline/`.
