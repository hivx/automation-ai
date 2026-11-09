# Eval: analyze

Dự án mẫu: dự án đã onboard có FEAT-001 (CSV export) — xem `evals/RESULTS.md`.

## Scenario 1 — Spec cỡ S ở chế độ decide
- Situation: spec cỡ s ở chế độ decide.
- Setup: `rm -f docs/team/features/FEAT-001/spec.md docs/team/features/FEAT-001/questions.md`
- Input: `/team:analyze FEAT-001 --decide`
- Baseline input: `Viết spec có Definition of Done cho docs/team/features/FEAT-001/intake.md, chế độ tự quyết.`
- Good: `spec.md` có 7 mục, `## Assumptions decided by the team`, `## Definition of Done`, tiêu chí đo được.
- Bad: Spec không có DoD, tiêu chí kiểu 'chạy tốt', hoặc chọn thư viện.
- Checks:
  - exists: `docs/team/features/FEAT-001/spec.md`
  - grep: `^## Definition of Done` in `docs/team/features/FEAT-001/spec.md`
  - grep: `^## Assumptions decided by the team` in `docs/team/features/FEAT-001/spec.md`
  - unchanged: `inventory`

## Scenario 2 — Chế độ ask với điểm lớn chưa rõ
- Situation: chế độ ask với điểm lớn chưa rõ.
- Setup: `rm -f docs/team/features/FEAT-001/spec.md; sed -i 's/Chế độ: decide.*/Chế độ: ask/' docs/team/features/FEAT-001/intake.md`
- Input: `/team:analyze FEAT-001`
- Baseline input: `Viết spec cho docs/team/features/FEAT-001/intake.md; hỏi nếu có điều lớn chưa rõ.`
- Good: Hoặc spec đủ DoD, hoặc `questions.md` ≤ 5 câu có lựa chọn + khuyến nghị và trạng thái NEEDS_ANSWER; không hỏi điều code đã trả lời.
- Bad: Hỏi > 5 câu, hỏi điều README/code đã nói rõ (header CSV).
- Checks:
  - absent: `(header|tiêu đề cột).*\?` in `docs/team/features/FEAT-001/questions.md`

## Scenario 3 — Amend spec đã duyệt
- Situation: amend spec đã duyệt.
- Setup: `printf '\n' >> docs/team/features/FEAT-001/spec.md`
- Input: `/team:analyze FEAT-001 --amend "Thêm cột currency"`
- Baseline input: `Sửa spec docs/team/features/FEAT-001/spec.md: thêm cột currency.`
- Good: Thêm `## Amendment 1`, đánh dấu [changed]; tiêu chí cũ vẫn còn.
- Bad: Sửa thẳng tiêu chí cũ, không có mục amendment.
- Checks:
  - grep: `^## Amendment` in `docs/team/features/FEAT-001/spec.md`
  - grep: `\[changed\]` in `docs/team/features/FEAT-001/spec.md`
