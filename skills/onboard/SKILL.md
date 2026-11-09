---
name: onboard
description: Dùng khi G0 của takeover đã được duyệt, hoặc repo rỗng cần cấu hình đội lần đầu (--new), để cài profile, config, settings, rule và khung docs/team cho dự án.
argument-hint: "[--new]"
disable-model-invocation: true
allowed-tools: Read Glob Bash(jq *) Bash(cat *) Bash(ls *) Bash(mkdir *) Bash(cp *) Bash(python3 *) Bash(git status *) Bash(echo *)
---

## Mục đích
Biến dự án thành nơi đội làm việc được: profile, config, settings, rule, khung `docs/team/`.

## Đầu vào
- `$ARGUMENTS`: rỗng (dự án có code) hoặc `--new` (repo rỗng).
- `docs/team/profile-proposal.md` (không có `--new`). `<kit>` = nội dung `.team/plugin_root`.

## Điều kiện trước
- Không `--new`: khối header (20 dòng đầu) của `docs/team/ai-readiness.md` có `Approved-by: <tên> <YYYY-MM-DD>` (G0). Không có → dừng, in lệnh duyệt.
- Kiểm: `python3 "$(cat .team/plugin_root)/scripts/team.py" status`.

## Các bước
Chi tiết từng file: `${CLAUDE_SKILL_DIR}/references/files.md`. `R` = `python3 "<kit>/scripts/render.py"`.
0. Ghi `.team/current.json` {stage: "onboard"} (hook role-policy nới quyền ghi cho bước này).
1. Profile: từ `profile-proposal.md`, hoặc chép `<kit>/profiles/<stack>.json` (`--new`: hỏi stack). Kiểm: `python3 "<kit>/scripts/check-profile.py" "<kit>/templates/schemas/profile.schema.json" .team/profile.json`.
2. Config: chép `<kit>/templates/project/team/config.json` → `.team/config.json`; dự án có sẵn để G0 bật.
3. `CLAUDE.md`: `R --template <kit>/templates/project/CLAUDE.md.tmpl --insert-block CLAUDE.md` (chèn/thay khối, không đụng phần khác).
4. Settings: `R --json --template <kit>/templates/project/claude/settings.json.tmpl --merge-into .claude/settings.json`; `R --json --template <kit>/templates/project/claude/settings.local.json.tmpl --merge-into .claude/settings.local.json` (Read thư mục kit, riêng máy). Giá trị đã có thắng.
5. Rules: mỗi `<kit>/templates/project/claude/rules/<x>.md.tmpl` → `R --template … --out .claude/rules/<x>.md` (không ghi đè file đã có).
6. CI: `github` → render `<kit>/templates/project/github/workflows/*.yml` vào `.github/workflows/`, chép PR/issue template, CODEOWNERS; `gitlab` → `<kit>/templates/project/gitlab/.gitlab-ci.yml`; `none` → bỏ qua.
7. Tạo khung `docs/team/` (features, adr, research, explore, journal, metrics, retro, proposals) và `skills-registry.md`, `kit-issues.md`.
8. Gộp `<kit>/templates/project/gitignore.tmpl` vào `.gitignore`.
9. In lệnh cài cho từng `plugins.recommended` — KHÔNG tự cài.
10. Chạy một lần `cmd.install`, `cmd.lint`, `cmd.test` (Bash); ghi lệnh + đầu ra vào `docs/team/onboarding.md` (mẫu `<kit>/templates/artifacts/onboarding.md`).
11. In bảng: đã tạo / bỏ qua (đã có) / việc người phải làm tay. Ghi journal. Ghi `.team/current.json` {stage: "idle"} để đóng ngoại lệ quyền của onboard.

## Đầu ra
- `.team/profile.json`, `.team/config.json`, `CLAUDE.md`, `.claude/settings.json`, `.claude/rules/`, `docs/team/onboarding.md`, khung `docs/team/`.

## Tiêu chí xong
- `check-profile.py` qua cho profile và config — dán đầu ra.
- `onboarding.md` có đầu ra thật của install/lint/test (đỏ cũng ghi).
- Khối `CLAUDE.md` ≤ 25 dòng; phần ngoài khối không đổi (`git diff` dán).

## Dấu hiệu sai
- "Ghi đè settings cho gọn" → gộp bằng jq.
- "Cài luôn plugin cho tiện" → chỉ in lệnh.
- "G0 chắc ổn" → không có dòng duyệt thì dừng.
- "Test đỏ, bỏ qua bước ghi" → ghi nguyên đầu ra.

## Lệnh tiếp theo
In: "Commit các file trên, rồi giao việc đầu tiên: `/team:intake \"<yêu cầu>\"`."
