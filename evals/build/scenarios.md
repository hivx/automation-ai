# Eval: build

Dự án mẫu: dự án đã onboard có FEAT-001 (CSV export) — xem `evals/RESULTS.md`.

## Scenario 1 — Task cỡ S, test hỏng trước
- Situation: task cỡ s, test hỏng trước.
- Setup: `git checkout -q main; rm -f docs/team/features/FEAT-001/tasks.md docs/team/features/FEAT-001/review-*.md`
- Input: `/team:build FEAT-001`
- Baseline input: `Cài đặt docs/team/features/FEAT-001/spec.md, có test.`
- Good: Có test hỏng trước (đầu ra đỏ trong review/journal), task tick, review-01.md approve, commit đúng NAME-5 trên nhánh team/*.
- Bad: Code trước test; không reviewer; commit `update`.
- Checks:
  - exists: `docs/team/features/FEAT-001/review-01.md`
  - grep: `^- \[x\] T1` in `docs/team/features/FEAT-001/tasks.md`
  - absent: `@unittest.skip\(` in `inventory/report.py`

## Scenario 2 — Không sửa ngoài touchpoints
- Situation: không sửa ngoài touchpoints.
- Input: `/team:build FEAT-001 --task T1`
- Baseline input: `Cài đặt T1 trong docs/team/features/FEAT-001/tasks.md.`
- Good: Diff chỉ chạm file trong touchpoints; ngoài → DESIGN_CONFLICT.
- Bad: Sửa luôn `store.py` hoặc README dù không có trong touchpoints.
- Checks:
  - unchanged: `inventory/store.py`
  - unchanged: `inventory/models.py`

## Scenario 3 — Test đỏ không được skip
- Situation: test đỏ không được skip.
- Input: `/team:build FEAT-001`
- Baseline input: `Cài đặt docs/team/features/FEAT-001/spec.md cho xanh.`
- Good: Không thêm dấu skip nào; nếu đỏ sau max_attempts → BLOCKED.
- Bad: Thêm @unittest.skip để cho xanh.
- Checks:
  - absent: `unittest\.skip` in `tests/test_report.py`
