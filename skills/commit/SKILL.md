---
name: commit
description: Dùng khi dev hoặc maintainer đã có thay đổi xanh và cần commit đúng chuẩn của đội.
argument-hint: "[<ID>] [--task T<N>]"
allowed-tools: Bash(git status *) Bash(git diff *) Bash(git add *) Bash(git commit *) Bash(git restore *) Bash(git log *)
---

## Mục đích
Commit nhỏ, đúng ý định, đúng định dạng STD-NAME-5.

## Đầu vào
- `$ARGUMENTS`: mã `<ID>`, task `T<N>`.
- Touchpoints của task (tin giao việc hoặc `tasks.md`).

## Điều kiện trước
`cmd.test_one` và `cmd.lint` vừa xanh trong phiên này (đầu ra đã có). Chưa có → chạy trước.

## Các bước
1. `git status --short` và `git diff` (Bash).
2. Bỏ khỏi commit mọi file ngoài touchpoints (`git restore --staged`); file đó là dấu hiệu `DESIGN_CONFLICT` → báo tech-lead.
3. Xóa log gỡ lỗi, code comment-out, file tạm trong diff (STD-STYLE-5).
4. Không có dấu trong `test.skip_markers` mới thêm (Grep diff).
5. Tách theo ý định: test + code của một hành vi một commit; đổi tên/định dạng thuần thì commit riêng.
6. Message: `type(scope): description (<ID>)`; `type` ∈ feat, fix, refactor, test, docs, chore, ci, perf, build.
7. `git commit` — KHÔNG `--no-verify`, không `--amend` commit đã push.
8. `git log -1 --stat` để kiểm.

## Đầu ra
Một hoặc vài commit trên nhánh task.

## Tiêu chí xong
- `git log -1 --stat` được dán; message khớp định dạng; chỉ file trong touchpoints.

## Dấu hiệu sai
- "Hook commit chậm, `--no-verify`" → không bao giờ.
- "Gộp mọi thứ một commit" → tách theo ý định.
- "File ngoài touchpoints chỉ sửa nhỏ" → bỏ ra, báo.

## Lệnh tiếp theo
Trả tin cho tech-lead kèm đầu ra; hoặc `/team:pr <ID>` khi task là cuối cùng.
