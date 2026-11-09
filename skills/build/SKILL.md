---
name: build
description: Dùng khi plan đã duyệt (hoặc việc cỡ S, bug-fix, hotfix) và cần dev viết test, code, reviewer chấm, rồi gộp từng task vào nhánh feature.
argument-hint: "<ID> [--task T<N>] [--decide]"
context: fork
agent: team:tech-lead
background: false
allowed-tools: Bash(python3 *) Bash(cat *) Bash(git *) Bash(touch .team/active-build) Bash(rm .team/active-build)
---

# Vòng build: dev → reviewer → sửa → gộp

## Tổng quan
Skill này chạy vòng xây dựng của một feature cho tới khi mọi task trong `tasks.md` được tick: dev (worktree riêng) viết test hỏng trước rồi code; reviewer (ngữ cảnh mới, chỉ đọc) chấm theo Review checklist (10); dev sửa blocker/major; tech-lead gộp nhánh task vào `team/<ID>` và chạy `cmd.test`. Skill chạy trong ngữ cảnh `tech-lead` (fork); tech-lead chỉ gọi `team:dev`, `team:reviewer` và Explore.

Luật không đổi theo cỡ: **cỡ S vẫn đi qua skill này với 1 dev + 1 reviewer** (K-34). Không ai nói "xong" khi chưa có đầu ra lệnh thật. `.team/active-build` bật ở đầu và xóa ở MỌI lối ra; hook `stop-check.sh` đọc nó để chạy lint/test khi dev và tech-lead dừng.

`$ARGUMENTS`: mã `<ID>`; `--task T<N>` để chạy một task; `--decide`. `<kit>` = nội dung `.team/plugin_root`.

## Khi nào dùng (và khi nào không)
Dùng khi:
- Plan đã có và G3 qua (hoặc không áp dụng theo `team.py`).
- Cỡ S, bug-fix, hotfix có `spec.md` (hoặc intake mô tả lỗi) mà chưa có `tasks.md` → tạo `tasks.md` một task rồi chạy.
- qa trả `rework` → chạy lại đúng task trượt bằng `--task T<N>`.

Không dùng khi:
- Còn cổng chờ duyệt trước build → dừng, in cổng.
- Việc là dọn dẹp không đổi hành vi → `/team:clean`.
- Việc là sửa CI → `/team:ci`.

## Tìm hiểu stack trước
1. Read `.team/profile.json`: `cmd.test_one`, `cmd.test`, `cmd.lint`, `cmd.typecheck`, `naming.test_file`, `naming.branch`, `structure.allowed_new_file_roots`, `protected_paths`. Thiếu `cmd.test_one` → dừng, báo (không đoán lệnh).
2. Read `.team/config.json`: `base_branch`, `limits.max_parallel_dev`, `limits.max_rework`, `limits.max_attempts`, `limits.max_agents_per_feature`.
3. Resume từ đĩa: `.team/active-build` đã có → đọc `tasks.md` và `git log --oneline <base_branch>..team/<ID>` TRƯỚC mọi việc; task đã tick không làm lại.

## Đầu vào và điều kiện trước
- `python3 "$(cat .team/plugin_root)/scripts/team.py" status <ID>`: không `WAITING_FOR_APPROVAL` cho cổng trước build.
- `tasks.md` với dòng `- [ ] T<N> — … — files: … — test: … — depends: …`; cỡ S chưa có → Write một task từ `spec.md` (files = touchpoints trong spec/intake, test = file test theo `naming.test_file`).
- `design.md` (cỡ M/L) để reviewer đối chiếu.
- Nhánh `team/<ID>` tồn tại (tạo từ `base_branch` nếu thiếu).

## Quy trình
1. **Bật build.** `touch .team/active-build`; Write `.team/current.json` {feature, stage: "build", agent: "tech-lead", started_at}.
2. **Kiểm trước khi gọi ai (preflight).** Lập bảng mỗi cặp task chạm chung file hay giao diện; task tự mâu thuẫn (test của nó không khớp touchpoints); task bắt làm điều Review checklist coi là lỗi. Có vấn đề → `DESIGN_CONFLICT` về team-leader, chưa gọi dev.
3. **Chọn task.** Task chưa tick, `depends:` đã tick; không song song hai task chung file; ≤ `limits.max_parallel_dev`.
4. **Ghi BASE.** `git rev-parse team/<ID>` → ghi `BASE=<sha>` vào dòng tiến độ của task trong `tasks.md` (Edit). Diff cho reviewer luôn là `BASE..<đầu nhánh task>`, không bao giờ `HEAD~1`.
5. **Gọi dev** (Agent `team:dev`), tin ≤ 10 dòng: mã task; tiêu chí (trích); touchpoints; `cmd.test_one` với `{file}` là file test; nhánh `team/<ID>-task-N` tạo từ `team/<ID>`; câu "chỉ sửa trong touchpoints"; nơi ghi báo cáo chi tiết. Mẫu tin: `${CLAUDE_SKILL_DIR}/references/handoffs.md`.
6. **Đọc trạng thái dev** — dòng đầu của tin trả là một trong `DONE`, `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, `BLOCKED`, `DESIGN_CONFLICT` (điểm quyết định):
   - `DONE`: kiểm có đầu ra ĐỎ đúng lý do (thiếu hành vi, không phải lỗi import/cú pháp) và XANH sau; có `cmd.test` đầy đủ; thiếu → trả lại dev (tính một lần thử).
   - `DONE_WITH_CONCERNS`: lo ngại về tính đúng hay phạm vi → giải quyết trước review; lo ngại khác → ghi vào review.
   - `NEEDS_CONTEXT`: bổ sung ngữ cảnh rồi gọi lại; không gửi lại tin cũ y nguyên.
   - `BLOCKED`: đổi một điều (thêm ngữ cảnh, tách task, báo kế hoạch sai); sau `limits.max_attempts` → dừng.
   - `DESIGN_CONFLICT`: dừng, báo team-leader.
7. **Gói review.** Write `docs/team/features/<ID>/review-pkg-T<N>.md`: danh sách commit, `git diff --stat` và `git diff BASE..team/<ID>-task-N`. Reviewer đọc một file.
8. **Gọi reviewer** (Agent `team:reviewer`): đường dẫn gói review, `design.md`, tiêu chí task, câu "chấm theo Review checklist (10)". Không kèm lời giải thích của dev; không dặn "đừng bắt lỗi X".
9. **Đọc phán quyết** — `approve` / `request-changes` / `design-defect`, kèm danh sách "không kiểm chứng được từ diff":
   - `design-defect` → dừng, báo team-leader.
   - Mục "không kiểm chứng được" → tech-lead (nắm bối cảnh nhiều task) giải quyết trước khi tick; thiếu thật → coi như trượt review.
10. **Vòng sửa** (`request-changes`): gửi dev các phát hiện blocker/major nguyên văn + đường dẫn review; dev mới nằm ở worktree mới nên phải `git switch team/<ID>-task-N` trong worktree của mình (K-14). Báo cáo sửa phải có: phát hiện → thay đổi → test phủ → lệnh + đầu ra. Gọi reviewer lại ở chế độ **xem lại có phạm vi**: chỉ diff sửa (`FIX_BASE..HEAD`), mỗi phát hiện cũ `ADDRESSED` / `NOT ADDRESSED`; ghi chú ngoài phạm vi vào `deferred`, không kéo dài vòng.
11. **Ngắt vòng.** Đếm vòng; > `limits.max_rework`, hoặc hai vòng cùng một lỗi → dừng; ghi cho từng phát hiện còn mở một phán định (reviewer sai / thật nhưng hoãn / chặn) và leo thang về team-leader. Vòng cuối trước trần có thể dùng một dev mới với báo cáo cũ làm đầu vào.
12. **Gộp và tick** (`approve`): gộp `team/<ID>-task-N` vào `team/<ID>` (git), chạy `cmd.test` trên `team/<ID>`. Đỏ → xác định do gộp hay do task trước khi làm gì khác; không tick. Xanh → tick task (`- [x] T<N>`), Write `review-NN.md` từ `<kit>/templates/artifacts/review.md` (phán quyết, phát hiện, số vòng, lệnh diff, mục `deferred`), ghi một dòng journal.
13. **Lặp** bước 3 cho task tiếp theo.
14. **Hết task.** Chạy `git diff <base_branch>...team/<ID>` và ghi đầu ra vào `docs/team/features/<ID>/diff.patch` bằng Write (cho writer). Ghi số vai đã dùng (vai khác nhau, không tính lần gọi lại trong vòng sửa) so với `limits.max_agents_per_feature`.
15. **Mọi lối ra** (xong, dừng, lỗi): `rm .team/active-build`.

## Đầu ra
- Commit trên `team/<ID>`; `docs/team/features/<ID>/tasks.md` đã tick; `review-NN.md` cho mỗi task; `diff.patch`.
- Một dòng journal cho mỗi lần gọi dev/reviewer (lý do trước khi gọi, kết quả sau).
- Tin trả team-leader ≤ 10 dòng:
  ```
  tech-lead -> team-leader | FEAT-012 | DONE
  Task tick: T1..T4 (review-01..04 approve). Vai dùng: dev, reviewer (trần M: 6)
  Rework: T3 hai vòng (max_rework=3), vòng 2 sạch
  cmd.test trên team/FEAT-012: exit 0, "Ran 42 tests … OK"
  Deferred (minor): review-03 STD-NAME-2
  File: docs/team/features/FEAT-012/{tasks,review-01..04,diff.patch}
  Tiếp: /team:verify FEAT-012
  ```

## Lý do tự bào chữa thường gặp
| Ý nghĩ | Làm đúng |
|---|---|
| "Cỡ S, sửa một dòng, khỏi reviewer" | Vẫn gọi `team:reviewer` (K-34). |
| "Dev nói test xanh" | Cần đầu ra đỏ rồi xanh được dán; thiếu thì trả lại. |
| "Đỏ vì lỗi import cũng là đỏ" | Đỏ phải vì thiếu hành vi; trả dev sửa test. |
| "Test đỏ chập chờn, không liên quan, gộp đi" | Dừng: tái hiện, ghi `debt.md` (STD-TEST-7); không gộp. |
| "Sửa ba dòng, tôi tự làm cho nhanh" | Trả dev; tech-lead chỉ ghi `docs/team/**`. |
| "Thêm một vòng sửa là xong" | Quá `max_rework` hoặc cùng lỗi hai lần: dừng, leo thang. |
| "Reviewer bắt bẻ, bỏ phát hiện đó" | Chỉ phán định ở trần, có ghi lại; không âm thầm bỏ. |
| "HEAD~1 là diff của task" | Dùng `BASE..đầu nhánh task` đã ghi. |
| "Tôi nhớ task 3 làm gì rồi" | Đọc lại dòng task và `git log`; tick trên đĩa là sự thật. |
| "Gọi qa luôn cho tiện" | tech-lead chỉ gọi dev, reviewer, Explore. |

## Dấu hiệu sai
- Test xanh ngay lần chạy đầu, hoặc không có đầu ra đỏ.
- Tin trả của dev không có lệnh, hoặc có "chắc là chạy".
- Diff chạm file ngoài touchpoints, hoặc `.team/profile.json`/`config.json`.
- Hai task đang chạy cùng chạm một file.
- `review-NN.md` approve mà không có lệnh diff hay phán quyết tầng 1.
- Cùng một phát hiện xuất hiện ở hai vòng liên tiếp.
- Task được tick mà không có commit gộp trên `team/<ID>`; `.team/active-build` còn lại sau khi dừng.
- Cỡ S chỉ có lần gọi dev, không có reviewer.

## Kiểm chứng
- [ ] Mỗi task: đầu ra đỏ (tên assertion trượt) và xanh của `cmd.test_one` được dán.
- [ ] `cmd.test` trên `team/<ID>` sau lần gộp cuối: exit 0, dán đầu ra.
- [ ] `git log --oneline <base_branch>..team/<ID>` được dán; mỗi commit dạng `type(scope): description (<ID>)`.
- [ ] `git diff --name-only` mỗi task là tập con của touchpoints.
- [ ] Mỗi task có `review-NN.md` với phán quyết, lệnh diff, số vòng; vòng sửa có ADDRESSED/NOT ADDRESSED.
- [ ] `ls .team/active-build` báo không có file; `diff.patch` có và khác rỗng.

## Xem thêm
- `${CLAUDE_SKILL_DIR}/references/handoffs.md` — mẫu tin gọi dev, reviewer, vòng sửa; bảng trạng thái.
- Agent `tech-lead`, `dev`, `reviewer`; `<kit>/templates/artifacts/review.md`, `tasks.md`.
- `/team:plan` (trước), `/team:verify` (sau), `/team:commit` (dev dùng).
- `handbook/STD.md`: Review checklist (10), STD-TEST-1/4/5, STD-DESIGN-1, STD-GIT-3/4.
