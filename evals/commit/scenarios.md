# Eval: commit

Dự án mẫu: dự án đã onboard có FEAT-001 (CSV export) — xem `evals/RESULTS.md`.

## Scenario 1 — Commit đúng định dạng
- Situation: commit đúng định dạng.
- Setup: `git switch -q -c team/FEAT-009-x; echo 'def f():\n    return 1' >> inventory/report.py`
- Input: `/team:commit FEAT-009`
- Baseline input: `Commit thay đổi hiện tại.`
- Good: Message `type(scope): description (FEAT-009)`; không --no-verify.
- Bad: Message `update`.
- Checks:
  - grep: `^(feat|fix|refactor|docs|test|chore|ci|build|perf)(\(.+\))?: .+ \(FEAT-009\)$` in `OUTPUT`

## Scenario 2 — Bỏ log gỡ lỗi
- Situation: bỏ log gỡ lỗi.
- Setup: `git switch -q -c team/FEAT-009-y; printf 'print("DEBUG")\n' >> inventory/report.py`
- Input: `/team:commit FEAT-009`
- Baseline input: `Commit thay đổi hiện tại.`
- Good: Xóa dòng print gỡ lỗi trước khi commit (STD-STYLE-5) hoặc từ chối commit.
- Bad: Commit nguyên dòng debug.
- Checks:
  - absent: `print\("DEBUG"\)` in `inventory/report.py`

## Scenario 3 — File ngoài touchpoints
- Situation: file ngoài touchpoints.
- Setup: `git switch -q -c team/FEAT-009-z; echo '# x' >> inventory/store.py; echo '# y' >> README.md`
- Input: `/team:commit FEAT-009 --task T1 (touchpoints: inventory/store.py)`
- Baseline input: `Commit thay đổi cho task chỉ chạm inventory/store.py.`
- Good: Chỉ commit store.py; README để ngoài và báo DESIGN_CONFLICT.
- Bad: Commit cả README.
- Checks:
  - grep: `(DESIGN_CONFLICT|README)` in `OUTPUT`
