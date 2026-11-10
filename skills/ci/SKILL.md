---
name: ci
description: Dùng khi pipeline CI đỏ, khi dự án cần dựng CI lần đầu, thêm một bước kiểm, hoặc viết và kiểm script deploy, rollback, smoke.
argument-hint: "setup|fix|add-stage|deploy-script [<run-id>|<stage>]"
disable-model-invocation: true
context: fork
agent: team:devops
background: false
allowed-tools: Bash(gh run *) Bash(gh workflow *) Bash(git *) Bash(cat *) Bash(python3 *)
---

# Giữ CI/CD đúng và xanh

## Tổng quan
Skill này giữ pipeline đúng và xanh mà không bao giờ nới kiểm tra. Skill chạy trong ngữ cảnh `devops` (fork). Câu hỏi đầu tiên khi CI đỏ không phải "sửa thế nào" mà "đỏ vì loại gì" — theo năm loại của STD-CI-4: code, test chập chờn, môi trường, cấu hình, phụ thuộc. Lỗi code không phải việc của devops: trả về để mở bug-fix. Xóa bước, `continue-on-error`, `if: false`, `|| true` trên bước kiểm đều là nới kiểm tra (STD-CI-3) và bị cấm.

Mọi thay đổi CI đi trên nhánh riêng `team/ci-<slug>` và PR riêng (`/team:pr`). Lệnh trong workflow là khe của profile (`cmd.*`, `ci.setup`), không ghi tay lệnh stack. Một khe rỗng sinh ra bước `run: true` — xanh mà không kiểm gì; skill phải nêu rõ những bước đó là "chưa cấu hình", không tính là cổng.

`$ARGUMENTS`: lệnh con `setup` | `fix <run-id>` | `add-stage <tên>` | `deploy-script`. `<kit>` = nội dung `.team/plugin_root`.

## Khi nào dùng (và khi nào không)
Dùng khi:
- `fix`: CI đỏ trên PR hay nhánh nền (playbook `ci-fix`).
- `setup`: dự án chưa có CI, hoặc onboard đã bỏ qua bước CI.
- `add-stage`: cần thêm bước kiểm (typecheck, build, quét bảo mật đã khai trong profile).
- `deploy-script`: cần lệnh deploy staging, smoke, lệnh lên prod và rollback đã kiểm cho `/team:release`.

Không dùng khi:
- Test đỏ vì code sai → `/team:intake --type bug "<tóm tắt>"`.
- Muốn bỏ bước chậm khỏi PR → không; tối ưu (cache, song song, lọc đường dẫn) hoặc đề xuất cho người duyệt.
- Muốn deploy → `/team:release` (có cổng G5).

## Tìm hiểu stack trước
1. Read `.team/profile.json`: `ci.provider`, `ci.runner`, `ci.setup[]`, `cmd.lint`, `cmd.typecheck`, `cmd.test`, `cmd.build`, `deploy.staging`, `deploy.smoke`, `deploy.prod_requires_reviewer`, `protected_paths`.
2. Read `.team/config.json`: `base_branch`, `protected_branches`.
3. Read `docs/team/ci.md` (lịch sử sự cố, mục Deploy) và các file workflow hiện có.
4. Checkpoint: liệt kê mọi khe `cmd.*` rỗng — bước tương ứng sẽ là `run: true`.

## Đầu vào và điều kiện trước
- `ci.provider` khác `none`; `none` → dừng, trỏ `/team:onboard` hay người khai profile.
- Provider `github`: `gh auth status` thành công; không → `BLOCKED` (thiếu quyền).
- `fix`: có run-id (hoặc lấy run đỏ gần nhất: `gh run list --branch <nhánh> --status failure --limit 1`).
- Secret chỉ ở kho secret của CI; không đọc `.env*` (protected).

## Quy trình
1. **Ghi vị trí.** Write `.team/current.json` {feature: "ci", stage: "<lệnh con>", agent: "devops", started_at}. Tạo nhánh `team/ci-<slug>` từ `base_branch`.
2. **`fix` — gom bằng chứng.** `gh run view <id> --log-failed` và `gh run view <id> --json headSha,conclusion,jobs`. Trích dòng lỗi THẬT đầu tiên (không phải dòng cuối "exit 1").
3. **`fix` — phân loại (điểm quyết định, trước mọi sửa).** Bằng chứng cần cho từng loại:
   - code: cùng test đỏ khi chạy khe `cmd.*` tương ứng trên cùng SHA → dừng, trả team-leader mở bug-fix. Không sửa.
   - test chập chờn: cùng SHA, đỏ → `gh run rerun <id> --failed` MỘT lần → xanh. Ghi `docs/team/debt.md` (bảng test chập chờn, hai run-id). Không tắt test.
   - môi trường: lỗi runner, mạng, hạn mức; diff không đổi gì liên quan.
   - cấu hình: lỗi YAML/workflow, `ci.setup` lệch profile, bước gọi khe sai.
   - phụ thuộc: lỗi phân giải gói hay lockfile, bản thượng nguồn đổi.
   Bảng tiêu chí: `${CLAUDE_SKILL_DIR}/references/classify.md`.
4. **`fix` — sửa (chỉ môi trường, cấu hình, phụ thuộc).** Chỉ sửa file workflow (hoặc đề xuất đổi `ci.setup` qua người/onboard — devops không ghi được profile). Phụ thuộc: cập nhật qua `cmd.install`, không sửa tay lockfile; lockfile protected → dừng, báo người. Checkpoint: `git diff` không có dòng xóa bước kiểm, `continue-on-error`, `if: false`, `|| true`. Chạy lại khe `cmd.*` tương ứng tại chỗ trước khi push.
5. **`setup`.** Sinh workflow từ `<kit>/templates/project/github/workflows/team-ci.yml` bằng `python3 "<kit>/scripts/render.py"` (như onboard), điền `ci.runner`, `ci.setup`, `cmd.lint`, `cmd.typecheck`, `cmd.test`, `cmd.build`. Ghim phiên bản runner và action (STD-CI-7) — thẻ như `ubuntu-latest`, `@v4` là chưa ghim: ghi vào `docs/team/ci.md` "chưa ghim" nếu dự án chưa chọn bản. Bảng khe → bước: khe rỗng ghi "chưa cấu hình", không phải cổng.
6. **`add-stage`.** Chỉ THÊM bước; `git diff --stat` file workflow chỉ có dòng thêm trong phần jobs/steps. Bước mới gọi khe profile. Bước tốn thời gian → chạy song song hay lọc đường dẫn, không gỡ khỏi PR.
7. **`deploy-script`.** Viết mục `## Deploy` của `docs/team/ci.md` và script (dưới `structure.scripts`) chỉ gọi `deploy.staging`, `deploy.smoke`; lên prod = job CI có environment bắt người duyệt (ưu tiên), hoặc lệnh người chạy. Dòng `rollback: <lệnh>` chỉ được ghi "đã kiểm" sau khi chạy thật trên staging — dán mã thoát và ngày. Đầu vào của script qua biến môi trường, không nội suy chuỗi vào lệnh shell. Secret từ kho secret (STD-SEC-2).
8. **Ghi `docs/team/ci.md`** (mẫu `<kit>/templates/artifacts/ci.md`): một dòng "Lịch sử sự cố" (ngày, run-id, loại, trích log, cách sửa, PR) hoặc cập nhật bảng Pipeline/Deploy.
9. **Commit và PR.** `/team:commit` (`ci(<phạm vi>): … (<mã>)`), rồi `/team:pr ci-<slug>`. PR CI không chạm `src/` hay test.
10. **Xác nhận.** `gh run view <id>` của PR sửa: `conclusion: success`, đúng nhánh, đúng SHA. Dán dòng đó.
11. **Trả** team-leader ≤ 10 dòng, dòng đầu `devops -> team-leader | ci <run-id|lệnh con> | <loại hoặc DONE>`.

## Đầu ra
- Workflow/script đã sửa trên `team/ci-<slug>`; `docs/team/ci.md`; dòng `debt.md` khi chập chờn; PR riêng.
- Tin trả mẫu:
  ```
  devops -> team-leader | ci run 9876 | cấu hình
  Trích log (job test, SHA 4e1c2aa): "setup-python: version 3.13 not found"
  Phân loại: cấu hình (ci.setup ghi 3.13, profile và runner có 3.12); không phải code
  Sửa: .github/workflows/team-ci.yml bước setup → 3.12; không bỏ bước nào (diff +1 −1)
  Kiểm: gh run 9881 trên team/ci-python-version → conclusion success
  docs/team/ci.md: thêm dòng sự cố 2026-11-10; PR #91
  Tiếp: người duyệt PR #91
  ```

## Lý do tự bào chữa thường gặp
| Ý nghĩ | Làm đúng |
|---|---|
| "Test này hay đỏ, tắt đi" | Chập chờn → `debt.md` với hai run-id; không tắt. |
| "Chạy lại tới khi xanh" | Phân loại trước; tối đa một lần chạy lại. |
| "Luật lint ồn, nới cấu hình" | Nới kiểm tra (STD-CI-3); sửa code qua bug-fix hoặc ghi nợ. |
| "Đánh dấu continue-on-error tạm thôi" | Như xóa bước; cấm. |
| "Khe rỗng nên bước xanh" | Xanh không có nghĩa đã kiểm; ghi "chưa cấu hình". |
| "Lỗi code có một dòng, tôi sửa luôn" | Không phải việc devops; trả để mở bug-fix. |
| "Ghim phiên bản sau" | STD-CI-7: ghim ngay, hoặc ghi "chưa ghim" có lý do. |
| "Dán token vào workflow để thử" | Kho secret; token đã lộ → báo người xoay vòng (STD-SEC-8). |
| "Rollback chắc chạy được" | Chưa chạy thật thì chưa "đã kiểm". |

## Dấu hiệu sai
- Phân loại không có trích log và SHA.
- PR sửa CI chạm `src/` hay file test.
- Diff workflow có `if: false`, `|| true`, bước bị comment, `continue-on-error`.
- Chạy lại quá một lần trên cùng SHA.
- Dòng `run:` chứa lệnh stack gõ tay thay vì khe profile.
- Chuỗi giống secret trong diff.
- Dòng sự cố trong `docs/team/ci.md` không có PR.

## Kiểm chứng
- [ ] Trích `gh run view --log-failed` + loại + SHA được ghi trong `docs/team/ci.md`.
- [ ] Chập chờn: hai run-id cùng SHA (đỏ, xanh) và dòng `debt.md`.
- [ ] Diff workflow được dán, không có bước kiểm bị xóa hay nới.
- [ ] `gh run view <id>` cuối của PR sửa: `conclusion: success`, đúng nhánh.
- [ ] `setup`: bảng khe → bước, khe rỗng được đánh dấu.
- [ ] `deploy-script`: lệnh rollback có mã thoát lần chạy thật trên staging.

## Xem thêm
- `${CLAUDE_SKILL_DIR}/references/classify.md` — năm loại STD-CI-4, bằng chứng và hành động cho từng loại. Mở ở bước 3.
- Agent `devops`; `<kit>/templates/artifacts/ci.md`; `<kit>/templates/project/github/workflows/team-ci.yml`.
- `/team:intake --type bug` (lỗi code), `/team:pr`, `/team:release` (dùng mục Deploy).
- `handbook/STD.md`: STD-CI-1, STD-CI-3, STD-CI-4, STD-CI-5, STD-CI-7, STD-SEC-2, STD-SEC-8.
