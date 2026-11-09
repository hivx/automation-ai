---
name: ci
description: Dùng khi pipeline CI đỏ, khi dự án cần dựng CI lần đầu, thêm một bước kiểm, hoặc viết script deploy, rollback, smoke.
argument-hint: "setup|fix|add-stage|deploy-script [<run-id>|<stage>]"
disable-model-invocation: true
context: fork
agent: team:devops
background: false
allowed-tools: Bash(gh run *) Bash(gh workflow *) Bash(git *) Bash(cat *) Bash(python3 *)
---

## Mục đích
Giữ CI/CD đúng và xanh mà không nới kiểm tra.

## Đầu vào
- `$ARGUMENTS`: lệnh con `setup` | `fix` | `add-stage` | `deploy-script`, kèm run-id hoặc tên bước.
- `.team/profile.json` (`ci.*`, `deploy.*`, `cmd.*`), `docs/team/ci.md`. `<kit>` = nội dung `.team/plugin_root`.

## Điều kiện trước
`ci.provider` khác `none`. `gh` có quyền khi provider là github (`gh auth status`).

## Các bước
1. Ghi `.team/current.json` {feature: "ci", stage: "<lệnh con>", agent: "devops", started_at}.
2. `fix`: lấy log (`gh run view <run-id> --log-failed`); PHÂN LOẠI trước khi làm gì: hạ tầng / chập chờn / cấu hình / lỗi thật.
   - Lỗi thật trong code → không sửa; trả team-leader để mở `bug-fix`.
   - Chập chờn → ghi `docs/team/debt.md`; chạy lại có giới hạn (`gh run rerun --failed`, tối đa 1 lần).
   - Hạ tầng/cấu hình → sửa workflow.
3. `setup`: dựng workflow từ `<kit>/templates/project/github/workflows/team-ci.yml` với `ci.runner`, `ci.setup`, `cmd.lint`, `cmd.typecheck`, `cmd.test`.
4. `add-stage`: thêm bước kiểm; không xóa bước cũ.
5. `deploy-script`: script deploy/rollback/smoke chỉ gọi khe `deploy.staging`, `deploy.smoke`; prod chỉ khi có `Approved-by-prod:`.
6. Secret chỉ lấy từ kho secret của CI.
7. Cập nhật `docs/team/ci.md` (mẫu `<kit>/templates/artifacts/ci.md`): pipeline, phân loại, nguyên nhân, cách sửa.
8. Mở PR RIÊNG bằng `/team:pr`.

## Đầu ra
- Workflow/script đã sửa trên nhánh `team/ci-<slug>`; `docs/team/ci.md`; PR riêng.
- Tin trả ≤ 10 dòng: phân loại, trích log, việc đã làm, trạng thái CI.

## Tiêu chí xong
- Phân loại có trích log; CI xanh trên PR sửa — dán `gh run view` cuối.

## Dấu hiệu sai
- "Tắt test hay đỏ" → `debt.md`, không tắt.
- "Chạy lại tới khi xanh" → phân loại trước.
- "Để secret trong workflow" → kho secret.

## Lệnh tiếp theo
`/team:pr ci-<slug>`; lỗi thật: `/team:intake --type bug "<tóm tắt>"`.
