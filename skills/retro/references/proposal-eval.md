# Eval and canary for a proposal

## An eval that discriminates
Same format as `evals/<skill>/scenarios.md`, so that `evals/run-eval.sh` can run it:
```markdown
## Scenario 1 — <the situation that caused the bottleneck>
- Situation: <cite journal/runs.jsonl>
- Input: `<the /team:… command with the proposed version>`
- Baseline input: `<the same command>`  (BEFORE = current kit, AFTER = kit + overlay)
- Good: <expected result>
- Bad: <what actually happened>
- Checks:
  - grep: `<regex>` in `<file|OUTPUT>`
  - exists: `<path>`
```
Rules:
- ≥ 3 scenarios: the original situation, one variant, one control (a job the current version already does right — it must stay right).
- At least one check that the current version FAILS and the proposed version PASSES. A check that passes on both versions is marked "does not discriminate" — it does not count as evidence.
- Checks are about content, not just "the file exists" (an empty file exists too).
- Wording changes (prompt): ≥ 3 runs per version; the spread is itself a metric.
- coach does not run the eval (read-only Bash): write "run by: <the human or the kit maintainer>", with the command `EVAL_KIT=<kit with overlay> evals/run-eval.sh <skill> <n> --project <sample project>`.

## Canary
| Item | What to record |
|---|---|
| Scope | the next N size S jobs (N = 3 by default; low confidence → 2, and watch closely) |
| Measure | the bottleneck's metric (turns, rework, time) via `measure.py --since <date applied>` against the baseline median of the same size |
| Keep | the metric is better than the baseline and no other metric is worse by more than 1 MAD |
| Rollback | the metric is worse than the baseline, or a canary job broke because of the change |
| Replace | better on the target metric but worse on another → propose a different version |
| Remove | no difference after N jobs → remove the overlay (simpler is better) |
| How to roll back | delete the overlay file (path), or restore the previous version (the version recorded in the first line) |

The next retro reads the canary result in its "follow up the previous retro" step and records a recommendation; the human decides.
