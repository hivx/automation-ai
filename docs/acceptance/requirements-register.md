# Sổ yêu cầu — trích từ `docs/requirements/ban-hieu-yeu-cau.md`

Mỗi dòng là một câu kiểm được. REQ-ID = `REQ-<Phần><Mục>-<n>`. Kết quả nằm ở `traceability-2026-11-10.md`.

| REQ-ID | Phần/mục | Yêu cầu | Loại | Cách kiểm | Mức |
|---|---|---|---|---|---|
| REQ-A1-1 | A1 | Repo `automation-ai`, plugin `team`, chứa agent + skill + quy tắc + hướng dẫn + workflow, cài một lệnh vào bất kỳ dự án nào (mọi ngôn ngữ) | structure | đọc manifest, chạy `claude plugin validate .`, đếm thư mục, grep lệnh stack | must |
| REQ-A1-2 | A1.1 | Hiểu dự án trước bằng quét có kiểm soát chi phí, viết báo cáo cho anh duyệt | content | đọc skills/takeover/SKILL.md, templates/artifacts/assessment.md | must |
| REQ-A1-3 | A1.2 | Yêu cầu thô → hỏi/tự quyết → nghiên cứu → thiết kế → chia task → build → nghiệm thu → tài liệu → commit/PR/CI-CD/deploy | structure | đối chiếu danh sách skill với chuỗi | must |
| REQ-A1-4 | A1.3 | Anh chỉ duyệt ở cổng, hoặc cho chạy tự động hoàn toàn | behavior | đổi `gates.G1_spec` trên dự án tạm, chạy `team.py status` | must |
| REQ-A1-5 | A1.4 | Đội tự đo, tự ghi chép, tự đề xuất cải tiến; anh duyệt trước khi áp dụng | behavior | chạy measure.py trên fixtures; đọc templates/artifacts/proposal.md | must |
| REQ-A1-6 | A1 (cuối) | Repo không do Claude chat viết trực tiếp; Claude Code chạy chuỗi prompt, anh duyệt từng bước | process | tìm dấu vết | should |
| REQ-A2-1 | A2 | Không riêng cho Frappe/ERPNext hay stack nào; không chứa tri thức nghiệp vụ dự án | content | grep -i frappe/erpnext; đọc templates | must |
| REQ-A2-2 | A2 | Không tự deploy production khi cổng bật | behavior | grep Approved-by-prod trong hook; đọc devops | must |
| REQ-A2-3 | A2, A4-PV | Không viết MCP server hay plugin mới trong bản 1 | structure | find .mcp.json, plugin.json khác, mcpServers | must |
| REQ-A3-1 | A3 #1 | Mỗi agent có hợp đồng: làm/không làm, vào, ra, tiêu chí xong, tool, giới hạn turn; có team-leader quản lý, tech-lead làm chính; không agent "làm tất cả" | structure | đọc scripts/agent-sections.txt, frontmatter 13 agent, kit-metrics | must |
| REQ-A3-2 | A3 #2 | Trạng thái nằm trên đĩa; vị trí TÍNH từ artifact, không lưu con trỏ riêng | behavior | dự án tạm: `.team/current.json` ghi stage "released" nhưng chỉ có intake.md; chạy `team.py status --root` | must |
| REQ-A3-3 | A3 #3 | Hook/permission/script là luật chạy 100%; điều không được sai phải là máy | behavior | gửi JSON hook giả vào check-git.sh, protect.sh | must |
| REQ-A3-4 | A3 #4 | Lõi độc lập nền tảng; lệnh build/test/lint, cấu trúc, quy ước tên ở `.team/profile.json`; agent/hook chỉ tham chiếu khe | config | jq profiles/_template.json; validate blacklist | must |
| REQ-A3-5 | A3 #5 | Mỗi lần gọi có lý do một câu ghi journal; không gọi mặc định | content | đọc team-leader.md, using-team | must |
| REQ-A3-6 | A3 #5 | Việc nhỏ team-leader tự xử hoặc giao MỘT agent duy nhất | config | đọc config + team-leader bước 6–7 | must |
| REQ-A3-7 | A3 #6 | Đo định lượng + journal định tính; sửa có bằng chứng, eval trước/sau, canary, rollback | content | đọc proposal.md, evals/run-eval.sh, retro | must |
| REQ-A3-8 | A3 #7 | Cổng là cấu hình bật/tắt; đề xuất là ghi chú chờ duyệt | behavior | như REQ-A1-4 | must |
| REQ-A3-9 | A3 #7 + #3 | Không lách cổng đang bật (điều không được sai phải là máy) | behavior | giả Write của team:analyst / team:team-leader thêm "Approved-by: Bot" vào spec.md, chạy protect.sh + role-policy.sh | must |
| REQ-A3-10 | A3 (nguyên tắc 2) | Hành vi: xóa `.team/current.json`, phiên mới `/team:status` cho cùng vị trí | behavior | B7: team.py trước/sau + `/team:status` sống ở phiên mới | must |
| REQ-A4-1 | A4 #1 | Cài: `/plugin marketplace add <owner>/automation-ai` → `/plugin install team@automation-ai` | config | đọc marketplace.json, README; `claude plugin validate .` | must |
| REQ-A4-2 | A4 #1 | Hỗ trợ `npx skills add <owner>/automation-ai` | behavior | đọc README, bố cục skills/ | must |
| REQ-A4-3 | A4 #1 | Chép thư mục `.claude/` bằng script | behavior | chạy install-local.sh vào dự án tạm | must |
| REQ-A4-4 | A4 #2, #3 | Chuỗi 7 prompt P0–P6 có tiêu chí nghiệm thu; Claude máy anh PHẢI tra docs chính thức trước khi viết | process | tìm dấu vết trong repo | must |
| REQ-A4-5 | A4 #4 | Tên vai `team-leader` (quản lý), `tech-lead` (làm chính) | structure | ls agents, frontmatter name | must |
| REQ-A4-6 | A4 #5 | Coach đầy đủ từ bản 1: đo bằng thuật toán, chẩn đoán 5 nguyên nhân, đề xuất có diff + eval, canary cỡ S; áp dụng qua anh | content | đọc coach.md, retro SKILL.md, proposal.md, chạy measure.py | must |
| REQ-A4-7 | A4 #6 | Tên repo `automation-ai`, plugin `team`, trung tính, không gắn Miyano | config | grep -i miyano/ai-dev-team | must |
| REQ-A4-8 | A4 #7 | GitHub issue mặc định; profile có khe `tracker` để nối Jira/Linear/Notion sau | config | jq .tracker profiles/*.json; schema | must |
| REQ-A4-9 | A4 #8 | maintainer, devops là vai riêng | structure | ls agents; role-policy keys | must |
| REQ-A4-10 | A4 #9 | Skill/agent tạm chỉ tạo khi cần, không tạo sẵn lúc cài; team-leader điều phối make-skill/make-agent; ghi journal; anh duyệt khi thăng cấp | behavior | chạy install-local; đọc onboard, make-skill | must |
| REQ-A4-11 | A4 #10 | Playbook bổ sung data-migration, integration, client-docs → tổng 16 | structure | ls workflows/*.md trừ README; đọc data-migration | must |
| REQ-A4-12 | A4 #11 | Báo cáo takeover: xương sống 3 câu hỏi (làm gì / đến đâu / cần làm gì); kỹ thuật là phụ lục | content | grep tiêu đề assessment.md | must |
| REQ-A4-13 | A4 điểm 1 | Hành vi: cài bằng marketplace nạp đủ 13 agent và 26 skill | behavior | B12: marketplace add <đường dẫn> + plugin install --scope project; hỏi phiên mới | must |
| REQ-A4-14 | A4 điểm 1 | Hành vi: `scripts/install-local.sh` chép kit và nạp được | behavior | B12: install-local vào dự án mới; hỏi phiên mới | must |
| REQ-A5-1 | A5 | Nội dung agent, skill, rule, tài liệu, prompt bằng tiếng Việt | content | lấy mẫu 10 file: agents/dev.md, skills/build/SKILL.md, docs/01-process.md, templates/artifacts/spec.md, workflows/hotfix.md, handbook/STD.md, scripts/protect.sh, scripts/validate.sh, hooks/role-policy.json, profiles/python.json | must |
| REQ-A5-2 | A5 | Định danh (tên file, key JSON, tên skill/agent, mã STD, nhánh, script) bằng tiếng Anh | structure | find tên file non-ASCII; jq keys | must |
| REQ-B1-1 | B1 | Có đủ 13 vai, tên file khớp `name` | structure | ls agents/; đọc frontmatter | must |
| REQ-B1-2 | B1 | team-leader tools = Read, Grep, Glob, Bash(đọc), Agent, TaskCreate/Update, AskUserQuestion, Write(docs/team/**) | config | frontmatter + role-policy.json | must |
| REQ-B1-3 | B1 | team-leader sonnet / low / maxTurns 30 | config | frontmatter | must |
| REQ-B1-4 | B1 | team-leader: được làm (intake, playbook & cỡ, hỏi/quyết, gọi có lý do, giữ cổng, leo thang, journal, điều phối skill tạm, nâng/hạ cỡ) / không viết code, spec, review; độ sâu | content | đọc thân + kit-metrics | must |
| REQ-B1-5 | B1 | tech-lead tools = Read, Grep, Glob, Bash(git, test), Agent, Edit(docs/team/**) | config | frontmatter + role-policy | must |
| REQ-B1-6 | B1 | tech-lead sonnet / medium / 60 | config | frontmatter | must |
| REQ-B1-7 | B1 | tech-lead: plan, task 2–5 phút có touchpoints, giao dev, review 2 tầng, tích hợp nhánh, tick, note task / không tự code, không bỏ review | content | đọc thân + kit-metrics | must |
| REQ-B1-8 | B1 | coach tools = Read, Grep, Glob, Bash(đọc), Write(retro/**, proposals) | config | frontmatter + role-policy | must |
| REQ-B1-9 | B1 | coach opus / high / 40 | config | frontmatter | must |
| REQ-B1-10 | B1 | coach: scorecard+journal → nút thắt → 5 nguyên nhân → đề xuất diff+eval → canary S → giữ/rollback/thay/gỡ; audit kit / không tự áp, không sửa kit, không sửa code | content | đọc thân + retro skill | must |
| REQ-B1-11 | B1 | analyst tools = Read, Grep, Glob, Agent(Explore), AskUserQuestion, Write(docs/team/**) | config | frontmatter + role-policy | must |
| REQ-B1-12 | B1 | analyst opus / high / 40 | config | frontmatter | must |
| REQ-B1-13 | B1 | analyst: spec + DoD, chuẩn hoá (Explore) → triage 7 mục → hỏi/quyết → spec, amendment / không chọn công nghệ, không thiết kế | content | đọc thân | must |
| REQ-B1-14 | B1 | researcher tools = Read, Grep, Glob, Bash, WebFetch, WebSearch, Agent, Write(docs/team/**) | config | frontmatter + role-policy | must |
| REQ-B1-15 | B1 | researcher opus / high / 50 | config | frontmatter | must |
| REQ-B1-16 | B1 | researcher: docs chính thức có URL + ngày, so phương án, POC trong worktree, nháp ADR, cache theo version / không quyết thay architect | content | đọc thân | must |
| REQ-B1-17 | B1 | architect tools = Read, Grep, Glob, Agent, Write(docs/team/**) | config | frontmatter + role-policy | must |
| REQ-B1-18 | B1 | architect opus / high / 40 | config | frontmatter | must |
| REQ-B1-19 | B1 | architect: kiến trúc từ NFR, ADR, đánh giá tác động, review thiết kế 3 câu / không code | content | đọc thân | must |
| REQ-B1-20 | B1 | designer tools = Read, Grep, Glob, Agent, Write(docs/team/**) | config | frontmatter + role-policy | must |
| REQ-B1-21 | B1 | designer opus / high (sonnet cỡ S/M) / 40 | config | frontmatter + skill design | must |
| REQ-B1-22 | B1 | designer: dữ liệu, API, luồng, quyền, migration, touchpoints, test plan / không đổi kiến trúc, không quyết nghiệp vụ | content | đọc thân | must |
| REQ-B1-23 | B1 | dev tools = Read, Edit, Write, Grep, Glob, Bash | config | frontmatter + role-policy | must |
| REQ-B1-24 | B1 | dev sonnet / medium / 60 | config | frontmatter | must |
| REQ-B1-25 | B1 | dev: một task, worktree, test fail trước, lệnh từ profile, lint sạch, commit chuẩn, chỉ touchpoints / không mở rộng phạm vi, sửa thiết kế, push nhánh chính, skip test | content | đọc thân | must |
| REQ-B1-26 | B1 | reviewer tools = Read, Grep, Glob, Bash(đọc); memory: project | config | frontmatter + role-policy | must |
| REQ-B1-27 | B1 | reviewer opus / high / 25 | config | frontmatter | must |
| REQ-B1-28 | B1 | reviewer: ngữ cảnh mới, chỉ diff + design + handbook; finding có STD, mức, file:line, cách sửa; verdict 3 loại / không sửa code, không góp ý ngoài STD | content | đọc thân | must |
| REQ-B1-29 | B1 | qa tools = Read, Grep, Glob, Bash; memory: project | config | frontmatter + role-policy | must |
| REQ-B1-30 | B1 | qa opus / high / 40 | config | frontmatter | must |
| REQ-B1-31 | B1 | qa: nghiệm thu từng tiêu chí bằng lệnh + output thật, DoD, migration lên/xuống, README, verdict 3 loại / không sửa code, không tin mô tả | content | đọc thân | must |
| REQ-B1-32 | B1 | writer tools = Read, Grep, Glob, Write(docs/**, CHANGELOG) | config | frontmatter + role-policy | must |
| REQ-B1-33 | B1 | writer sonnet / medium / 30 | config | frontmatter | must |
| REQ-B1-34 | B1 | writer: As-Built (khác design ở đâu), release notes, CHANGELOG, README, mô tả PR / không sửa code | content | đọc thân | must |
| REQ-B1-35 | B1 | maintainer tools = Read, Edit, Write, Grep, Glob, Bash | config | frontmatter + role-policy | must |
| REQ-B1-36 | B1 | maintainer sonnet / medium / 60 | config | frontmatter | must |
| REQ-B1-37 | B1 | maintainer: dọn không đổi hành vi, một loại một PR, simplification/deprecation/observability / không đổi hành vi, không gộp vào feature | content | đọc thân | must |
| REQ-B1-38 | B1 | devops tools = Read, Edit, Write, Grep, Glob, Bash(gh, ci) | config | frontmatter + role-policy + thử hook | must |
| REQ-B1-39 | B1 | devops sonnet / medium / 60 | config | frontmatter | must |
| REQ-B1-40 | B1 | devops: dựng CI/CD, chẩn đoán đỏ (phân loại trước), script deploy/rollback/smoke, docs/team/ci.md / không xoá test, không tự deploy prod, không ghi secret | content | đọc thân + grep hook | must |
| REQ-B1-41 | B1 | Agent tạm: chỉ tạo khi team-leader thấy cần, theo nhu cầu | process | skill make-agent + role-policy _temp + test | should |
| REQ-B2-1 | B2 | Chỉ team-leader và tech-lead gọi agent khác | behavior | role-policy.json agents + thử hook | must |
| REQ-B2-2 | B2 | Agent con không gọi nhau, trừ Explore | behavior | role-policy + test_hooks.sh | must |
| REQ-B2-3 | B2 | Ma trận ai gọi ai viết rõ và nhất quán | content | handbook/who-calls-whom.md vs agents/dev.md vs role-policy | should |
| REQ-B2-4 | B2 | Bàn giao = một file + tin ≤ 10 dòng, tự đủ | process | who-calls-whom + agents | must |
| REQ-B2-5 | B2 | tech-lead → dev: ID task, tiêu chí, touchpoints, cmd.test_one, nhánh, "chỉ sửa trong touchpoints" | content | tech-lead.md, build skill, handoffs.md | must |
| REQ-B2-6 | B2 | dev → tech-lead: file đã sửa, test kèm output thật, gì còn thiếu | content | dev.md, handoffs.md | must |
| REQ-B2-7 | B2 | Hook thực thi đúng khi chạy thật (agent_type có trong input của phiên chính và subagent) | behavior | cần phiên Claude thật | must |
| REQ-B3-1 | B3 | sonnet cho điều phối, dev, writer; opus cho analyst, researcher, architect, designer, reviewer, qa, coach | config | frontmatter 13 agent | must |
| REQ-B3-2 | B3 | haiku cho triage / việc cơ học | config | grep haiku | must |
| REQ-B3-3 | B3 | Không đổi model giữa phiên dài | content | grep | must |
| REQ-B3-4 | B3 | `.team/config.json → models` có giá trị từng vai | config | jq templates/project/team/config.json | must |
| REQ-B3-5 | B3 | Ghi đè models trong config có hiệu lực | behavior | grep nơi đọc `models` | must |
| REQ-C1-1 | C1 G0 | Tiếp nhận dự án: `/team:takeover`, team-leader (+Explore, researcher), 5 artifact assessment/ai-readiness/profile-proposal/debt/open-questions; G0 bật cho dự án cũ, dự án mới bỏ qua | structure | đọc skill, template, config; grep researcher | must |
| REQ-C1-2 | C1 #0 | Tiếp nhận yêu cầu: `/team:intake`, team-leader, `intake.md`, không cổng | structure | đọc skill + fixture team.py | must |
| REQ-C1-3 | C1 #1 | Phân tích: `/team:analyze`, analyst, `spec.md`, G1 bật | structure | frontmatter + config + test | must |
| REQ-C1-4 | C1 #2 | Nghiên cứu: `/team:research`, researcher, `research.md` + cache `docs/team/research/` | structure | đọc skill | must |
| REQ-C1-5 | C1 #3 | Kiến trúc: `/team:architect`, architect, `architecture.md` hoặc `arch-impact.md`, `adr/ADR-NNN.md`, G2 bật | structure | đọc skill + fixture | must |
| REQ-C1-6 | C1 #4 | Thiết kế chi tiết: `/team:design`, designer, `design.md`, G2b tắt | structure/config | frontmatter + config | must |
| REQ-C1-7 | C1 #5 | Kế hoạch: `/team:plan`, tech-lead, `plan.md` + `tasks.md`, G3 bật | structure | frontmatter + test | must |
| REQ-C1-8 | C1 #6 | Xây dựng: `/team:build`, tech-lead → dev, reviewer; code, commit, `review-NN.md`, tick task | structure | đọc skill | must |
| REQ-C1-9 | C1 #7 | Nghiệm thu: `/team:verify`, qa, `acceptance.md`, G4 bật | structure | frontmatter + test | must |
| REQ-C1-10 | C1 #8 | Phát hành: `/team:asbuilt`, `/team:pr`, `/team:release`; writer, tech-lead, devops; asbuilt/CHANGELOG/PR/deploy; G5 luôn là người | structure/behavior | đọc skill + fixture | must |
| REQ-C1-11 | C1 #9 | Vận hành: `/team:intake --type bug`, `/team:clean`, `/team:ci`, `/team:retro`; team-leader, maintainer, devops, coach; `defects.md`, `debt.md`, `retro/` | structure | ls templates; grep defects | must |
| REQ-C1-12 | C1 mở cổng | Dòng `Approved-by: <tên> <YYYY-MM-DD>` ở đầu artifact mở cổng | behavior | fixture team.py | must |
| REQ-C1-13 | C1 mở cổng | Comment `@claude approve Gn` trên issue mở cổng | behavior | đọc workflow CI | must |
| REQ-C1-14 | C1 cổng tắt | Cổng tắt trong `.team/config.json` không chặn | behavior | fixture team.py | must |
| REQ-C1-15 | C1 mặc định | Bộ cổng mặc định G0/G1/G2/G3/G4/G5 bật, G2b tắt | config | đọc config | must |
| REQ-C1-16 | C1 (G0) | Hành vi: G0 chặn `/team:onboard` khi chưa có `Approved-by:` trong ai-readiness.md | behavior | B2: `/team:onboard --yes` trước khi duyệt | must |
| REQ-C1-17 | C1 (giai đoạn 0) | Hành vi: `/team:intake "<thô>" --size S --decide` ghi intake.md (playbook, cỡ, chế độ, giả định), journal, ngân sách vai | behavior | B5 | must |
| REQ-C2-1 | C2 | `scripts/team.py status/next` tính trạng thái từ artifact, không lưu con trỏ | structure | chạy lệnh | must |
| REQ-C2-2 | C2 | `intake.md` → intaken | behavior | fixture | must |
| REQ-C2-3 | C2 | `spec.md` có DoD → specified | behavior | fixture | must |
| REQ-C2-4 | C2 | `research.md` → researched | behavior | fixture | must |
| REQ-C2-5 | C2 | `arch-impact.md` / architecture được tham chiếu → architected | behavior | fixture | must |
| REQ-C2-6 | C2 | `design.md` → designed | behavior | test | must |
| REQ-C2-7 | C2 | `plan.md` + `tasks.md` → planned | behavior | test | must |
| REQ-C2-8 | C2 | Tick hết task → built | behavior | test | must |
| REQ-C2-9 | C2 | `acceptance.md` verdict accepted → verified | behavior | test | must |
| REQ-C2-10 | C2 | `asbuilt.md` + Released → released | behavior | test | must |
| REQ-C2-11 | C2 | Cổng chưa duyệt chặn MỌI giai đoạn sau kể cả khi artifact sau đã có | behavior | fixture | must |
| REQ-C2-12 | C2 | Bộ kiểm trạng thái chạy xanh | measure | `bash scripts/tests/run-all.sh` | should |
| REQ-C3-1 | C3 S | S: diff một câu, ≤ 3 file, không đổi schema/API; intake → analyze rút gọn bỏ G1 → build 1 dev → verify tự động không qa riêng → release | behavior/content | fixture + đọc skill | must |
| REQ-C3-2 | C3 M | M: một module, đổi dữ liệu/API, 1–5 ngày; intake → analyze → [research] → design → plan → build → verify → release | behavior | fixture | must |
| REQ-C3-3 | C3 L | L: nhiều module, NFR mới, > 5 ngày; đủ 9 giai đoạn; kiến trúc bắt buộc; task đầu walking skeleton | behavior | fixture + đọc plan | must |
| REQ-C3-4 | C3 | team-leader chấm cỡ ở intake | content | đọc intake, template | must |
| REQ-C3-5 | C3 | Ép cỡ bằng `--size` hoặc label `team:size:*` | config | đọc skill + CI | must |
| REQ-C3-6 | C3 | Nâng/hạ cỡ giữa chừng ghi lý do vào `intake.md` | content | grep | must |
| REQ-C4-1 | C4 | `ask` là chế độ mặc định | config | đọc config | must |
| REQ-C4-2 | C4 ask | Chỉ hỏi mục có hệ quả lớn/không đảo ngược (xoá/migrate dữ liệu, API công khai, nghiệp vụ, chi phí) | content | đọc skill/agent | must |
| REQ-C4-3 | C4 ask | ≤ 5 câu/đợt, mỗi câu 2–4 phương án + khuyên dùng + hệ quả | content | đọc skill + mẫu | must |
| REQ-C4-4 | C4 ask | ≤ 2 đợt | content/config | đọc skill + config | must |
| REQ-C4-5 | C4 ask | Không hỏi cái có trong code | content | đọc skill | must |
| REQ-C4-6 | C4 ask | Mục nhỏ → ghi `## Giả định tự quyết` | content | grep tiêu đề | must |
| REQ-C4-7 | C4 decide | decide: không hỏi, trừ điều cấm tuyệt đối (hook/deny chặn) | content | đọc skill | must |
| REQ-C4-8 | C4 decide | Mỗi quyết định ghi: chọn gì / vì sao / phương án khác / nếu sai sửa thế nào | content | đọc skill/agent | must |
| REQ-C4-9 | C4 | Bật decide bằng `--decide`, label `team:decide`, hoặc `config.default_mode` | config | đọc skill + CI | must |
| REQ-C4-10 | C4 CI | Trong CI: câu hỏi → comment issue theo mẫu, label `team:needs-answer`, dừng `WAITING_FOR_ANSWER` | behavior | đọc CI + fixture team.py | must |
| REQ-C4-11 | C4 (ask) | Hành vi: chế độ ask → ≤ 5 câu, mỗi câu có phương án + khuyên dùng + hệ quả, ≤ 2 đợt | behavior | B8: intake + `/team:analyze` yêu cầu mơ hồ | must |
| REQ-C4-12 | C4 (decide) | Hành vi: `--decide` → không hỏi, có mục giả định với chọn/vì sao/phương án/cách sửa | behavior | B8: cùng yêu cầu với `--decide` | must |
| REQ-C5-1 | C5 | tech-lead đọc `tasks.md`, chọn task chưa làm, không bị chặn, phụ thuộc xong | content | đọc skill | must |
| REQ-C5-2 | C5 | dev (worktree): test fail trước → implement → `cmd.test_one` → `cmd.lint` → commit | content | đọc agent | must |
| REQ-C5-3 | C5 | reviewer (context mới): tầng 1 đúng spec → tầng 2 chất lượng; findings có mã STD | content | đọc agent | must |
| REQ-C5-4 | C5 | dev sửa blocker/major (≤ max_rework vòng) | content | đọc skill | must |
| REQ-C5-5 | C5 | tech-lead tick task, ghi `review-NN.md`, merge vào `team/<ID>`, chạy `cmd.test` | content | đọc skill | must |
| REQ-C5-6 | C5 | Tick hết → `/team:verify` | behavior | test | must |
| REQ-C5-7 | C5 | Task 2–5 phút, có đường dẫn file cụ thể | content | đọc skill + mẫu | must |
| REQ-C5-8 | C5 | Hai task chạm cùng file không song song | content | đọc skill/agent | must |
| REQ-C5-9 | C5 | Không ai nói "xong" khi chưa có output chứng minh | behavior | đọc hook + test | must |
| REQ-C5-10 | C5 | Hành vi: feature cỡ S chạy analyze → build (dev worktree, test hỏng trước, reviewer, finding có mã STD) → verify → dừng G4 trên dự án mới onboard, không cần người sửa giữa chừng | behavior | B6 `/team:run FEAT-001 --until-blocked` | must |
| REQ-C6-1 | C6 | Dừng khi task `BLOCKED` sau `max_attempts` | behavior | đọc skill + test | must |
| REQ-C6-2 | C6 | Dừng khi rework vượt `max_rework` | content | đọc skill | must |
| REQ-C6-3 | C6 | Dừng khi `DESIGN_CONFLICT` / `design-defect` | behavior | fixture | must |
| REQ-C6-4 | C6 | Dừng khi cổng bật chưa duyệt | behavior | test | must |
| REQ-C6-5 | C6 | Dừng khi vượt `feature_budget_usd` | behavior | grep đo chi phí | must |
| REQ-C6-6 | C6 | Dừng khi chạm `protected_paths` | behavior | test hook | must |
| REQ-C6-7 | C6 | Dừng khi hai vòng rework cùng lỗi | content | đọc skill | must |
| REQ-C6-8 | C6 | Mỗi lần dừng nêu: lý do, việc gì, cần ai làm gì, lệnh để tiếp tục | content | grep 13 agent | must |
| REQ-C7-1 | C7 | 16 playbook trong `workflows/` | structure | ls | must |
| REQ-C7-2 | C7 | Mỗi playbook có: điều kiện áp dụng, cỡ mặc định, chuỗi skill, vai trò, cổng, điểm dừng, tiêu chí xong | structure | grep tiêu đề 16+4 file | must |
| REQ-C7-3 | C7 | team-leader chọn playbook ở intake (loại việc trước, rồi cỡ) | content | đọc README + intake | must |
| REQ-C7-4 | C7 takeover | Quét 4 tầng → báo cáo 3 câu → G0 → onboard; cỡ L; cổng G0 | content | đọc playbook | must |
| REQ-C7-5 | C7 new-project | onboard --new → intake(L) → analyze → research → architect → design → plan (walking skeleton) → build…; L; đủ cổng | content/behavior | đọc + fixture | must |
| REQ-C7-6 | C7 new-feature | intake → analyze → [research] → design → plan → build → verify → asbuilt → pr → release; M; G1, G3, G4 | content | đọc playbook | must |
| REQ-C7-7 | C7 change-request | analyze --amend → architect (impact) → plan (chèn) → build…; M; G1, G3 | content/behavior | đọc + fixture | must |
| REQ-C7-8 | C7 bug-fix | intake(bug) → test fail trước → build (1 task) → verify → pr; S; G4 nếu M | content/behavior | đọc + fixture | must |
| REQ-C7-9 | C7 hotfix | intake(hotfix) → build tối thiểu từ prod → verify nhanh → pr → release prod (người duyệt) → bug-fix đầy đủ sau; S; G5 | content/behavior | đọc + fixture | must |
| REQ-C7-10 | C7 refactor | intake → design ngắn → maintainer → verify (test trước = sau) → pr; M; G2b bật | content/behavior | đọc + test | must |
| REQ-C7-11 | C7 dependency-upgrade | research (changelog, breaking) → plan → build → verify toàn bộ → pr; M; G3 | content/behavior | đọc + fixture | must |
| REQ-C7-12 | C7 data-migration | analyze → design (mapping, rollback) → plan → build (dry-run bản sao) → verify (đối chiếu số) → release có cửa sổ; M/L; G1, G3, G4 | content/behavior | đọc + fixture | must |
| REQ-C7-13 | C7 integration | research (API, auth, giới hạn) → architect (impact) → design (contract, retry, idempotent) → plan → build → verify (sandbox) → release; M/L; G2, G3, G4 | behavior | fixture team.py | must |
| REQ-C7-14 | C7 ci-fix | devops chẩn đoán → ci fix → pr riêng; S; không cổng | content | đọc + fixture | must |
| REQ-C7-15 | C7 docs-only | writer → pr, auto-merge khi CI xanh; S; không cổng | content | đọc | must |
| REQ-C7-16 | C7 client-docs | analyze (đối tượng, phạm vi) → writer → review nội dung → pr; S/M; G1 rút gọn | content/behavior | đọc + fixture | must |
| REQ-C7-17 | C7 release | release notes → tag → deploy staging → UAT → prod; —; G4, G5 | content | đọc | must |
| REQ-C7-18 | C7 spike | research → cache → (đề xuất ADR); —; — | content/behavior | đọc + fixture | must |
| REQ-C7-19 | C7 retro | retro → coach → đề xuất overlay có eval → canary cỡ S → anh duyệt | content | đọc | must |
| REQ-C7-20 | C7 batch | Workflow kịch bản hoá `build-all-tasks` | content | đọc | should |
| REQ-C7-21 | C7 batch | Workflow kịch bản hoá `verify-all` | content | đọc | should |
| REQ-C7-22 | C7 batch | Workflow kịch bản hoá `weekly-retro` | content | đọc | should |
| REQ-C7-23 | C7 batch | Workflow kịch bản hoá `clean-sweep` | content | đọc | should |
| REQ-C8-1 | C8 | Trả lời làm gì / đến đâu / cần làm gì; chỉ quét, đánh giá, báo cáo, không sửa gì | content | đọc skill | must |
| REQ-C8-2 | C8 | Tầng sau chỉ chạy khi tầng trước chưa trả lời được; mỗi tầng có ngân sách | content | đọc skill + tiers.md | must |
| REQ-C8-3 | C8 T0 | Metadata bằng script, không đọc nội dung: cây thư mục, manifest, git log --stat (vùng nóng, nhịp, tác giả), issue/PR, CHANGELOG, tag; ≈ 0 token | behavior | chạy detect-stack.sh --deep | must |
| REQ-C8-4 | C8 T1 | README, docs, ADR, CLAUDE.md, spec/plan; mục lục trước, thân khi liên quan; ghi ngày cập nhật | content | đọc skill | must |
| REQ-C8-5 | C8 T2 | Đối chiếu tuyên bố ↔ thực tế: tính năng → code/test, TODO/FIXME, test skip, nhánh chưa merge, migration chưa chạy; mẫu (module chính + vùng nóng) | content | đọc skill | must |
| REQ-C8-6 | C8 T3 | Đọc sâu chỉ khi T2 lộ mâu thuẫn, module không tài liệu, hoặc `--full` | content | đọc skill | must |
| REQ-C8-7 | C8 báo cáo | Xương sống 3 câu hỏi | content | đọc mẫu | must |
| REQ-C8-8 | C8 phụ lục | Stack & sức khoẻ: build/test chạy được, lint, coverage, phụ thuộc lỗi thời/CVE, bí mật lộ, test flaky | content | đọc mẫu | must |
| REQ-C8-9 | C8 phụ lục | Quy ước thực tế đo từ code | content | đọc mẫu | must |
| REQ-C8-10 | C8 phụ lục | ai-readiness: CLAUDE.md (dài, nội dung, lỗi thời, mâu thuẫn); `.claude/`, plugin, MCP, AGENTS.md giữ/cắt/viết lại; kết luận ngay / chỉnh profile / dọn trước | content/behavior | đọc mẫu + detect-stack | must |
| REQ-C8-11 | C8 phụ lục | Profile đề xuất có bằng chứng từng khe | content | đọc mẫu | must |
| REQ-C8-12 | C8 phụ lục | Nợ kỹ thuật chặn / nên / sau | content | đọc mẫu | must |
| REQ-C8-13 | C8 phụ lục | Câu hỏi mở ≤ 10 | content | đọc mẫu | must |
| REQ-C8-14 | C8 | Ghi rõ đã quét gì / chưa / độ tin cậy | content | grep mẫu | must |
| REQ-C8-15 | C8 | Cache T0–T1 cho giai đoạn sau | behavior | chạy explore-cache.sh | must |
| REQ-C8-16 | C8 G0 | Anh duyệt `ai-readiness.md` → mới chạy `onboard` | content | đọc onboard | must |
| REQ-C8-17 | C8 | T0 bằng script (`scripts/detect-stack.sh`), chỉ bash/python stdlib/git | structure | đọc + chạy script | should |
| REQ-C8-18 | C8 | Hành vi: takeover trên repo mẫu: T0 bằng script, T1 mục lục, T2 thấy README↔code và test skip, T3 không chạy, 5 báo cáo, chỉ `docs/team/` đổi | behavior | B1 `/team:takeover` | must |
| REQ-D1-1 | D1 | Ba mức thực thi 3 máy / 2 agent / 1 văn bản với cơ chế đúng | content | đọc STD.md | must |
| REQ-D1-2 | D1 | Mỗi quy tắc có mức và "thực thi bởi" | structure | đọc 12 bảng | must |
| REQ-D1-3 | D1 | Quy tắc ghi mức 3 thật sự do máy chặn | behavior | grep scripts + thử check-git | must |
| REQ-D1-4 | D1 | Quy tắc mức 1 vi phạm ≥ 2 lần → coach đề xuất nâng mức | process | STD.md, coach.md, retro skill, measure.py | must |
| REQ-D2-1 | D2 | Mã `STD-<MẢNG>-n`, 12 mảng | structure | đọc STD.md + gen script | must |
| REQ-D2-2 | D2 | STRUCT: file mới trong allowed_new_file_roots; test theo quy ước; không commit file sinh bởi tool; artifact đúng tên | content | đối chiếu bảng | must |
| REQ-D2-3 | D2 | NAME: theo profile + codebase; tên nói ý định; nhánh team/<ID>-<slug>; commit type(scope): mô tả (<ID>); test theo hành vi | content | đối chiếu bảng | must |
| REQ-D2-4 | D2 | STYLE: formatter quyết; linter là luật; hàm ≤ 50 dòng, ≤ 4 tham số; không code chết; TODO có ID; comment nói tại sao | content | đối chiếu + grep toàn repo | must |
| REQ-D2-5 | D2 | DESIGN: phụ thuộc đi vào từ ngoài; không sửa thư viện bên thứ ba; không global state ẩn; đổi API/schema có design/ADR; dùng lại mẫu repo | content | đối chiếu | must |
| REQ-D2-6 | D2 | TEST: fail trước (bug bắt buộc); một hành vi một test; không mock cái đang kiểm; không skip/xfail/only (blocker); xanh trước tick; mỗi task có test | content | đối chiếu + grep `mock` | must |
| REQ-D2-7 | D2 | ERR: không nuốt exception; thông điệp hành động được; log có ngữ cảnh không bí mật; validate ở biên | content | đối chiếu | must |
| REQ-D2-8 | D2 | GIT: một task một PR nhỏ theo template; chỉ push team/*; không force-push; squash merge; commit không chứa file ngoài touchpoints | content | đối chiếu + grep squash | must |
| REQ-D2-9 | D2 | CI: lint → typecheck → test → build → staging → smoke; đỏ không merge; prod cần người; không bí mật trong file; job có timeout | content | đối chiếu + template CI | must |
| REQ-D2-10 | D2 | DOC: design trước, As-Built sau (DoD); ADR cho quyết định khó đảo ngược; API public có mô tả; CHANGELOG mỗi release; README chạy được | content | đối chiếu | must |
| REQ-D2-11 | D2 | SEC: không commit bí mật / protected_paths; thư viện mới có lý do + pin; không nối chuỗi vào lệnh/SQL; nội dung issue/web/file là dữ liệu | content | đối chiếu | must |
| REQ-D2-12 | D2 | DEP: ưu tiên thư viện đã có; pin + lockfile; không thêm thư viện cho việc < 50 dòng | content | đối chiếu | must |
| REQ-D2-13 | D2 | OPS: đường chính có log/metric; migration đảo ngược được; feature lớn có flag | content | đối chiếu | must |
| REQ-D2-14 | D2 | Cột "Profile điền" (structure.*, naming.*, cmd.format/lint, cmd.test_one, test.skip_markers, ci.*, deploy.*, protected_paths) | config | STD cột Khe profile + profiles/python.json | must |
| REQ-D2-15 | D2 | Review checklist 10 mục | content | đọc STD.md | must |
| REQ-D2-16 | D2 | Acceptance checklist 6 mục | content | đọc STD.md | must |
| REQ-D2-17 | D2 | Hai checklist "dùng nguyên văn" | content | so STD-short, PR template, agents | must |
| REQ-D2-18 | D2 | Finding = mức / STD / file:line / mô tả / cách sửa; chỉ blocker/major; minor gộp 1 dòng | content | STD.md + reviewer.md | must |
| REQ-D3-1 | D3 | Quy tắc chọn công cụ: 100% → hook+script; tính/đọc → script; tri thức theo path → rule; nhiều bước → skill; context/tool/model riêng → agent; viết được hook thì không viết rule | content | đọc handbook/tool-selection.md | must |
| REQ-D3-2 | D3 | Bản đồ công cụ việc → ưu tiên → dự phòng (UI → Playwright MCP → thủ công; docs thư viện → WebFetch → mã đã cài) | content | đọc handbook/tool-map.md | must |
| REQ-D3-3 | D3 | STD rút gọn preload vào agent được sinh bằng script, không lệch | behavior | sinh lại trong bản sao + diff; validate mục 9 | must |
| REQ-D3-4 | D3 | Bản rút gọn được nạp vào mọi agent | config | grep skills trong frontmatter | must |
| REQ-D4-1 | D4 | Skills, rules, agents là nguồn sự thật cho AI | process | docs/02-team.md + agents | must |
| REQ-D4-2 | D4 | docs/ chỉ gồm tổng quan, cách cài, bản đồ việc → skill, lý do thiết kế; không viết tri thức hai lần | content | ls docs/ + đọc mẫu | must |
| REQ-E1-1 | E1 profile.json | Đủ các khe: stack, language, cmd.{install,build,test,test_one,lint,typecheck,format,run,migrate}, formatters_by_ext, structure, naming, test.skip_markers, protected_paths, ci, deploy, ui, tracker, plugins, notes | config | Đọc schema + jq từng profile | must |
| REQ-E1-2 | E1 | `test_one` bắt buộc | config | check-profile.py với profile biến thể | must |
| REQ-E1-3 | E1 | `{file}` là placeholder DUY NHẤT | config | check-profile.py với `pytest {path} {file}` | must |
| REQ-E1-4 | E1 | protected_paths luôn có bí mật, lockfile, vendored, cấu hình prod | config | jq protected_paths 6 profile + probe protect.sh | must |
| REQ-E1-5 | E1 | allowed_new_file_roots là danh sách đóng (doc gồm src, tests, docs, scripts, .github, .claude, .team) | behavior | Feed JSON vào protect.sh | must |
| REQ-E1-6 | E1 | 6 profile mẫu python, node-ts, go, java-maven, flutter, _template hợp schema | config | `check-profile.py … profiles/<x>.json` cho cả 6 | must |
| REQ-E1-7 | E1 | Monorepo: profile gốc + `packages` ghi đè theo thư mục | behavior | grep `packages` trong scripts/skills | must |
| REQ-E1-8 | E1 | Lệnh chạy được từ gốc repo | content | Đọc schema/notes/profiles | should |
| REQ-E1-9 | E1 | Hành vi: profile do takeover đề xuất và onboard ghi phải dùng được với script của kit (`naming.test_file` theo mẫu `{name}`) | behavior | B3/B6: đọc `.team/profile.json`, check-structure.sh | must |
| REQ-E1-10 | E1 | Hành vi: protected_paths của profile onboard có bí mật (`.env*`, thư mục secrets), lockfile, vendored, cấu hình prod | behavior | B3: `jq .protected_paths .team/profile.json` | must |
| REQ-E2-1 | E2 config.json | gates G0,G1,G2,G2b=false,G3,G4,G5 | config | Đọc template + schema | must |
| REQ-E2-2 | E2 | default_size auto, default_mode ask, base_branch main | config | Đọc template | must |
| REQ-E2-3 | E2 | protected_branches = main, master, develop, release | config | Diff với tài liệu | must |
| REQ-E2-4 | E2 | limits max_rework 3, max_attempts 3, max_questions_round 2, max_parallel_dev 2, max_agents S3 M6 L10, budget null, context_warn_pct 60 | config | Diff | must |
| REQ-E2-5 | E2 | models theo 13 vai đúng bảng | config | Diff + so frontmatter agents | must |
| REQ-E2-6 | E2 | approvers mỗi cổng `["@owner"]` | config | Diff | must |
| REQ-E2-7 | E2 | journal.max_lines_per_entry 5; memory {40, 50, true}; channels {issue-comment, ""} | config | Diff | must |
| REQ-E2-8 | E2 | "Tự động hoàn toàn" = mọi cổng false trừ G5_prod, default_mode decide | content | grep định nghĩa | must |
| REQ-E3-1 | E3 current.json | {feature, stage, agent, started_at} do skill ghi khi bắt đầu giai đoạn, gitignore | behavior | grep skills + gitignore.tmpl | must |
| REQ-E3-2 | E3 | Hook đọc current.json để ghi metrics | behavior | Chạy scorecard.sh với transcript giả | must |
| REQ-E3-3 | E3 | `.team/plugin_root` (SessionStart ghi), `.team/active-build` (marker Stop), `.team/session/<id>.md` (handoff) | behavior | Chạy session-start.sh, handoff.sh, đọc stop-check.sh | must |
| REQ-E4-1 | E4 Project | `.claude/settings.json`: enabledPlugins, allow theo cmd.* + git an toàn | config | render.py settings.json.tmpl với profile python | must |
| REQ-E4-2 | E4 Project | deny: push nhánh bảo vệ, force-push, rm -rf, Edit protected_paths, Read .env* | config | Đọc deny đã render | must |
| REQ-E4-3 | E4 Project/Local | skillOverrides ẩn skill trùng; hook cần tham số; Local: ghi đè cá nhân | config | Đọc 2 template | must |
| REQ-E4-4 | E4 User | `~/.claude/settings.json`: autoMemoryEnabled, plugin cá nhân | content | grep autoMemoryEnabled toàn repo | should |
| REQ-E4-5 | E4 | Permission mode: plan ở phân tích/kiến trúc, acceptEdits ở build, dontAsk + allowlist ở CI/headless | process | grep acceptEdits/plan/dontAsk | must |
| REQ-E5-1 | E5 | Không viết MCP/plugin mới | structure | find .mcp.json; marketplace.json | must |
| REQ-E5-2 | E5 | Profile khai plugins.required/recommended; onboard chỉ in lệnh cài | content | Đọc onboard | must |
| REQ-E5-3 | E5 | SessionStart báo thiếu plugin (không chặn) | behavior | session-start.sh với required=foo-plugin@mkt | must |
| REQ-E5-4 | E5 | Khuyến nghị mặc định: LSP theo ngôn ngữ, security-guidance, github/gitlab | config | jq plugins.recommended | should |
| REQ-E5-5 | E5 | Theo nhu cầu: Playwright MCP (qa, ui), docs MCP (researcher), Sentry/Slack (devops, team-leader), tracker (intake) | content | grep agents/skills | should |
| REQ-E5-6 | E5 | Không cài plugin trùng (superpowers, commit-commands, pr-review-toolkit), ẩn bằng skillOverrides; superpowers/agent-skills là nguồn học; plugin-dev chỉ trên repo kit | content | grep | should |
| REQ-E5-7 | E5 | Rule theo path nói khi nào dùng tool nào; skill nêu tool từng bước; agent chỉ tool của vai | content | Đọc rules/*.tmpl, tools frontmatter | must |
| REQ-F1-1 | F1 takeover | Quét 4 tầng, 3 câu hỏi + phụ lục, không sửa; team-leader | content | Đọc toàn bộ SKILL.md | must |
| REQ-F1-2 | F1 onboard | Profile, khối CLAUDE.md, rules, settings, hook, CI, docs/team, gitignore; team-leader | content | Đọc | must |
| REQ-F1-3 | F1 intake | Nhận yêu cầu, cấp ID, playbook, cỡ, chế độ, intake.md, journal; team-leader | content | Đọc | must |
| REQ-F1-4 | F1 run | Tính trạng thái, kiểm cổng, gọi skill kế, --until-blocked; team-leader | content | Đọc | must |
| REQ-F1-5 | F1 status | Trạng thái từ artifact bằng script, việc cần người | content | Đọc + chạy team.py status | must |
| REQ-F1-6 | F1 session | Kế hoạch phiên: tương tác/headless, model, ngân sách, compact tại ranh giới, kiểm context; team-leader | content | Đọc | must |
| REQ-F1-7 | F1 using-team | Mệnh lệnh: MỌI agent kiểm playbook/skill trước khi làm | content | Đọc + grep `skills:` agents | must |
| REQ-F1-8 | F1 feedback | Chấm artifact, gắn agent/skill → feedback.jsonl; mọi vai trò và người | behavior | Đọc + role-policy.sh với từng vai | must |
| REQ-F1-9 | F1 retro | Số đo + journal → nút thắt → chẩn đoán → đề xuất có diff/eval → canary; coach | content | Đọc | must |
| REQ-F1-10 | F1 analyze | Spec + DoD; hỏi/tự quyết; amendment; analyst | content | Đọc | must |
| REQ-F1-11 | F1 research | Nguồn chính thức URL+ngày; phương án; POC; nháp ADR; cache theo version; researcher | content | Đọc | must |
| REQ-F1-12 | F1 architect | architecture.md / arch-impact.md, ADR; architect | content | Đọc | must |
| REQ-F1-13 | F1 design | design.md 8 mục; touchpoints; test plan; designer | content | Đọc | must |
| REQ-F1-14 | F1 plan | plan.md + tasks.md slice dọc, task 2–5 phút; tech-lead | content | Đọc | must |
| REQ-F1-15 | F1 build | dev → reviewer 2 tầng → tick; worktree; trần rework; tech-lead | content | Đọc + agents/dev.md | must |
| REQ-F1-16 | F1 verify | Nghiệm thu bằng lệnh + output; verdict; cỡ S tự động; qa | content | Đọc | must |
| REQ-F1-17 | F1 asbuilt | As-Built, release notes, CHANGELOG; writer | content | Đọc | must |
| REQ-F1-18 | F1 release | Điều kiện → PR → CI → merge → staging → smoke → prod (G5); tech-lead, devops | content | Đọc | must |
| REQ-F1-19 | F1 clean | Dọn không đổi hành vi theo loại; một loại một PR; maintainer | content | Đọc | must |
| REQ-F1-20 | F1 commit | Tách commit theo ý; message chuẩn; gỡ debug; loại file ngoài touchpoints; dev, maintainer | content | Đọc | must |
| REQ-F1-21 | F1 pr | Tạo/cập nhật PR theo mẫu; trả lời review có STD/design; rebase; không merge trái phép; tech-lead | content | Đọc | must |
| REQ-F1-22 | F1 ci | setup/fix/add-stage/deploy-script; phân loại trước khi sửa; devops | content | Đọc | must |
| REQ-F1-23 | F1 make-skill | Skill tạm vào .claude/skills/ chỉ khi team-leader thấy cần; kiểm trùng; ca kiểm; registry | content | Đọc | must |
| REQ-F1-24 | F1 make-agent | Agent chuyên môn tạm khi đủ lớn; team-leader | content | Đọc | must |
| REQ-F1-25 | F1 audit-kit | Skill không dùng, agent vượt turn, prompt mâu thuẫn, tài liệu lệch, bảo mật chính kit; coach | content | Đọc SKILL + references/checks.md | must |
| REQ-F1-26 | F1 handbook | STD rút gọn + quy trình + giao thức; preload mọi agent; user-invocable false | config | Đọc + grep `skills:` 13 agent | must |
| REQ-F1-27 | F1 chuẩn viết | description "Dùng khi…" < 500 ký tự | config | Đếm ký tự 26 description | must |
| REQ-F1-28 | F1 chuẩn viết | description không tóm tắt quy trình | content | grep "rồi/sau đó" trong description | must |
| REQ-F1-29 | F1 chuẩn viết | Process không viết văn xuôi | content | Đọc 26 mục Quy trình | must |
| REQ-F1-30 | F1 chuẩn viết | Mỗi bước có checkpoint và điều kiện thoát | content | grep "điểm quyết định/checkpoint/thoát nếu" + đọc | must |
| REQ-F1-31 | F1 chuẩn viết | Bảng anti-rationalization + red flags | content | `python3 scripts/kit-metrics.py` | must |
| REQ-F1-32 | F1 chuẩn viết | Kết thúc bằng yêu cầu bằng chứng | content | Đọc mục cuối | must |
| REQ-F1-33 | F1 chuẩn viết | Ngân sách chữ: skill hay nạp < 200 từ, khác < 500 | measure | kit-metrics.py + skill-budgets.txt | must |
| REQ-F1-34 | F1 chuẩn viết | Không `@file` | config | grep `@….md/json/sh/py` trong skills, agents | must |
| REQ-F1-35 | F1 chuẩn viết | Mỗi skill có eval baseline → with-skill trước khi phát hành | measure | ls evals/*/out | must |
| REQ-F2-1 | F2 vòng đời | Bước 1–3: team-leader thấy nhu cầu ở intake/plan → kiểm sẵn có (kit, .claude/skills, plugin) → giao make-skill (researcher lấy mẫu nếu cần) | process | Đọc intake, make-skill | must |
| REQ-F2-2 | F2 | Bước 4: sinh `.claude/skills/<tên>/` với mục đích, khi dùng, vào/ra, bước, tool, mẫu, tiêu chí xong, 1–2 ca; nhãn temp; registry | content | Đọc references/skill-template.md, registry template | must |
| REQ-F2-3 | F2 | Bước 5–6: giao "dùng /<tên> cho bước X", journal; temp → project (người duyệt) → kit (≥ 2 dự án) hoặc retired (30 ngày) | process | Đọc make-skill bước 11–12, retro bước 12, registry | must |
| REQ-F2-4 | F2 | Trần số skill tạm; make-agent cùng vòng đời | config | Đọc config + make-agent | must |
| REQ-F2-5 | F2 bước 1–5 | Hành vi: yêu cầu cần chuyên môn lặp ("6 màn hình CRUD giống nhau") → team-leader điều phối `/team:make-skill`, ghi registry, journal | behavior | B9 | must |
| REQ-F2-6 | F2 | Hành vi: yêu cầu cỡ S thường không tạo skill tạm | behavior | B5 | must |
| REQ-F3-1 | F3 PreToolUse Edit/Write | protect.sh chặn protected_paths, .git/, file mới ngoài allowed roots | behavior | Chạy test_hooks.sh + tự feed JSON | must |
| REQ-F3-2 | F3 PreToolUse Bash git | check-git.sh chặn push nhánh bảo vệ, force-push, rewrite; nhắc commit message | behavior | test_hooks.sh | must |
| REQ-F3-3 | F3 PostToolUse Edit/Write | format.sh chạy formatter theo đuôi file từ profile | behavior | Feed JSON với formatters_by_ext `.py` | must |
| REQ-F3-4 | F3 Stop (build) | lint + typecheck + test_one cho test đã đổi + check-structure; tôn trọng stop_hook_active | behavior | test_hooks.sh + đọc stop-check.sh | must |
| REQ-F3-5 | F3 Stop (research) | Phải có `## Nguồn` có URL | behavior | Đọc stop-check.sh + test | must |
| REQ-F3-6 | F3 SessionStart startup/resume/compact/clear | Ghi plugin_root; in trạng thái ngắn; nạp lại handoff; sau compact nhắc 6 luật | behavior | Feed source=compact và resume | must |
| REQ-F3-7 | F3 SessionEnd | log-session.sh + handoff | behavior | hooks.json + feed SessionEnd | must |
| REQ-F3-8 | F3 PreCompact | handoff.sh ghi bàn giao ≤ 40 dòng, chỉ khác biệt | behavior | Feed PreCompact | must |
| REQ-F3-9 | F3 PostCompact | Đếm compact/feature | behavior | Feed 2 lần PostCompact | must |
| REQ-F3-10 | F3 SubagentStop | scorecard.sh ghi agent, turn, thời gian vào metrics | behavior | Feed với transcript giả | must |
| REQ-F3-11 | F3 chung | hooks.json dùng ${CLAUDE_PLUGIN_ROOT}; bộ test hook xanh | behavior | `bash scripts/tests/test_hooks.sh` | must |
| REQ-F3-12 | F3 | Hành vi sống: Write `random/new.py` → STD-STRUCT-1; `git push origin main` → chặn; `.env` → chặn; push `team/*` được check-git cho qua | behavior | B4 phiên haiku + hook trực tiếp | must |
| REQ-F4-1 | F4 team.py | status / next / metrics / scorecard | behavior | Chạy trên dự án tạm | must |
| REQ-F4-2 | F4 detect-stack, check-structure, explore-cache | Siêu dữ liệu T0; kiểm cấu trúc; hash thư mục ↔ docs/team/explore/*.md | behavior | Chạy từng script | must |
| REQ-F4-3 | F4 log-run, handoff | Ghi dòng metrics; bàn giao | behavior | Chạy | must |
| REQ-F4-4 | F4 measure.py, gen-handbook-short.py | Điểm hiệu quả, xu hướng, bất thường, xếp hạng; sinh STD rút gọn | behavior | --help, unittest, chạy fixtures, --stdout diff | must |
| REQ-F4-5 | F4 validate.sh, install-local.sh; chỉ bash + python3 stdlib + jq | Frontmatter, tên, xref, ngân sách chữ; chép vào .claude/ | behavior | Chạy validate (thường, --strict), install-local --dry-run, grep import | must |
| REQ-F5-1 | F5 tầng 0 | Nạp lười, Explore, một phiên một feature, cảnh báo > context_warn_pct | behavior | Đọc session, rules, session-start | must |
| REQ-F5-2 | F5 tầng 1–2 | Handoff ≤ 40 dòng ghi PreCompact/SessionEnd, nạp SessionStart, đếm compact; artifact ở docs/team/features/<ID>/ | behavior | Xem REQ-F3-6..9 | must |
| REQ-F5-3 | F5 tầng 3–4 | Auto memory vs docs/team phân định bằng rule; reviewer/qa/coach `memory: project` nhỏ, có ngày | config | Đọc team-core.md.tmpl, frontmatter | must |
| REQ-F5-4 | F5 tiêu chí đáng lưu | Dùng lại ≥ 2 hoặc đắt; kết luận không quá trình; ngày/version; trần kích thước và số file | content | Đọc rule + grep enforcement | must |
| REQ-F5-5 | F5 | Coach dọn định kỳ; prompt cache: prefix ổn định, không đổi model giữa phiên, fan-out cùng model/tool | content | grep coach/retro; đọc session | should |
| REQ-F5-6 | F5 tầng 1 | Hành vi: PreCompact/SessionEnd ghi `.team/session/<id>.md` ≤ handoff_max_lines, chỉ thông tin ngoài artifact; SessionStart sau compact in 6 luật | behavior | B11: xem .team/session/, chạy session-start.sh source=compact, handoff.sh | must |
| REQ-F6-1 | F6 journal | docs/team/journal/<feature>.md, 3–5 dòng: giao ai, việc gì, kết quả, thời gian/vòng, nhận xét, ý cải thiện; trần dòng | content | Đọc journal-entry.md | must |
| REQ-F6-2 | F6 scorecard | gọi, turn, thời gian, rework/bác, STD vi phạm, token (log local), lần người can thiệp; so trung vị cùng cỡ | measure | Chạy team.py scorecard, measure --logs; grep nơi ghi | must |
| REQ-F6-3 | F6 measure.py | Điểm hiệu quả, xu hướng, bất thường, xếp hạng; không dùng LLM | measure | --help + 9 unittest + chạy fixtures | must |
| REQ-F6-4 | F6 | Feedback tại chỗ; cảnh báo khi vượt ngưỡng 2 lần | behavior | grep cơ chế cảnh báo | must |
| REQ-F6-5 | F6 | Chẩn đoán 5 nguyên nhân có bằng chứng | content | Đọc retro + proposal.md | must |
| REQ-F6-6 | F6 | Overlay header `# Overlay từ retro <date>: <lý do>` + version | content | Đọc proposal.md | should |
| REQ-F6-7 | F6 | Eval trước/sau → canary N việc cỡ S → giữ/rollback/thay/gỡ; áp dụng qua người | process | Đọc proposal.md, retro | must |
| REQ-F6-8 | F6 | Số đo gọi thừa: agent/feature theo cỡ so max_agents_per_feature; retro định kỳ, kit-issues, audit-kit | measure | grep scripts + retro | must |
| REQ-F6-9 | F6 | Hành vi: `/team:retro` ra `retro/<date>.md` với ≥ 1 đề xuất có diff + eval + canary; không sửa agent/skill; dẫn measure.py | behavior | B10 | must |
| REQ-F6-10 | F6 scorecard | Hành vi: lần chạy ghi `runs.jsonl` và `scorecard.json` | behavior | B6c: docs/team/metrics/ | must |
| REQ-G1-1 | G1 | `.claude-plugin/plugin.json` (name team, version, description) + `marketplace.json` tự host, source ./ | structure | đọc 2 file | must |
| REQ-G1-2 | G1 | README (cài 3 cách; dùng hằng ngày; cấu trúc), CLAUDE.md (3 nơi cùng lúc; không ghi cứng stack; tên khớp), CHANGELOG.md, LICENSE MIT | content | đọc file | must |
| REQ-G1-3 | G1 | agents/ 13 file đúng tên; skills/ 26 thư mục SKILL.md (+ references/ nếu dài) | structure | ls, đếm | must |
| REQ-G1-4 | G1 | workflows/ 16 playbook + `lot/` (3–4 workflow kịch bản hoá) | structure | ls workflows | must |
| REQ-G1-5 | G1 | hooks/hooks.json; scripts/ có lib.sh, protect.sh, check-git.sh, format.sh, stop-check.sh, session-start.sh, log-session.sh, handoff.sh, log-run.sh, detect-stack.sh, check-structure.sh, explore-cache.sh, team.py, measure.py, gen-handbook-short.py, validate.sh, install-local.sh | structure | kiểm từng file | must |
| REQ-G1-6 | G1 | handbook/: STD.md (12 mảng, checklist review/nghiệm thu), tool-selection.md, tool-map.md, who-calls-whom.md | content | grep tiêu đề STD.md, wc | must |
| REQ-G1-7 | G1 | profiles/ _template, python, node-ts, go, java-maven, flutter | structure | ls profiles | must |
| REQ-G1-8 | G1 | templates/artifacts (18 mẫu đã kê), templates/project (CLAUDE.md.tmpl, claude/settings.json.tmpl, rules/*.tmpl, team/config.json, github/workflows/team-ci.yml, team-feature.yml, PR template, ISSUE_TEMPLATE/team-feature.yml, CODEOWNERS, gitignore.tmpl), templates/schemas (stage-result.json, profile.schema.json) | structure | ls/find templates | must |
| REQ-G1-9 | G1 | evals/: mỗi skill kỷ luật có baseline/, with-skill/, scenarios.md | structure | ls evals/* | must |
| REQ-G1-10 | G1 | docs/00-tong-quan.md … 08-kenh-kich-hoat.md và docs/huong-dan/ (bat-dau-5-phut, muon-gi-go-gi, cay-quyet-dinh, phien-mau, ai-dang-cho-gi, su-co, ngay-dau-tren-du-an-cu) | structure | ls docs, docs/guides | must |
| REQ-G1-11 | G1 | .github/workflows/validate.yml: validate.sh + kiểm json/bash/python | config | đọc file | must |
| REQ-G2-1 | G2 | CLAUDE.md dự án: khối `<!-- team:start --> … <!-- team:end -->` ≤ 25 dòng chèn vào, không ghi đè cũ | behavior | render.py --insert-block vào CLAUDE.md có sẵn "# Old project / keep me" | must |
| REQ-G2-2 | G2 | .team/profile.json, config.json commit; current.json, plugin_root, session/ gitignore | config | đọc gitignore.tmpl, onboard bước 3–4, 10 | must |
| REQ-G2-3 | G2 | .claude/settings.json: permissions + enabledPlugins + skillOverrides (commit); settings.local.json cá nhân (gitignore) | behavior | render.py --json --merge-into trên profile python | must |
| REQ-G2-4 | G2 | .claude/rules/team-core.md, source.md, tests.md, tool-map.md | structure | ls templates/project/claude/rules | must |
| REQ-G2-5 | G2 | .claude/skills/ và .claude/agents/ là overlay của dự án (commit) | content | đọc make-skill, protect.sh | must |
| REQ-G2-6 | G2 | docs/team/: assessment, ai-readiness, profile-proposal (takeover); architecture.md, adr/, glossary, debt, defects, open-questions | content | grep nơi ghi từng file | must |
| REQ-G2-7 | G2 | features/<ID>/ (intake…asbuilt, review-NN), research/ cache theo chủ đề@version, explore/ có hash, journal/<ID>.md, metrics/ (runs, sessions, feedback .jsonl, scorecard.json), retro/, proposals/, skills-registry, kit-issues, ci.md, onboarding.md; .github/ (team-ci, team-feature, PR/issue template, CODEOWNERS) | structure | onboard bước 9; grep người ghi; chạy explore-cache.sh --hash | must |
| REQ-G2-8 | G2 | Hành vi: onboard tạo profile + config hợp schema, khối CLAUDE.md ≤ 25 dòng giữ nội dung cũ, settings allow/deny, rules, khung docs/team, gitignore; in lệnh cài plugin, không cài | behavior | B3 `/team:onboard --yes --accept-clean-first` | must |
| REQ-H1-1 | H1 | CLI/Desktop/IDE: câu hỏi bằng AskUserQuestion tại chỗ | config | grep tools trong agents | must |
| REQ-H1-2 | H1 | GitHub Actions: label team:intake, team:run; comment `@claude approve Gn`; hỏi bằng comment + label team:needs-answer, dừng | config | đọc team-feature.yml | must |
| REQ-H1-3 | H1 | Scheduled task: retro, clean-sweep định kỳ; webhook sau deploy → smoke; chỉ decide | content | đọc workflows/batch, docs/08 | must |
| REQ-H1-4 | H1 | Headless `claude -p` với `--bare --max-turns --max-budget-usd --output-format json`; bắt buộc decide | content | đọc docs/08-channels.md | must |
| REQ-H1-5 | H1 | Projects (cloud): nhiều feature song song, duyệt ở "Waiting on you", hỏi trong thread | content | grep "Waiting on you" | must |
| REQ-H3-1 | H3 | Cú pháp Claude Code đổi: bắt tra docs + xác nhận phiên bản; phụ lục cú pháp dự phòng | process | grep kiểm phiên bản trong scripts | must |
| REQ-H3-2 | H3 | Phình to: trần chữ; kiểm trùng; audit-kit; skill tạm chỉ khi cần | measure | chạy kit-metrics.py; đọc validate mục 6c, make-skill | must |
| REQ-H3-3 | H3 | Khó kiểm hành vi: repo mẫu ở P6; evals skill kỷ luật; canary cỡ S | process | ls evals, đọc RESULTS.md | must |
| REQ-H3-4 | H3 | Rule bị bỏ qua khi context dài: điều không được sai → hook/permission | behavior | xem REQ-A3-3; tests | must |
| REQ-H3-5 | H3 | SessionStart nhắc lại luật sau compact; anti-rationalization | behavior | chạy session-start.sh với source=compact | must |
| REQ-H3-6 | H3 | Token thừa: nguyên tắc 5; lý do gọi ghi journal; `max_agents_per_feature` | config | jq config; grep nơi dùng | must |
| REQ-H3-7 | H3 | Memory tràn: tiêu chí đáng lưu; trần; coach dọn | config | đọc docs/05, handoff.sh, grep explore_cache_max_files | must |
| REQ-H3-8 | H3 | Định danh tiếng Việt làm script lỗi: quy định ngôn ngữ; validate kiểm | behavior | bản sao: thêm workflows/batch/dọn-dẹp.md và key "lệnh_thử" vào config.json, chạy validate.sh | must |
| REQ-I-1 | I | Skill là mệnh lệnh: `using-team` ép kiểm skill trước mọi việc | content | đọc skills/using-team/SKILL.md, frontmatter team-leader | should |
| REQ-I-2 | I | Process không prose; bảng anti-rationalization + red flags; kết thúc bằng yêu cầu bằng chứng | measure | kit-metrics cột Tự bào chữa/Dấu hiệu sai/Kiểm chứng | should |
| REQ-I-3 | I | Viết skill như TDD: baseline không skill → ghi lý do viện nguyên văn → skill tối thiểu → chạy lại; `evals/` | process | đọc evals/*/scenarios.md, RESULTS.md, make-skill | should |
| REQ-I-4 | I | Description "Dùng khi…" < 500 ký tự, không tóm tắt quy trình; không `@file` | content | vòng kiểm description 26 skill; grep @ | must |
| REQ-I-5 | I | Ngân sách chữ 200/500 | measure | đọc scripts/skill-budgets.txt; kit-metrics | must |
| REQ-I-6 | I | Review 2 tầng; task 2–5 phút; verify-before-done | content | đọc reviewer.md, plan SKILL.md, stop-check | should |
| REQ-I-7 | I | Token đo được ở mọi phiên local từ log Claude Code (cách ccusage) | behavior | đọc measure.py | should |
| REQ-I-8 | I | Giữ bộ nhỏ; validate trong CI; theo spec skill chính thức; MIT, học có ghi nguồn | config | validate.yml, docs/credits.md | should |
| REQ-I-9 | I | Ba thứ khác biệt: quản lý + cổng bật/tắt, profile theo stack, vòng đo–journal–coach | structure | tổng hợp bằng chứng | should |
| REQ-J-1 | J (bản 1) | CLAUDE.md block, rules, settings template | structure | xem REQ-G2-1, G2-3, G2-4 | must |
| REQ-J-2 | J (bản 1) | 26 skill, 13 agent, 6 hook lõi | structure | ls; jq hooks.json | must |
| REQ-J-3 | J (bản 1) | Profile + 5 mẫu; scripts (gồm measure.py cơ bản) | structure | ls profiles, chạy measure.py | must |
| REQ-J-4 | J (bản 1) | 16 playbook, takeover 4 tầng, journal | content | xem REQ-A4-11, A1-2; templates/artifacts/journal-entry.md | must |
| REQ-J-5 | J (bản 1) | Coach đầy đủ; evals cho skill kỷ luật; hướng dẫn người dùng; GitHub Actions template | content | xem REQ-A4-6, G1-9, G1-10; templates/project/github | must |
| REQ-J-6 | J (bản 2) | GitLab CI để bản 2 (không làm ở bản 1) | structure | find gitlab | should |
| REQ-J-7 | J (bản 2) | Scorecard nâng cao, canary tự động hơn để bản 2 | content | đọc measure.py, retro, proposal-eval | should |
| REQ-J-8 | J (bản 2) | Thăng cấp skill lên kit để bản 2 | content | grep promot/lên kit | should |
| REQ-J-9 | J (bản 2) | Cấu hình mẫu cho MCP ngoài; workflow lô mở rộng để bản 2 | structure | grep mcp trong templates/profiles; đếm batch | should |
