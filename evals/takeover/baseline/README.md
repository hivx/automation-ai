# Baseline — takeover without the skill

Run the scenario on a copy of the sample project, using a copy of the kit with the `skills/takeover` folder REMOVED; the input is a natural-language sentence ("Baseline input" in `../scenarios.md`), not the `/team:takeover` command.

```bash
evals/run-eval.sh takeover <n> --project <sample-project> --mode baseline
```
The script builds the kit copy itself (tar excluding `skills/takeover`), runs `claude -p --plugin-dir <copy> --max-turns/--max-budget-usd` as set in `evals/config.json`, and saves the results to `evals/takeover/out/<date>/s<n>-baseline/`.
