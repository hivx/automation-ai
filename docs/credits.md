# Ghi công

Cách viết skill và agent của kit (cấu trúc mục, bảng tự bào chữa, dấu hiệu sai, mục kiểm chứng, trạng thái trả DONE/NEEDS_CONTEXT/BLOCKED, vòng sửa có trần, xem lại có phạm vi) học từ các repo dưới đây. Nội dung được viết lại bằng tiếng Việt cho quy trình và vai của kit; không chép nguyên khối. HEAD đã đọc: `docs/research/reference-kits.md`.

| Repo | Giấy phép | Học gì |
|---|---|---|
| addyosmani/agent-skills | MIT | Cấu trúc skill (Overview, When to Use, Common Rationalizations, Red Flags, Verification, See Also); TDD, planning, code review, git workflow, interview-me, spec-driven, context-engineering; vòng 2: documentation-and-adrs, shipping-and-launch, source-driven-development, api-and-interface-design, ci-cd-and-automation, code-simplification, deprecation-and-migration, observability-and-instrumentation, security-and-hardening, using-agent-skills |
| obra/superpowers | MIT | using-superpowers, writing-skills (vòng 2 thêm references: discovery, bulletproofing, testing-skills-with-subagents, CLAUDE_MD_TESTING, anthropic-best-practices), writing-plans, executing-plans, subagent-driven-development (trạng thái trả, vòng sửa, xem lại có phạm vi), verification-before-completion, receiving-code-review |
| anthropics/skills | theo từng skill (skill-creator: Apache-2.0; repo không có LICENSE gốc) | vòng 2: skill-creator (SKILL.md, agents/grader, analyzer, comparator, references/schemas) — eval phân biệt được, câu kích hoạt gần giống |
| wshobson/agents | MIT | agent-teams (team-lead, implementer, reviewer, debugger); vòng 2: docs-architect, c4-container, backend-architect, database-architect, deployment-engineer, devops-troubleshooter, legacy-modernizer, postmortem-writing |
| VoltAgent/awesome-claude-code-subagents | MIT | code-reviewer, qa-expert, test-automator, multi-agent-coordinator; vòng 2 (ít dùng, phần lớn bị bỏ): technical-writer, research-analyst, architect-reviewer, api-designer, devops-engineer, refactoring-specialist, security-auditor, business-analyst, agent-organizer |
| bmad-code-org/BMAD-METHOD | MIT | craft-subagents, preparing-a-repo-for-agents; vòng 2: bmad-architecture (phép thử ngưỡng quyết định, ràng buộc ADR), bmad-agent-architect, bmad-agent-analyst, bmad-retrospective (kê nguồn, theo dõi retro trước) |
| affaan-m/everything-claude-code | MIT | vòng 2: hooks/README, hooks.json, config-protection (kiểm hook mở khi lỗi, phủ matcher), rules/common, CLAUDE.md mẫu, hướng dẫn cài chọn lọc (kế hoạch trước khi ghi, lũy đẳng) |
