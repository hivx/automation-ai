# Plan self-review (5 points) and the interface block template

## The 5 points — do them before returning
| # | Point | How to check | If it fails |
|---|---|---|---|
| 1 | Spec coverage | Every `AC-n` in spec.md appears in at least one task | Add a task, or add the criterion to the owning task |
| 2 | No vague words | Search plan/tasks for "TBD", "handle edge cases", "as needed", "etc." | Replace with a file name, a test name, a value |
| 3 | Consistent names | The function/field/route names in the `Returns:` of an earlier task match the `Receives:` of the later task | Fix it in one place and record it under Shared constraints |
| 4 | Review focus | ≤ 5 edge inputs/failure modes, each with a test | Add the test to the owning task |
| 5 | Proportion | plan.md + tasks.md are shorter than the expected code | Remove pasted code, keep the decisions |

## Template of one complete task
```
- [ ] T3 — Reject expired OTP codes — files: src/auth/otp.py, tests/auth/test_otp.py — test: tests/auth/test_otp.py — depends: T2
  - Criterion: AC-2 (a code older than 5 minutes returns error 401)
  - Receives: `verify_code(user_id: str, code: str, now: datetime) -> bool` (from T2)
  - Returns: `OtpExpired` (new exception, used in T4)
  - Expect: `cmd.test_one` with tests/auth/test_otp.py → test_expired passes
```

## The one-file-one-owner table (plan.md)
| File | Owning task | Other tasks touching it | Order |
|---|---|---|---|
| src/auth/otp.py | T2 | T3 | T2 → T3 |
