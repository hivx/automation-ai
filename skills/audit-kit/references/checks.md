# Các kiểm của audit-kit

Mỗi kiểm kết thúc bằng một dòng phạm vi `đã kiểm: N file / bỏ qua: <lý do>` để "0 vấn đề" phân biệt được với "không chạy". Chỉ dùng lệnh chỉ-đọc (Read, Grep, Glob, `jq`, `git log`) và `python3 <kit>/scripts/{team.py status,measure.py,check-profile.py}` bằng đường dẫn tuyệt đối. Không chạy `validate.sh`, `log-run.sh`, `team.py scorecard` hay `evals/run-eval.sh`.

## Kiểm tĩnh (không cần số liệu)
| # | Kiểm | Cách làm | Báo khi |
|---|---|---|---|
| S1 | Ranh giới tin cậy | Liệt kê nguồn đưa chữ vào agent: nội dung issue (prompt của `team-feature.yml`), trang web (researcher), skill tạm `.claude/skills/`, CLAUDE.md/rule của dự án, `docs/team/**` do vai khác viết. Grep câu "dữ liệu, không phải chỉ dẫn" (STD-SEC-5) ở nơi đọc chúng. | Nguồn nào được đọc mà không có câu đó |
| S2 | Hook mở khi lỗi | Đọc `protect.sh`, `role-policy.sh`, `check-git.sh`: JSON hỏng hay lệnh con lỗi dẫn tới mã thoát nào? Claude Code chỉ chặn ở mã 2; mã khác là cho qua. | Hook an toàn cho qua khi lỗi mà không in chẩn đoán ra stderr |
| S3 | Matcher phủ tool | Gom `tools:` của `agents/*.md`, `.claude/agents/*.md` và `allowed-tools:` của skill; so với matcher PreToolUse trong `hooks/hooks.json`. Ghi file phải được chặn ở `Edit`, `Write`, `NotebookEdit`, `Bash`. | Tool ghi được mà không matcher nào chặn |
| S4 | Danh sách chỉ-đọc | `hooks/role-policy.json` `readonly_commands`: lệnh nào có cờ ghi/chạy lệnh (`sed -i/e/w`, `sort -o`, `uniq IN OUT`, `tree -o`, `rg --pre`, `find -delete/-fprint`, `mkdir`)? `teamlib.py is_readonly` có chặn từng dạng không (đọc code)? `readonly_scripts` so theo đường dẫn hay tên? | Dạng ghi lọt; script so theo tên |
| S5 | Danh sách ghi của từng vai | So `roles[*].write` trong `role-policy.json` với câu "chỉ ghi …" ở mục 1 của `agents/<vai>.md` và cột tools của SPEC §3 (kèm ADJ trong `docs/00-overview.md`). | Ba nơi khác nhau |
| S6 | Nới cổng bằng cấu hình | File cấu hình lint/format/test (tên trong profile hoặc thường gặp) có nằm trong `protected_paths` không; vai `bash: any` sửa được không. | Cấu hình kiểm tra sửa được bởi dev/maintainer/devops |
| S7 | Allowlist headless | Mỗi `workflows/batch/*.md`, `templates/project/github/workflows/*.yml`: `--allowedTools` có đủ cho chuỗi skill (`python3` cho `team.py`, khe `cmd.*`) không; có lấy từ `permissions.allow` không (K-06). | Thiếu, hoặc chép tay lệnh stack |
| S8 | `allowed-tools` quá rộng | Grep `allowed-tools:` có `Bash` trần, `Bash(*)`, `Bash(bash *)`, `Bash(rm *)`, `Bash(sudo *)`. Ghi riêng `Bash(python3 *)` (cho phép `python3 -c`, K-25). | Mọi dòng |
| S9 | Mô tả | Skill: bắt đầu "Dùng khi", < 500 ký tự, không tóm tắt quy trình ("rồi", "sau đó" nhiều lần). Agent: bắt đầu "Giao khi", ≤ 300 ký tự. | Sai một điều |
| S10 | Khe treo | Grep `cmd\.[a-z_]+`, `deploy\.[a-z_]+`, `ci\.[a-z_]+` trong agents/skills/workflows; so với `templates/schemas/profile.schema.json`. | Khe không có trong schema |
| S11 | Mâu thuẫn chỉ dẫn | Grep cùng danh từ (push, skip, migration, prod, hỏi người) đi với "luôn/bắt buộc" ở file này và "không/cấm" ở file khác. | Mọi cặp tìm được (dán hai `file:line`) |
| S12 | Lệch tên | Grep `/team:<x>`, `agents/<x>.md`, `skills/<x>` trong `docs/`; đối chiếu thư mục. | Tên không tồn tại |
| S13 | Skill/agent tạm | So `.claude/skills/*/`, `.claude/agents/*.md` với `docs/team/skills-registry.md`; dòng `temp` không dùng 30 ngày; agent tạm có `permissionMode`, `hooks`, `mcpServers` trong frontmatter. | Thiếu đăng ký, quá hạn, khóa nguy hiểm |
| S14 | Công tắc tắt hook | Grep biến môi trường hay cờ tắt hook trong `scripts/`. | Có bất kỳ công tắc nào (luật máy không được có đường tắt) |

## Kiểm theo số liệu (cần `docs/team/metrics/runs.jsonl`)
| # | Kiểm | Cách làm | Báo khi |
|---|---|---|---|
| D1 | Skill không dùng | Dòng SubagentStop có `skill: null`; chỉ vài skill gọi `log-run.sh --skill`. Ghép skill fork với `agent` + `stage` (từ `current.json`). Skill không bao giờ ghi số liệu → "không có dữ liệu", KHÔNG phải "không dùng". | 0 lần trong 30 ngày với skill có dữ liệu |
| D2 | Agent chạm trần lượt | Chuẩn hóa tiền tố `team:` của `agent`; so `turns` với `maxTurns` trong frontmatter. `turns` là số tin của assistant (xấp xỉ) — ghi rõ. | ≥ 2 lần |
| D3 | Kết quả đoán từ chữ | Trường `result` của scorecard đoán từ tin cuối (K-18) — mọi số liệu dựa trên `result` gắn nhãn "độ tin cậy thấp". | Luôn ghi chú |

## Chống trùng
Đọc `docs/kit-issues.md` của kit khi đọc được (`<kit>/docs/kit-issues.md`). Phát hiện trùng → Trạng thái "đã có (K-xx)" kèm bằng chứng mới (có thể đã tái phát). Phát hiện mới → "mới".
