# Acceptance evidence

## What a claim needs
| Claim | Needs | Not enough |
|---|---|---|
| "Tests pass" | `cmd.test` output on the recorded commit, 0 failures, exit code 0 | An earlier run, old CI, the dev's word |
| "The build is fine" | `cmd.build` exit code 0 | Lint passing |
| "The bug is fixed" | A test reproducing the original symptom: red before the fix (pasted by the dev), green now | A new test that has only ever been green |
| "Criterion AC-n passes" | The command in the "how to check" column + output matching the expectation | Reading the code and finding it right |
| "The migration is safe" | Up → down → up all exit 0, counts reconcile | The up direction only |
| "The docs are correct" | The commands/steps in the README run and match the behavior | The README mentions it |

## Evidence row
`AC-2 | <cmd.test_one tests/auth/test_otp.py> | exit 1 | AssertionError: 200 != 401 | tests/auth/test_otp.py::test_expired | fail`

## Classify the failure before concluding
| Kind | Sign | Verdict |
|---|---|---|
| Wrong code | The test matches the criterion, the code returns the wrong thing | rework (owning task) |
| Wrong test | The test checks something other than the criterion, or can never fail | rework (STD-TEST-5) |
| Flaky | Same commit, different results across 3 runs | rework + `debt.md` (STD-TEST-7) |
| Environment | The command cannot run (missing service, permissions) | BLOCKED, no conclusion |
| Design | The code matches the design, the design does not satisfy the criterion | design-defect |

## Acceptance checklist (6) — quote it verbatim from handbook/STD.md when grading
Record each item: pass / fail + STD code.
