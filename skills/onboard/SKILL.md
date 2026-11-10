---
name: onboard
description: Dùng khi G0 của takeover đã được duyệt, hoặc repo rỗng cần cấu hình đội lần đầu (--new), để cài profile, config, settings, rule, CI và khung docs/team cho dự án.
argument-hint: "[--new] [--accept-clean-first]"
disable-model-invocation: true
allowed-tools: Read Glob Bash(jq *) Bash(cat *) Bash(ls *) Bash(mkdir *) Bash(cp *) Bash(python3 *) Bash(git status *) Bash(echo *) Bash(awk *) Bash(wc *)
---

# Đưa đội vào dự án

## Tổng quan
Skill này biến dự án thành nơi đội làm việc được: `.team/profile.json`, `.team/config.json`, khối đội trong `CLAUDE.md`, `.claude/settings.json` + `settings.local.json`, rule theo đường dẫn, CI, khung `docs/team/`. Skill chạy trong phiên chính (team-leader) với ngoại lệ quyền của giai đoạn `onboard` (ghi `CLAUDE.md`, `.gitignore`, `.claude/rules/**`, `.github/**`, profile/config; `cp` chỉ từ `<kit>/templates/`). Ngoại lệ mở khi `.team/current.json` có `stage: onboard` và PHẢI đóng (`stage: idle`) ở mọi lối ra, kể cả khi dừng sớm.

Ba luật: gộp, không ghi đè (settings gộp JSON, CLAUDE.md chèn khối giữa `<!-- team:start -->` và `<!-- team:end -->`, rule có rồi thì bỏ qua); in lệnh cài plugin, không tự cài (SPEC §8); chạy lại onboard phải ra "bỏ qua (đã có)" cho mọi file — nếu không là onboard có lỗi.

`$ARGUMENTS`: rỗng (dự án có code, sau G0) | `--new` (repo rỗng) | `--accept-clean-first` (người đã xác nhận chạy dù AI-readiness là `clean-first`). `<kit>` = nội dung `.team/plugin_root`. `R` = `python3 "<kit>/scripts/render.py"`.

## Khi nào dùng (và khi nào không)
Dùng khi:
- `docs/team/ai-readiness.md` có `Approved-by:` (G0 đã duyệt) sau `/team:takeover`.
- Repo rỗng bắt đầu dự án mới (`--new`, playbook `new-project`).
- Nâng phiên bản kit: chạy lại để thêm phần còn thiếu (mọi phần đã có được giữ).

Không dùng khi:
- Chưa takeover dự án có code → `/team:takeover` trước.
- Muốn đổi một lệnh trong profile → người sửa `profile.json` (hoặc chạy lại onboard với đề xuất mới); agent không sửa profile ngoài onboard.
- Muốn cài plugin → onboard chỉ in lệnh.

## Tìm hiểu stack trước
1. Read `docs/team/profile-proposal.md` (đề xuất từng khe kèm bằng chứng) và `docs/team/ai-readiness.md` (dòng `Verdict:`); `--new`: hỏi người stack (phiên chính được dùng AskUserQuestion) rồi chọn `<kit>/profiles/<stack>.json`.
2. Read `.claude/settings.json`, `.claude/settings.local.json`, `CLAUDE.md`, `.gitignore` hiện có — để biết sẽ gộp gì và giữ gì.
3. Read `<kit>/.claude-plugin/plugin.json`: phiên bản kit (ghi vào `onboarding.md`).
4. `plugins.required`/`recommended` của profile; `enabledPlugins` hiện có (plugin trùng chức năng `team`: superpowers, commit-commands, pr-review-toolkit).

## Đầu vào và điều kiện trước
- Không `--new`: 20 dòng đầu `docs/team/ai-readiness.md` có `Approved-by: <tên> <YYYY-MM-DD>`. Không có → dừng, in lệnh duyệt.
- K-09: `Verdict: clean-first` → DỪNG trước mọi ghi: liệt kê việc dọn mà ai-readiness nêu, hỏi người xác nhận riêng (AskUserQuestion), hoặc chạy lại với `--accept-clean-first`. `adjust-profile` → dùng `profile-proposal.md` kèm chỉnh sửa trong lần duyệt G0.
- Kiểm: `python3 "<kit>/scripts/team.py" status`.

## Quy trình
Chi tiết từng file và cách gộp: `${CLAUDE_SKILL_DIR}/references/files.md`.
1. **Mở ngoại lệ.** Write `.team/current.json` {stage: "onboard"}. Từ đây mọi lối ra (kể cả lỗi) đều kết thúc bằng bước 13.
2. **Kế hoạch trước khi ghi.** In bảng: file đích | cách ghi (tạo / gộp JSON / chèn khối / bỏ qua vì đã có) | nguồn mẫu. Đây cũng là khung bảng của `onboarding.md`.
3. **Profile.** Từ `profile-proposal.md` (hoặc `<kit>/profiles/<stack>.json`) → Write `.team/profile.json`. Kiểm: `python3 "<kit>/scripts/check-profile.py" "<kit>/templates/schemas/profile.schema.json" .team/profile.json` — `cmd.test_one` và `cmd.format` phải có `{file}` (K-01). Đỏ → sửa đề xuất hoặc dừng; không ghi profile sai.
4. **Config.** `<kit>/templates/project/team/config.json` → `.team/config.json` (có rồi: giữ, chỉ thêm khóa thiếu); dự án có code để G0 bật. Kiểm bằng `check-profile.py` với `config.schema.json`.
5. **CLAUDE.md.** `R --template "<kit>/templates/project/CLAUDE.md.tmpl" --insert-block CLAUDE.md`. Kiểm máy: `awk '/<!-- team:start/,/<!-- team:end/' CLAUDE.md | wc -l` ≤ 25; `git diff CLAUDE.md` chỉ chạm khối.
6. **Settings.** `R --json --template "<kit>/templates/project/claude/settings.json.tmpl" --merge-into .claude/settings.json`; tương tự `settings.local.json.tmpl` → `.claude/settings.local.json` (`Read(//<kit>/**)` riêng máy, ADJ-19). Giá trị đã có thắng → rà lại: `Bash(*)`, `defaultMode: bypassPermissions`, hay `"agent"` khác `team:team-leader` còn sót → ghi vào "việc người phải làm tay", không báo thành công im lặng. Plugin trùng chức năng → in mục `skillOverrides` cần thêm.
7. **Rules.** Mỗi `<kit>/templates/project/claude/rules/<x>.md.tmpl` → `R --template … --out .claude/rules/<x>.md` (có rồi → bỏ qua).
8. **CI.** `ci.provider` = `github` → render `<kit>/templates/project/github/workflows/*.yml` vào `.github/workflows/`, chép PR/issue template, CODEOWNERS bằng `cp` từ `<kit>/templates/` (không ghi đè); `gitlab` → `.gitlab-ci.yml` khung; `none` → bỏ qua. Ghi vào việc tay: secret `ANTHROPIC_API_KEY`, và runner CI cần `--allowedTools` (đã có trong mẫu, K-06).
9. **Khung `docs/team/`**: `features/`, `adr/`, `research/`, `explore/`, `journal/`, `metrics/`, `retro/`, `proposals/`, `agents/`; `skills-registry.md`, `kit-issues.md` từ mẫu.
10. **`.gitignore`.** Gộp dòng còn thiếu từ `<kit>/templates/project/gitignore.tmpl` (có `.claude/worktrees/`, `.team/current.json`, `.team/session/`).
11. **Plugin: chỉ in.** `claude plugin install <tên>@<marketplace>` cho từng `plugins.required` (cảnh báo chặn) và `recommended`. Không cài.
12. **Chạy thử một lần.** `git status --short` trước; `cmd.install`, `cmd.lint`, `cmd.test` (Bash) — ghi lệnh, mã thoát, đầu ra (đỏ cũng ghi); `git status --short` sau: lockfile hay file protected đổi → báo, không commit chúng. Kiểm `grep -c '{{' CLAUDE.md .claude/settings.json .claude/rules/*.md` = 0 (khe rỗng còn sót).
13. **Đóng ngoại lệ.** Write `.team/current.json` {stage: "idle"}. Làm bước này ở MỌI lối ra.
14. **Báo.** Write `docs/team/onboarding.md` (mẫu `<kit>/templates/artifacts/onboarding.md`): bảng bước 2 với trạng thái thật, phiên bản kit, bảng chạy thử, plugin chưa cài, việc tay. Journal một dòng.

## Đầu ra
- `.team/profile.json`, `.team/config.json`, khối trong `CLAUDE.md`, `.claude/settings.json`, `.claude/settings.local.json`, `.claude/rules/*.md`, `.github/**` (nếu github), khung `docs/team/`, `docs/team/onboarding.md`.
- Tin cho người:
  ```
  onboard | xong (kit team 0.3.0)
  Đã tạo 11, gộp 2 (settings.json, .gitignore), bỏ qua 3 (đã có); CLAUDE.md khối 21 dòng, ngoài khối không đổi
  check-profile: profile OK, config OK
  Chạy thử: cmd.install exit 0; cmd.lint exit 0; cmd.test exit 1 (2 failed — đã có trước, ghi debt)
  Plugin chưa cài: pyright-lsp (recommended) — lệnh trong onboarding.md
  Việc tay: thêm secret ANTHROPIC_API_KEY; gỡ "Bash(*)" có sẵn trong settings.json
  Tiếp: commit các file trên, rồi /team:intake "<yêu cầu>"
  ```

## Lý do tự bào chữa thường gặp
| Ý nghĩ | Làm đúng |
|---|---|
| "G0 chắc đã ổn" | Không có `Approved-by:` → dừng, đóng ngoại lệ. |
| "clean-first nhưng đã duyệt, cứ chạy" | Xác nhận riêng (K-09) hoặc `--accept-clean-first`. |
| "Ghi đè settings/CLAUDE.md cho gọn" | Gộp JSON, chèn khối; báo giá trị cũ còn giữ. |
| "Cài luôn plugin còn thiếu" | Chỉ in lệnh. |
| "cmd.install đổi lockfile, commit luôn" | Báo; lockfile thuộc vùng cấm. |
| "Đếm dòng khối bằng mắt" | `awk … | wc -l` (K-08). |
| "Lỗi giữa chừng, để stage onboard đó" | Luôn ghi `stage: idle` khi ra. |
| "Test đỏ, khỏi ghi" | Ghi nguyên đầu ra đỏ vào `onboarding.md`. |
| "Chép file mẫu từ dự án khác cho nhanh" | `cp` chỉ từ `<kit>/templates/` (hook chặn chỗ khác, K-26). |

## Dấu hiệu sai
- `.team/current.json` còn `stage: onboard` sau khi chạy.
- Còn `{{` trong file đã render.
- `git diff CLAUDE.md` chạm dòng ngoài khối đội.
- Có ghi vào `~/.claude/`; plugin bị cài.
- `onboarding.md` không có mã thoát của lần chạy thử.
- `Bash(*)` hay `bypassPermissions` còn trong settings mà không có cảnh báo.
- Chạy lại onboard mà có file "đã tạo" mới (onboard không lũy đẳng).

## Kiểm chứng
- [ ] Đầu ra `check-profile.py` cho profile và config được dán.
- [ ] `git diff CLAUDE.md` chỉ trong khối; số dòng khối từ `awk | wc -l` ≤ 25.
- [ ] `grep -c '{{'` trên file đã render = 0; `jq '.agent, .permissions.deny' .claude/settings.json` được dán.
- [ ] `cat .team/current.json` cho thấy `idle`.
- [ ] Bảng chạy thử trong `onboarding.md` có mã thoát; `git status --short` trước/sau `cmd.install` được dán.

## Xem thêm
- `${CLAUDE_SKILL_DIR}/references/files.md` — từng file đích, nguồn mẫu, cách gộp. Mở ở bước 2–10.
- `/team:takeover` (trước), `/team:intake` (sau); `scripts/render.py --help`, `scripts/check-profile.py --help`.
- `docs/04-profile.md`, `docs/06-install.md`; `hooks/role-policy.json` (ngoại lệ `onboard`).
