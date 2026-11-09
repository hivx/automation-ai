---
name: commit
description: Dùng khi dev hoặc maintainer đã có thay đổi xanh và cần commit đúng chuẩn của đội.
argument-hint: "[<ID>] [--task T<N>]"
allowed-tools: Bash(git status *) Bash(git diff *) Bash(git add *) Bash(git commit *) Bash(git restore *) Bash(git log *)
---

# Commit đúng chuẩn của đội

## Tổng quan
Skill này biến một thay đổi đã xanh thành một hoặc vài commit nhỏ, đúng ý định, đúng định dạng `type(scope): description (<ID>)` (STD-NAME-5), chỉ chứa file trong touchpoints. Người dùng skill là dev hoặc maintainer, chạy ngay trong worktree của họ (không fork). Commit là điểm lưu: mỗi commit phải hoàn tác được riêng mà dự án vẫn build và qua test (STD-GIT-2).

Hook `check-git.sh` chặn `--no-verify`, `-n` và force-push, và cảnh báo khi message sai định dạng; skill này làm phần hook không làm được: chọn file, tách ý định, viết message có nghĩa, quét secret trong phần đã stage.

`$ARGUMENTS`: mã `<ID>`, `--task T<N>`. Touchpoints lấy từ tin giao việc hoặc dòng task trong `docs/team/features/<ID>/tasks.md`.

## Khi nào dùng (và khi nào không)
Dùng khi:
- Dev vừa có `cmd.test_one` xanh và `cmd.lint` sạch cho task đang làm.
- Maintainer xong một loại dọn dẹp và đã có đầu ra `cmd.test` trước/sau giống nhau.
- Vòng sửa sau review: commit MỚI cho phần sửa (không amend commit đã gửi review).

Không dùng khi:
- Test còn đỏ, hoặc chưa chạy lại sau lần sửa cuối → chạy lại trước.
- Thay đổi chạm file ngoài touchpoints → dừng, `DESIGN_CONFLICT`.
- Muốn đẩy nhánh hay mở PR → `/team:pr` (tech-lead).
- Cần đổi lockfile → chỉ qua `cmd.install` trong task phụ thuộc (STD-DEP-2).

## Tìm hiểu stack trước
1. Read `.team/profile.json`: `cmd.test_one`, `cmd.lint`, `cmd.typecheck`, `test.skip_markers`, `protected_paths`, `naming.branch`.
2. `git branch --show-current` phải là nhánh task `team/<ID>-…` (worktree của chính mình, K-14). Sai nhánh → dừng, báo.
3. Danh sách loại commit: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `ci`, `perf`, `build`.

## Đầu vào và điều kiện trước
- Đầu ra `cmd.test_one` xanh và `cmd.lint` sạch có SAU lần sửa file cuối cùng. Có sửa sau đó → chạy lại.
- Touchpoints của task (danh sách đường dẫn).
- Cây làm việc không có xung đột gộp dở.

## Quy trình
1. **Nhìn toàn cảnh.** `git status --short` và `git diff` (Bash). Ghi danh sách file đã đổi.
2. **Lọc theo touchpoints.** File không thuộc touchpoints → không đưa vào commit (`git restore --staged <file>` nếu đã stage); ghi vào báo cáo dưới mục "Thấy nhưng không chạm" và trả `DESIGN_CONFLICT` nếu thay đổi đó là cần cho task. File thuộc `protected_paths`, `.env*`, lockfile, `.team/profile.json`, kết quả build → không bao giờ commit.
3. **Dọn diff.** Xóa log gỡ lỗi, code bị comment-out, file tạm, TODO mới không có mã task (STD-STYLE-5). Code mồ côi do thay đổi tạo ra → liệt kê trong báo cáo, không âm thầm xóa thứ ngoài touchpoints.
4. **Tách theo ý định (điểm quyết định).** Mỗi commit một ý: test + code của một hành vi → `feat`/`fix`; đổi tên hay định dạng thuần → `refactor`/`chore` riêng; tài liệu → `docs`. Định dạng do formatter ép trên file trong touchpoints thì đi cùng commit của file đó; định dạng lan sang file khác → hoàn tác.
5. **Stage có chủ đích.** `git add <đường dẫn cụ thể>` cho từng ý; không `git add -A`, không `git add .`.
6. **Xem phần đã stage.** `git diff --staged --name-only` (so với touchpoints) và `git diff --staged` (đọc lại từng dòng). Với từng hunk, trả lời được ba câu: hunk này phục vụ tiêu chí nào (`AC-n`)? test nào sẽ trượt nếu bỏ hunk này? hunk có làm đổi hợp đồng (chữ ký, tên trường, định dạng) mà plan không ghi không? Hunk không trả lời được câu đầu → bỏ khỏi commit; câu thứ ba có → `DESIGN_CONFLICT`.
7. **Quét phần đã stage.**
   - Dấu bỏ qua test: tìm mọi chuỗi trong `test.skip_markers` trong `git diff --staged`; có → dừng (blocker STD-TEST-4).
   - Secret: tìm các mẫu trong `${CLAUDE_SKILL_DIR}/references/secret-patterns.md`; có → dừng, báo người qua tech-lead (STD-SEC-1, STD-SEC-8). Ghi vị trí, không chép giá trị.
8. **Phép thử nguyên tử.** "Hoàn tác riêng commit này thì dự án còn build và qua test không?" Không → gộp hoặc tách lại.
9. **Cỡ.** > 300 dòng đổi hoặc > 3 file ở task cỡ S → ghi lo ngại `DONE_WITH_CONCERNS` gợi ý tech-lead tách task; không tự đổi phạm vi.
10. **Viết message.** Dòng đầu: `type(scope): description (<ID>)`, mệnh lệnh, tự đứng được, ≤ 72 ký tự nếu có thể. Thân (khi thay đổi không tầm thường): VÌ SAO, ràng buộc, tiêu chí `AC-n` đã phủ. Cấm dòng đầu kiểu "fix", "update", "misc", "phase 1". Ví dụ: `${CLAUDE_SKILL_DIR}/references/messages.md`.
11. **Commit.** `git commit` (KHÔNG `--no-verify`, không `-n`).
    Hook commit của dự án báo lỗi (điểm quyết định):
    - Lỗi định dạng/lint trên file trong touchpoints → sửa, chạy lại `cmd.lint`, stage lại, commit MỚI.
    - Lỗi test → quay về dev: chạy `cmd.test_one`, sửa, chạy lại; không commit khi còn đỏ.
    - Lỗi trên file ngoài touchpoints (hook quét cả repo) → không sửa file đó; ghi vào báo cáo, trả `DONE_WITH_CONCERNS` để tech-lead quyết.
    - Hook không chạy được (thiếu công cụ) → ghi lỗi nguyên văn, trả `BLOCKED`; không bỏ qua hook.
    Hook `check-git.sh` của kit chặn cứng `--no-verify`/`-n`; thông báo của nó là luật, không phải gợi ý.
12. **Điểm lưu khi đỏ.** Sau một lát cắt mà `cmd.test_one` đỏ và không rõ vì sao: không chồng thêm sửa đổi. Quay về commit xanh gần nhất cho file của mình (`git restore <file>` trên file trong touchpoints), tìm nguyên nhân, làm lại từng bước nhỏ. Không dùng `reset --hard` (mất việc của người khác, và không có trong quyền của skill).
13. **Không sửa lịch sử đã gửi.** Không `--amend`, không `reset --hard`, không rebase commit đã đưa reviewer xem; vòng sửa dùng commit mới.
14. **Kiểm sau commit.** `git log -1 --stat` cho mỗi commit; `git status --short` sạch với các file của task.
15. **Báo cáo.** Trả người gọi ≤ 10 dòng: trạng thái, commit (sha + dòng đầu), file, lệnh test đã chạy kèm đầu ra, "Thấy nhưng không chạm", lo ngại.

## Đầu ra
- Một hoặc vài commit trên nhánh task `team/<ID>-…`.
- Tin trả mẫu:
  ```
  dev -> tech-lead | FEAT-012 T3 | DONE
  Commit: a1b2c3d fix(otp): reject expired code (FEAT-012)
  File: src/auth/otp.py, tests/auth/test_otp.py (đúng touchpoints)
  Test: <cmd.test_one tests/auth/test_otp.py> → 6 passed; lint: exit 0
  Quét staged: skip marker 0, secret 0
  Thấy nhưng không chạm: src/auth/session.py:88 nuốt lỗi (ghi debt, không sửa)
  ```

## Lý do tự bào chữa thường gặp
| Ý nghĩ | Làm đúng |
|---|---|
| "Một task thì một commit cho tất cả" | Tách theo ý định: test + code một hành vi; đổi tên/định dạng riêng. |
| "Hook commit chậm, `--no-verify`" | Không bao giờ; sửa điều hook báo (hook máy cũng chặn). |
| "Message viết sau" | Viết dòng đầu đúng định dạng ngay. |
| "File thừa đó chỉ sửa nhỏ" | Bỏ ra khỏi commit, báo `DESIGN_CONFLICT`. |
| "Test xanh trước lần sửa cuối" | Chạy lại `cmd.test_one`, `cmd.lint`. |
| "Amend commit đã gửi review" | Commit mới (STD-GIT-4). |
| "Code comment-out để nhớ" | Xóa; STD-STYLE-5. |
| "Lockfile đổi thì commit luôn" | Lockfile được bảo vệ; chỉ qua `cmd.install` ở task phụ thuộc. |
| "`git add -A` cho nhanh" | Add đúng đường dẫn trong touchpoints. |
| "Formatter sửa cả file khác, cứ để" | Chỉ giữ thay đổi trên file trong touchpoints. |
| "Hook lỗi ở file người khác, tắt hook một lần" | Không tắt; báo `DONE_WITH_CONCERNS` cho tech-lead. |
| "Đỏ rồi, sửa thêm vài chỗ chắc xanh" | Quay về điểm lưu xanh, tìm nguyên nhân trước. |

## Dấu hiệu sai
- `git add -A` hoặc `git add .` trong lịch sử lệnh.
- Message không có `(<ID>)`, hoặc loại không thuộc danh sách.
- Commit chứa file ngoài touchpoints, `.env*`, lockfile, `.team/profile.json`, kết quả build.
- `--no-verify`, `-n`, `--amend`, `reset --hard` trong bất kỳ lệnh nào.
- Test và một refactor không liên quan trong cùng commit.
- Không có đầu ra test sau lần sửa cuối.
- Thay đổi > 300 dòng mà không có thân message.

## Kiểm chứng
- [ ] `git status --short` trước và sau được dán; sau là sạch với file của task.
- [ ] `git diff --staged --name-only` là tập con của touchpoints.
- [ ] Đầu ra `cmd.test_one` và `cmd.lint` (và `cmd.typecheck` nếu có) có sau lần sửa cuối.
- [ ] Kết quả quét skip marker và secret trong phần đã stage (rỗng) được dán.
- [ ] Nếu hook commit báo lỗi: đầu ra lỗi và commit mới sau khi sửa được dán (không có `--no-verify`).
- [ ] `git log -1 --stat` cho mỗi commit; dòng đầu khớp `^(feat|fix|refactor|test|docs|chore|ci|perf|build)(\(.+\))?: .+ \((FEAT|BUG|CHG)-[0-9]+\)$`.

## Xem thêm
- `${CLAUDE_SKILL_DIR}/references/messages.md` — ví dụ message tốt/xấu, tách commit.
- `${CLAUDE_SKILL_DIR}/references/secret-patterns.md` — mẫu quét secret trong phần đã stage.
- Agent `dev`, `maintainer`; skill `/team:build` (vòng gọi commit), `/team:pr`.
- `handbook/STD.md`: STD-NAME-5, STD-GIT-2/4/5, STD-STYLE-5, STD-SEC-1, STD-DEP-2.
