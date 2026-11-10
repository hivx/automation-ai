# 00 — Tổng quan

## Là gì, cho ai
`automation-ai` là plugin `team` cho Claude Code. Cài vào một dự án bất kỳ, nó cho Claude Code một đội IT có vai rõ ràng, quy trình 9 giai đoạn, cổng duyệt và luật máy.

Dành cho:
- Trưởng nhóm muốn giao yêu cầu thô và chỉ duyệt tài liệu ở các cổng.
- Lập trình viên muốn Claude làm có kỷ luật: test trước, review riêng, nghiệm thu bằng đầu ra thật.
- Người tiếp nhận một dự án cũ, cần biết nhanh dự án đang ở đâu.

Không phải là: quy trình cho một stack cụ thể; kho kiến thức nghiệp vụ của dự án; công cụ tự deploy production; nơi viết MCP server hay plugin mới.

## Bảy nguyên tắc
| # | Nguyên tắc | Nghĩa là |
|---|---|---|
| P1 | Agent là một con người | Mỗi vai có hợp đồng; không có agent "làm tất". |
| P2 | Trạng thái nằm trên đĩa | Vị trí hiện tại tính từ artifact trong `docs/team/`. |
| P3 | Máy trước LLM | Điều không được sai phải do hook/quyền/script chặn. |
| P4 | Độc lập nền tảng | Lệnh và cấu trúc dự án nằm trong `.team/profile.json`. |
| P5 | Gọi đúng người, khi cần | Mỗi lần gọi có lý do một câu trong journal. |
| P6 | Đo rồi mới sửa | Scorecard + journal; thay đổi có eval, canary, rollback. |
| P7 | Con người quyết định | Cổng là cấu hình; không bao giờ vượt cổng đang bật. |

## Ý tưởng tiếp nhận: ba câu hỏi
`/team:takeover` chỉ trả lời ba câu, không sửa gì:
1. Dự án **làm gì**?
2. Dự án **đã tới đâu**?
3. **Việc tiếp theo** là gì?

Quét theo 4 tầng, tầng sau chỉ chạy khi tầng trước chưa trả lời được: T0 siêu dữ liệu (cây thư mục, manifest, git log) → T1 tài liệu → T2 đối chiếu tài liệu với code, lấy mẫu → T3 đọc sâu từng module. Báo cáo ghi rõ đã quét gì, chưa quét gì, độ tin cậy. Người duyệt `ai-readiness.md` (cổng G0) rồi mới chạy `/team:onboard`.

## Cái gì nằm ở đâu
| Muốn biết | Xem |
|---|---|
| Đặc tả đầy đủ | `SPEC.md` |
| Quy trình, cổng, cỡ việc | `docs/01-process.md` |
| Các vai và ai gọi ai | `docs/02-team.md` |
| Sổ tay kỹ thuật | `handbook/STD.md` (tóm tắt: `docs/03-handbook.md`) |
| Khe của profile | `docs/04-profile.md` |
| Token, memory | `docs/05-tokens-and-memory.md` |
| Cài đặt, gỡ cài | `docs/06-install.md` |
| Tự cải tiến | `docs/07-improvement.md` |
| Kênh (CLI, GitHub, headless) | `docs/08-channels.md` |
| Vấn đề đã biết của kit, backlog | [`docs/kit-issues.md`](kit-issues.md) |
| Kiểm định chất lượng skill/agent | [`docs/research/kit-audit-round1.md`](research/kit-audit-round1.md), [`kit-audit-round2.md`](research/kit-audit-round2.md) |
| Bộ kit tham khảo, so sánh | [`docs/research/reference-kits.md`](research/reference-kits.md) |
| Ghi công | [`docs/credits.md`](credits.md) |
| Bắt đầu trong 5 phút | [`docs/guides/5-minute-start.md`](guides/5-minute-start.md) |
| Muốn X thì gõ Y | [`docs/guides/want-x-type-y.md`](guides/want-x-type-y.md) |
| Chọn playbook | [`docs/guides/decision-tree.md`](guides/decision-tree.md) |
| Phiên mẫu | [`docs/guides/sample-sessions.md`](guides/sample-sessions.md) |
| Đọc `/team:status`, ai chờ ai | [`docs/guides/who-is-waiting-for-what.md`](guides/who-is-waiting-for-what.md) |
| Khi có sự cố | [`docs/guides/incidents.md`](guides/incidents.md) |
| Ngày đầu trên dự án có sẵn | [`docs/guides/first-day-on-existing-project.md`](guides/first-day-on-existing-project.md) |

Trong dự án đã cài: cấu hình ở `.team/`, artifact ở `docs/team/`, quy tắc theo đường dẫn ở `.claude/rules/`.

## Điều chỉnh đã chốt (so với SPEC)
SPEC giữ nguyên văn. Các điểm dưới đây đã được người duyệt ngày 2026-11-09, sau khi đối chiếu với docs chính thức của Claude Code 2.1.319. Chúng thắng SPEC khi khác nhau.

| Mã | Điều chỉnh | Lý do (docs) |
|---|---|---|
| ADJ-01 | `team-leader` chạy làm agent của phiên chính: `/team:onboard` ghi `"agent": "team:team-leader"` vào `.claude/settings.json`. Chỉ phiên chính hỏi người. `analyst` và vai khác trả câu hỏi về dưới dạng file + trạng thái `NEEDS_ANSWER`. | Subagent không bao giờ có `AskUserQuestion`. |
| ADJ-02 | Giới hạn theo vai (đường dẫn được ghi, lệnh Bash được chạy, agent được gọi) do hook PreToolUse của plugin thực thi, đọc `agent_type` và bảng role-policy. Trường `tools` của agent chỉ ghi tên tool. | `tools` không nhận giới hạn đường dẫn; plugin agent bỏ qua `hooks`, `permissionMode`, `mcpServers`. |
| ADJ-03 | Chạy headless có sửa file thì KHÔNG dùng `--bare`. `--bare` chỉ cho báo cáo chỉ đọc (status, metrics). | `--bare` tắt mọi hook, kể cả hook của plugin. |
| ADJ-04 | Độ sâu gọi: phiên chính (team-leader) → tech-lead → dev/reviewer → Explore = 3 tầng, đúng mặc định `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`. Không hạ giá trị này. | Subagent lồng nhau tối đa 3 tầng mặc định. |
| ADJ-05 | Mục plugin trong `marketplace.json` không ghi `version`; chỉ `plugin.json` ghi. | Ghi cả hai thì `plugin.json` thắng và validate cảnh báo. |
| ADJ-06 | `effort` nhận `low|medium|high|xhigh|max`; SessionStart có thêm matcher `fork`. | Docs hiện hành. |
| ADJ-07 | Bỏ `TaskCreate/TaskUpdate` khỏi tool của team-leader; `tasks.md` là trạng thái. | Hai tool này chỉ mặc định có trên model cũ. |
| ADJ-08 | Cài cục bộ (`install-local.sh`, `npx skills`) không có namespace: lệnh là `/team-<tên>` (ADJ-22). Hook được nối vào `.claude/settings.json` (P5). `npx skills` chỉ cài skill. | `${CLAUDE_PLUGIN_ROOT}` và `hooks/hooks.json` chỉ có hiệu lực trong plugin. |
| ADJ-09 | Cổng áp theo cỡ việc: cỡ S không qua G1 theo thiết kế; playbook refactor bật G2b. | Đọc đơn giản nhất của SPEC §4. |
| ADJ-10 | `designer` mặc định opus; team-leader truyền `model: sonnet` khi gọi cho việc cỡ S/M. | Một file agent chỉ có một `model`. |
| ADJ-11 | Bổ sung tool so với SPEC §3: `Write` cho tech-lead và qa (phải tạo `plan.md`, `tasks.md`, `review-NN.md`, `acceptance.md`); `Skill` cho mọi vai (dùng skill tạm, `/team:commit`); bỏ `AskUserQuestion` khỏi analyst (ADJ-01). | Edit không tạo được file mới; thiếu `Skill` thì subagent không gọi được skill. |
| ADJ-12 | Skill `handbook` không dùng `` !`cat` ``; bước 1 của nó là Read `${CLAUDE_PLUGIN_ROOT}/handbook/STD-short.md` (dự phòng `<kit>`). | Thử nghiệm: khi nạp sẵn vào subagent, lệnh `!` đi qua kiểm quyền và subagent KHÔNG khởi động được ở chế độ `dontAsk`, kể cả khi cho phép `Bash(cat *)`. |
| ADJ-13 | Skill fork sang vai ghi tên có tiền tố plugin: `agent: team:<vai>`; đặt `background: false` để `/team:run` chạy nối tiếp. | Thử nghiệm: tên trần (`analyst`) bị bỏ qua, skill chạy bằng agent chung. Skill fork mặc định chạy nền. |
| ADJ-14 | `make-skill`, `make-agent` để Claude gọi được (không `disable-model-invocation`): team-leader tạo skill tạm khi cần (SPEC §9). `pr` và `audit-kit` fork sang tech-lead và coach. | Prompt P4 vừa liệt kê hai skill này là "chỉ người gọi" vừa nói team-leader gọi chúng; team-leader chỉ đọc Bash nên không tự mở PR được. |
| ADJ-15 | Skill không dùng `` !`lệnh` ``; điều kiện trước là một bước chạy `python3 "$(cat .team/plugin_root)/scripts/team.py" status` bằng Bash. | Cùng lý do ADJ-12: lệnh `!` đi qua kiểm quyền và có thể chặn skill khởi động. |
| ADJ-16 | Playbook `data-migration` bật G2b (duyệt `design.md`), như `refactor`. | SPEC không nói; rủi ro mất dữ liệu. |
| ADJ-17 | Hook `role-policy.sh` + `hooks/role-policy.json` thực thi ADJ-02. Khi `.team/current.json` có `stage: onboard`, team-leader được ghi thêm `CLAUDE.md`, `.claude/rules/`, `.github/`, `.gitignore`. | Onboard chạy trong phiên chính (team-leader). |
| ADJ-18 | `scripts/render.py` dựng file dự án từ template (thay `{{…}}`, nở danh sách, gộp không ghi đè); `scripts/teamlib.py` chứa logic chung của hook. | Tránh để LLM tự điền JSON settings. |
| ADJ-19 | `Read(//<kit>/**)` ghi vào `.claude/settings.local.json`, không phải settings dùng chung. | Đường dẫn kit khác nhau giữa các máy; dry-run P4 cho thấy cần quyền này. |
| ADJ-20 | `stop-check.sh` chạy cả ở SubagentStop của `team:dev`, `team:maintainer`, `team:researcher`. | Vòng build chạy trong subagent; chỉ Stop của phiên chính thì quá muộn. |
| ADJ-21 | STD-GIT-3 ở mức máy: chỉ push `team/*` hoặc tag; `--force-with-lease` cũng bị chặn; Edit/Write vào `.claude/settings*.json` bị chặn. | Đơn giản nhất và an toàn nhất. |
| ADJ-22 | Cài cục bộ: `install-local.sh` bỏ tiền tố `team:` của tên agent, đổi skill thành `team-<tên>` (tránh đụng `/status`, `/run`, `/verify`…), gộp hook vào `.claude/settings.json`; role-policy nhận cả tên không tiền tố. | Không có namespace plugin khi cài cục bộ. |
| ADJ-23 | coach ghi: `docs/team/retro/**`, `docs/team/proposals/**`, `docs/team/kit-issues.md` (audit-kit), `docs/team/metrics/scorecard.json` (chỉ qua `team.py scorecard`), `.team/current.json`, memory của mình — một danh sách trong `agents/coach.md` = `hooks/role-policy.json`. | SPEC §3 chỉ nêu retro/proposals, nhưng audit-kit phải ghi kit-issues và mọi giai đoạn ghi `current.json` (K-43). |
| ADJ-24 | Không có khe deploy cho prod hay rollback (SPEC §8 chỉ có `deploy.staging`, `deploy.smoke`, `deploy.prod_requires_reviewer`): lệnh prod và rollback đã kiểm nằm ở `docs/team/ci.md` mục `## Deploy`, do `/team:ci deploy-script` viết qua PR. devops chỉ kích hoạt đúng lệnh/pipeline đó sau `Approved-by-prod:`; ưu tiên job CI có environment bắt người duyệt (STD-OPS-7). | SPEC §13 cấm bịa khe; đề xuất khe mới trong báo cáo. |
| ADJ-25 | researcher được ghi mọi file trong worktree riêng `.claude/worktrees/<n>/` (POC), không ghi cây chính (`worktree_write` trong role-policy). | SPEC §3 "POC in worktree" không làm được khi role-policy chỉ cho `docs/team/**`. |
| ADJ-26 | `team.py`: playbook không có analyze (bug-fix, hotfix, refactor, dependency-upgrade, spike, ci-fix, docs-only) không cần `spec.md`; bug-fix, hotfix, refactor không cần `plan.md`; refactor được tính `built` khi `/team:clean` ghi `tasks.md` (T1 tick). | Chuỗi SPEC §5 của các playbook này không có bước đó; trước đây trạng thái kẹt (K-47). |
| ADJ-27 | analyst, architect, designer, writer có tool `Bash`, chỉ để chạy lệnh chỉ-đọc (`team.py status`, `explore-cache.sh`, `git log`); role-policy giữ `bash: read-only`. | Skill của các vai này cần kiểm trạng thái; eval analyze s1 (2026-11-09) cho thấy analyst bỏ bước vì không có Bash (K-52). |
| ADJ-28 | `intake` để Claude gọi được (bỏ `disable-model-invocation`): khi người gõ yêu cầu thô, team-leader tự chạy `/team:intake`. | SPEC §3: team-leader làm intake; trước đây `using-team` trỏ tới một skill chỉ người gọi được (K-70). |
| ADJ-29 | Cỡ S vẫn nghiệm thu bằng `/team:verify` (qa, bước kiểm thu gọn), không phải "verify tự động không có qa riêng"; qa tính trong trần 3 vai của cỡ S (analyst, tech-lead, qa). | SPEC §4 nói "verify (automated, no separate qa)"; kit giữ người nghiệm thu độc lập vì cỡ S cũng có thể sai (K-15, K-78). |
