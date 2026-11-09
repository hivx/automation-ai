---
name: build
description: Dùng khi plan đã duyệt (hoặc việc cỡ S, bug-fix, hotfix) và cần dev viết test, code, reviewer chấm, rồi gộp từng task vào nhánh feature.
argument-hint: "<ID> [--task T<N>] [--decide]"
context: fork
agent: team:tech-lead
background: false
allowed-tools: Bash(python3 *) Bash(cat *) Bash(git *) Bash(touch .team/active-build) Bash(rm .team/active-build)
---

## Mục đích
Chạy vòng build: dev → reviewer → sửa → gộp, tới khi mọi task tick.

## Đầu vào
- `$ARGUMENTS`: mã `<ID>`; `--task T<N>` để chạy một task.
- `tasks.md`, `design.md`, `.team/profile.json`, `.team/config.json` (`limits.*`). `<kit>` = nội dung `.team/plugin_root`.

## Điều kiện trước
G3 đã duyệt (khi bật). Cỡ S, bug-fix, hotfix không có `tasks.md` → tạo `tasks.md` một task từ `spec.md`. Kiểm: `python3 "$(cat .team/plugin_root)/scripts/team.py" status <ID>`.

## Các bước
1. `touch .team/active-build`; ghi `.team/current.json` {feature, stage: "build", agent: "tech-lead", started_at}.
2. Chọn task chưa tick, phụ thuộc đã xong; không song song hai task chung file; ≤ `limits.max_parallel_dev`.
3. Gọi dev (Agent, `team:dev`): mã task, tiêu chí, touchpoints, `cmd.test_one`, nhánh `team/<ID>-task-N`, "chỉ sửa trong touchpoints".
4. Kiểm tin trả của dev có đầu ra đỏ rồi xanh; thiếu → trả lại (tính một lần thử).
5. Gọi reviewer (Agent, `team:reviewer`) với diff + `design.md`.
6. `request-changes` → dev sửa blocker/major; đếm vòng; > `limits.max_rework` hoặc hai vòng cùng lỗi → dừng.
7. `design-defect` hoặc `DESIGN_CONFLICT` → dừng, báo team-leader.
8. `approve` → gộp vào `team/<ID>` (git), chạy `cmd.test`; đỏ → dừng. Xanh → tick task, viết `review-NN.md` từ `<kit>/templates/artifacts/review.md`.
9. Task BLOCKED sau `limits.max_attempts` → dừng.
10. Hết task → chạy `git diff <config.base_branch>...team/<ID>` và ghi đầu ra vào `docs/team/features/<ID>/diff.patch` bằng Write (cho writer).
11. Ở MỌI lối ra (xong hay dừng) → `rm .team/active-build`.

## Đầu ra
- Commit trên `team/<ID>`; `tasks.md` đã tick; `review-NN.md`.
- Tin trả ≤ 10 dòng: task tick / còn lại, đầu ra `cmd.test`, số vòng rework, lý do dừng nếu có.

## Tiêu chí xong
- Mọi task tick, mỗi task có `review-NN.md` approve.
- `cmd.test` xanh trên `team/<ID>` — dán lệnh và đầu ra; `.team/active-build` đã xóa.

## Dấu hiệu sai
- "Nhỏ, khỏi reviewer" → luôn gọi.
- "Test đỏ không liên quan, gộp" → dừng.
- "Tôi sửa luôn cho dev" → trả dev.
- "Quên xóa active-build khi dừng" → xóa ở mọi lối ra.

## Lệnh tiếp theo
`/team:verify <ID>`; khi dừng: in lý do, task, ai làm gì, `/team:build <ID> --task T<N>`.
