# Bộ kit tham khảo

Nghiên cứu cho P7 (cách viết skill/agent). Bản sao nông: `git clone --depth 1 <repo> /tmp/ref/<tên>`. Vòng sau chỉ học lại repo có HEAD khác hash dưới đây. Ghi công: `docs/credits.md`.

## Repo và HEAD (vòng 1, 2026-11-09)
| Repo | HEAD | Dùng cho |
|---|---|---|
| addyosmani/agent-skills | 301b02b12bff98e4688e6984af6556802322bbde | cấu trúc skill (Overview · When to Use · Process · Common Rationalizations · Red Flags · Verification · See Also); TDD, planning, code review, git workflow, spec, interview |
| obra/superpowers | 22f0b463e7a5e579904dd6211a520321035526f7 | using-skills, writing-plans, executing-plans, subagent-driven-development, verification-before-completion |
| anthropics/skills | 2c5958ecac7cee2b583967a2c4981d0f4a75c579 | skill-creator, đặc tả SKILL.md |
| wshobson/agents | 9c61ab243def98f72da12abd41cfcf5bcd91af9d | agent-teams, debugger |
| VoltAgent/awesome-claude-code-subagents | ed74d115b7fb7026a22a4f816a8e3250f425e3b4 | code-reviewer, qa-expert, test-automator, multi-agent-coordinator |
| affaan-m/everything-claude-code | d2ef2680594f9a17526a6e1a2e18b3d242c5d17b | rules, hooks, settings (vòng sau) |
| bmad-code-org/BMAD-METHOD | a867e1604b365d48ea03cbd109da1066ba0c84bc | persona agent, craft-subagents |
| ryoppippi/ccusage | 0c1bdd193524dcbbceef9caae3a5f4e8f8d06b9d | đọc log token (vòng sau, cho `measure.py --logs`) |

## So sánh (đo bằng `wc -w`, bỏ frontmatter với SKILL.md)
| Bộ | Số skill | Trung vị chữ SKILL.md | Số agent | Trung vị chữ agent | Mục hay dùng |
|---|---|---|---|---|---|
| addyosmani/agent-skills | 25 | 1.985 | 4 | 583 | Overview (26), When to Use (24), Common Rationalizations (24), Red Flags (24), Verification (24), See Also (8) |
| obra/superpowers | 15 | 1.246 | — | — | Overview, When to use, quy trình, Red Flags, bảng rationalization |
| anthropics/skills | 19 | 1.149 | — | — | tùy skill |
| wshobson/agents | — | — | 202 | 951 | Capabilities, Behavioral traits, Response approach |
| VoltAgent subagents | — | — | 166 | 901 | Focus areas, checklist, communication protocol |
| **team — TRƯỚC (v0.1.0)** | 26 | 292 (skill đầy đủ) · 191 (nạp thường xuyên) | 13 | 342 | 8 mục riêng |

## Nơi đi tới
Bảng cập nhật cuối vòng ("SAU") nằm ở cuối file này.

## Nơi đi tới — SAU vòng 1 (2026-11-09)
| Bộ | Trung vị chữ skill đầy đủ | Trung vị chữ skill kỷ luật | Trung vị chữ agent | Mục |
|---|---|---|---|---|
| addyosmani/agent-skills | 1.985 | — | 583 | 7 mục chuẩn |
| obra/superpowers | 1.246 | — | — | — |
| **team — SAU vòng 1** | 303,5 (20 skill; 7 đã viết lại: 1.316–1.590) | **1.502,5** | 348 (13; 5 đã viết lại: 902–1.062) | 10 mục skill, 10 mục agent, 4 mục skill nạp thường xuyên |

Ghi chú: chữ của team đếm theo âm tiết tiếng Việt (mỗi âm tiết là một từ khi tách bằng khoảng trắng), nên cùng một nội dung cho số "chữ" cao hơn tiếng Anh khoảng 1,3–1,5 lần.
