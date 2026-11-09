# Eval: make-skill

Dự án mẫu: dự án đã onboard có FEAT-001 (CSV export) — xem `evals/RESULTS.md`.

## Scenario 1 — Có nhu cầu thật
- Situation: có nhu cầu thật.
- Input: `/team:make-skill csv-format "Định dạng CSV của dự án dùng lặp lại cho mọi export"`
- Baseline input: `Tạo một skill cho định dạng CSV của dự án.`
- Good: `.claude/skills/csv-format/SKILL.md` có 8 mục, dòng temp, `references/tests.md`, registry có dòng.
- Bad: Skill không có ca thử, không đăng ký.
- Checks:
  - exists: `.claude/skills/csv-format/SKILL.md`
  - exists: `.claude/skills/csv-format/references/tests.md`
  - grep: `csv-format` in `docs/team/skills-registry.md`
  - grep: `team: temp` in `.claude/skills/csv-format/SKILL.md`

## Scenario 2 — Trùng skill có sẵn
- Situation: trùng skill có sẵn.
- Input: `/team:make-skill verify-again "Nghiệm thu feature bằng lệnh thật"`
- Baseline input: `Tạo skill nghiệm thu feature.`
- Good: Từ chối: trùng `/team:verify`.
- Bad: Tạo skill trùng.
- Checks:
  - grep: `(trùng|verify|từ chối)` in `OUTPUT`
  - absent: `verify-again` in `docs/team/skills-registry.md`

## Scenario 3 — Không có nhu cầu
- Situation: không có nhu cầu.
- Input: `/team:make-skill misc`
- Baseline input: `Tạo vài skill dự phòng cho sau này.`
- Good: Từ chối vì không có nhu cầu một câu.
- Bad: Tạo skill sẵn.
- Checks:
  - grep: `(nhu cầu|từ chối)` in `OUTPUT`
