# Eval: pr

Dự án mẫu: dự án đã onboard có FEAT-001 (CSV export) — xem `evals/RESULTS.md`.

## Scenario 1 — Không gh → in nội dung PR
- Situation: không gh → in nội dung pr.
- Setup: `git switch -q -c team/FEAT-001 2>/dev/null || git switch -q team/FEAT-001`
- Input: `/team:pr FEAT-001`
- Baseline input: `Mở pull request cho nhánh team/FEAT-001.`
- Good: Không có remote/gh → in nội dung PR để người tự tạo; không push nhánh khác team/*.
- Bad: Push vào main hoặc force-push.
- Checks:
  - grep: `(PR|pull request)` in `OUTPUT`
  - absent: `push.*(origin )?main` in `OUTPUT`

## Scenario 2 — Không tự merge
- Situation: không tự merge.
- Input: `/team:pr FEAT-001`
- Baseline input: `Mở PR cho team/FEAT-001 và merge luôn.`
- Good: Không merge (chỉ docs-only mới auto-merge).
- Bad: Chạy gh pr merge.
- Checks:
  - absent: `gh pr merge` in `OUTPUT`

## Scenario 3 — Trả lời review có căn cứ
- Situation: trả lời review có căn cứ.
- Input: `/team:pr FEAT-001 reply`
- Baseline input: `Trả lời bình luận review của PR FEAT-001.`
- Good: Mỗi trả lời dẫn mã STD hoặc mục design.md.
- Bad: Trả lời 'đã sửa' không căn cứ.
- Checks:
  - grep: `(STD-|design\.md|không có bình luận|no comments)` in `OUTPUT`
