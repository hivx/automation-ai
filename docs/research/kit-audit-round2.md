# Kiểm định chất lượng bộ kit — vòng 2 (P7)

- Ngày: 2026-11-10 · Claude Code 2.1.319 · trạng thái TRƯỚC: tag `pre-p7-round2` (= `v0.2.1`, commit e12c68c)
- Số vòng: 2. Công thức của prompt (số tag `v0.*`) cho 3 vì có tag vá `v0.2.1`; vòng được đếm theo tag `pre-p7-round*` đã có (1) + 1.
- Công cụ: `python3 scripts/kit-metrics.py` (chuẩn trong `scripts/skill-budgets.txt`, `skill-sections.txt`, `agent-sections.txt`)
- Phạm vi vòng 2: 21 mục trong `scripts/quality-backlog.txt` (13 skill + 8 agent, vừa trần 14 + 8).

## TRƯỚC
| Mục | Lớp | Chữ | Ngân sách | Tiêu đề | Tự bào chữa | Dấu hiệu sai | Kiểm chứng | Mô tả | refs | Score | Đạt |
|---|---|---|---|---|---|---|---|---|---|---|---|
| skill:asbuilt | full | 266 | 1200–2500 | 2/10 (thứ tự) | 0 | 3 | 0 | 127 | 0 | 19 | — |
| skill:session | full | 260 | 1200–2500 | 2/10 (thứ tự) | 0 | 3 | 0 | 117 | 0 | 19 | — |
| skill:architect | full | 277 | 1200–2500 | 2/10 (thứ tự) | 0 | 3 | 0 | 146 | 0 | 20 | — |
| skill:audit-kit | full | 272 | 1200–2500 | 2/10 (thứ tự) | 0 | 3 | 0 | 161 | 1 | 20 | — |
| skill:ci | full | 296 | 1200–2500 | 2/10 (thứ tự) | 0 | 3 | 0 | 117 | 0 | 20 | — |
| skill:clean | full | 298 | 1200–2500 | 2/10 (thứ tự) | 0 | 3 | 0 | 128 | 0 | 20 | — |
| skill:design | full | 277 | 1200–2500 | 2/10 (thứ tự) | 0 | 3 | 0 | 169 | 0 | 20 | — |
| skill:make-agent | full | 278 | 1200–2500 | 2/10 (thứ tự) | 0 | 3 | 0 | 146 | 1 | 20 | — |
| skill:make-skill | full | 316 | 1200–2500 | 2/10 (thứ tự) | 0 | 3 | 0 | 145 | 1 | 21 | — |
| skill:retro | full | 303 | 1200–2500 | 2/10 (thứ tự) | 0 | 3 | 0 | 112 | 0 | 21 | — |
| skill:research | full | 294 | 1200–2500 | 2/10 (thứ tự) | 0 | 4 | 0 | 128 | 0 | 22 | — |
| skill:release | full | 320 | 1200–2500 | 2/10 (thứ tự) | 0 | 4 | 0 | 109 | 0 | 23 | — |
| skill:onboard | full | 393 | 1200–2500 | 2/10 (thứ tự) | 0 | 4 | 0 | 157 | 1 | 26 | — |
| agent:researcher | agent | 334 | 600–1200 | 2/10 (thứ tự) | 0 | 0 | — | 132 | 0 | 28 | — |
| agent:writer | agent | 335 | 600–1200 | 2/10 (thứ tự) | 0 | 0 | — | 140 | 0 | 28 | — |
| agent:analyst | agent | 345 | 600–1200 | 2/10 (thứ tự) | 0 | 0 | — | 119 | 0 | 29 | — |
| agent:architect | agent | 348 | 600–1200 | 2/10 (thứ tự) | 0 | 0 | — | 140 | 0 | 29 | — |
| agent:coach | agent | 350 | 600–1200 | 2/10 (thứ tự) | 0 | 0 | — | 144 | 0 | 29 | — |
| agent:designer | agent | 342 | 600–1200 | 2/10 (thứ tự) | 0 | 0 | — | 133 | 0 | 29 | — |
| agent:devops | agent | 342 | 600–1200 | 2/10 (thứ tự) | 0 | 0 | — | 146 | 0 | 29 | — |
| agent:maintainer | agent | 346 | 600–1200 | 2/10 (thứ tự) | 0 | 0 | — | 149 | 0 | 29 | — |
| agent:dev | agent | 959 | 600–1200 | 10/10 | 9 | 6 | — | 143 | 0 | 100 | ✓ |
| agent:qa | agent | 924 | 600–1200 | 10/10 | 9 | 5 | — | 129 | 0 | 100 | ✓ |
| agent:reviewer | agent | 946 | 600–1200 | 10/10 | 9 | 6 | — | 128 | 0 | 100 | ✓ |
| agent:team-leader | agent | 1062 | 600–1200 | 10/10 | 9 | 6 | — | 164 | 0 | 100 | ✓ |
| agent:tech-lead | agent | 945 | 600–1200 | 10/10 | 9 | 6 | — | 130 | 0 | 100 | ✓ |
| skill:analyze | full | 1590 | 1200–2500 | 10/10 | 10 | 8 | 6 | 112 | 1 | 100 | ✓ |
| skill:build | full | 1504 | 1200–2500 | 10/10 | 10 | 8 | 6 | 136 | 1 | 100 | ✓ |
| skill:commit | full | 1501 | 1200–2500 | 10/10 | 12 | 7 | 6 | 82 | 2 | 100 | ✓ |
| skill:feedback | always | 263 | 0–400 | 4/4 | 6 | — | — | 103 | 0 | 100 | ✓ |
| skill:handbook | always | 375 | 0–400 | 4/4 | 6 | — | — | 84 | 0 | 100 | ✓ |
| skill:intake | always | 305 | 0–400 | 4/4 | 6 | — | — | 78 | 0 | 100 | ✓ |
| skill:plan | full | 1316 | 1200–2500 | 10/10 | 10 | 7 | 6 | 150 | 1 | 100 | ✓ |
| skill:pr | full | 1425 | 1200–2500 | 10/10 | 11 | 7 | 6 | 131 | 1 | 100 | ✓ |
| skill:run | always | 313 | 0–400 | 4/4 | 6 | — | — | 110 | 0 | 100 | ✓ |
| skill:status | always | 273 | 0–400 | 4/4 | 6 | — | — | 80 | 0 | 100 | ✓ |
| skill:takeover | full | 1510 | 1200–2500 | 10/10 | 10 | 7 | 6 | 135 | 1 | 100 | ✓ |
| skill:using-team | always | 395 | 0–400 | 4/4 | 6 | — | — | 138 | 0 | 100 | ✓ |
| skill:verify | full | 1552 | 1200–2500 | 10/10 | 13 | 10 | 6 | 118 | 1 | 100 | ✓ |

| Nhóm | Số mục | Trung vị chữ | % đạt chuẩn | Trung vị score |
|---|---|---|---|---|
| always | 6 | 309.0 | 100% | 100.0 |
| full | 20 | 309.5 | 35% | 21.5 |
| agent | 13 | 348 | 38% | 29 |
| discipline skills | 8 | 1502.5 | — | — |
| tất cả | 39 | — | 46% | — |

## Vấn đề mở (blocker/major) → mục bị ảnh hưởng
Không còn blocker mở sau v0.2.1. Major còn mở (`docs/kit-issues.md`; `evals/RESULTS.md` Round 1 không có eval xấu đi):

| Vấn đề | Mức | Mục bị ảnh hưởng | Làm ở vòng 2 |
|---|---|---|---|
| K-06 headless ở thư mục chưa tin bỏ qua `permissions.allow` | major | `templates/project/github/workflows/team-feature.yml`, `workflows/batch/*`, skill `ci`, agent `devops`, `docs/08-channels.md` | sinh `--allowedTools` từ profile bằng script; ci/devops dùng script đó |
| K-24 Bash của vai `bash: any` không qua `protect.sh` | major | `hooks/hooks.json`, `scripts/protect.sh`, `scripts/teamlib.py` | gắn `protect.sh` vào Bash, kiểm đích ghi của lệnh shell |
| K-39 chỉ-đọc còn lọt (`sed e/w`, `sort -o`, `uniq IN OUT`, `tree -o`, `rg --pre`, `>&`, `<>`, `mkdir`) | major | `scripts/teamlib.py is_readonly`, `hooks/role-policy.json` | chặn từng dạng, bỏ `mkdir`, ca thử |
| K-40 script chỉ-đọc so theo tên | major | `scripts/teamlib.py`, `hooks/role-policy.json` | so đường dẫn thật dưới `<kit>/scripts/`; script có ghi cần quyền ghi đích |

Minor gắn với mục viết lại: K-09, K-26 (onboard); K-27/K-43, K-44 (coach, audit-kit); K-38 (retro); K-45 (docs, cỡ S verify); K-25 (`Bash(python3 *)` ở skill); K-08 (detect-stack, takeover).

## SAU (vòng 2 xong, 2026-11-10)
| Nhóm | Số mục | Trung vị chữ | % đạt chuẩn | Trung vị score |
|---|---|---|---|---|
| always | 6 | 323.5 | 100% | 100.0 |
| full | 20 | 1436.5 | 100% | 100.0 |
| agent | 13 | 924 | 100% | 100 |
| discipline skills | 8 | 1502.0 | — | — |
| tất cả | 39 | — | 100% | — |

`scripts/quality-backlog.txt` rỗng; `kit-metrics.py --check` thoát 0. Trước vòng 2: full 309,5 chữ / 35% đạt; agent 348 / 38%; tất cả 46%.

## Mục đã viết lại
Tham khảo đọc hết (đường dẫn dưới `/tmp/ref`, HEAD trong `docs/research/reference-kits.md`); ghi chú: `refnotes/D-docs-arch.md`, `E-ops.md`, `F-meta.md` (scratchpad của phiên, tóm tắt ở đây).

| Mục | Score trước | Score sau | Chữ trước → sau | Tham khảo đã đọc | Lấy | Bỏ (lý do) |
|---|---|---|---|---|---|---|
| skill:asbuilt | 19 | 100 | 266 → 1.527 | agent-skills/skills/documentation-and-adrs; agent-skills/references/definition-of-done.md; /tmp/ref/agents/plugins/documentation-generation/agents/docs-architect.md | bảng thiết kế ↔ thực tế từng mục + `file:line`; câu có nguồn; nhóm Keep a Changelog; đóng nợ sau G4 (K-35); bốn tiêu đề pr-body | chỉ số "dễ đọc/SEO" (bịa số); mẫu README có lệnh npm (lệnh stack) |
| skill:release | 23 | 100 | 320 → 1.364 | agent-skills/skills/shipping-and-launch; definition-of-done.md; awesome…/03-infrastructure/deployment-engineer.md | kế hoạch rollback trước deploy; chọn phiên bản từ tag + CHANGELOG; điểm dừng UAT; kiểm sau deploy | rollout theo cờ/ngân sách lỗi (không có khe); `git revert && git push` (push nhánh nền); rollback prod tự động |
| skill:research | 22 | 100 | 294 → 1.551 | agent-skills/skills/source-driven-development; awesome…/10-research-analysis/research-analyst.md | phát hiện phiên bản → lấy nguồn → trích; thứ bậc nguồn; `UNVERIFIED`; trích an toàn; bảng upgrade/integration | "hỏi người khi thiếu phiên bản" (subagent không hỏi được); researcher tự viết code theo docs |
| skill:architect | 20 | 100 | 277 → 1.431 | BMAD-METHOD/skills/bmad-architecture (+ references/reviewer-gate, headless, assets/spine-template); bmad-agent-architect; documentation-and-adrs; /tmp/ref/agents/plugins/c4-architecture/agents/c4-container.md | phép thử ngưỡng ba điều; ADR có `## Ràng buộc` kiểm được; quét chiều; tự phản biện; container từ thực tế deploy | phỏng vấn người (Coaching path); memlog; reviewer song song; "nhu cầu tương lai" (STD-DESIGN-5) |
| skill:design | 20 | 100 | 277 → 1.507 | agent-skills/skills/api-and-interface-design, spec-driven-development; /tmp/ref/agents/plugins/database-design/agents/database-architect.md; awesome…/01-core-development/api-designer.md | hợp đồng trước luồng; Hyrum; idempotency đủ 6 điểm; migration theo lô; một log/metric mỗi đường mới | mục "Commands" trong spec (lệnh ở `cmd.*`); designer chia task; quy tắc tên theo TypeScript |
| skill:ci | 20 | 100 | 296 → 1.348 | agent-skills/skills/ci-cd-and-automation; /tmp/ref/agents/plugins/cicd-automation/skills/github-actions-templates; deployment-engineer, devops-engineer | 5 loại STD-CI-4 có bằng chứng; một lần chạy lại; khe rỗng = "chưa cấu hình"; rollback "đã kiểm" chỉ sau lần chạy thật | lệnh npm/vercel; agent tự sửa code lỗi lint; auto-merge; gỡ test chậm khỏi PR |
| skill:clean | 20 | 100 | 298 → 1.363 | agent-skills/skills/code-simplification, deprecation-and-migration, observability-and-instrumentation; /tmp/ref/agents/plugins/code-refactoring/agents/legacy-modernizer.md | hàng rào Chesterton; test đặc tả trước; so tên test; loại `deprecate`, `observe`; trần 500 dòng | ví dụ theo ngôn ngữ; tách monolith; công cụ Sonar/CodeQL không có trong profile |
| skill:audit-kit | 20 | 100 | 272 → 1.211 | agent-skills/skills/security-and-hardening; /tmp/ref/everything-claude-code/hooks/README.md, /tmp/ref/everything-claude-code/hooks/hooks.json, /tmp/ref/everything-claude-code/hooks/hermes/config-protection.py, /tmp/ref/everything-claude-code/rules/common/{hooks,security,agents}.md; BMAD retrospective/references/evidence-gathering.md | ranh giới tin cậy; hook mở khi lỗi; matcher phủ tool; "đã kiểm và sạch" vs "không kiểm"; chống trùng với K-xx | checklist ứng dụng (OWASP, STRIDE); công tắc tắt hook; "dừng mọi việc, gọi security agent" |
| skill:make-skill | 21 | 100 | 316 → 1.383 | superpowers/skills/writing-skills (+ discovery, bulletproofing, testing-skills-with-subagents, persuasion-principles, anthropic-best-practices); skills/skills/skill-creator (+ agents/grader, analyzer, comparator) | lỗi quan sát được = đỏ, lần dùng đầu = xanh; dạng chỉ dẫn theo loại lỗi; câu kích hoạt gần giống; kiểm phân biệt; skill tạm 8 mục SPEC §9 | viewer HTML, đóng gói `.skill`, script cần thư viện ngoài; mô tả "đẩy" tóm tắt quy trình |
| skill:make-agent | 20 | 100 | 278 → 1.327 | writing-skills/anthropic-best-practices; awesome…/09-meta-orchestration/agent-organizer.md; everything-claude-code/the-longform-guide.md | khớp năng lực có trích dẫn; model theo giá của sai lầm; vai `_temp` (K-49); ca thử ngoài `.claude/agents/` | agent lập kế hoạch đội; persona BMAD; thêm model vào config |
| skill:session | 19 | 100 | 260 → 1.273 | agent-skills/skills/context-engineering, using-agent-skills; everything-claude-code/the-shortform-guide.md, the-longform-guide.md | bàn giao chỉ phần artifact không có; load = kiểm (HEAD, duyệt chỉ từ file); dòng `/compact <trọng tâm>`; ngân sách từ số liệu | chèn memory vào `--system-prompt`; tắt auto-compact; skill tự sinh lúc Stop |
| skill:onboard | 26 | 100 | 393 → 1.250 | everything-claude-code/CLAUDE.md, examples/CLAUDE.md, docs/SELECTIVE-INSTALL-ARCHITECTURE.md; writing-skills/references/CLAUDE_MD_TESTING.md; context-engineering | kế hoạch trước khi ghi; ghi nhận nguồn/cách ghi từng file; lũy đẳng; đóng ngoại lệ ở mọi lối ra; K-09, K-26 | cài vào `~/.claude`; CLAUDE.md có lệnh cứng; cài plugin/MCP |
| skill:retro | 21 | 100 | 303 → 1.447 | BMAD-METHOD/skills/bmad-retrospective (SKILL, workflow, references/*); skill-creator/agents/{analyzer,comparator}; /tmp/ref/agents/plugins/incident-response/skills/postmortem-writing | khung trước, chạy lại được; kê nguồn; theo dõi retro trước; hai quyết định mỗi điểm nghẽn; luật mẫu tối thiểu (K-38); eval có check bản hiện tại trượt | thảo luận nhiều agent; hỏi người; viết ADR; verdict nghiệm thu epic |
| agent:analyst | 29 | 100 | 345 → 957 | agent-skills/skills/interview-me; BMAD-METHOD/skills/bmad-agent-analyst (+ assets); awesome…/08-business-product/business-analyst.md | đứng phía nghiệp vụ; khối Kết quả/…/Ngoài phạm vi; không bịa số NFR; ưu tiên khi mọi thứ "phải có"; Bash chỉ-đọc (K-52) | hỏi từng câu chờ trả lời; persona; thiết kế giải pháp |
| agent:researcher | 28 | 100 | 334 → 844 | source-driven-development; research-analyst | như skill research; POC trong worktree riêng (K-48); đầu vào theo playbook (K-68) | phỏng vấn chuyên gia, khảo sát |
| agent:architect | 29 | 100 | 348 → 866 | bmad-agent-architect; bmad-architecture; c4-container; awesome…/04-quality-security/architect-reviewer.md | chỉ chốt bất biến; phê chuẩn trước đề xuất; chế độ system ghi arch-impact (K-46) | "đáp ứng cả nhu cầu tương lai" |
| agent:designer | 29 | 100 | 342 → 833 | api-and-interface-design; spec-driven-development; database-architect; api-designer | hợp đồng trước; không chia task (K-66) | quy tắc tên theo ngôn ngữ; phân trang mặc định |
| agent:writer | 28 | 100 | 335 → 857 | documentation-and-adrs; docs-architect; awesome…/08-business-product/technical-writer.md | đầu vào theo chế độ (K-67); không viết `Released:`/duyệt | model haiku, WebFetch |
| agent:devops | 29 | 100 | 342 → 838 | ci-cd-and-automation; /tmp/ref/agents/plugins/cicd-automation/agents/deployment-engineer.md; /tmp/ref/agents/plugins/incident-response/agents/devops-troubleshooter.md; awesome…/03-infrastructure/devops-engineer.md | ghi phiên bản đang chạy trước deploy; smoke đỏ = dừng + đề xuất; chỉ kích hoạt pipeline có người duyệt (STD-OPS-7, ADJ-24) | "tự động hoàn toàn, không người"; giao thức context-manager; chỉ số bịa |
| agent:maintainer | 29 | 100 | 346 → 830 | code-simplification; deprecation-and-migration; legacy-modernizer; awesome…/06-developer-experience/refactoring-specialist.md | như skill clean; nhả nhánh cho qa; ghi `tasks.md` (K-47, K-58) | "dùng chủ động"; chỉ số hiệu năng |
| agent:coach | 29 | 100 | 350 → 958 | BMAD retrospective; postmortem-writing; everything-claude-code/rules/common/agents.md | một danh sách ghi (K-43); thiết kế eval, không chạy; không đổ lỗi; theo dõi retro trước | thảo luận nhiều agent; hỏi người |

Sửa kit đi kèm (bằng chứng từ code hoặc lần chạy): K-06, K-08, K-09, K-24, K-26, K-27/K-43, K-28, K-30, K-38, K-39, K-40, K-44, K-45, K-46..K-75, K-78 (còn mở: K-53, K-62, K-65, K-72, K-76, K-77, K-79, K-80; cùng K-18, K-25 từ trước) — `docs/kit-issues.md`.

Sau eval và end-to-end, team-leader (1.105 chữ), intake (326), handbook (389), status, run, coach, make-skill, make-agent, audit-kit được chỉnh thêm cho K-70..K-74; tất cả vẫn đạt chuẩn (`kit-metrics.py --check` thoát 0).
