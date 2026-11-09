# CLAUDE.md — repo bộ kit `automation-ai` (plugin `team`)

Đây là repo của BỘ KIT, không phải dự án dùng kit. Đặc tả: `SPEC.md` (không sửa). Điều chỉnh đã duyệt so với SPEC: `docs/00-overview.md` mục "Điều chỉnh đã chốt".

## Kiểm tra trước khi báo xong
- `scripts/validate.sh` — phải ra `0 fail`. Từ P4 dùng `scripts/validate.sh --strict`.
- `claude plugin validate .` — manifest plugin + marketplace.
- Dán đầu ra thật vào báo cáo. Không nói "xong" khi chưa có đầu ra.

## Luật không ngoại lệ
1. Đổi quy trình là đổi CÙNG LÚC: docs + skill/agent + hook/template. Không để lệch.
2. Không ghi cứng lệnh stack (test, build, lint...) trong agents/, skills/, hooks/, scripts/. Chỉ tham chiếu khe `cmd.*` của `.team/profile.json`.
3. Tên phải khớp mọi nơi: docs ↔ agents ↔ skills ↔ templates ↔ scripts. Đổi tên thì grep và sửa hết.
4. Văn xuôi bằng tiếng Việt. Định danh luôn bằng tiếng Anh: tên file/thư mục, key JSON, tên skill/agent, mã STD, nhánh, script, cờ CLI, key frontmatter.
5. Chỉ dùng bash, python3 (stdlib), jq, git, gh (tùy chọn). Không thêm phụ thuộc.
6. Chuẩn chất lượng (P7): skill nạp thường xuyên ≤ 400 chữ, 4 mục; skill khác 1.200–2.500 chữ, 10 mục; agent 600–1.200 chữ, 10 mục. Cấu hình: `scripts/skill-budgets.txt`, `skill-sections.txt`, `agent-sections.txt`; đo: `scripts/kit-metrics.py`; mục chưa đạt nằm trong `scripts/quality-backlog.txt` (chỉ được rút ngắn). Phần dài chuyển vào `references/`.
7. Không dùng `@file` trong skill/agent. Trong plugin, trỏ file bằng `${CLAUDE_PLUGIN_ROOT}`.
8. Mô tả skill bắt đầu bằng "Dùng khi", < 500 ký tự, không tóm tắt quy trình.
9. Không viết MCP server, không tạo plugin khác ngoài `team`.
10. Không viết một kiến thức hai lần: skill/rule/agent là sự thật cho AI; `docs/` chỉ tổng quan, cài đặt, bản đồ việc → skill, lý do thiết kế.

## Bố cục
- `.claude-plugin/` manifest · `agents/` 13 vai · `skills/<tên>/SKILL.md` 26 skill · `workflows/` 16 playbook + `batch/`
- `hooks/hooks.json` · `scripts/` · `handbook/` · `profiles/` · `templates/{artifacts,project,schemas}/` · `evals/<skill>/` · `docs/`

## Thêm một vai (agent)
1. Tạo `agents/<role>.md`: frontmatter `name` = tên file, `description` ("Giao khi…"), `tools`, `model`, `effort`, `maxTurns`; thân theo 10 mục của `scripts/agent-sections.txt` (có ví dụ tin trả và tin dừng 4 dòng).
2. Plugin agent bỏ qua `hooks`, `permissionMode`, `mcpServers`: giới hạn đường dẫn/lệnh đặt ở bảng role-policy của hook.
3. Cập nhật `docs/02-team.md`, `handbook/who-calls-whom.md`, `models` mẫu trong config, playbook liên quan.
4. Chạy `scripts/validate.sh`.

## Thêm một giai đoạn
1. Tạo skill `skills/<stage>/SKILL.md` và template artifact trong `templates/artifacts/`.
2. Thêm luật tính trạng thái vào `scripts/team.py`; thêm cổng (nếu có) vào `templates/project/team/config.json`.
3. Cập nhật `docs/01-process.md`, playbook trong `workflows/`, `docs/guides/want-x-type-y.md`.
4. Chạy `scripts/validate.sh`.

## Chạy thử kit trên dự án mẫu
```
cd /đường/dẫn/dự-án-mẫu
claude --plugin-dir /đường/dẫn/automation-ai
```
Trong phiên đó gõ `/team:takeover`. Không chạy kit ngay trong repo này.
