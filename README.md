# automation-ai — plugin `team` cho Claude Code

`automation-ai` là bộ AGENT + SKILL + QUY TẮC + HƯỚNG DẪN + QUY TRÌNH cài được cho Claude Code. Cài vào bất kỳ dự án phần mềm nào (mọi ngôn ngữ, mọi nền tảng), Claude Code trở thành một đội IT chuyên nghiệp: tiếp nhận dự án và báo cáo hiện trạng, nhận yêu cầu thô rồi làm trọn từ phân tích đến phát hành, chỉ dừng ở các cổng duyệt bạn bật, và tự đo lường để đề xuất cải tiến chính mình. Lệnh, cấu trúc và quy ước của từng dự án nằm trong `.team/profile.json`, không nằm trong lõi.

**Trạng thái: v0.2.1 — dùng được; vòng 1 nâng chất lượng xong cho 13 skill và 5 agent chính (xem [`docs/research/kit-audit-round1.md`](docs/research/kit-audit-round1.md)); hạn chế đã biết trong [`CHANGELOG.md`](CHANGELOG.md).**

Đặc tả đầy đủ: [`SPEC.md`](SPEC.md). Tài liệu cho người: [`docs/`](docs/00-overview.md).

## Dòng chảy 9 giai đoạn

```
 G0 takeover ──[G0]──► onboard            (chỉ dự án đã có code)

 0 intake ─► 1 analyze ──[G1]──► 2 research ─► 3 architect ──[G2]──► 4 design ──[G2b]──►
 5 plan ──[G3]──► 6 build (dev ⇄ reviewer) ─► 7 verify ──[G4]──► 8 release ──[G5: luôn là người]──► 9 operate
                                                                                                    │
                     retro ◄── journal + scorecard ◄────────────────────────────────────────────────┘

 [Gn] = cổng duyệt (bật/tắt trong .team/config.json; G5_prod luôn cần người)
 Cỡ S: intake → analyze → build → verify → release.  Cỡ M bỏ architect.  Cỡ L đi đủ 9 bước.
```

## Bảy nguyên tắc

1. **Agent là một con người** — mỗi vai có hợp đồng làm việc; luôn có quản lý (`team-leader`) và người làm chính (`tech-lead`).
2. **Trạng thái nằm trên đĩa** — mỗi giai đoạn để lại artifact trong `docs/team/`; vị trí hiện tại được tính từ artifact.
3. **Máy trước LLM** — hook, quyền, script là LUẬT; rule, skill, CLAUDE.md là HƯỚNG DẪN.
4. **Độc lập nền tảng** — lõi chỉ có quy trình và vai; lệnh của stack nằm ở các khe `cmd.*` của profile.
5. **Gọi đúng người, chỉ khi cần** — mỗi lần gọi có một câu lý do ghi vào journal.
6. **Đo rồi mới sửa** — scorecard định lượng + journal định tính; mọi thay đổi có bằng chứng, eval, canary, rollback.
7. **Con người quyết định** — cổng là cấu hình; đề xuất cải tiến chờ người duyệt.

## Cài đặt

Cách 1 — marketplace (khuyên dùng), gõ trong Claude Code:

```
/plugin marketplace add <owner>/automation-ai
/plugin install team@automation-ai
```

Cách 2 — `npx skills` (tùy chọn, nếu CLI này có sẵn). Chỉ cài skill, không có agent và hook, nên các luật máy không chạy:

```
npx skills add <owner>/automation-ai
```

Cách 3 — chép cục bộ vào `.claude/` của dự án (không cần marketplace):

```
git clone https://github.com/<owner>/automation-ai
automation-ai/scripts/install-local.sh [--dry-run] [--force] /đường/dẫn/dự-án
```

Khi cài cục bộ, lệnh là `/team-<tên>` thay vì `/team:<tên>`. Chi tiết, gỡ cài và phạm vi settings: [`docs/06-install.md`](docs/06-install.md).

## Giờ đầu tiên trên dự án đã có code

1. `/team:takeover` — quét 4 tầng có kiểm soát chi phí, không sửa gì; viết `docs/team/assessment.md`, `ai-readiness.md`, `profile-proposal.md`, `debt.md`, `open-questions.md`.
2. Đọc báo cáo, trả lời câu hỏi mở, thêm dòng `Approved-by: <tên> <YYYY-MM-DD>` vào đầu `docs/team/ai-readiness.md` (cổng G0).
3. `/team:onboard` — tạo `.team/profile.json`, `.team/config.json`, khối `team` trong `CLAUDE.md`, `.claude/settings.json`; in lệnh cài plugin khuyên dùng (không tự cài).
4. `/team:intake "<yêu cầu thô>"` — `team-leader` chọn playbook và cỡ việc; theo dõi bằng `/team:status`.

Hướng dẫn từng bước: [`docs/guides/first-day-on-existing-project.md`](docs/guides/first-day-on-existing-project.md).

## Lệnh hằng ngày

| Việc | Lệnh | Ai làm |
|---|---|---|
| Tiếp nhận dự án có sẵn | `/team:takeover` | team-leader (+ researcher) |
| Cấu hình đội cho dự án | `/team:onboard` | team-leader |
| Giao một yêu cầu mới | `/team:intake "<yêu cầu>"` | team-leader |
| Báo lỗi | `/team:intake --type bug "<mô tả>"` | team-leader → dev |
| Chạy tiếp tới cổng kế | `/team:run` | team-leader → tech-lead |
| Xem đang ở đâu, ai chờ ai | `/team:status` | team-leader |
| Lưu / nạp lại phiên | `/team:session` | team-leader |
| Nghiệm thu | `/team:verify` | qa |
| Mở pull request | `/team:pr` | tech-lead |
| Phát hành | `/team:release` | devops (người duyệt prod) |
| Sửa CI đỏ | `/team:ci` | devops |
| Dọn dẹp không đổi hành vi | `/team:clean` | maintainer |
| Góp ý về đội | `/team:feedback "<góp ý>"` | team-leader |
| Nhìn lại và cải tiến | `/team:retro` | coach |

Bảng đầy đủ: [`docs/guides/want-x-type-y.md`](docs/guides/want-x-type-y.md).

## Cấu trúc repo

```
.claude-plugin/   plugin.json (team), marketplace.json (automation-ai)
agents/           13 vai: team-leader, tech-lead, coach, analyst, researcher, architect,
                  designer, dev, reviewer, qa, writer, maintainer, devops
skills/<tên>/     26 skill = lệnh /team:<tên>
workflows/        16 playbook + batch/
hooks/            hooks.json (luật máy)
scripts/          validate.sh, install-local.sh, team.py, ... (bash + python3 stdlib + jq)
handbook/         STD.md (sổ tay kỹ thuật) và phụ lục
profiles/         profile mẫu theo stack
templates/        artifacts/, project/, schemas/
evals/            kịch bản eval cho skill kỷ luật
docs/             tài liệu cho người
```

## Yêu cầu

- Claude Code ≥ 2.1.
- `bash`, `python3` (chỉ thư viện chuẩn), `jq`, `git`; `gh` là tùy chọn.

## Giấy phép

MIT — xem [`LICENSE`](LICENSE).
