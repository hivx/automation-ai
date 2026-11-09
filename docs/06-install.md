# 06 — Cài đặt

Yêu cầu: Claude Code ≥ 2.1; `bash`, `python3`, `jq`, `git`; `gh` tùy chọn.

## Ba cách cài
| Cách | Lệnh | Có agent | Có hook | Tên lệnh |
|---|---|---|---|---|
| 1. Marketplace (khuyên dùng) | `/plugin marketplace add <owner>/automation-ai` rồi `/plugin install team@automation-ai` | có | có | `/team:<tên>` |
| 2. `npx skills` (tùy chọn) | `npx skills add <owner>/automation-ai` | không | không | `/<tên>` |
| 3. Chép cục bộ | `scripts/install-local.sh [--dry-run] [--force] <dự-án>` | có (tên không tiền tố) | có (gộp vào `.claude/settings.json`) | `/<tên>` |

- Cách 1 cũng chạy được bằng shell: `claude plugin marketplace add <owner>/automation-ai`, `claude plugin install team@automation-ai`.
- Cách 2 thiếu luật máy (hook), chỉ hợp để đọc thử skill.
- Cách 3 chép `agents/` → `.claude/agents/`, `skills/` → `.claude/skills/`, phần còn lại → `.claude/team-kit/`, ghi `.team/plugin_root`. Chạy lại an toàn; file khác bản đích thì bỏ qua trừ khi có `--force` (mã thoát 1 khi có file bị bỏ qua).
- Thử kit chưa đóng gói: từ thư mục dự án, `claude --plugin-dir /đường/dẫn/automation-ai`.

## Sau khi cài: takeover → onboard
1. Dự án đã có code: `/team:takeover` → đọc `docs/team/` → duyệt `ai-readiness.md` (G0).
2. Repo rỗng: bỏ qua takeover, chạy `/team:onboard --new`.
3. `/team:onboard` tạo `.team/profile.json`, `.team/config.json`, khối `<!-- team:start -->…<!-- team:end -->` trong `CLAUDE.md` (chèn, không ghi đè), `.claude/settings.json`, `.claude/rules/`, mẫu GitHub. Nó cũng đặt `team-leader` làm agent của phiên chính (ADJ-01).

## Ba phạm vi settings
| Phạm vi | File | Dùng cho |
|---|---|---|
| Dự án (commit) | `.claude/settings.json` | `enabledPlugins`; `agent`; `permissions.allow` từ `cmd.*` + git an toàn; `permissions.deny`: push nhánh bảo vệ, force-push, `rm -rf`, sửa `protected_paths`, đọc `.env*`; hook riêng dự án; `skillOverrides` để ẩn skill trùng |
| Cục bộ (gitignore) | `.claude/settings.local.json` | Tùy chỉnh của riêng máy bạn |
| Người dùng | `~/.claude/settings.json` | Thói quen cá nhân trên mọi dự án |

Chế độ quyền theo giai đoạn: `plan` khi phân tích/kiến trúc; `acceptEdits` khi build; `dontAsk` + allowlist tối thiểu cho CI/headless. Đặt bằng settings hoặc cờ CLI (plugin agent bỏ qua `permissionMode`).

## Chính sách plugin và MCP
- Kit không viết MCP server hay plugin nào khác.
- Profile khai `plugins.required` / `plugins.recommended`; onboard in lệnh cài, không tự cài; SessionStart cảnh báo nếu thiếu (không chặn).
- Khuyên dùng mặc định: plugin LSP cho ngôn ngữ, security-guidance, github/gitlab.
- Theo nhu cầu: Playwright MCP (qa khi `ui: true`), MCP tài liệu thư viện (researcher), Sentry/Slack (devops/team-leader), tracker (intake).
- Không cài plugin trùng chức năng `team` (superpowers, commit-commands, pr-review-toolkit). Bắt buộc phải có thì ẩn skill trùng bằng `skillOverrides`.

## Gỡ cài
- Marketplace: `/plugin uninstall team@automation-ai`, rồi `/plugin marketplace remove automation-ai` nếu không dùng nữa.
- Cục bộ: xóa `.claude/agents/` và `.claude/skills/` mà kit đã chép (xem log của install-local), `.claude/team-kit/`, `.team/plugin_root`.
- Dữ liệu của đội (`docs/team/`, `.team/profile.json`, `.team/config.json`) là của dự án: giữ hoặc xóa tùy bạn. Khối `team` trong `CLAUDE.md` nằm giữa hai dấu `team:start`/`team:end`, xóa cả khối.

## Hook được cài (luật máy)
`hooks/hooks.json` của plugin; khi cài cục bộ, `install-local.sh` gộp cùng nội dung vào `.claude/settings.json` với đường dẫn `${CLAUDE_PROJECT_DIR}/.claude/team-kit/scripts/`.

| Sự kiện | Script | Làm gì |
|---|---|---|
| PreToolUse `Edit\|Write\|NotebookEdit` | `protect.sh`, `role-policy.sh` | Chặn `protected_paths`, `.git/`, `.claude/settings*.json`, file mới ngoài `allowed_new_file_roots`; giới hạn ghi theo vai |
| PreToolUse `Bash` | `check-git.sh`, `role-policy.sh` | Chỉ push `team/*` (và tag); chặn force-push, `--delete`, `--no-verify`, `reset --hard`/`rebase -i` trên nhánh bảo vệ; cảnh báo message sai; lệnh theo vai |
| PreToolUse `Agent` | `role-policy.sh` | Ai được gọi ai (`handbook/who-calls-whom.md`) |
| PostToolUse `Edit\|Write` | `format.sh` | Formatter theo `formatters_by_ext` |
| Stop; SubagentStop `team:dev\|maintainer\|researcher` | `stop-check.sh` | Khi có `.team/active-build`: lint, typecheck, test file đã đổi, cấu trúc; khi research: bắt buộc `## Sources` có URL |
| SubagentStop (mọi agent) | `scorecard.sh` | Ghi một dòng vào `docs/team/metrics/runs.jsonl` |
| SessionStart | `session-start.sh` | Ghi `.team/plugin_root`, nạp tóm tắt trạng thái |
| PreCompact, SessionEnd | `handoff.sh` | Bàn giao phiên |
| PostCompact, SessionEnd | `log-session.sh` | Số liệu phiên |

Giới hạn theo vai nằm trong `hooks/role-policy.json`; phiên không có agent (người tự làm) không bị giới hạn theo vai, chỉ bị các hook khác.

## Ghi chú về settings
- `skillOverrides` trong `.claude/settings.json` mặc định rỗng. Dùng để ẩn skill trùng của plugin khác: `{"<plugin>:<skill>": "off"}` hoặc `"user-invocable-only"`. JSON không cho chú thích nên ghi chú nằm ở đây.
- `Read(//<kit>/**)` nằm trong `.claude/settings.local.json` (riêng máy) để agent đọc `handbook/STD-short.md` của kit.
- `.claude/settings*.json` không sửa được bằng Edit/Write (hook chặn); đổi qua `/team:onboard` hoặc tự sửa tay.
