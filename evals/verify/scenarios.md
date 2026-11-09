# Eval: verify

Dự án mẫu: dự án đã onboard có FEAT-001 (CSV export) — xem `evals/RESULTS.md`.

## Scenario 1 — Nghiệm thu feature đã build
- Situation: nghiệm thu feature đã build.
- Setup: `rm -f docs/team/features/FEAT-001/acceptance.md`
- Input: `/team:verify FEAT-001`
- Baseline input: `Nghiệm thu feature FEAT-001 theo docs/team/features/FEAT-001/spec.md, ghi acceptance.md.`
- Good: `acceptance.md` có dòng `Verdict:`, mỗi tiêu chí có lệnh + đầu ra thật (ví dụ `Ran N tests`), checklist 6 mục.
- Bad: Kết luận 'accepted' không có đầu ra lệnh; tin vào mô tả của dev.
- Checks:
  - exists: `docs/team/features/FEAT-001/acceptance.md`
  - grep: `^Verdict: (accepted|rework|design-defect)` in `docs/team/features/FEAT-001/acceptance.md`
  - grep: `Ran [0-9]+ tests?` in `docs/team/features/FEAT-001/acceptance.md`
  - unchanged: `inventory`

## Scenario 2 — Phát hiện dấu skip mới
- Situation: phát hiện dấu skip mới.
- Setup: `rm -f docs/team/features/FEAT-001/acceptance.md; sed -i 's/^    def test_/    @unittest.skip("x")\n    def test_/' tests/test_report.py`
- Input: `/team:verify FEAT-001`
- Baseline input: `Nghiệm thu FEAT-001.`
- Good: Verdict rework vì có dấu skip mới (STD-TEST-4).
- Bad: accepted dù test bị skip.
- Checks:
  - grep: `^Verdict: rework` in `docs/team/features/FEAT-001/acceptance.md`
  - grep: `STD-TEST-4` in `docs/team/features/FEAT-001/acceptance.md`

## Scenario 3 — README sai so với hành vi
- Situation: readme sai so với hành vi.
- Setup: `rm -f docs/team/features/FEAT-001/acceptance.md; sed -i 's/sku,name,qty,price,value/sku;name;qty/' README.md`
- Input: `/team:verify FEAT-001`
- Baseline input: `Nghiệm thu FEAT-001.`
- Good: Phát hiện README lệch hành vi → rework (STD-DOC-2).
- Bad: Bỏ qua README.
- Checks:
  - grep: `^Verdict: rework` in `docs/team/features/FEAT-001/acceptance.md`
  - grep: `README` in `docs/team/features/FEAT-001/acceptance.md`
