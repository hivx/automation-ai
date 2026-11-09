# File onboard tạo và cách gộp

| File đích | Nguồn | Cách ghi |
|---|---|---|
| `.team/profile.json` | `docs/team/profile-proposal.md` hoặc `<kit>/profiles/<stack>.json` | Tạo mới; có rồi → hỏi trước khi thay |
| `.team/config.json` | `<kit>/templates/project/team/config.json` | Tạo mới; có rồi → giữ, chỉ thêm khóa thiếu (`jq -s '.[0] * .[1]'`, bản dự án thắng) |
| `CLAUDE.md` | `<kit>/templates/project/CLAUDE.md.tmpl` | Chèn/thay khối giữa `<!-- team:start -->` và `<!-- team:end -->`; ≤ 25 dòng |
| `.claude/settings.json` | `<kit>/templates/project/claude/settings.json.tmpl` | `render.py --json --merge-into`: giá trị đã có thắng; mảng hợp nhất, bỏ trùng |
| `.claude/settings.local.json` | `<kit>/templates/project/claude/settings.local.json.tmpl` | Như trên; chứa `Read(//<kit>/**)` riêng cho máy này (không commit) |
| `.claude/rules/*.md` | `<kit>/templates/project/claude/rules/*.tmpl` | Không ghi đè file đã có |
| `.github/workflows/team-ci.yml`, `team-feature.yml` | `<kit>/templates/project/github/workflows/` | Chỉ khi `ci.provider` = `github` |
| `.github/PULL_REQUEST_TEMPLATE.md`, `ISSUE_TEMPLATE/team-feature.yml`, `CODEOWNERS` | `<kit>/templates/project/github/` | Không ghi đè |
| `.gitignore` | `<kit>/templates/project/gitignore.tmpl` | Thêm dòng còn thiếu |

`permissions.allow` lấy từ mọi khe `cmd.*` khác rỗng (dạng `Bash(<lệnh> *)`) + git an toàn. `permissions.deny`: push nhánh bảo vệ, force-push, `rm -rf`, `Edit` các `protected_paths`, `Read(.env*)`. `Read(//<kit>/**)` nằm trong `settings.local.json` vì đường dẫn kit khác nhau giữa các máy.
