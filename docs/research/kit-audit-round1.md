# Kiểm định chất lượng bộ kit — vòng 1 (P7)

- Ngày: 2026-11-09 · Claude Code 2.1.319 · trạng thái TRƯỚC: tag `pre-p7-round1` (= `v0.1.0`, commit a6b7036)
- Công cụ: `python3 scripts/kit-metrics.py` (chuẩn trong `scripts/skill-budgets.txt`, `skill-sections.txt`, `agent-sections.txt`)
- Chuẩn: skill nạp thường xuyên ≤ 400 chữ, 4 mục; skill khác 1.200–2.500 chữ, 10 mục; agent 600–1.200 chữ, 10 mục.

## TRƯỚC
| Mục | Lớp | Chữ | Ngân sách | Tiêu đề | Tự bào chữa | Dấu hiệu sai | Kiểm chứng | Mô tả | refs | Score | Đạt |
|---|---|---|---|---|---|---|---|---|---|---|---|
| skill:asbuilt | full | 266 | 1200–2500 | 2/10 (thứ tự) | 0 | 3 | 0 | 127 | 0 | 19 | — |
| skill:commit | full | 242 | 1200–2500 | 2/10 (thứ tự) | 0 | 3 | 0 | 82 | 0 | 19 | — |
| skill:make-agent | full | 267 | 1200–2500 | 2/10 (thứ tự) | 0 | 3 | 0 | 146 | 1 | 19 | — |
| skill:session | full | 260 | 1200–2500 | 2/10 (thứ tự) | 0 | 3 | 0 | 117 | 0 | 19 | — |
| skill:architect | full | 277 | 1200–2500 | 2/10 (thứ tự) | 0 | 3 | 0 | 146 | 0 | 20 | — |
| skill:audit-kit | full | 272 | 1200–2500 | 2/10 (thứ tự) | 0 | 3 | 0 | 161 | 1 | 20 | — |
| skill:ci | full | 296 | 1200–2500 | 2/10 (thứ tự) | 0 | 3 | 0 | 117 | 0 | 20 | — |
| skill:clean | full | 298 | 1200–2500 | 2/10 (thứ tự) | 0 | 3 | 0 | 128 | 0 | 20 | — |
| skill:design | full | 277 | 1200–2500 | 2/10 (thứ tự) | 0 | 3 | 0 | 169 | 0 | 20 | — |
| skill:plan | full | 282 | 1200–2500 | 2/10 (thứ tự) | 0 | 3 | 0 | 150 | 0 | 20 | — |
| skill:pr | full | 290 | 1200–2500 | 2/10 (thứ tự) | 0 | 3 | 0 | 131 | 0 | 20 | — |
| skill:make-skill | full | 305 | 1200–2500 | 2/10 (thứ tự) | 0 | 3 | 0 | 145 | 1 | 21 | — |
| skill:retro | full | 303 | 1200–2500 | 2/10 (thứ tự) | 0 | 3 | 0 | 112 | 0 | 21 | — |
| skill:research | full | 294 | 1200–2500 | 2/10 (thứ tự) | 0 | 4 | 0 | 128 | 0 | 22 | — |
| skill:verify | full | 274 | 1200–2500 | 2/10 (thứ tự) | 0 | 4 | 0 | 118 | 0 | 22 | — |
| skill:analyze | full | 325 | 1200–2500 | 2/10 (thứ tự) | 0 | 4 | 0 | 112 | 0 | 23 | — |
| skill:release | full | 304 | 1200–2500 | 2/10 (thứ tự) | 0 | 4 | 0 | 109 | 0 | 23 | — |
| skill:build | full | 350 | 1200–2500 | 2/10 (thứ tự) | 0 | 4 | 0 | 136 | 0 | 24 | — |
| skill:onboard | full | 393 | 1200–2500 | 2/10 (thứ tự) | 0 | 4 | 0 | 157 | 1 | 26 | — |
| skill:takeover | full | 433 | 1200–2500 | 2/10 (thứ tự) | 0 | 4 | 0 | 135 | 1 | 27 | — |
| agent:qa | agent | 337 | 600–1200 | 2/10 (thứ tự) | 0 | 0 | — | 129 | 0 | 28 | — |
| agent:researcher | agent | 334 | 600–1200 | 2/10 (thứ tự) | 0 | 0 | — | 132 | 0 | 28 | — |
| agent:writer | agent | 335 | 600–1200 | 2/10 (thứ tự) | 0 | 0 | — | 140 | 0 | 28 | — |
| agent:analyst | agent | 345 | 600–1200 | 2/10 (thứ tự) | 0 | 0 | — | 119 | 0 | 29 | — |
| agent:architect | agent | 348 | 600–1200 | 2/10 (thứ tự) | 0 | 0 | — | 140 | 0 | 29 | — |
| agent:coach | agent | 350 | 600–1200 | 2/10 (thứ tự) | 0 | 0 | — | 144 | 0 | 29 | — |
| agent:designer | agent | 342 | 600–1200 | 2/10 (thứ tự) | 0 | 0 | — | 133 | 0 | 29 | — |
| agent:dev | agent | 342 | 600–1200 | 2/10 (thứ tự) | 0 | 0 | — | 143 | 0 | 29 | — |
| agent:devops | agent | 342 | 600–1200 | 2/10 (thứ tự) | 0 | 0 | — | 146 | 0 | 29 | — |
| agent:maintainer | agent | 346 | 600–1200 | 2/10 (thứ tự) | 0 | 0 | — | 149 | 0 | 29 | — |
| agent:reviewer | agent | 349 | 600–1200 | 2/10 (thứ tự) | 0 | 0 | — | 128 | 0 | 29 | — |
| agent:team-leader | agent | 345 | 600–1200 | 2/10 (thứ tự) | 0 | 0 | — | 164 | 0 | 29 | — |
| agent:tech-lead | agent | 342 | 600–1200 | 2/10 (thứ tự) | 0 | 0 | — | 130 | 0 | 29 | — |
| skill:feedback | always | 222 | 0–400 | 0/4 (thứ tự) | 0 | — | — | 103 | 0 | 50 | — |
| skill:handbook | always | 182 | 0–400 | 0/4 (thứ tự) | 0 | — | — | 84 | 0 | 50 | — |
| skill:intake | always | 194 | 0–400 | 0/4 (thứ tự) | 0 | — | — | 78 | 0 | 50 | — |
| skill:run | always | 189 | 0–400 | 0/4 (thứ tự) | 0 | — | — | 110 | 0 | 50 | — |
| skill:status | always | 138 | 0–400 | 0/4 (thứ tự) | 0 | — | — | 80 | 0 | 50 | — |
| skill:using-team | always | 200 | 0–400 | 0/4 (thứ tự) | 0 | — | — | 138 | 0 | 50 | — |

| Nhóm | Số mục | Trung vị chữ | % đạt chuẩn | Trung vị score |
|---|---|---|---|---|
| always | 6 | 191.5 | 0% | 50.0 |
| full | 20 | 292.0 | 0% | 20.0 |
| agent | 13 | 342 | 0% | 29 |
| discipline skills | 8 | 297.5 | — | — |
| tất cả | 39 | — | 0% | — |

## Vấn đề mở (blocker/major) → mục bị ảnh hưởng
Không còn blocker mở sau v0.1.0. Major còn mở (từ `docs/kit-issues.md`, `evals/RESULTS.md`):

| Vấn đề | Mức | Mục bị ảnh hưởng | Xử lý vòng 1 |
|---|---|---|---|
| K-34 cỡ S bỏ reviewer (team-leader gọi thẳng dev) | major | agent team-leader, skill build, skill run | Viết lại: cỡ S vẫn qua `/team:build` (1 dev + reviewer) |
| K-15 định nghĩa `max_agents_per_feature`; verify cỡ S luôn fork qa | major | agent team-leader, skill verify, config | Viết lại: đếm VAI khác nhau, không tính gọi lại trong vòng sửa |
| K-16/K-19 team-leader đọc cổng sai, cổng chặn cả đội | minor→ảnh hưởng hành vi | agent team-leader, skill run, intake | Viết lại: cổng chỉ theo `team.py`, chỉ chặn feature của nó |
| K-33 eval using-team không phân biệt hai chế độ | minor | evals/using-team | Viết lại kịch bản 1 |
| K-06 headless phải truyền `--allowedTools` | major | workflows/batch, team-feature.yml | Vòng sau (không phải nội dung skill/agent) |
| K-24 Bash của vai `bash: any` không qua protect | major | hooks, teamlib | Vòng sau (luật máy) |

## SAU (vòng 1 xong, 2026-11-09)
| Nhóm | Số mục | Trung vị chữ | % đạt chuẩn | Trung vị score |
|---|---|---|---|---|
| always | 6 | 309 | 100% | 100 |
| full | 20 | 303.5 | 35% (7/20) | 21.5 |
| agent | 13 | 348 | 38% (5/13) | 29 |
| discipline skills | 8 | **1.502,5** | — | — |
| tất cả | 39 | — | 46% (18/39) | — |

100% mục đã viết lại đạt chuẩn (18/18). Mục chưa viết lại nằm trong `scripts/quality-backlog.txt` (21 mục).

## Mục đã viết lại
Ref: A = `/tmp/ref/agent-skills/skills`, AA = `/tmp/ref/agent-skills/agents`, S = `/tmp/ref/superpowers/skills`, V = `/tmp/ref/awesome-claude-code-subagents/categories`, W = `/tmp/ref/agents/plugins`, B = `/tmp/ref/BMAD-METHOD`. Ghi chú đọc chi tiết: `refnotes/A-planning.md`, `B-build.md`, `C-agents.md` (scratch của phiên P7).

| Mục | Score trước | Score sau | Chữ trước → sau | Tham khảo đã đọc | Lấy | Bỏ |
|---|---|---|---|---|---|---|
| skill:using-team | 50 | 100 | 200 → 395 | A/using-agent-skills, S/using-superpowers, S/writing-skills | bảng loại việc → skill; thứ tự ưu tiên; subagent không khám phá lại | "1% là phải gọi"; TodoWrite; skill của plugin khác |
| skill:handbook | 50 | 100 | 182 → 375 | S/verification-before-completion | ghi file bằng Write; bảng tự bào chữa | — |
| skill:status | 50 | 100 | 138 → 273 | S/subagent-driven-development (resuming) | in nguyên đầu ra; cổng theo cột "Cổng áp dụng" | — |
| skill:run | 50 | 100 | 189 → 313 | S/executing-plans | cổng chỉ theo team.py (K-02); cỡ S qua build (K-34); dừng khi giai đoạn không đổi | chạy liên tục không dừng |
| skill:intake | 50 | 100 | 194 → 305 | A/spec-driven-development | cổng chỉ chặn feature của nó (K-19) | — |
| skill:feedback | 50 | 100 | 222 → 263 | — | ghi bằng Write (K-10) | — |
| skill:analyze | 23 | 100 | 325 → 1.590 | A/interview-me, A/spec-driven-development, S/brainstorming | giả thuyết + độ tin cậy; nhìn trước khi hỏi; phép thử dừng hỏi; đổi tính từ thành số; câu trả lời mơ hồ | hỏi từng câu một với người; mẫu spec có lệnh stack; design doc |
| skill:plan | 20 | 100 | 282 → 1.316 | A/planning-and-task-breakdown, S/writing-plans | bản đồ file trước; khối Nhận/Trả; ràng buộc chung; tự kiểm 5 điểm; không ghi đè kế hoạch dở | đường dẫn tasks/plan.md; lệnh ghi cứng; menu bàn giao |
| skill:takeover | 27 | 100 | 433 → 1.510 | A/context-engineering, A/source-driven-development, B/preparing-a-repo-for-agents | bảng khẳng định/thực tế; độ cũ tài liệu; dòng ngân sách mỗi tầng; nội dung đáng ngờ; kiểm chỉ-đọc cuối | tra docs ngoài; viết AGENTS.md lúc takeover |
| skill:build | 24 | 100 | 350 → 1.504 | S/subagent-driven-development (+prompt, fix-loop, preflight, resuming), S/executing-plans, S/test-driven-development, A/test-driven-development, A/incremental-implementation | trạng thái DONE/…/BLOCKED; đỏ đúng lý do; BASE..HEAD; gói review; xem lại có phạm vi; ngắt vòng; chạy tiếp từ đĩa | reviewer chạy test; 5 vòng; thư mục ledger riêng; merge vào base |
| skill:verify | 22 | 100 | 274 → 1.510 | S/verification-before-completion, A/code-review-and-quality, A/debugging-and-error-recovery | cổng cho từng tiêu chí; gắn commit; bảng khẳng định cần gì; phân loại lỗi; bằng chứng hồi quy | qa tự hoàn tác code; menu merge |
| skill:commit | 19 | 100 | 242 → 1.501 | A/git-workflow-and-versioning, A/incremental-implementation, A/code-review-and-quality | xem phần đã stage; quét secret; phép thử nguyên tử; xử lý hook lỗi; điểm lưu | nhánh feature/; reset --hard; bisect |
| skill:pr | 20 | 100 | 290 → 1.425 | S/receiving-code-review, S/finishing-a-development-branch, S/requesting-code-review | test sau rebase; phân loại bình luận trước khi sửa; YAGNI; không xã giao; kiểm CI | merge cục bộ; gh api cho luồng trả lời; force-push |
| agent:team-leader | 29 | 100 | 345 → 1.062 | W/agent-teams/team-lead, V/09-meta-orchestration/{multi-agent-coordinator,agent-organizer}, B/craft-subagents | đếm vai (K-15); bàn giao bằng file; xử lý theo trạng thái trả; chạy tiếp từ artifact | nhắn tin ngang hàng; vai điều phối riêng |
| agent:tech-lead | 29 | 100 | 342 → 945 | S/subagent-driven-development (fix-loop, handling-reports, cannot-verify, preflight), W/agent-teams/team-lead | preflight; BASE; ngắt vòng có phán định; mục "không kiểm chứng được" | gọi lại cùng dev bằng SendMessage; cấm song song |
| agent:dev | 29 | 100 | 342 → 959 | S/subagent-driven-development/implementer-prompt, W/agent-teams/team-implementer, AA/test-engineer, W/debugging-toolkit/debugger | đỏ đúng lý do; mốc ban đầu; "thấy nhưng không chạm"; trạng thái trả | hỏi người; checklist làm-mọi-thứ |
| agent:reviewer | 29 | 100 | 349 → 946 | S/subagent-driven-development/{task-reviewer,re-review}-prompt, AA/code-reviewer, W/agent-teams/team-reviewer, AA/security-auditor | test trước code; thiếu/thừa/hiểu sai; lời giải thích không hạ mức; confirmed/suspected | reviewer có Write/Edit; ngưỡng số bịa |
| agent:qa | 28 | 100 | 337 → 902 | V/04-quality-security/{qa-expert,test-automator}, AA/test-engineer, S/verification-before-completion | gắn commit; ngoài đường thuận; KHÔNG KIỂM ĐƯỢC → NEEDS_ANSWER; 3 lần chạy cho chập chờn | qa viết test; số liệu bịa |
