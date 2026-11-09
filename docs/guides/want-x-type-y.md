<!-- GENERATED — do not edit; run scripts/gen-guides.py -->
# Muốn X thì gõ Y

Bảng sinh từ `skills/*/SKILL.md`. Cài cục bộ (không qua marketplace): gõ `/team-<tên>` thay cho `/team:<tên>`.

| Khi | Gõ | Vai chạy | Để lại |
|---|---|---|---|
| feature đã qua intake và cần spec có Definition of Done, hoặc khi spec đã duyệt phải sửa đổi (--amend) | `/team:analyze <ID> [--amend "<thay đổi>"] [--decide]` | analyst | `docs/team/features/<ID>/spec.md`, `<kit>/templates/artifacts/spec.md`, `docs/team/features/<ID>/questions.md` |
| việc cỡ L cần kiến trúc hệ thống, khi thay đổi chạm nhiều module hay NFR cần đánh giá tác động, hoặc khi cần review ba câu cho design.md | `/team:architect <ID> [system\|impact\|review]` | architect | `docs/team/architecture.md`, `docs/team/features/<ID>/arch-impact.md`, `docs/team/adr/ADR-NNN.md` |
| feature đã accepted và cần As-Built, release notes, mục CHANGELOG, cập nhật README và nội dung PR trước khi phát hành | `/team:asbuilt <ID>` | writer | `docs/team/features/<ID>/asbuilt.md`, `pr-body.md`, `CHANGELOG.md` |
| cần kiểm toán chính bộ kit team đang chạy trong dự án: skill không ai dùng, agent chạm trần lượt, chỉ dẫn mâu thuẫn, tài liệu lệch tên, lỗ hổng an toàn | `/team:audit-kit [--since <YYYY-MM-DD>]` | coach | `docs/team/kit-issues.md` |
| plan đã duyệt (hoặc việc cỡ S, bug-fix, hotfix) và cần dev viết test, code, reviewer chấm, rồi gộp từng task vào nhánh feature | `/team:build <ID> [--task T<N>] [--decide]` | tech-lead | `team/<ID>`, `docs/team/features/<ID>/tasks.md`, `review-NN.md` |
| pipeline CI đỏ, khi dự án cần dựng CI lần đầu, thêm một bước kiểm, hoặc viết script deploy, rollback, smoke | `/team:ci setup\|fix\|add-stage\|deploy-script [<run-id>\|<stage>]` | devops | `team/ci-<slug>`, `docs/team/ci.md` |
| cần dọn dẹp không đổi hành vi một loại nợ: code chết, đặt tên, cấu trúc, phụ thuộc thừa, test mồ côi hoặc đơn giản hóa | `/team:clean <dead-code\|naming\|structure\|deps\|tests\|simplify> [<đường dẫn>] [--decide]` | maintainer | `team/<ID>-clean-<kind>`, `docs/team/debt.md` |
| dev hoặc maintainer đã có thay đổi xanh và cần commit đúng chuẩn của đội | `/team:commit [<ID>] [--task T<N>]` | dev, maintainer | `team/<ID>-…`, `dev -> tech-lead \| FEAT-012 T3 \| DONE
  Commit: a1b2c3d fix(otp): reject expired code (FEAT-012)
  File: src/auth/otp.py, tests/auth/test_otp.py (đúng touchpoints)
  Test: <cmd.test_one tests/auth/test_otp.py> → 6 passed; lint: exit 0
  Quét staged: skip marker 0, secret 0
  Thấy nhưng không chạm: src/auth/session.py:88 nuốt lỗi (ghi debt, không sửa)` |
| spec đã duyệt cần thiết kế chi tiết (dữ liệu, API, luồng, quyền, migration, touchpoints, test plan) trước khi lập kế hoạch, hoặc refactor cần bản thiết kế ngắn | `/team:design <ID> [--short]` | designer | `docs/team/features/<ID>/design.md` |
| người hoặc một vai muốn ghi nhận xét về một agent hay skill của đội: tốt, chậm, sai, khó dùng | `/team:feedback <agent\|skill> <1-5> "<nhận xét>" [<ID>]` | team-leader | — |
| người giao một yêu cầu thô, một số issue, một lỗi hay hotfix cho đội | `/team:intake "<yêu cầu>" \| #<issue> [--type bug\|hotfix\|change] [--size S\|M\|L] [--decide]` | team-leader | — |
| team-leader thấy một chuyên môn riêng của dự án đủ lớn để cần ngữ cảnh, bộ tool hoặc model riêng, mà không vai nào của kit đảm nhận được | `/team:make-agent <name> "<nhu cầu một câu>"` | team-leader | `.claude/agents/<name>.md`, `.claude/agents/<name>.tests.md` |
| team-leader thấy một task cần chuyên môn riêng của dự án mà kit chưa có, hoặc một chuỗi bước sẽ lặp lại, và đã nêu được nhu cầu một câu | `/team:make-skill <name> "<nhu cầu một câu>"` | team-leader | `.claude/skills/<name>/SKILL.md`, `.claude/skills/<name>/references/tests.md`, `docs/team/skills-registry.md` |
| G0 của takeover đã được duyệt, hoặc repo rỗng cần cấu hình đội lần đầu (--new), để cài profile, config, settings, rule và khung docs/team cho dự án | `/team:onboard [--new]` | team-leader | `.team/profile.json`, `.team/config.json`, `CLAUDE.md` |
| feature đã có spec và design được duyệt và cần chia thành task 2–5 phút có touchpoints, hoặc khi change-request cần chèn task mới (--insert) | `/team:plan <ID> [--insert]` | tech-lead | `docs/team/features/<ID>/plan.md`, `<kit>/templates/artifacts/plan.md`, `docs/team/features/<ID>/tasks.md` |
| nhánh feature hoặc nhánh sửa CI đã sẵn sàng cần mở hay cập nhật pull request, hoặc cần trả lời bình luận review của người | `/team:pr <ID> [create\|update\|reply]` | tech-lead | `docs/team/journal/<ID>.md`, `tech-lead -> team-leader \| FEAT-012 \| DONE
  PR: https://github.com/<owner>/<repo>/pull/42 — head team/FEAT-012 → base main
  cmd.test trên đầu nhánh sau rebase: exit 0, "Ran 42 tests … OK"
  Kiểm CI: pending. Không merge (chờ người duyệt).
  Bình luận: 0 mở
  Tiếp: người review PR; sau merge chạy /team:release FEAT-012` |
| feature đã accepted và duyệt G4, cần merge, gắn tag, đưa lên staging rồi prod khi người đã duyệt G5 | `/team:release <ID> [staging\|prod]` | team-leader | `CHANGELOG.md`, `docs/team/features/<ID>/asbuilt.md` |
| spec còn câu hỏi kỹ thuật, cần so sánh phương án, đọc changelog trước khi nâng cấp, tìm hiểu API ngoài, hoặc làm spike | `/team:research <ID> "<câu hỏi>"` | researcher | `docs/team/features/<ID>/research.md`, `docs/team/research/<topic>@<version>.md` |
| đến kỳ nhìn lại, sau feature nhiều rework, khi góp ý vượt ngưỡng hai lần, hoặc scorecard có bất thường | `/team:retro [--since <YYYY-MM-DD>] [--decide]` | coach | `docs/team/retro/<date>.md`, `docs/team/proposals/<date>/*.md` |
| người muốn đội chạy tiếp feature tới giai đoạn hoặc cổng kế tiếp, hoặc chạy liên tục tới khi bị chặn | `/team:run [<ID>] [--until-blocked]` | team-leader | — |
| bắt đầu, lưu hoặc nạp lại một phiên làm việc dài: chọn kênh, model theo vai, ngân sách và điểm nén ngữ cảnh | `/team:session [plan\|save\|load] [<ID>]` | team-leader | `.team/session/plan.md`, `.team/session/<id>.md` |
| người hỏi feature đang ở đâu, ai đang chờ ai, hay việc gì đang bị chặn | `/team:status [<ID>]` | team-leader | — |
| đội nhận một repo đã có code mà chưa có .team/profile.json, hoặc người hỏi dự án này làm gì, đã tới đâu, việc tiếp theo là gì | `/team:takeover [--full]` | team-leader | `docs/team/assessment.md`, `docs/team/ai-readiness.md`, `docs/team/profile-proposal.md` |
| bắt đầu bất kỳ việc gì không tầm thường trong dự án có đội team, trước khi hành động hay hỏi lại: kiểm skill và playbook phù hợp | `/team:using-team` | team-leader, tech-lead (nạp sẵn) | — |
| mọi task của feature đã tick và cần nghiệm thu độc lập từng tiêu chí bằng lệnh chạy thật trước khi phát hành | `/team:verify <ID>` | qa | `docs/team/features/<ID>/acceptance.md`, `<kit>/templates/artifacts/acceptance.md`, `.team/current.json` |
